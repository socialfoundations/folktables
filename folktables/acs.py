"""Data source and problem definitions for American Community Survey (ACS) Public Use Microdata Sample (PUMS)."""
import os

import numpy as np
import pandas as pd

from . import folktables
from .load_acs import load_acs


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

ACSIncome = folktables.BasicProblem(
    features=[
        'AGEP',
        'COW',
        'SCHL',
        'MAR',
        'OCCP',
        'POBP',
        'RELP',
        'WKHP',
        'SEX',
        'RAC1P',
    ],
    target='PINCP',
    target_transform=lambda x: x > 50000,
    group='RAC1P',
    preprocess=adult_filter,
    postprocess=lambda x: np.nan_to_num(x, -1),
)

ACSEmployment = folktables.BasicProblem(
    features=[
        'AGEP',
        'SCHL',
        'MAR',
        'RELP',
        'DIS',
        'ESP',
        'CIT',
        'MIG',
        'MIL',
        'ANC',
        'NATIVITY',
        'DEAR',
        'DEYE',
        'DREM',
        'SEX',
        'RAC1P',
    ],
    target='ESR',
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=lambda x: x,
    postprocess=lambda x: np.nan_to_num(x, -1),
)

ACSHealthInsurance = folktables.BasicProblem(
    features=[
        'AGEP',
        'SCHL',
        'MAR',
        'SEX',
        'DIS',
        'ESP',
        'CIT',
        'MIG',
        'MIL',
        'ANC',
        'NATIVITY',
        'DEAR',
        'DEYE',
        'DREM',
        'RACAIAN',
        'RACASN',
        'RACBLK',
        'RACNH',
        'RACPI',
        'RACSOR',
        'RACWHT',
        'PINCP',
        'ESR',
        'ST',
        'FER',
    ],
    target='HINS2',
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=lambda x: x,
    postprocess=lambda x: np.nan_to_num(x, -1),
)

def public_coverage_filter(data):
    """
    Filters for the public health insurance prediction task; focus on low income Americans, and those not eligible for Medicare
    """
    df = data
    df = df[df['AGEP'] < 65]
    df = df[df['PINCP'] <= 30000]
    return df

ACSPublicCoverage = folktables.BasicProblem(
    features=[
        'AGEP',
        'SCHL',
        'MAR',
        'SEX',
        'DIS',
        'ESP',
        'CIT',
        'MIG',
        'MIL',
        'ANC',
        'NATIVITY',
        'DEAR',
        'DEYE',
        'DREM',
        'PINCP',
        'ESR',
        'ST',
        'FER',
        'RAC1P',
    ],
    target='PUBCOV',
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=public_coverage_filter,
    postprocess=lambda x: np.nan_to_num(x, -1),
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

ACSTravelTime = folktables.BasicProblem(
    features=[
        'AGEP',
        'SCHL',
        'MAR',
        'SEX',
        'DIS',
        'ESP',
        'MIG',
        'RELP',
        'RAC1P',
        'PUMA',
        'ST',
        'CIT',
        'OCCP',
        'JWTR',
        'POWPUMA',
        'POVPIP',
    ],
    target="JWMNP",
    target_transform=lambda x: x > 20,
    group='RAC1P',
    preprocess=travel_time_filter,
    postprocess=lambda x: np.nan_to_num(x, -1),
)

ACSMobility = folktables.BasicProblem(
    features=[
        'AGEP',
        'SCHL',
        'MAR',
        'SEX',
        'DIS',
        'ESP',
        'CIT',
        'MIL',
        'ANC',
        'NATIVITY',
        'RELP',
        'DEAR',
        'DEYE',
        'DREM',
        'RAC1P',
        'GCL',
        'COW',
        'ESR',
        'WKHP',
        'JWMNP',
        'PINCP',
    ],
    target="MIG",
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=lambda x: x.drop(x.loc[(x['AGEP'] <= 18) | (x['AGEP'] >= 35)].index),
    postprocess=lambda x: np.nan_to_num(x, -1),
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

ACSEmploymentFiltered = folktables.BasicProblem(
    features=[
        'AGEP',
        'SCHL',
        'MAR',
        'SEX',
        'DIS',
        'ESP',
        'MIG',
        'CIT',
        'MIL',
        'ANC',
        'NATIVITY',
        'RELP',
        'DEAR',
        'DEYE',
        'DREM',
        'RAC1P',
        'GCL',
    ],
    target="ESR",
    target_transform=lambda x: x == 1,
    group='RAC1P',
    preprocess=employment_filter,
    postprocess=lambda x: np.nan_to_num(x, -1),
)

ACSIncomePovertyRatio = folktables.BasicProblem(
    features=[
        'AGEP',
        'SCHL',
        'MAR',
        'SEX',
        'DIS',
        'ESP',
        'MIG',
        'CIT',
        'MIL',
        'ANC',
        'NATIVITY',
        'RELP',
        'DEAR',
        'DEYE',
        'DREM',
        'RAC1P',
        'GCL',
        'ESR',
        'OCCP',
        'WKHP',
    ],
    target='POVPIP',
    target_transform=lambda x: x < 250,
    group='RAC1P',
    preprocess=lambda x: x,
    postprocess=lambda x: np.nan_to_num(x, -1),
)
