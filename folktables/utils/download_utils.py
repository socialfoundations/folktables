import asyncio
from dataclasses import dataclass
import pathlib

import requests

from folktables import exceptions


@dataclass
class DownloadResource:
    """Stores the data necessary to download the datasets.

    Attributes
    ----------
    url : str
        The URL from where the dataset will be downloaded.
    download_path : pathlib.Path
        Where we'll be saving the content of the HTTP request.
    """
    url: str
    download_path: pathlib.Path


def download_file(url, download_path):
    """Makes a GET request to the specified URL and saves the
    contents of the response to the specified path.

    Parameters
    ----------
    url : str
        URL from where the data will be downloaded.
    download_path : pathlib.Path
        Path to where the downloaded content will be stored.

    Returns
    -------
    download_path : str
        Path to where the content is stored.

    Raises
    ------
    exceptions.FileDownloadError
        This exception is raised if we get an error from our HTTP request
        (i.e., the status code we get from the response is not 200).
    """
    response = requests.get(url)

    if response.status_code != 200:
        raise exceptions.FileDownloadError(
            f'Failed to download the data from: {url}\n'
            f'The HTTP request returned a {response.status_code} status code.'
        )

    with open(download_path, 'wb') as handle:
        handle.write(response.content)

    return download_path


async def async_download_file(url, download_path):
    """Wrapper around `download_file` function in order to give it
    asynchronous capabilities.
    """
    return await asyncio.to_thread(download_file, url, download_path)


def determine_files_to_download(files_resources, download, make_dir=True):
    """Determines which datasets should be downloaded based on whether they
    currently exist in local memory at the specified location.

    Parameters
    ----------
    files_resources : list[FilesResource]
        The FilesResource for the files the user has requested to (down)load.
    download : bool
        Whether the dataset should be downloaded or not.
    make_dir : bool
        Flag to determine whether we should attempt to create a directory
        for every file that has been requested by the user.

    Returns
    -------
    files_to_download : list[FilesResource]
        The datasets that should be downloaded.

    Raises
    ------
    FileNotFoundError
        This error is raised when a file is not found in local memory and
        the user has set the `download` flag to `False`.
    """
    files_to_download = []
    for resource in files_resources:
        # I'm adding this if statement to account for the ACS case in which we
        # only download one dataset at a time and don't have to worry
        # about downloading multilpe files.
        if make_dir:
            pathlib.Path(resource.load_resource.data_dir).mkdir(exist_ok=True)

        if resource.load_resource.file_path.is_file():
            continue

        if not download:
            raise FileNotFoundError(
                f'Could not find the file '
                f'{resource.load_resource.file_name}. Call `get_data` '
                f'with `download=True` to download the '
                f'dataset and corresponding schema.'
            )

        files_to_download.append(resource)

    return files_to_download


async def async_download_files(files_to_download):
    """Asynchronous way of downloading multilpe datasets from a website.

    Parameters
    ----------
    files_to_download : list[FilesResource]
        The FilesResources of the files to be downloaded.
    """
    await asyncio.gather(
        *[async_download_file(
            resource.download_resource.url,
            resource.download_resource.download_path)
          for resource in files_to_download]
    )


def download_datasets(files_to_download):
    """Downloads the datasets from their corresponding websites.
    We're currently using `asyncio` to download multiple files
    asynchronously. This, however, relies on `asyncio`'s `to_thread`
    function which is only available in versions of Python that are 3.9+.

    Parameters
    ----------
    files_to_download : list[FilesResource]
        The FilesResources of the files to be downloaded.
    """
    files_names = list(
        map(lambda resource: resource.load_resource.file_name,
            files_to_download)
    )
    files_names = ' '.join(files_names)
    print(f'Downloading {len(files_to_download)} file(s): {files_names}')

    if len(files_to_download) > 1:
        # We only want to download the files asynchronously if we have to
        # download more than one, as there is not point in paying
        # the price to spawn a thread if we only have to download one file.
        asyncio.run(async_download_files(files_to_download))
    else:
        resource = files_to_download[0]
        download_file(resource.download_resource.url,
                      resource.download_resource.download_path)
