import json


def save_data_to_json(data: list, dst_filepath: str) -> None:
    """Saves data to json.

    Args:
        data: Source data to save in json format.
        dst_filepath: Path to destination file.

    """
    with open(dst_filepath, 'w') as json_file:
        json.dump(data, json_file, indent=2)
