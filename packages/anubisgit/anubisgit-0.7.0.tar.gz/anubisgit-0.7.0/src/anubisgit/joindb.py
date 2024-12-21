""" Join Anubis databases"""

import json

from pathlib import Path, PurePath


def join_anubisgit_files(path_: str, fname: str) -> dict:
    """
    Join anubisgit files found in an Anubis timemachine folder

    Args:
        path_ (str): Path to the output folder of timemachine
        fname (str): File name with extension

    Returns:
        dict_ (dict): Dict with joined data
    """
    root = Path(path_)
    list_path = [x for x in root.iterdir() if x.is_dir()]

    dict_ = dict()
    for month_path in list_path:
        ppath = PurePath(month_path)
        date_str = ppath.parts[-1].split("_")[-1]

        file_ = month_path / fname
        if file_.is_file():
            try:
                with open(file_, "r") as fin:
                    dict_[date_str] = json.load(fin)
            except json.decoder.JSONDecodeError:
                print("Format not available not a json file")
        else:
            pass

    return dict_


def join_monthly_ddb(path_: str) -> None:
    """
    This function will dump the concatenated data from the various months
    selected.

    Note : There is a list(dict_) in the json.dump function used to write the file.
    Even though this is not a common behaviour, it is to simplify further data interaction
    by using pandas.read_json that works only if you have a list and not a dict.

    Args:
        path (str): Path name to the location you want the file to be stored

    Returns:
        Dump json file in folder.
    """
    root = Path(path_)

    list_filename_to_join = [
        "commits",
        "blame",
        "branch_status",
        "git_size",
        "complexity",
    ]

    for file in list_filename_to_join:
        dict_ = join_anubisgit_files(path_, fname=f"{file}.json")
        with open(root / f"joined_{file}_monthly.json", "w") as fout:
            json.dump([dict_], fout, indent=4)
