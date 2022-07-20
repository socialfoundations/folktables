from . import folktables
from . import load_sipp


class SIPPDataSource(folktables.DataSource):
    """Data source implementation for SIPP data."""

    def __init__(self, panels, root_dir='data'):
        """Creates a data source around the SIPP data for a specific panels.

        Parameters
        ----------
        panels : list[int]
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
            if not isinstance(waves, list) and not waves:
                # TODO: create our own ErrorTypes for better software design.
                raise ValueError('')

        if os_to_support.lower() not in {
                load_sipp.SupportedOS.WINDOWS_MAC.value,
                load_sipp.SupportedOS.GNU_LINUX.value}:
            # TODO: create our own ErrorTypes for better software design.
            raise ValueError('')

        # We always want to include `pnum` and `ssuid` in the variables
        # extracted in order to be able to determine unique individuals.
        variables = map(lambda var: var.upper(), variables)
        variables = set(variables)
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
    def _create_unique_ids(data):
        """
        """
        ...

    @staticmethod
    def _reshape_df(data):
        """
        """
        ...
