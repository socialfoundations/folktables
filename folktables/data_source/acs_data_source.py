from dataclasses import dataclass
import io
import pathlib
import random

import numpy as np
import pandas as pd

from folktables.utils import download_utils
from folktables.utils import files_resources
from folktables.utils import load_utils

ACS_BASE_URL = 'https://www2.census.gov/programs-surveys/acs/data/pums/'

STATES_CODES = {
    'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06', 'CO': '08',
    'CT': '09', 'DE': '10', 'FL': '12', 'GA': '13', 'HI': '15', 'ID': '16',
    'IL': '17', 'IN': '18', 'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22',
    'ME': '23', 'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28',
    'MO': '29', 'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33', 'NJ': '34',
    'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38', 'OH': '39', 'OK': '40',
    'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45', 'SD': '46', 'TN': '47',
    'TX': '48', 'UT': '49', 'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54',
    'WI': '55', 'WY': '56', 'PR': '72'
}


@dataclass
class ACSResource(files_resources.FilesResource):
    """Extends the `DatasetResource` class to add infomration specific
    to the SIPP dataset.

    We currently don't need to any any more attributes to this class; however,
    we're still creating it to keep things uniform across different
    DataSources.
    """


class ACSDataSource:
    """Data source implementation for SIPP data."""

    def __init__(self, survey_year, horizon, survey, root_dir="data"):
        """Create data source around PUMS data for specific year,
        time horizon, survey type.

        Parameters
        ----------
        survey_year : str
            Year of ACS PUMS data, e.g., '2018'.
        horizon: str
            Must be '1-Year' or '5-Year'.
        survey: str
            Must be 'person' or 'household'.
        """
        if horizon not in {'1-Year', '5-Year'}:
            raise ValueError('Horizon must be either "1-Year" or "5-Year"')

        if int(survey_year) < 2014:
            raise ValueError('Year must be >= 2014')

        self._survey_year = survey_year
        self._horizon = horizon
        self._survey = survey
        self._root_dir = root_dir

    def get_data(self,
                 states=None,
                 density=1.0,
                 random_seed=0,
                 join_household=False,
                 download=False):
        """(Down)loads a sample of the ACS dataset based on the specified
        states.

        Parameters
        ----------
        states : list[str]
            The states for which datasets will be downloaded.
        density : float
            Used to sample the datasets.
        random_seed : int
            Seed for the random number generator.
        join_household : bool:
            Whether or not to join with the households dataset.
        download : bool
            Whether the dataset should be downloaded or not.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the sample of the ACS dataset.
        """
        if states is None:
            states = list(STATES_CODES.keys())
        else:
            states = list(map(lambda state: state.upper(), states))

        data = self._load_acs(states=states,
                              survey=self._survey,
                              density=density,
                              random_seed=random_seed,
                              download=download)
        if join_household:
            orig_len = len(data)
            assert self._survey == 'person'
            household_data = self._load_acs(states=states,
                                            survey='household',
                                            serial_filter_list=list(
                                                data['SERIALNO']
                                            ),
                                            download=download)

            # We only want to keep the columns in the household dataframe
            # that don't appear in the person dataframe, but we *do* want
            # to include the SERIALNO column to merge on.
            household_cols = (
                set(household_data.columns) - set(data.columns)
            ).union(set(['SERIALNO']))
            join = pd.merge(
                data, household_data[list(household_cols)], on=['SERIALNO']
            )
            assert len(join) == orig_len,\
                f'Lengths do not match after join: {len(join)} vs {orig_len}'
            return join

        return data

    def _load_acs(self,
                  states=None,
                  survey='person',
                  density=1,
                  random_seed=1,
                  serial_filter_list=None,
                  download=False):
        """Driver method to (down)load the ACS dataset.

        Parameters
        ----------
        states : list[str]
            The states for which datasets will be downloaded.
        survey : str
            Whether the user is requesting the "person" or "household" survey.
        density : float
            Used to sample the datasets.
        random_seed : int
            Seed for the random number generator.
        serial_filter_list : list[str]
            Serial numbers for the respondents to be included in the
            sampled data.
        download : bool
            Whether the dataset should be downloaded or not.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the sample of the ACS dataset.
        """

        if serial_filter_list is not None:
            serial_filter_list = set(serial_filter_list)

        acs_resources = self._create_acs_resources(states, survey)

        files_to_download = download_utils.determine_files_to_download(
            files_resources=acs_resources,
            download=download,
            make_dir=False
        )

        if files_to_download:
            self._download_data(files_to_download)

        return self._load_data(acs_resources,
                               density,
                               random_seed,
                               serial_filter_list)

    def _create_acs_resources(self,
                              states,
                              survey):
        """Creates a list of ACSResources containing the information
        needed to (down)load the requested datasets.

        Parameters
        ----------
        states : list[str]
            The states for which datasets will be downloaded.
        survey : str
            Whether the user is requesting the "person" or "household" survey.

        Returns
        -------
        acs_resources : list[ACSResource]
            The ACSResources for the datasets to be (down)loaded.
        """
        data_dir = pathlib.Path(self._root_dir,
                                str(self._survey_year),
                                self._horizon)
        pathlib.Path(data_dir).mkdir(exist_ok=True, parents=True)
        survey_code = 'p' if survey == 'person' else 'h'

        acs_resources = []
        for state in states:
            acs_resources.append(
                self._setup_acs_files_resources(data_dir,
                                                state,
                                                survey_code)
            )

        return acs_resources

    def _setup_acs_files_resources(self, data_dir, state, survey_code):
        """Sets up an ACSResource for a dataset to be (down)loaded. This
        method dynamically generates the URLs, file paths, and download
        paths necessary to perform the download and load functions.

        Parameters
        ----------
        data_dir : pathlib.Path
            The directory where the data will be stored.
        state : str
            The state for which the data will be downloaded.
        survey_code : str
            Whether the user is requesting the "person" or "household" survey.

        Returns
        -------
        ACSResource
            Object containign all the information necessary to (down)load
            the dataset.
        """
        try:
            state_code = STATES_CODES[state]
        except KeyError:
            raise ValueError(
                f'"{state}" in an invalid state. Please select one of the '
                f'following:\n{list(STATES_CODES.keys())}'
            )

        if int(self._survey_year) >= 2017:
            data_file_name = f'psam_{survey_code}{state_code}.csv'
        else:
            # 2016 and earlier use different file names.
            data_file_name = \
                f'ss{str(self._survey_year)[-2:]}'\
                f'{survey_code}{state.lower()}.csv'

        zip_file_name = f'csv_{survey_code}{state.lower()}.zip'
        url = f'{ACS_BASE_URL}{self._survey_year}/{self._horizon}/'\
              f'{zip_file_name}'

        data_download_resource = download_utils.DownloadResource(
            url=url, download_path=pathlib.Path(data_dir, zip_file_name)
        )
        data_load_resource = load_utils.LoadResource(
            file_name=data_file_name, data_dir=data_dir,
            file_path=pathlib.Path(data_dir, data_file_name)
        )
        return ACSResource(download_resource=data_download_resource,
                           load_resource=data_load_resource)

    @staticmethod
    def _create_data_sample(acs_resources,
                            density,
                            random_seed,
                            serial_filter_list):
        """Creates a sample from all the datasets the user has requested.

        Parameters
        ----------
        acs_resources : list[ACSResource]
            The ACSResources of the files to be loaded.
        density : float
            Used to sample the datasets.
        random_seed : int
            Seed for the random number generator.
        serial_filter_list : list[str]
            Serial numbers for the respondents to be included in the
            sampled data.

        Returns
        -------
        sample : io.StringIO
            In memory file-like object containing the sampled data.
        """
        random.seed(random_seed)
        sample = io.StringIO()
        first = True

        for resource in acs_resources:
            with open(resource.load_resource.file_path, 'r') as file:
                if first:
                    sample.write(next(file))
                    first = False
                else:
                    next(file)

                for line in file:
                    if serial_filter_list is None:
                        if random.uniform(0, 1) < density:
                            sample.write(line.replace(' ', ''))
                    else:
                        serialno = line.split(',')[1]
                        if serialno in serial_filter_list:
                            sample.write(line.replace(' ', ''))

        sample.seek(0)
        return sample

    def _load_data(self,
                   acs_resources,
                   density,
                   random_seed,
                   serial_filter_list):
        """Loads a sample of the datasets specified by the user into a
        pandas DataFrame.

        Parameters
        ----------
        acs_resources : list[ACSResource]
            The ACSResources of the files to be loaded.
        density : float
            Used to sample the datasets.
        random_seed : int
            Seed for the random number generator.
        serial_filter_list : list[str]
            Serial numbers for the respondents to be included in the
            sampled data.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the sample of the ACS dataset.
        """
        sample = self._create_data_sample(acs_resources,
                                          density,
                                          random_seed,
                                          serial_filter_list)
        data_types = {
            'PINCP': np.float64,
            'RT': str,
            'SOCP': str,
            'SERIALNO': str,
            'NAICSP': str
        }

        return pd.read_csv(sample, dtype=data_types)

    @staticmethod
    def _download_data(files_to_download):
        """Downloads the dataset files that couldn't be found in local
        memory, and extracts them from the Zip file that they come in.

        Parameters
        ----------
        files_to_download : list[ACSResource]
            The ACSResources of the files to be downloaded.
        """
        download_utils.download_datasets(files_to_download)

        for file in files_to_download:
            load_utils.extract_content_from_zip(
                file.load_resource.data_dir,
                file.load_resource.file_name,
                file.download_resource.download_path
            )
