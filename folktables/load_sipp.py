import asyncio
from dataclasses import dataclass
from enum import Enum
import json
import os
import requests
from typing import Optional
import zipfile

import pandas as pd

SIPP_BASE_URL = 'https://www2.census.gov/programs-surveys/sipp/data/datasets/'


class SupportedOS(Enum):
    """Enumeration of the OS SIPP supports for download."""
    WINDOWS_MAC = 'windows/mac'
    GNU_LINUX = 'gnu/linux'


class SupportedPanels(Enum):
    """Enumeration of the OS SIPP supports for download."""
    PANEL_2014 = 2014
    PANEL_2018 = 2018
    PANEL_2019 = 2019
    PANEL_2020 = 2020


@dataclass
class FileResources:
    """Stores the data necessary to download and load the data files."""
    file_name: str
    file_path: str
    url: str
    data_dir: str
    download_path: str
    panel: int
    wave: Optional[int] = None
    zip_file_name: Optional[str] = None


def load_json(file_path):
    """
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    return data


def download_file(url, download_path):
    """Downloads the file from a specified URL and returns the response.

    Parameters
    ----------
    url : str
        URL from where the data will be downloaded.
    download_path : str
        Path to where the downloaded content will be stored.
    """
    response = requests.get(url)

    if response.status_code != 200:
        # TODO: we'll probably want to create our own exception to account
        # for this scenario.
        raise ValueError(f'{response.status_code}\n{url}')

    with open(download_path, 'wb') as handle:
        handle.write(response.content)

    return download_path


async def async_download_file(url, download_path):
    """Wrapper around `download_file` function in order to give it
    asynchronous capabilities.
    """
    return await asyncio.to_thread(download_file, url, download_path)


def extract_zip(data_dir, file_name, download_path):
    """
    """
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extract(file_name, path=data_dir)

    if download_path != os.path.join(data_dir, file_name):
        os.remove(download_path)


def capitalize_variable_names(file_path):
    """Capitalizes all the variable names (first row) for a given file.

    Notes
    -----
    This is needed because the capitalization of variables is not consistent
    across panels. For instance, `SSUID` is capitalized in the 2018 panel
    but not in the 2014 panel. Hence, to have everything consistent across
    panels, we're capitalizing all variables. This incurs a lot of cost to
    the program, but it will only happen when the user first downloads the
    dataset.
    """
    # TODO: think of a better way to do this (OR WHETHER WE WANT TO HANDLE
    # THIS).
    with open(file_path, 'r') as file:
        data = file.readlines()

    data[0] = data[0].upper()

    with open(file_path, 'w') as file:
        file.writelines(data)


async def download_and_extract(files_resources, download):
    """
    """
    # Determine which files we have to download.
    files_to_download = []
    files_names = []
    for file_resource in files_resources:
        os.makedirs(file_resource.data_dir, exist_ok=True)

        if os.path.isfile(file_resource.file_path):
            continue

        if not download:
            raise FileNotFoundError(
                f'Could not find the file {file_resource.file_name}. '
                f'Call `get_data` with `download=True` to download the '
                f'dataset and corresponding schema.'
            )
        files_to_download.append(file_resource)
        files_names.append(file_resource.file_name)

    if not files_to_download:
        # We don't need to download or extract any files.
        return

    files_names = ' '.join(files_names)
    print(f'Downloading {len(files_to_download)} files: {files_names}')
    # Download all the files that don't exist in the specified `root_dir`.
    await asyncio.gather(
        *[async_download_file(file.url, file.download_path)
          for file in files_to_download]
    )

    # Extract the data files from their Zip files.
    for file in files_to_download:
        if file.zip_file_name is None:
            continue
        extract_zip(file.data_dir, file.file_name, file.download_path)
        capitalize_variable_names(file.file_path)


def setup_files_resources(base_data_dir, panel, os_to_support, wave=None):
    """Generates the URL, file name, and directory name for each file to be
    downloaded.

    Parameters
    ----------
    base_data_dir : str
        Path to the directory where the files are (or will be) stored.
    panel : int
        Year of the data to be loaded.
    os_to_support : str
        OS specification in order to download the correct file.
    wave : Optional[int]
        Number representing the wave to be downloaded. This is only used when
        the 2014 panel is being requested.

    Returns
    -------
    data_file_resource : FileResources
        Object containing the file name, url, path to directory, and name of
        the zip file for the data being (down)loaded.
    schema_file_resource : FileResources
        Object containing the file name, url, and path to directory for the
        schema of the data being (down)loaded.
    """
    file_name = f'pu{panel}'
    panel_url = f'{SIPP_BASE_URL}{panel}/'

    if panel == SupportedPanels.PANEL_2014.value:
        # The 2014 panel follows its own convention, so we'll need to
        # modify the variables to account for it.
        file_name = f'{file_name}w{wave}'
        panel_url = f'{panel_url}w{wave}/'

    data_file_name = f'{file_name}.csv'
    schema_file_name = f'{file_name}_schema.json'

    if os_to_support == SupportedOS.WINDOWS_MAC.value:
        if panel == SupportedPanels.PANEL_2014.value:
            zip_file_name = f'{file_name}.zip'
        else:
            zip_file_name = f'{file_name}_csv.zip'
    else:
        zip_file_name = f'{file_name}.csv.gz'

    data_url = f'{panel_url}{zip_file_name}'
    schema_url = f'{panel_url}{schema_file_name}'

    if panel == SupportedPanels.PANEL_2014.value:
        name, extension = os.path.splitext(data_file_name)
        data_file_name = f'{name.upper()}{extension}'

    # We'll create two FileResources: one for the data and one for the schema.
    data_file_resources = FileResources(file_name=data_file_name,
                                        file_path=os.path.join(
                                             base_data_dir, data_file_name),
                                        url=data_url,
                                        data_dir=base_data_dir,
                                        download_path=os.path.join(
                                            base_data_dir, zip_file_name),
                                        zip_file_name=zip_file_name,
                                        panel=panel,
                                        wave=wave)

    schema_file_resources = FileResources(file_name=schema_file_name,
                                          file_path=os.path.join(
                                             base_data_dir, schema_file_name),
                                          url=schema_url,
                                          data_dir=base_data_dir,
                                          download_path=os.path.join(
                                             base_data_dir, schema_file_name),
                                          panel=panel,
                                          wave=wave)

    return data_file_resources, schema_file_resources


def load_sipp(root_dir,
              panels,
              waves,
              variables,
              os_to_support,
              download=False):
    """
    """
    # Create the URLs,file names, and file paths we'll need to download
    # and load the data and schema files.
    files_resources = []
    for panel in panels:
        base_data_dir = os.path.join(root_dir, f'sipp_{panel}')

        if panel == SupportedPanels.PANEL_2014.value:
            for wave in waves:
                data_resources, schema_resources = setup_files_resources(
                    base_data_dir, panel, os_to_support, wave
                )
                files_resources.append(data_resources)
                files_resources.append(schema_resources)
        else:
            data_resources, schema_resources = setup_files_resources(
                base_data_dir, panel, os_to_support
            )
            files_resources.append(data_resources)
            files_resources.append(schema_resources)

    asyncio.run(download_and_extract(files_resources, download))

    # Now that we have all the files the user has requested, we're going to
    # go ahead and get the datatypes from the schema and load the data into
    # a pandas DataFrame.
    # TODO: double check that variables across different SIPP panels are
    # conserved (i.e., that no variable from the 2014 panel gets deprecated,
    # because if so, we'll need to change the code below to account for it).
    schema_resources = files_resources[1]
    schema_json = load_json(schema_resources.file_path)
    data_types = {}
    for data in schema_json:
        if data['name'] in variables:
            dtype = None

            if data['dtype'] == 'integer':
                dtype = 'Int64'
            elif data['dtype'] == 'string':
                dtype = 'object'
            elif data['dtype'] == 'float':
                dtype = 'Float64'

            data_types[data['name']] = dtype

    data = {}
    for i in range(0, len(files_resources), 2):
        data_resources = files_resources[i]

        panel_i = data_resources.panel
        wave_i = data_resources.wave

        dict_entry_name = f'panel_{panel_i}'
        load_message = f'Loading the data for the {panel_i} panel'
        if wave_i is not None:
            dict_entry_name = f'{dict_entry_name}_wave_{wave_i}'
            load_message = f'{load_message} with corresponding wave {wave_i}'

        print(load_message)
        data[dict_entry_name] = pd.read_csv(data_resources.file_path,
                                            dtype=data_types,
                                            sep='|',
                                            header=0,
                                            usecols=list(variables))
    return data
