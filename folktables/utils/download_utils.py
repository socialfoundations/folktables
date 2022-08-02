import concurrent.futures
import os
import pathlib

import requests

from folktables import exceptions


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


def async_download_file(files_resource):
    """Wrapper around `download_file` function. This function allows us to
    get the `url` and `download_path` from a `files_resource` and pass them
    to the `download_file` function.
    """
    return download_file(files_resource.url,
                         files_resource.download_path)


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
        if make_dir:
            pathlib.Path(resource.data_dir).mkdir(exist_ok=True)

        if resource.file_path.is_file():
            continue

        if not download:
            raise FileNotFoundError(
                f'Could not find the file '
                f'{resource.file_name}. Call `get_data` '
                f'with `download=True` to download the '
                f'dataset and corresponding schema.'
            )

        files_to_download.append(resource)

    return files_to_download


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
        map(lambda resource: resource.file_name, files_to_download)
    )
    files_names = ' '.join(files_names)
    print(f'Downloading {len(files_to_download)} file(s): {files_names}')

    # We're currently using the number of threads equivalent to the minimum
    # between the number of CPUs and the number of files to download; however,
    # we can change this to follow a different behavior.
    num_cpus = os.cpu_count()
    if num_cpus is None:
        num_threads = 1
    else:
        num_threads = min(num_cpus, len(files_to_download))

    if len(files_to_download) > 1:
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=num_threads
        ) as executor:
            executor.map(async_download_file, files_to_download)

    else:
        resource = files_to_download[0]
        download_file(resource.url, resource.download_path)
