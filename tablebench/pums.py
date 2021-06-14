"""Data source and problem definitions for Census Public Use Microdata Sample (PUMS)."""

from . import load_pums
from . import data_source

from .load_pums import state_list

import numpy as np
import pandas as pd
from sklearn import preprocessing


class PUMSDataSource(data_source.DataSource):
    """Data source implementation for Census Public Use Microdata Sample."""

    def __init__(self, survey_year, horizon, survey):
        """Create data source around PUMS data for specific year, time horizon, survey type.

        Args:
            survey_year: String. Year of PUMS data, e.g., '2018'
            horizon: String. Must be '1-Year' or '5-Year'
            survey: String. Must be 'person' or 'household'

        Returns:
            PUMSDataSource
        """
        self._survey_year = survey_year
        self._horizon = horizon
        self._survey = survey

    def get_data(self, states=None, density=1.0, random_seed=0, join_household=False):
        """Get data from given list of states, density, and random seed. Optionally add household features."""
        data = load_pums.load_pums(year=self._survey_year,
                                   states=states,
                                   horizon=self._horizon,
                                   survey=self._survey,
                                   density=density,
                                   random_seed=random_seed)
        if join_household:
            orig_len = len(data)
            assert self._survey == 'person'
            household_data = load_pums.load_pums(year=self._survey_year,
                                                 states=states,
                                                 horizon=self._horizon,
                                                 survey='household',
                                                 serial_filter_list=list(data['SERIALNO']))
            
            # We only want to keep the columns in the household dataframe that don't appear in the person
            # dataframe, but we *do* want to include the SERIALNO column to merge on.
            household_cols = (set(household_data.columns) - set(data.columns)).union(set(['SERIALNO']))
            join = pd.merge(data, household_data[list(household_cols)], on=['SERIALNO'])
            assert len(join) == orig_len, f'Lengths do not match after join: {len(join)} vs {orig_len}'
            return join
        else:
            return data


def adult_filter(data):
    """Mimic the filters in place for Adult data.
    
    Adult documentation notes: Extraction was done by Barry Becker from 
    the 1994 Census database. A set of reasonably clean records was extracted 
    using the following conditions:
    ((AAGE>16) && (AGI>100) && (AFNLWGT>1)&& (HRSWK>0))
    """
    df = data
    df = df[df['AGEP'] > 16]
    df = df[df['PINCP'] > 100]
    df = df[df['WKHP'] > 0]    
    df = df[df['PWGTP'] >= 1]
    return df


PUMSAdult = data_source.BasicProblem(
    feature_transforms={
        'AGEP': None,
        'COW': None,
        'SCHL' : None,
        'MAR' : None,
        'OCCP' : None,
        'POBP' : None,
        'RELP' : None,
        'WKHP' : None,
        'SEX' : None,
        'RAC1P' : None
    },
    target='PINCP',
    target_transform=lambda x: x > 50000,    
    group='RAC1P',
    preprocess=adult_filter,
    postprocess=preprocessing.scale
)

PUMSAdultSex = data_source.BasicProblem(
    feature_transforms={
        'AGEP': None,
        'COW': None,
        'SCHL' : None,
        'MAR' : None,
        'OCCP' : None,
        'POBP' : None,
        'RELP' : None,
        'WKHP' : None,
        'SEX' : None,
        'RAC1P' : None
    },
    target='PINCP',
    target_transform=lambda x: x > 50000,    
    group='SEX',
    preprocess=adult_filter,
    postprocess=preprocessing.scale
)



PUMSEmployment = data_source.BasicProblem(
    feature_transforms={
        'AGEP' : None,
        'SCHL' : None,
        'MAR' : None,
        'RELP' : None,
        'DIS' : None,
        'ESP' : None,
        'CIT' : None,
        'MIG' : None,
        'MIL' : None,
        'ANC' : None,
        'NATIVITY' : None,
        'DEAR' : None,
        'DEYE' : None,
        'DREM' : None,
        'SEX' : None,
        'RAC1P' : None
    },
    target='ESR',
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=lambda x: x,
    postprocess=lambda x: preprocessing.scale(np.nan_to_num(x, -1))
)


PUMSHealthInsurance = data_source.BasicProblem(
    feature_transforms={
        'AGEP' : None,
        'SCHL' : None,
        'MAR' : None,
        'SEX' : None,
        'DIS' : None,
        'ESP' : None,
        'CIT' : None,
        'MIG' : None,
        'MIL' : None,
        'ANC' : None,
        'NATIVITY' : None,
        'DEAR' : None,
        'DEYE' : None,
        'DREM' : None,
        'RACAIAN' : None,
        'RACASN' : None,
        'RACBLK' : None,
        'RACNH' : None,
        'RACPI' : None,
        'RACSOR' : None,
        'RACWHT' : None,
        'PINCP': None,
        'ESR': None,
        'ST': None,
        'FER': None
    },
    target='HINS2',
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=lambda x: x,
    postprocess=lambda x: preprocessing.scale(np.nan_to_num(x, -1))
)

def public_coverage_filter(data):
    """
    Filters for the public health insurance prediction task; focus on low income Americans, and those not eligible for Medicare
    """
    df = data
    df = df[df['AGEP'] < 65]
    df = df[df['PINCP'] <= 30000]
    return df

PUMSPublicCoverage = data_source.BasicProblem(
    feature_transforms={
        'AGEP' : None,
        'SCHL' : None,
        'MAR' : None,
        'SEX' : None,
        'DIS' : None,
        'ESP' : None,
        'CIT' : None,
        'MIG' : None,
        'MIL' : None,
        'ANC' : None,
        'NATIVITY' : None,
        'DEAR' : None,
        'DEYE' : None,
        'DREM' : None,
        'PINCP': None,
        'ESR': None,
        'ST': None,
        'FER': None,
        'RAC1P': None
    },
    target='PUBCOV',
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=public_coverage_filter,
    postprocess=lambda x: preprocessing.scale(np.nan_to_num(x, -1))
)

def travel_time_filter(data):
    """
    Filters for the employment prediction task
    """
    df = data
    df = df[df['AGEP'] > 16]
    df = df[df['PWGTP'] >= 1]
    df = df[df['ESR'] == 1]
    return df

PUMSTravelTime = data_source.BasicProblem(
    feature_transforms={
        'AGEP': None,
        'SCHL': None,
        'MAR': None,
        'SEX': None,
        'DIS': None,
        'ESP': None,
        'MIG': None,
        'RELP': None,
        'RAC1P': None,
        'PUMA': None,
        'ST': None,
        'CIT': None,
        'OCCP': None,
        'JWTR': None,
        'POWPUMA': None,
        'POVPIP': None
    },
    target="JWMNP",
    target_transform=lambda x: x > 20,
    group='RAC1P',
    preprocess=travel_time_filter,
    postprocess=lambda x: preprocessing.scale(np.nan_to_num(x, -1))
)

PUMSMobility = data_source.BasicProblem(
    feature_transforms={
        'AGEP': None,
        'SCHL': None,
        'MAR': None,
        'SEX': None,
        'DIS': None,
        'ESP': None,
        'CIT': None,
        'MIL': None,
        'ANC': None,
        'NATIVITY':None,
        'RELP': None,
        'DEAR': None,
        'DEYE': None,
        'DREM': None,
        'RAC1P': None,
        'GCL': None,
        'COW': None,
        'ESR': None,
        'WKHP': None,
        'JWMNP': None,
        'PINCP': None
    },
    target="MIG",
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=lambda x : x.drop(x.loc[(x['AGEP'] <= 18) | (x['AGEP'] >= 35)].index),
    postprocess=lambda x: preprocessing.scale(np.nan_to_num(x, -1))
)

def employment_filter(data):
    """
    Filters for the employment prediction task
    """
    df = data
    df = df[df['AGEP'] > 16]
    df = df[df['AGEP'] < 90]
    df = df[df['PWGTP'] >= 1]
    return df

PUMSEmploymentFiltered = data_source.BasicProblem(
    feature_transforms={
        'AGEP': None,
        'SCHL': None,
        'MAR': None,
        'SEX': None,
        'DIS': None,
        'ESP': None,
        'MIG': None,
        'CIT': None,
        'MIL': None,
        'ANC': None,
        'NATIVITY':None,
        'RELP': None,
        'DEAR': None,
        'DEYE': None,
        'DREM': None,
        'RAC1P': None,
        'GCL': None,
    },
    target="ESR",
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess= employment_filter,
    postprocess=lambda x: preprocessing.scale(np.nan_to_num(x, -1))
)

PUMSIncomePovertyRatio = data_source.BasicProblem(
    feature_transforms={
        'AGEP': None,
        'SCHL': None,
        'MAR': None,
        'SEX': None,
        'DIS': None,
        'ESP': None,
        'MIG': None,
        'CIT': None,
        'MIL': None,
        'ANC': None,
        'NATIVITY': None,
        'RELP': None,
        'DEAR': None,
        'DEYE': None,
        'DREM': None,
        'RAC1P': None,
        'GCL': None,
        'ESR': None,
        'OCCP': None,
        'WKHP': None
    },
    target='POVPIP',
    target_transform=lambda x: x < 250,
    group='RAC1P',
    preprocess=lambda x: x,
    postprocess=lambda x: preprocessing.scale(np.nan_to_num(x, -1))
)