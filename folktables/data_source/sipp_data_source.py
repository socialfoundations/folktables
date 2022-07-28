from dataclasses import dataclass
from enum import Enum
import os
import pathlib
from typing import Optional

import pandas as pd

from folktables import exceptions
from folktables.utils import download_utils
from folktables.utils import files_resources
from folktables.utils import load_utils

PNUM_VAR = 'PNUM'
SSUID_VAR = 'SSUID'
SIPP_BASE_URL = 'https://www2.census.gov/programs-surveys/sipp/data/datasets/'


class SupportedOS(Enum):
    """Enumeration of the OS SIPP supports for download."""
    WINDOWS_MAC = 'windows/mac'
    GNU_LINUX = 'gnu/linux'


class SupportedPanels(Enum):
    """Enumeration of the available SIPP panels."""
    PANEL_2014 = 2014
    PANEL_2018 = 2018
    PANEL_2019 = 2019
    PANEL_2020 = 2020


@dataclass
class SIPPResource(files_resources.FilesResource):
    """Extends the `DatasetResource` class to add infomration specific
    to the SIPP dataset.

    Attributes
    ----------
    panel : int
        The year of the SIPP dataset to (down)load.
    wave : Optional[int]
        The wave of the panel to be (down)loaded. This only applies if
        the user wants to (down)load the 2014 panel.
    """
    panel: int
    wave: Optional[int] = None


class SIPPDataSource:
    """Data source implementation for SIPP data."""

    def __init__(self, panels, root_dir='data'):
        """Creates a data source around the SIPP data for a specific panels.

        Parameters
        ----------
        panels : Union[list[int], set[int], tuple[int]]
            Year's of the SIPP data to be downloaded.
            We're currently only supporting panels starting from 2014
            (i.e., >= 2014).
        root_dir : str
            Name of the root directory where the data will be stored.
        """
        self._panels = set(sorted(panels))
        self._root_dir = root_dir

    def get_data(self,
                 variables,
                 waves=None,
                 os_to_support='windows/mac',
                 download=False):
        """Gets data from the given list of variables

        Parameters
        ----------
        variables : list[str]
            Names of the variables to be included in the dataset.
        waves : Optional[list[int]]
            The panel waves to be downloaded, e.g., `[1, 2, 3]`.
        os_to_support : str
            OS specification in order to download the correct file. We only
            allow two values: `windows/mac` or `gnu/linux`. This takes a
            default value of `windows/mac`.
        download : bool
            Whether the dataset should be downloaded from the Census Bureau's
            website. This takes a default value of `False`.

        Returns
        -------
        dict[str, pd.DataFrame]
            A dictionary whose keys represent the panel (e.g., "panel_2018")
            and waves (if data for the 2014 panel was requested) and map
            to pandas DataFrames containing the respective SIPP dataset.
        """
        if SupportedPanels.PANEL_2014.value in self._panels:
            # If the year of the SIPP data is 2014, then the user must provide
            # a list of waves they want to download.
            if not isinstance(waves, list):
                raise TypeError(
                    'We are expecting a variable of type `list` for the '
                    '`variables` parameter.'
                )
            if not waves:
                raise ValueError(
                    'The variable you passed for the `variables` parameter '
                    'was empty. You must pass a variable of type `list[int]`'
                )
            # We want to avoid the case in which the user passes duplicate
            # values as this would result in downloading the same file
            # more than once.
            waves = set(waves)

        os_to_support = self._validate_os_to_support(os_to_support)

        variables = self._validate_variables(variables)

        # Create the SIPPResources for the panels to be (down)loaded.
        sipp_resources = self._create_sipp_resources(waves, os_to_support)

        files_to_download = download_utils.determine_files_to_download(
            sipp_resources, download
        )

        if files_to_download:
            self._download_data(files_to_download)

        return self._load_data(sipp_resources, variables)

    def _download_data(self, files_to_download):
        """Downloads the datasets that are not already found in local memory.
        This method, additionally, capitalizes all variable names in order
        to keep dataset conventions consistent across panels.

        Parameters
        ----------
        files_to_download : list[SIPPResource]
            The SIPPResources for the files (and their schemas) that need to
            be downloaded.
        """
        download_utils.download_datasets(files_to_download)

        for file in files_to_download:
            _, extension = os.path.splitext(
                file.download_resource.download_path
            )
            if extension != '.zip':
                continue
            load_utils.extract_content_from_zip(
                file.load_resource.data_dir,
                file.load_resource.file_name,
                file.download_resource.download_path
            )
            self._capitalize_variable_names(file.load_resource.file_path)

    def _load_data(self, sipp_resources, variables):
        """Generates a dictionary whose keys map to pandas DataFrames
        containing the requested SIPP datasets.

        Parameters
        ----------
        sipp_resources : list[SIPPResource]
            The SIPPResources necessary to load the SIPP datasets.
        variables : set(str)
            The variables the user wants to load.

        Returns
        -------
        data : dict[str, pd.DataFrame]
            A dictionary whose keys represent the panel (e.g., "panel_2018")
            and waves (if data for the 2014 panel was requested) and map
            to pandas DataFrames containing the respective SIPP dataset.
        """
        data_types = self._setup_data_types(sipp_resources[1], variables)

        data = {}
        for i in range(0, len(sipp_resources), 2):
            data_resource = sipp_resources[i]

            panel_i = data_resource.panel
            wave_i = data_resource.wave

            dict_entry_name = f'panel_{panel_i}'
            load_message = f'Loading the data for the {panel_i} panel'
            if wave_i is not None:
                dict_entry_name = f'{dict_entry_name}_wave_{wave_i}'
                load_message = f'{load_message} with corresponding wave '\
                               f'{wave_i}'

            print(load_message)
            data[dict_entry_name] = pd.read_csv(
                data_resource.load_resource.file_path,
                dtype=data_types,
                sep='|',
                header=0,
                usecols=list(variables)
            )
        return data

    def _create_sipp_resources(self, waves, os_to_support):
        """Creates a list of SIPPResources for corresponding to the datasets
        and their corresponding schemas the user wants to download.

        Parameters
        ----------
        waves : list[int]
            The panel waves to be downloaded, e.g., `[1, 2, 3]`.

        os_to_support : Enum[SupportedOS]
            Enum defining for which OS the file should be downloaded.

        Returns
        -------
        sipp_resources : list[SIPPResource]
            The SIPPResources necessary to (down)load the SIPP datasets.
        """
        sipp_resources = []
        for panel in self._panels:
            data_dir = pathlib.Path(self._root_dir, f'sipp_{panel}')

            if panel == SupportedPanels.PANEL_2014.value:
                for wave in waves:
                    sipp_resources.extend(
                        self._setup_sipp_files_resources(data_dir,
                                                         panel,
                                                         os_to_support,
                                                         wave)
                    )
            else:
                sipp_resources.extend(
                    self._setup_sipp_files_resources(data_dir,
                                                     panel,
                                                     os_to_support)
                )

        return sipp_resources

    @staticmethod
    def _validate_os_to_support(os_to_support):
        """Checks that the user has correctly specified an OS and converts
        it to the equivalent enum.

        Parameters
        ----------
        os_to_support : str
            Name of the OS for which the user wants to (down)load the data.

        Returns
        -------
        Enum[SupportedOS]
            The enum representation of the value the user passed.

        Raises
        ------
        exceptions.UnsupportedOSError
            This is raised when the user passes the value for an OS for which
            the SIPP data is not supported.
        """
        if os_to_support.lower() not in {
                SupportedOS.WINDOWS_MAC.value,
                SupportedOS.GNU_LINUX.value}:
            raise exceptions.UnsupportedOSError(
                f'The value "{os_to_support}" you passed in the '
                f'`os_to_support` parameter is not supported by the Census '
                f'Bureau to download the SIPP dataset. Please pass one of the'
                f' following options: '
                f'`{SupportedOS.WINDOWS_MAC.value}`, '
                f'`{SupportedOS.GNU_LINUX.value}`'
            )

        if os_to_support.lower() == SupportedOS.WINDOWS_MAC.value:
            return SupportedOS.WINDOWS_MAC
        return SupportedOS.GNU_LINUX

    @staticmethod
    def _validate_variables(variables):
        """Checks that the variables passed by the user contain the variables:
        `PNUM` and `SSUID` as they are helpful when identifying unique
        respondents. It additionally converts the list of variables into a
        set for faster hashing in the future.

        Paraemters
        ----------
        variables : list[str]
            The variables the user wants to load.
        """
        variables = set(map(lambda var: var.upper(), variables))
        if PNUM_VAR not in variables:
            print(f'Adding `{PNUM_VAR}` to the list of variables.')
            variables.add(PNUM_VAR)
        if SSUID_VAR not in variables:
            print(f'Adding `{SSUID_VAR}` to the list of variables.')
            variables.add(SSUID_VAR)

        return variables

    @staticmethod
    def _setup_data_types(schema_resource, variables):
        """Get the data types for the variables requested by the user from
        the dataset's schema.

        Parameters
        ----------
        schema_resource : SIPPResource
            A SIPPResource for a schema file.
        variables : list[str]
            Names of the variables to be included in the dataset.

        Returns
        -------
        data_types : dict[str, str]
            A dictionary mapping variable names to their corresponding data
            types.
        """
        schema_json = load_utils.load_json(
            schema_resource.load_resource.file_path
        )
        data_types = {}
        for data in schema_json:
            if data['name'] in variables:
                dtype = None

                if data['dtype'] == 'integer':
                    dtype = 'int64'
                elif data['dtype'] == 'string':
                    dtype = 'object'
                elif data['dtype'] == 'float':
                    dtype = 'float64'

                data_types[data['name']] = dtype

        return data_types

    @staticmethod
    def _setup_sipp_files_resources(data_dir,
                                    panel,
                                    os_to_support,
                                    wave=None):
        """Sets up a SIPPResource for a dataset to be (down)loaded. This
        method dynamically generates the URLs, file paths, and download
        paths necessary to perform the download and load functions.

        Parameters
        ----------
        data_dir : pathlib.Path
            The directory where the data will be stored.
        panel : int
            The year of the dataset to be downloaded.
        os_to_support : Enum[SupportedOS]
            Enum defining for which OS the file should be downloaded.
        wave : int
            The panel's wave to be downloaded.

        Returns
        -------
        [data_resource, schema_resource] : list[SIPPResource, SIPPResource]
            A list containing two SIPPResources, one for the dataset and one
            for its corresponding schema.
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

        if os_to_support == SupportedOS.WINDOWS_MAC:
            if panel == SupportedPanels.PANEL_2014:
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

        data_download_resource = download_utils.DownloadResource(
            url=data_url, download_path=pathlib.Path(data_dir, zip_file_name)
        )
        schema_download_resource = download_utils.DownloadResource(
            url=schema_url, download_path=pathlib.Path(data_dir,
                                                       schema_file_name)
        )

        data_load_resource = load_utils.LoadResource(
            file_name=data_file_name, data_dir=data_dir,
            file_path=pathlib.Path(data_dir, data_file_name)
        )
        schema_load_resource = load_utils.LoadResource(
            file_name=schema_file_name, data_dir=data_dir,
            file_path=pathlib.Path(data_dir, schema_file_name)
        )

        data_resource = SIPPResource(
            download_resource=data_download_resource,
            load_resource=data_load_resource,
            panel=panel,
            wave=wave
        )
        schema_resource = SIPPResource(
            download_resource=schema_download_resource,
            load_resource=schema_load_resource,
            panel=panel,
            wave=wave
        )

        return [data_resource, schema_resource]

    @staticmethod
    def _capitalize_variable_names(file_path):
        """Capitalizes all the variable names (first row) for a given file.

        Parameters
        ----------
        file_path : str
            Path to where the file is stored.

        Notes
        -----
        This is needed because the capitalization of variables is not
        consistent across panels. For instance, `SSUID` is capitalized in the
        2018 panel but not in the 2014 panel. Hence, to have everything
        consistent across panels, we're capitalizing all variables. This
        incurs a lot of cost to the program, but it will only happen when the
        user first downloads the dataset.
        """
        # TODO: think of a better way to do this (OR WHETHER WE WANT TO HANDLE
        # THIS).
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.readlines()

        data[0] = data[0].upper()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(data)
