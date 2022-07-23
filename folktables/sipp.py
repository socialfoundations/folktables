from . import exceptions
from . import folktables
from . import load_sipp


class SIPPDataSource(folktables.DataSource):
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
                 download=False,
                 os_to_support='windows/mac'):
        """Gets data from the given list of variables

        Parameters
        ----------
        variables : list[str]
            Names of the variables to be included in the dataset.
        waves : Optional[list[int]]
            The panel waves to be downloaded, e.g., `[1, 2, 3]`.
        download : bool
            Whether the dataset should be downloaded from the Census Bureau's
            website. This takes a default value of `False`.
        os_to_support : str
            OS specification in order to download the correct file. We only
            allow two values: `windows/mac` or `gnu/linux`. This takes a
            default value of `windows/mac`.
        """
        if 2014 in self._panels:
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

        if os_to_support.lower() not in {
                load_sipp.SupportedOS.WINDOWS_MAC.value,
                load_sipp.SupportedOS.GNU_LINUX.value}:
            raise exceptions.UnsupportedOSError(
                f'The value "{os_to_support}" you passed in the '
                f'`os_to_support` parameter is not supported by the Census '
                f'Bureau to download the SIPP dataset. Please pass one of the'
                f' following options: '
                f'`{load_sipp.SupportedOS.WINDOWS_MAC.value}`, '
                f'`{load_sipp.SupportedOS.GNU_LINUX.value}`'
            )

        # We always want to include `pnum` and `ssuid` in the variables
        # extracted in order to be able to determine unique individuals.
        variables = set(map(lambda var: var.upper(), variables))
        if 'PNUM' not in variables:
            print('Adding `PNUM` to the list of variables.')
            variables.add('PNUM')
        if 'SSUID' not in variables:
            print('Adding `SSUID` to the list of variables.')
            variables.add('SSUID')

        return load_sipp.load_sipp(root_dir=self._root_dir,
                                   panels=self._panels,
                                   waves=waves,
                                   variables=variables,
                                   os_to_support=os_to_support.lower(),
                                   download=download)

    @staticmethod
    def create_unique_ids(data):
        """Creates unique IDs for the all respondents in the SIPP dataset.

        Parameters
        ----------
        data : pd.DataFrame
            Data frame containing the SIPP data from which the unique IDs will
            be generated.

        Notes
        -----
        The unique ID is determined by concatenating `PNUM` to `SSUID`.
        """
        ...

    @staticmethod
    def reshape_df(data):
        """Reshapes the SIPP data so that each respondent only spans
        one row.

        Parameters
        ----------
        data : pd.DataFrame
            Data frame containing the SIPP data in its original format
            (i.e., the one returned by the method `get_data`).
        """
        ...
