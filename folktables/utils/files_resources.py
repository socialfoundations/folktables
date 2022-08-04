from dataclasses import dataclass
import pathlib


@dataclass
class FilesResource:
    """Stores information needed to (down)load a dataset.

    Attributes
    ----------
    url : str
        The URL from where the dataset will be downloaded.
    download_path : pathlib.Path
        Where we'll be saving the content of the HTTP request.
    file_name : str
        Name of the file where the dataset is stored in local memory.
    data_dir : str
        Name of the directory where the dataset is stored in local memory.
    """
    url: str
    download_path: pathlib.Path
    file_name: str
    data_dir: str

    @property
    def file_path(self):
        """Generates a pathlib.Path object pointing to where the data
        is (will be) stored based on the `file_name` and `data_dir`
        properties.

        Returns
        -------
        pathlib.Path
            The path to where the file is (will be) stored.
        """
        return pathlib.Path(self.data_dir, self.file_name)
