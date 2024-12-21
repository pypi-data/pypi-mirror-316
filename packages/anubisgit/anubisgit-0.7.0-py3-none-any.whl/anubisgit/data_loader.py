from pathlib import Path, PurePath
from datetime import datetime
import json
from loguru import logger


def anubisgit_date(date_str: str) -> datetime.date:
    """Extract datetime.date from string

    Might evolve if we store differently anubisgit

    Args:
        data_str (str): Date to be formatted for anubisgit
    Raises:
        NotImplementedError: If unable to read the date

    Returns:
        datetime.date: Formated date
    """

    size = len(date_str.split("-"))
    if size == 2:
        return datetime.strptime(date_str, "%Y-%m")
    elif size == 3:
        return datetime.strptime(date_str, "%Y-%m-%d")
    else:
        raise NotImplementedError(f"Date {date_str} could not be parsed")


def date_from_pathname(pathname: str) -> datetime.date:
    """
    Extract datetime.date from foldername

    Args:
        pathname (str): Name of the folder

    Returns:
        date (datetime.date) : A datetime object
    """
    ppath = PurePath(pathname)
    date_str = ppath.parts[-1].split("_")[-1]
    date = anubisgit_date(date_str)
    return date


def load_jsons(
    folder: str, fname: str, date_start: str = None, date_end: str = None
) -> dict:
    """Load the ANUBIS JSON into a dict ordered by dates

    Args:
        folder (str): Path to the source folder
        fname (str): Filename to join
        date_start (str, optionnal): Date start included, using strptime format %Y-%m-%d. Defaults to None
        date_end (str,optionnal): Date end included, using strptime format %Y-%m-%d. Defaults to None

    Returns:
        datadict (dict): dictionary with keys as datetime objects

    """
    suffix = fname.split(".")[-1]
    if suffix != "json":
        raise NotImplementedError(
            f"Cannot join file {fname}, suffix {suffix} not implemented."
        )

    root = Path(folder)
    list_path = sorted([x for x in root.iterdir() if x.is_dir()])

    if date_start is None:
        date_start = date_from_pathname(list_path[0])
    else:
        date_start = anubisgit_date(date_start)

    if date_end is None:
        date_end = date_from_pathname(list_path[-1])
    else:
        date_end = anubisgit_date(date_end)

    dict_ = dict()

    for month_path in list_path:
        file_ = month_path / fname
        date = date_from_pathname(month_path)
        if date < date_start:
            # too early
            continue
        if date > date_end:
            # too late
            continue

        if not file_.is_file():
            # In case file is missing
            logger.debug(f"{file_.as_posix()} is missing")
            continue
        with open(file_, "r") as fin:
            dict_[date] = json.load(fin)
    return dict_


def load_tags(folder: str) -> dict:
    """
    Load tags as dictionary of datetimes

    Args:
        folder (str): Path to the folder

    Returns:
        tag_dict (dict): Dictionnary of tags associated with datetimes/
    """
    root = Path(folder)
    with open(root / "tags_history.json", "r") as fin:
        tags = json.load(fin)

    def _read_date(datestr):
        head_ = datestr.split("T")[0]
        return datetime.strptime(head_, "%Y-%m-%d")

    tag_dict = {tag: _read_date(datestr) for tag, datestr in tags.items()}
    return tag_dict


def load_authors(folder: str) -> dict:
    """
    Load authors as dictionnary of authors

    Args:
        folder (str): Path to the folder

    Returns:
        authors_lower (dict): Dict of authors associated with their git names
    """
    root = Path(folder)
    with open(root / "authors_list.json", "r") as fin:
        authors_raw = json.load(fin)

    authors_lower = {key.lower(): value for key, value in authors_raw.items()}

    return authors_lower
