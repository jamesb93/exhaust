import json as rj


def write_json(json_file_path: str, in_dict: dict, indent: int = 4):
    """Takes a dictionary and writes it to JSON file"""
    with open(json_file_path, "w+") as fp:
        rj.dump(in_dict, fp, indent=indent)