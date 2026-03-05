import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
import os
import json
from pathlib import Path



@ensure_annotations
def read_yaml(path_to_yaml: str) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.

    Args:
        path_to_yaml (str): The file path to the YAML file."""
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    except BoxValueError as e:
        raise ValueError(f"Error converting YAML content to ConfigBox: {e}")
    except Exception as e:
        raise ValueError(f"Error reading YAML file: {e}")
# Define a function to create directories if they don't exist
def create_directories(path_to_directories: list[str]) -> None:
    """
    Creates directories if they do not exist.

    Args:
        path_to_directories (list): A list of directory paths to create."""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)

# Define a function to save a Python object as a JSON file
def save_json(path:Path, data: object) -> None:
    """
    Saves a Python object as a JSON file.

    Args:
        path (Path): The file path where the JSON file will be saved.
        data (object): The Python object to be saved as JSON."""
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
# Define a function to load a Python object from a JSON file
def load_json(path: Path) -> object:
    """
    Loads a Python object from a JSON file.

    Args:
        path (Path): The file path to the JSON file."""
    with open(path, 'r') as json_file:
        return json.load(json_file)
# Define a function to save a Python object using joblib