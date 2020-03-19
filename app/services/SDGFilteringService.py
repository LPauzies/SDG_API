import pandas as pd

from typing import Union

DATA_PATH = "data/data.csv"

### PRIVATE FUNCTIONS ###
def _read_data() -> pd.DataFrame:
    try:
        return pd.read_csv(DATA_PATH, header=0, low_memory=False)
    except Exception as e:
        raise Exception("Cannot read the API data")

def _is_country_existing(df: pd.DataFrame, country: str) -> bool:
    return country in df.GeoAreaName.values

def _is_country_code_existing(df: pd.DataFrame, country_code: int) -> bool:
    return country_code in df.GeoAreaCode.values

### PUBLIC FUNCTIONS ###
def get_data_from_one_country(country: str) -> pd.DataFrame:
    df = _read_data()
    if (_is_country_existing(df, country)):
        return df[df['GeoAreaName'] == country]
    else:
        raise Exception("Country is not referenced in our API")

def get_data_from_one_geographical_code(country_code: int) -> pd.DataFrame:
    df = _read_data()
    if (_is_country_code_existing(df, country)):
        return df[df['GeoAreaCode'] == country_code]
    else:
        raise Exception("Country code is not referenced in our API")

if __name__ == '__main__':
    try:
        df = get_data_from_one_country('ddd')
        print(df.head())
    except Exception as e:
        print(e)
