from abc import ABC
from dataclasses import dataclass

from folktables.utils import download_utils
from folktables.utils import load_utils


@dataclass
class FilesResource(ABC):
    """Stores information needed to (down)load the SIPP dataset.

    Attributes
    ----------
    download_resource : download_utils.DownloadResource
        Object containing information necessary to download the SIPP
        dataset.
    load_resource : download_utils.DownloadResource
        Object containing information necessary to load the SIPP dataset.
    """
    download_resource: download_utils.DownloadResource
    load_resource: load_utils.LoadResource
