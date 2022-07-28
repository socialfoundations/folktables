from dataclasses import dataclass
import json
import pathlib
import zipfile


@dataclass
class LoadResource:
    """Stores the data necessary to download the datasets.

    Attributes
    ----------
    file_name : str
        Name of the file where the dataset is stored in local memory.
    data_dir : str
        Name of the directory where the dataset is stored in local memory.
    file_path : pathlib.Path
        Where the dataset will be stored in local memory.
    """
    file_name: str
    data_dir: str
    file_path: pathlib.Path


def extract_content_from_zip(data_dir, file_name, download_path):
    """Extracts the contents from a Zip file, and removes the Zip file
    if its file path is not the same as that of the extracted
    file.

    Parameters
    ----------
    data_dir : str
        Path to the directory where the file will be stored.
    file_name : str
        Name that will be given to the extracted file.
    download_path : str
        Path to where the Zip file is located.
    """
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extract(file_name, path=data_dir)

    if download_path != pathlib.Path(data_dir, file_name):
        pathlib.Path.unlink(download_path)


def load_json(file_path):
    """Loads a JSON file based on the given file path.

    Parameters
    ----------
    file_path : pathlib.Path
        Path to the JSON file to be loaded.

    Returns
    -------
    data : dict
        A dictionary containing the JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data
