import typing
import pandas as pd

ORIGINAL_DATA_PATH = "original_data/data.csv"

# data csv
def _read_data() -> pd.DataFrame:
    return pd.read_csv(ORIGINAL_DATA_PATH, header=0, low_memory=False)

def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    columns = map(lambda x : x[1:-1] if (x.startswith("[") and (x.endswith("]"))) else x, map(lambda x : x.strip(), df.columns))
    columns = map(lambda x : x.replace(" ", "_"), columns)
    return df.rename(columns = dict(zip(df.columns, columns)))

def _ignore_non_ascii_characters(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['GeoAreaName'].str.len().eq(df['GeoAreaName'].str.encode('ascii', errors='ignore').str.len())]

def _remove_NV_values(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['Value'] != "NV"];

def _upper_country_values(df: pd.DataFrame) -> pd.DataFrame:
    df['GeoAreaName'] = df['GeoAreaName'].apply(lambda x : x.upper())
    return df

def _suppress_useless_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns = ['Goal','Target', 'Indicator', 'Time_Detail', 'UpperBound', 'LowerBound', 'BasePeriod', 'FootNote', 'Nature', 'Quantile', 'Reporting_Type', 'Type_of_skill'])

# countries csv
def _read_countries() -> pd.DataFrame:
    return pd.read_csv(ORIGINAL_COUNTRIES_PATH, header=0, low_memory=False)

def _replace_weird_values(df: pd.DataFrame) -> pd.DataFrame:
    df['name'] = df['name'].apply(lambda x: x.replace("[","(").replace("]",")"))
    return df

def _upper_country_names(df: pd.DataFrame) -> pd.DataFrame:
    df['name'] = df['name'].apply(lambda x: x.upper())
    return df

if __name__ == '__main__':
    df_data = _read_data()
    df_data = _standardize_column_names(df_data)
    df_data = _ignore_non_ascii_characters(df_data)
    df_data = _remove_NV_values(df_data)
    df_data = _upper_country_values(df_data)
    df_data = _suppress_useless_columns(df_data)
    df_data = df_data.sort_values(by=['GeoAreaName'])

    df_countries = pd.read_csv("../services/data/countries.csv", header=0, low_memory=False)

    df = pd.merge(df_data, df_countries, how="inner", left_on="GeoAreaName", right_on="name")

    #Adjust the result dataframe
    df = df.drop(columns = ['name'])
    df = df.rename(columns={"country":"Country_code", "latitude":"Latitude", "longitude":"Longitude"})
    df.to_csv("../services/data/data.csv", index=False)
