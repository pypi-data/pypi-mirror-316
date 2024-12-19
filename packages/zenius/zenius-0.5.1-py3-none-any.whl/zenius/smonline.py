import os
import shutil
import sys
import zipfile as zf
from concurrent.futures.process import ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import date, datetime
from itertools import chain
from pathlib import Path
from threading import Thread
from typing import NamedTuple, Optional

import questionary as qy
import requests
from bs4 import BeautifulSoup as bs
from bs4 import Tag
from bs4.element import ResultSet
from iterfzf import iterfzf  # type: ignore
from loguru import logger

base = "https://search.stepmaniaonline.net"


class Job(NamedTuple):
    name: str
    thread: Thread


class Jobs:
    tracker: list[Job] = []

    @classmethod
    def track_jobs(cls) -> None:
        running: list[Job] = []
        for job in cls.tracker:
            if job.thread.is_alive():
                running.append(job)
            else:
                logger.debug(f"END THREAD: {job.name}")
        cls.tracker = running

    @classmethod
    def add(cls, name: str, thread: Thread) -> None:
        logger.trace(f"START THREAD: {name}")
        thread.daemon = True
        thread.start()
        cls.tracker.append(Job(name, thread))


class Storage:
    root: Path = Path.home() / ".local" / "zenius"
    songs: Path = root / "songs"
    log: Path = root / "smonline.log"


Storage.songs.mkdir(parents=True, exist_ok=True)


class Entry(NamedTuple):
    id_: int
    title: str
    size: str
    num_charts: int
    cdate: date
    download: str

    def __repr__(self) -> str:
        return f'{self.id_},\t"{self.title}" | {self.num_charts} | {self.size} | {self.cdate}'


@dataclass
class Cache:
    _results: set[Entry] = field(default_factory=set)

    def build(self) -> None:
        logger.info("Building pack cache...")
        self._results = get_all_packs()

    @property
    def results(self) -> set[Entry]:
        if not self._results:
            self.build()
        return self._results

    @property
    def map(self) -> dict[int, Entry]:
        return {entry.id_: entry for entry in self.results}


cache = Cache()


def get_entries(search: str) -> list[Entry]:
    url = base + f"/packs/{search}"
    html = requests.get(url).text
    soup = bs(html, "lxml")
    listings = soup.select("table.table tbody tr")
    rows = []
    for listing in listings:
        if row := gen_row(listing.select("td")):
            rows.append(row)
    return list(rows)


def gen_row(columns: ResultSet[Tag]) -> Optional[Entry]:
    if not isinstance(columns[0].a, Tag):
        return None
    link = columns[0].a.get("href")
    title = columns[0].a.text
    if not isinstance(link, str):
        return None
    id_ = int(link.split("/")[-1])
    size = columns[1].text
    num_charts = int(columns[2].text)
    cdate = datetime.strptime(columns[3].text, "%Y-%b-%d").date()
    if not isinstance(columns[4].a, Tag):
        return None
    download = columns[4].a.get("href")
    if not isinstance(download, str):
        return None
    download = f"{base}/static/new/{download.split("link/")[-1]}"
    return Entry(id_, title, size, num_charts, cdate, download)


"""Generate optimized search space with the following code

from string import ascii_lowercase, digits

chars = ascii_lowercase + digits

total = set()
bogus = []
for char in chars:
    previous = set(total)
    print(f"Getting results for {char}")
    results = get_entries(char)
    total.update(results)
    unique = total - previous
    if len(unique) > 10:
        print(f"\tAdding {len(total - previous)} entries")
    elif len(unique) > 0:
        print(unique)
    else:
        bogus.append(char)

optimized = sorted(set(chars) - set(bogus))
"""
optimized = list("01abcdefghijklmnoprstv")


def get_all_packs() -> set[Entry]:
    with ProcessPoolExecutor() as pp:
        results = set(chain.from_iterable(pp.map(get_entries, optimized)))
    return results


def download_zip(title: str, url: str) -> None:
    if pack_exists(title):
        logger.warning(f"Pack {title} from {url} exists. Skipping")
        return None
    prefix = Storage.songs
    prefix.mkdir(parents=True, exist_ok=True)
    archive = prefix / Path(f"{title}.zip")
    with requests.get(url, stream=True) as response:
        with open(archive, "wb") as file:
            shutil.copyfileobj(response.raw, file)
    if not zf.is_zipfile(archive):
        logger.error(f"Cannot download {title} from {url}")
        return None
    with zf.ZipFile(archive, "r") as zipped:
        extracted_name = zipped.getinfo(zipped.namelist()[0]).filename.split("/")[0]
        extracted_path = prefix / extracted_name
        destination = prefix / title
        zipped.extractall(path=prefix)
    shutil.move(extracted_path, destination)
    archive.unlink()
    logger.debug(f"Downloaded {title}\n\t{url}")


def pack_exists(title: str, storage: Path = Storage.songs) -> bool:
    packs = [f.name for f in os.scandir(storage) if f.is_dir()]
    if title in packs:
        return True
    return False


def main_() -> None:
    results = get_all_packs()
    results_dict = {entry.id_: entry for entry in results}
    while True:
        selection = iterfzf(iter([str(result) for result in results]), multi=True)
        for s in selection:
            id_ = int(s.split(",")[0])
            row = results_dict[id_]
            print(row)
            print(row.download)
        input("Continue?")


def interface(menu: str) -> str:
    if menu == "main":
        choices = [
            qy.Choice("Search Title", "title", shortcut_key="t"),
            qy.Choice("Search Artist", "artist", shortcut_key="a"),
            qy.Choice("Search Pack", "pack", shortcut_key="p"),
        ]
        choice = qy.select(
            "Choose an option", choices=choices, use_shortcuts=True
        ).ask()
        if not choice:
            Jobs.track_jobs()
            jobs = Jobs.tracker
            if len(jobs) > 0:
                print(f"{len(jobs)} Active job(s):")
                for job in jobs:
                    print(f"\t{job.name}")
            message = "Do you want to quit?"
            if qy.confirm(message, default=False).ask() is True:
                return "exit"
        menu = choice
    if menu == "pack":
        packs = cache.map
        selection = iterfzf(
            iter([str(entry) for entry in packs.values()]), multi=True, sort=True
        )
        if not selection or len(selection) == 0:
            return "main"
        rows = [packs[int(s.split(",")[0])] for s in selection]
        for row in rows:
            name = f"Downloading pack: {row.title}"
            thread = Thread(target=download_zip, args=[row.title, row.download])
            Jobs.add(name, thread)
    return "main"


def main() -> None:
    logger.remove()
    logger.add(Storage.log, retention="1 day")
    logger.add(sys.stdout, level="INFO")
    menu = "main"
    logger.info("Booting up!")
    while True:
        if menu == "exit":
            break
        Jobs.track_jobs()
        menu = interface(menu)


if __name__ == "__main__":
    main()
