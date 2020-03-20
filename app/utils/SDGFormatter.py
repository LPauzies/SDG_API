import typing
import pandas as pd

ORIGINAL_DATA_PATH = "original_data/data.csv"

def _read_data() -> pd.DataFrame:
    return pd.read_csv(ORIGINAL_DATA_PATH, header=0, low_memory=False)

def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    columns = map(lambda x : x[1:-1] if (x.startswith("[") and (x.endswith("]"))) else x, map(lambda x : x.strip(), df.columns))
    columns = map(lambda x : x.replace(" ", "_"), columns)
    return df.rename(columns = dict(zip(df.columns, columns)))

def _ignore_non_ascii_characters(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['GeoAreaName'].str.len().eq(df['GeoAreaName'].str.encode('ascii', errors='ignore').str.len())]

def _upper_country_values(df: pd.DataFrame) -> pd.DataFrame:
    df['GeoAreaName'] = df['GeoAreaName'].apply(lambda x : x.upper())
    return df

def _suppress_useless_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns = ['Goal','Target', 'Indicator', 'Time_Detail', 'UpperBound', 'LowerBound', 'BasePeriod', 'FootNote', 'Nature', 'Quantile', 'Reporting_Type', 'Type_of_skill'])

if __name__ == '__main__':
    df = _read_data()
    df = _standardize_column_names(df)
    df = _ignore_non_ascii_characters(df)
    df = _upper_country_values(df)
    df = _suppress_useless_columns(df)
    df.describe(include='all')
    df.to_csv("../services/data/data.csv", index=False)
