"""External analysis for anubisgit"""

from tucan.struct_common import FIELDS_EXTENSIVE, FIELDS_INTENSIVE, FIELDS_SIZES


def rearrange_tucan_complexity_db(tucan_out: dict) -> dict:
    """
    Reformat the complexity database of tucan to be a better fit for anubisgit parsing
    and gathering of data.

    Args:
        tucan_out (dict): Dict of the tucan structural analysis

    Returns:
        dict: Rearranged tucan structural / complexity dict
    """
    fields = FIELDS_SIZES + FIELDS_EXTENSIVE + FIELDS_INTENSIVE
    fields.extend([f"{field}_int" for field in FIELDS_INTENSIVE])
    fields.extend([f"{field}_ext" for field in FIELDS_EXTENSIVE])

    # Initialize empty lists for each field
    tucan_db = {field: [] for field in fields}
    tucan_db.update(
        {"param": [], "size": [], "file": [], "function": [], "start": [], "end": []}
    )
    # Iterate over files and functions
    for file_name, functions in tucan_out.items():
        if functions:
            for func_name, func_data in functions.items():
                if not func_data["contains"]:
                    # Add field values to tucan_db
                    for field in fields:
                        tucan_db[field].append(func_data[field])

                    # Add additional fields
                    tucan_db["param"].append(1)  # Params default to 1
                    tucan_db["size"].append(
                        func_data["ssize"]
                    )  # TODO :move ev'rthg in anubisgit from size to ssize
                    tucan_db["file"].append(file_name)
                    tucan_db["function"].append(func_name)
                    tucan_db["start"].append(func_data["lines"][0])
                    tucan_db["end"].append(func_data["lines"][1])
    return tucan_db
