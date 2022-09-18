from enum import Enum
import io
import pathlib
import random

import numpy as np
import pandas as pd

from folktables.utils import download_utils
from folktables.utils import files_resources
from folktables.utils import load_utils

ACS_BASE_URL = 'https://www2.census.gov/programs-surveys/acs/data/pums/'
ACS_DEFINITIONS_URL = 'https://www2.census.gov/programs-surveys/acs/tech_docs'\
    '/pums/data_dict/'

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

DATA_TYPES = {
    'PINCP': np.float64,
    'RT': str,
    'SOCP': str,
    'SERIALNO': str,
    'NAICSP': str
}


class Horizons(Enum):
    """The supported horizons."""
    YEAR_1 = '1-Year'
    YEAR_5 = '5-Year'


class Surveys(Enum):
    """The valid survey types."""
    PERSON = 'person'
    HOUSEHOLD = 'household'


class ACSDataSource:
    """Data source implementation for ACS data."""

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
        root_dir : str
            String representing the path to where the data is (shoudl be)
            stored.
        """
        self._survey_year = self._validate_survey_year(survey_year)
        self._horizon = self._validate_horizon(horizon)
        self._survey = self._validate_survey(survey)
        self._root_dir = root_dir

    @staticmethod
    def _validate_survey_year(survey_year):
        """Checks that the survey year is greater than or equal to 2014.

        Parameters
        ----------
        survey_year : str
            The year of the survey the user is requesting.

        Returns
        -------
        survey_year : str
            The same survey year the user is requesting if it's valid.

        Raises
        ------
        ValueError
            This exception is raised if the survey year is less than 2014.
        """
        if int(survey_year) < 2014:
            raise ValueError('Year must be >= 2014')

        return survey_year

    @staticmethod
    def _validate_horizon(horizon):
        """Checks that the horizon the user is requesting is either a 1-Year
        or 5-Year horizon.

        Parameters
        ----------
        horizon : str
            The horizon the user is requesting.

        Returns
        -------
        Horizons
            The enumeration of the horizon the user is requesting.

        Raises
        ------
        ValueError
            A ValueError is raised if the horizon being requested is not one
            of: `1-Year` or `5-Year`.
        """
        if horizon not in {Horizons.YEAR_1.value, Horizons.YEAR_5.value}:
            raise ValueError('Horizon must be either "1-Year" or "5-Year"')

        if horizon == Horizons.YEAR_1.value:
            return Horizons.YEAR_1

        return Horizons.YEAR_5

    @staticmethod
    def _validate_survey(survey):
        """Cheks the survey being requested is either for a person or a
        household.

        Parameters
        ----------
        survey : str
            The type of survey the user is requesting.

        Returns
        -------
        Surveys
            The enumeration of the survey the user is requesting.

        Raises
        ------
        ValueError
            A ValueError is raised if the survey being requested is not one of:
            `person` or `household`.
        """
        if survey not in {Surveys.PERSON.value, Surveys.HOUSEHOLD.value}:
            raise ValueError(
                f'Survey must be either {Surveys.PERSON.value} '
                f'or {Surveys.HOUSEHOLD.value}'
            )

        if survey == Surveys.PERSON.value:
            return Surveys.PERSON

        return Surveys.HOUSEHOLD

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
            states = [state.upper() for state in states]

        data = self._load_acs(states=states,
                              survey=self._survey.value,
                              density=density,
                              random_seed=random_seed,
                              download=download)

        if not join_household:
            return data

        orig_len = len(data)

        if self._survey.value == 'person':
            raise ValueError(
                'Make sure that if `join_household` is True, that the '
                '`survey` value is `person`.'
            )

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

    def get_definitions(self, download=False):
        """Gets the categorial data definitions dataframe.
        Only works for year>=2017 as previous years don't include .csv
        definition files.

        Parameters
        ----------
        download : bool
            Whether the dataset should be downloaded or not.
        """
        if int(self._survey_year) < 2017:
            raise ValueError(
                '`get_definitions` is only supported for survey years >= 2017.'
            )

        base_datadir = pathlib.Path(self._root_dir,
                                    self._survey_year,
                                    self._horizon.value)

        file_path = pathlib.Path(base_datadir, 'definition.csv')
        if file_path.is_file():
            return pd.read_csv(file_path,
                               sep=',',
                               header=None,
                               names=list(range(7)))

        if not download:
            raise FileNotFoundError(
                f'Could not find {self._survey_year} {self._horizon.value} '
                f'attribute definition. Call get_definitions with download='
                f'True to download the definitions.'
            )

        # Create the directory if it doesn't exist.
        pathlib.Path(base_datadir).mkdir(exist_ok=True,
                                         parents=True)

        print('Downloading the attribute definition file...')
        if self._horizon.value == '1-Year':
            year_string = self._survey_year
        else:
            year_string = f'{int(self._survey_year) - 4}-{self._survey_year}'

        url = f'{ACS_DEFINITIONS_URL}PUMS_Data_Dictionary_{year_string}.csv'

        download_utils.download_file(url, file_path)

        return pd.read_csv(file_path,
                           sep=',',
                           header=None,
                           names=list(range(7)))

    def _load_acs(self,
                  states=None,
                  survey='person',
                  density=1.0,
                  random_seed=1,
                  serial_filter_list=None,
                  download=False):
        """Driver method to (down)load the ACS dataset.

        Parameters
        ----------
        states : list[str]
            The states for which datasets will be downloaded.
        survey : Surveys
            Enum of the survey type the user is requesting. It can take one
            of two values: `person` or `household`.
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

        acs_resources = self._create_files_resources(states, survey)

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

    def _create_files_resources(self,
                                states,
                                survey):
        """Creates a list of FilesResource containing the information
        needed to (down)load the requested datasets.

        Parameters
        ----------
        states : list[str]
            The states for which datasets will be downloaded.
        survey : str
            Whether the user is requesting the "person" or "household" survey.

        Returns
        -------
        acs_resources : list[FilesResource]
            The FilesResources for the datasets to be (down)loaded.
        """
        data_dir = pathlib.Path(self._root_dir,
                                str(self._survey_year),
                                self._horizon.value)
        pathlib.Path(data_dir).mkdir(exist_ok=True, parents=True)
        survey_code = 'p' if survey == 'person' else 'h'

        return [
            self._setup_files_resources(data_dir, state, survey_code)
            for state in states
        ]

    def _setup_files_resources(self, data_dir, state, survey_code):
        """Sets up a FilesResource for a dataset to be (down)loaded. This
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
        FilesResource
            Object containign all the information necessary to (down)load
            the dataset.
        """
        try:
            state_code = STATES_CODES[state]
        except KeyError:
            raise ValueError(
                f'"{state}" in an invalid state. Please make sure it is one of'
                f' the following:\n{list(STATES_CODES.keys())}'
            )

        if int(self._survey_year) >= 2017:
            data_file_name = f'psam_{survey_code}{state_code}.csv'
        else:
            # 2016 and earlier use different file names.
            data_file_name = \
                f'ss{str(self._survey_year)[-2:]}'\
                f'{survey_code}{state.lower()}.csv'

        zip_file_name = f'csv_{survey_code}{state.lower()}.zip'
        url = f'{ACS_BASE_URL}{self._survey_year}/{self._horizon.value}/'\
              f'{zip_file_name}'

        return files_resources.FilesResource(
            url=url,
            download_path=pathlib.Path(data_dir, zip_file_name),
            file_name=data_file_name,
            data_dir=data_dir
        )

    @staticmethod
    def _create_data_sample(acs_resources,
                            density,
                            random_seed,
                            serial_filter_list):
        """Creates a sample from all the datasets the user has requested.

        Parameters
        ----------
        acs_resources : list[FilesResource]
            The FilesResources of the files to be loaded.
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
            with open(resource.file_path, 'r') as file:
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
        acs_resources : list[FilesResource]
            The FilesResources of the files to be loaded.
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

        return pd.read_csv(sample, dtype=DATA_TYPES)

    @staticmethod
    def _download_data(files_to_download):
        """Downloads the dataset files that couldn't be found in local
        memory, and extracts them from the Zip file that they come in.

        Parameters
        ----------
        files_to_download : list[FilesResource]
            The FilesResources of the files to be downloaded.
        """
        download_utils.download_datasets(files_to_download)

        for file in files_to_download:
            load_utils.extract_content_from_zip(
                file.data_dir,
                file.file_name,
                file.download_path
            )


def generate_categories(features, definition_df):
    """Generates a categories dictionary using the provided definition
    dataframe. Does not create a category mapping for variables requiring the
    2010 Public use microdata area code (PUMA) as these need an additional
    definition file which are not unique without the state code.

    Parameters
    ----------
    features : list[str]
        List of features to include in the categories dicetionary.
        Numeric features will be ignored.
    definition_df : pd.DataFrame
        Pandas DataFrame received from ```ACSDAtaSource.get_definitions()```.

    Returns
    -------
        categories : dict[str, dict]
            Nested dictionary with columns of categorical features and their
            corresponding encodings.
    """
    categories = {}
    for feature in features:
        if 'PUMA' in feature:
            continue

        # Extract definitions for this feature.
        coll_definition = definition_df[
            (definition_df[0] == 'VAL') & (definition_df[1] == feature)
        ]

        # Extracts if the feature is numeric or categorical --> 'N' == numeric.
        coll_type = coll_definition.iloc[0][2]
        if coll_type == 'N':
            # Do not add to categories.
            continue

        # Transform to numbers as downloaded definitions are in string format.
        # -99999999999999.0 is used as a placeholder value for NaN as multiple
        # NaN values are seen as different keys in a dictionary, a placeholder
        # is needed.
        mapped_col = pd.to_numeric(
            coll_definition[4], errors='coerce'
        ).fillna(-99999999999999.0)

        mapping_dict = dict(
            zip(mapped_col.tolist(), coll_definition[6].tolist())
        )

        # Add default value when not already available from definitions.
        if -99999999999999.0 not in mapping_dict:
            mapping_dict[-99999999999999.0] = 'N/A'

        # Transform placeholder value back to NaN ensuring a single NaN key
        # instaid of multiple.
        mapping_dict[float('nan')] = mapping_dict[-99999999999999.0]
        del mapping_dict[-99999999999999.0]

        categories[feature] = mapping_dict

    return categories
