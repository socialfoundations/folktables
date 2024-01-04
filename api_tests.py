from folktables import ACSDataSource, ACSPublicCoverage
import requests
import datetime

def req():
    start = datetime.datetime.now()
    data_source = ACSDataSource(survey_year='2018', horizon='1-Year', survey='person')
    acs_data = data_source.get_data(states=["CA"], download=True)
    features, label, group = ACSPublicCoverage.df_to_numpy(acs_data)
    delta = datetime.datetime.now() - start
    print(delta)

def req_api():
    start = datetime.datetime.now()
    resp = requests.get('https://api.census.gov/data/2018/acs/acs1/pums?get=AGEP,SCHL,MAR,SEX,DIS,ESP,CIT,MIG,MIL,ANC,NATIVITY,DEAR,DEYE,DREM,PINCP,ESR,ST,FER,RAC1P,PUBCOV&in=state:06')
    delta = datetime.datetime.now() - start
    print(delta)

req()

req_api()