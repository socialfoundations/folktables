"""Load PUMS data from Census CSV files."""

import os
import pathlib
import random
import io

import numpy as np
import pandas as pd


state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
              'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
              'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
              'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
              'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'PR']


state_codes = {'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06',
               'CO': '08', 'CT': '09', 'DE': '10', 'FL': '12', 'GA': '13',
               'HI': '15', 'ID': '16', 'IL': '17', 'IN': '18', 'IA': '19',
               'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23', 'MD': '24',
               'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29',
               'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33', 'NJ': '34',
               'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38', 'OH': '39',
               'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45',
               'SD': '46', 'TN': '47', 'TX': '48', 'UT': '49', 'VT': '50',
               'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55', 'WY': '56',
               'PR': '72'}


def load_pums(states=None, year=2018, horizon='1-Year',
              survey='person', density=1, random_seed=1,
              serial_filter_list=None):
    """
    Load sample of PUMS data from Census csv files into DataFrame.

    If a serial filter list is passed in, density and random_seed are ignored
    and the output is instead filtered with the provided list (only entries with
    a serial number in the list are kept).
    """

    if serial_filter_list is not None:
        serial_filter_list = set(serial_filter_list)  # set for faster membership check

    int_year = int(year)
    str_year = str(int_year)
    if states is None:
        states = state_list
    
    assert int_year >= 2014
    
    random.seed(random_seed)
    
    file_dir = str((pathlib.Path(__file__).parent.parent.parent / 'data' / str_year / horizon).absolute())
    
    file_names = []
    for state in states:
        state_code = state_codes[state]
        if survey == 'person':
            if int_year >= 2017:
                file_name = 'psam_p%s.csv' % state_code
            else:
                # 2016 and earlier use different file names
                file_name = 'ss%sp%s.csv' % (str_year[-2:], state.lower())
        else:
            if int_year >= 2017:
                file_name = 'psam_h%s.csv' % state_code
            else:
                # 2016 and earlier use different file names
                file_name = 'ss%sh%s.csv' % (str_year[-2:], state.lower())    
        file_names.append(os.path.join(file_dir, file_name))

    sample = io.StringIO()

    first = True
    
    for file_name in file_names:
      
        with open(file_name, 'r') as f:
            
            if first:
                sample.write(next(f))
                first = False
            else:
                next(f)

            if serial_filter_list is None:
                for line in f:
                    if random.uniform(0, 1) < density:
                        # strip whitespace found in some early files
                        sample.write(line.replace(' ',''))
            else:
                for line in f:
                    serialno = line.split(',')[1]
                    if serialno in serial_filter_list:
                        # strip whitespace found in some early files
                        sample.write(line.replace(' ',''))

            
    sample.seek(0)
    
    dtypes = {'PINCP' : np.float64, 'RT' : str, 'SOCP' : str, 'SERIALNO' : str, 'NAICSP' : str}
                    
    return pd.read_csv(sample, dtype=dtypes)
