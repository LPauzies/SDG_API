import pandas as pd

from app.config import DATA_PATH

from typing import List

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

def _is_topic_existing(df: pd.DataFrame, topic: str) -> bool:
    return topic in df.SeriesCode.values

def _is_country_contained_in_values(df: pd.DataFrame, country: str) -> bool:
    for country_ in filter(lambda x: " " in x or "-" in x, df.GeoAreaName.values):
        if country in country_:
            return country_
    return None

def _is_country_code_existing(df: pd.DataFrame, country_code: str) -> bool:
    return country_code in df.Country_code.values

def _is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False

def _are_some_float(list_: List) -> bool:
    return len(list(filter(lambda x: _is_float(x), list_))) > 0

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

def get_data_from_one_geographical_code(country_code: str) -> pd.DataFrame:
    df = _read_data()
    if (_is_country_code_existing(df, country_code)):
        return df[df['Country_code'] == country_code]
    else:
        raise SDGFilteringException("This country code is not referenced in our API")

def get_countries() -> pd.DataFrame:
    df = _read_data()
    return df[['GeoAreaName', 'GeoAreaCode', 'Country_code', 'Latitude', 'Longitude']].drop_duplicates()

def get_goals() -> pd.DataFrame:
    df = _read_data()
    return df[['SeriesCode', 'SeriesDescription']].drop_duplicates()

def get_topic_from_one_country(country_code: str, topic: str) -> pd.DataFrame:
    df = get_data_from_one_geographical_code(country_code)
    if (_is_topic_existing(df, topic)):
        return df[df['SeriesCode'] == topic]
    else:
        raise SDGFilteringException("This topic is not referenced in our API")

def get_topic_data(topic: str) -> pd.DataFrame:
    df = _read_data()
    if (_is_topic_existing(df, topic)):
        df = df[df['SeriesCode'] == topic].sort_values(by=['GeoAreaName', 'TimePeriod'], ascending=False).drop_duplicates(subset=['GeoAreaName'])
        if (_are_some_float(list(df['Value']))):
            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
            df = df.dropna(subset=['Value'])
            df = df.sort_values(by=['Value'])
        return df
    else:
        raise SDGFilteringException("This topic is not referenced in our API")
