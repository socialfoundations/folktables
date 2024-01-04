"""Load CPS microdata from Census CSV files."""
import os
import io
import requests
import pandas as pd

state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
              'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
              'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
              'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
              'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC']


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
                'DC': '11'}

def load_cps(root_dir, year, month, states=None, download=False):
    """
    Load sample of CPS microdata from Census csv files into DataFrame.

    If download is False it is assumed the csv for the requested month and year have already been
    downloaded and root_dir will be checked. Pass True for download if this is not the case.
    """
    df = retrieve_data(root_dir, year, month, states, download)
    return df

def retrieve_data(root_dir, year, month, states=None, download=False):
    """Actually download the csv from the Census Bureau website if needed, return data as DataFrame"""
    datadir = os.path.join(root_dir, str(year), str(month))
    os.makedirs(datadir, exist_ok=True)    
    filename = f'{month}{year[-2:]}pub.csv'
    filepath = os.path.join(datadir, filename)
    if os.path.isfile(filepath):
        df = pd.read_csv(filepath).replace(' ','')
    elif download == False:
        raise FileNotFoundError(f'Could not find survey data for {month} {year}. Call get_data with download=True to download the dataset.')
    else:
        df = download_data(filepath, year, month)

    if states != None:
        df = filter_by_state(df, states)

    return df

def download_data(filepath, year, month):
    """Download the csv from Census Bureau website and convert to dataframe"""
    print(f'Downloading CPS data for {month} {year}...')
    url = f'https://www2.census.gov/programs-surveys/cps/datasets/{year}/basic/{month}{year[-2:]}pub.csv'
    response = requests.get(url)
    with open(filepath, 'wb') as handle:
        handle.write(response.content)
    df = pd.read_csv(filepath).replace(' ','')
    return df

def filter_by_state(dataframe, state_list):
    pass