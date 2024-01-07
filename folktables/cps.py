"""Data source and problem definitions for Community Population Survey (CPS)"""
import numpy as np
import pandas as pd
from datetime import datetime

from . import folktables
from .load_cps import load_cps

class CPSDataSource(folktables.DataSource):
    """Data source implementation for CPS montly microdata."""

    def __init__(self, survey_year, survey_month, root_dir="data"):
        """Create data source for the microdata of a specific month and year
        
        Args:
            survey_year: int. Year of CPS microdata, e.g., 2023
            survey_month: String: First 3 letters of the month of the survey, e.g., 'jan' or 'jul'

        Returns:
            CPSDataSource
        """
        assert type(survey_month) == type('')
        survey_year = int(survey_year)
        # back through 1994 is provided, but files are raw text (not .csv) and need specific parses written
        if survey_year not in range(2020, datetime.now().year+1):
            raise ValueError("Data not available for the specified year")
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        if survey_month.lower() not in months:
            raise ValueError(f'Please specify the month with its first three letters, available options are: {months}')
        self._survey_year = str(survey_year)
        self._survey_month = survey_month.lower()
        self._root_dir = root_dir

    def get_data(self, states=None, download=False):
        """Get data from a given list of states, or all states if no `states` argument.

        Args:
            states: List of Strings. Two letter codes for states, including the District of 
            Columbia, e.g., ['RI', 'NY', 'PR']
            download: Boolean. True will download the `.csv` file for the specified survey year & 
            month. Use False if this data has already been downloaded.

        Returns:
            A pandas DataFrame of the requested data
        """
        data = load_cps(root_dir=self._root_dir,
                        year=self._survey_year,
                        month=self._survey_month,
                        states=states,
                        download=download)
        return data

CPSEmployment = folktables.BasicProblem(
    features=[
        'PRTAGE',
        'PEEDUCA',
        'PESEX',
        'PEMARITL',
        'PRDASIAN',
        'PRDTHSP',
        'PENATVTY',
        'HEHOUSUT',
        'HEFAMINC'
    ],
    target='PEMLR',
    target_transform=lambda x: (x==1) | (x==2),
    group='PTDTRACE',
    preprocess=lambda x: x,
    postprocess=lambda x: np.nan_to_num(x, -1),
)
