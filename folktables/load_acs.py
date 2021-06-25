"""Load ACS PUMS data from Census CSV files."""
import os
import random
import io
import requests
import zipfile

import numpy as np
import pandas as pd


state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
              'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
              'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
              'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
              'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'PR']


_STATE_CODES = {'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06',
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


def download_and_extract(url, datadir, remote_fname, file_name, delete_download=False):
    """Helper function to download and unzip files."""
    download_path = os.path.join(datadir, remote_fname)
    response = requests.get(url)
    with open(download_path, 'wb') as handle:
        handle.write(response.content)
    
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extract(file_name, path=datadir)
    
    if delete_download and download_path != os.path.join(datadir, file_name):
        os.remove(download_path)


def initialize_and_download(datadir, state, year, horizon, survey, download=False):
    """Download the dataset (if required)."""
    assert horizon in ['1-Year', '5-Year']
    assert int(year) >= 2014
    assert state in state_list
    assert survey in ['person', 'household']

    state_code = _STATE_CODES[state]
    survey_code = 'p' if survey == 'person' else 'h'
    if int(year) >= 2017:
        file_name = f'psam_{survey_code}{state_code}.csv'
    else:
        # 2016 and earlier use different file names
        file_name = f'ss{str(year)[-2:]}{survey_code}{state.lower()}.csv'
    
    # Assume is the path exists and is a file, then it has been downloaded
    # correctly
    file_path = os.path.join(datadir, file_name)
    if os.path.isfile(file_path):
        return file_path
    if not download:
        raise FileNotFoundError(f'Could not find {year} {horizon} {survey} survey data for {state} in {datadir}. Call get_data with download=True to download the dataset.')
    
    print(f'Downloading data for {year} {horizon} {survey} survey for {state}...')
    # Download and extract file
    base_url= f'https://www2.census.gov/programs-surveys/acs/data/pums/{year}/{horizon}'
    remote_fname = f'csv_{survey_code}{state.lower()}.zip'
    url = os.path.join(base_url, remote_fname)
    try:
        download_and_extract(url, datadir, remote_fname, file_name, delete_download=True)
    except Exception as e:
        print(f'\n{os.path.join(datadir, remote_fname)} may be corrupted. Please try deleting it and rerunning this command.\n')
        print(f'Exception: ', e)

    return file_path


def load_acs(root_dir, states=None, year=2018, horizon='1-Year',
             survey='person', density=1, random_seed=1,
             serial_filter_list=None,
             download=False):
    """
    Load sample of ACS PUMS data from Census csv files into DataFrame.

    If a serial filter list is passed in, density and random_seed are ignored
    and the output is instead filtered with the provided list (only entries with
    a serial number in the list are kept).
    """
    if int(year) < 2014:
        raise ValueError('Year must be >= 2014')

    if serial_filter_list is not None:
        serial_filter_list = set(serial_filter_list)  # set for faster membership check

    if states is None:
        states = state_list
    
    random.seed(random_seed)
    
    base_datadir = os.path.join(root_dir, str(year), horizon)
    os.makedirs(base_datadir, exist_ok=True)
    
    file_names = []
    for state in states:
        file_names.append(
            initialize_and_download(base_datadir, state, year, horizon, survey, download=download)
        )

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
