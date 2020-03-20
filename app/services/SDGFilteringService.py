import pandas as pd

from typing import Union
from app.config import DATA_PATH

class SDGFilteringException(Exception):
    pass

### PRIVATE FUNCTIONS ###
def _read_data() -> pd.DataFrame:
    try:
        return pd.read_csv(DATA_PATH, header=0, low_memory=False)
    except Exception as e:
        raise OSError("Cannot read the API data")

def _is_country_existing(df: pd.DataFrame, country: str) -> bool:
    return country in df.GeoAreaName.values

def _is_country_contained_in_values(df: pd.DataFrame, country: str) -> bool:
    for country_ in filter(lambda x: " " in x or "-" in x, df.GeoAreaName.values):
        if country in country_:
            return country_
    return None

def _is_country_code_existing(df: pd.DataFrame, country_code: int) -> bool:
    return country_code in df.GeoAreaCode.values

### PUBLIC FUNCTIONS ###
# Can raise OSError if CSV is not accessible
def get_data_from_one_country(country: str) -> pd.DataFrame:
    df = _read_data()
    if (_is_country_existing(df, country)):
        return df[df['GeoAreaName'] == country]
    else:
        country_near = _is_country_contained_in_values(df, country)
        if (country_near is not None):
            return df[df['GeoAreaName'] == country_near]
        else:
            raise SDGFilteringException("This country is not referenced in our API")

def get_data_from_one_geographical_code(country_code: int) -> pd.DataFrame:
    df = _read_data()
    if (_is_country_code_existing(df, country_code)):
        return df[df['GeoAreaCode'] == country_code]
    else:
        raise SDGFilteringException("This country code is not referenced in our API")

def get_countries() -> pd.DataFrame:
    df = _read_data()
    return df[['GeoAreaName', 'GeoAreaCode']].drop_duplicates()

def get_goals() -> pd.DataFrame:
    df = _read_data()
    return df[['SeriesCode', 'SeriesDescription']].drop_duplicates()
