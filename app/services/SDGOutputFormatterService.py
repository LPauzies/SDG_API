from flask_restful import fields, marshal
from typing import Any

import pandas as pd

coordinates_fields = {
    'latitude' : fields.Float,
    'longitude' : fields.Float
}

# SDG Formatter
sdg_formatter_data_fields = {
    'time period' : fields.Integer,
    'value' : fields.String,
    'extra data' : fields.List(fields.String)
}

sdg_formatter_topic_fields = {
    'goal code' : fields.String,
    'goal description' : fields.String,
    'unit' : fields.String,
    'source' : fields.String,
    'data' : fields.List(fields.Nested(sdg_formatter_data_fields))
}

sdg_formatter_json_fields = {
    'country' : fields.String,
    'numerical country code' : fields.Integer,
    'country code' : fields.String,
    'coordinates' : fields.Nested(coordinates_fields),
    'goals' : fields.List(fields.Nested(sdg_formatter_topic_fields))
}

def sdg_formatter(df: pd.DataFrame) -> Any:
    json = {}
    json['country'] = df['GeoAreaName'].values[0]
    json['numerical country code'] = df['GeoAreaCode'].values[0]
    json['country code'] = df['Country_code'].values[0]
    json['coordinates'] = {
        "latitude" : df['Latitude'].values[0],
        "longitude" : df['Longitude'].values[0]
    }
    json['goals'] = []
    df_serieCode = df.drop(columns=['GeoAreaName', 'GeoAreaCode', 'Country_code', 'Latitude', 'Longitude'])
    for serieCode in df_serieCode.SeriesCode.unique():
        topic = {}
        df_topic = df_serieCode[df_serieCode['SeriesCode'] == serieCode]
        topic['goal code'] = df_topic['SeriesCode'].values[0]
        topic['goal description'] = df_topic['SeriesDescription'].values[0]
        topic['unit'] = df_topic['Units'].values[0]
        topic['source'] = df_topic['Source'].values[0]
        topic['data'] = []
        df_data = df_topic.drop(columns=['SeriesCode', 'SeriesDescription', 'Units', 'Source'])
        cols = df_data.columns
        for _, row in df_data.iterrows():
            data = {}
            data['time period'] = row['TimePeriod']
            data['value'] = row['Value']
            data['extra data'] = []
            for col in cols:
                if col != 'TimePeriod' or col != 'Value':
                    s = "NULL" if str(row[col] == "nan") else str(row[col])
                    data['extra data'].append("{}:{}".format(col,s))
            topic['data'].append(data)
        json['goals'].append(topic)
    return marshal(json, sdg_formatter_json_fields)

# SDG Formatter Countries
sdg_formatter_countries_country_field = {
    'country' : fields.String,
    'numerical country code' : fields.Integer,
    'country code' : fields.String,
    'coordinates' : fields.Nested(coordinates_fields)
}

sdg_formatter_countries_countries_fields = {
    'countries' : fields.List(fields.Nested(sdg_formatter_countries_country_field))
}

def sdg_formatter_countries(df: pd.DataFrame) -> Any:
    json = {}
    json['countries'] = []
    for _, row in df.iterrows():
        data = {}
        data['country'] = row['GeoAreaName']
        data['numerical country code'] = row['GeoAreaCode']
        data['country code'] = row['Country_code']
        data['coordinates'] = {
            "latitude" : row['Latitude'],
            "longitude" : row['Longitude']
        }
        json['countries'].append(data)
    return marshal(json, sdg_formatter_countries_countries_fields)

# SDG Formatter Goals
sdg_formatter_goals_goal_field = {
    'topic' : fields.String,
    'topic code' : fields.String
}

sdg_formatter_goals_goals_fields = {
    'goals' : fields.List(fields.Nested(sdg_formatter_goals_goal_field))
}

def sdg_formatter_goals(df: pd.DataFrame) -> Any:
    json = {}
    json['goals'] = []
    for _, row in df.iterrows():
        data = {}
        data['topic'] = row['SeriesDescription']
        data['topic code'] = row['SeriesCode']
        json['goals'].append(data)
    return marshal(json, sdg_formatter_goals_goals_fields)

# SDG Formatter Goal for a country
sdg_formatter_goal_country_data_fields = {
    'time period' : fields.Integer,
    'value' : fields.String,
    'extra data' : fields.List(fields.String)
}

sdg_formatter_goal_country_goals_fields = {
    'goal' : fields.String,
    'goal code' : fields.String,
    'country' : fields.String,
    'numerical country code' : fields.Integer,
    'country code' : fields.String,
    'coordinates' : fields.Nested(coordinates_fields),
    'unit' : fields.String,
    'source' : fields.String,
    'data' : fields.List(fields.Nested(sdg_formatter_goal_country_data_fields))
}

def sdg_formatter_goal_country(df: pd.DataFrame) -> Any:
    json = {}
    json['goal'] = df['SeriesDescription'].values[0]
    json['goal code'] = df['SeriesCode'].values[0]
    json['country'] = df['GeoAreaName'].values[0]
    json['numerical country code'] = df['GeoAreaCode'].values[0]
    json['country code'] = df['Country_code'].values[0]
    json['coordinates'] = {
        'latitude' : df['Latitude'].values[0],
        'longitude' : df['Longitude'].values[0]
    }
    json['unit'] = df['Units'].values[0]
    json['source'] = df['Source'].values[0]
    json['data'] = []
    df_data = df.drop(columns=['GeoAreaName', 'GeoAreaCode', 'SeriesCode', 'SeriesDescription', 'Units', 'Source', 'Country_code', 'Latitude', 'Longitude'])
    cols = df_data.columns
    for _, row in df_data.iterrows():
        data = {}
        data['time period'] = row['TimePeriod']
        data['value'] = row['Value']
        data['extra data'] = []
        for col in cols:
            if col != 'TimePeriod' and col != 'Value':
                s = "NULL" if str(row[col] == "nan") else str(row[col])
                data['extra data'].append("{}:{}".format(col,s))
        json['data'].append(data)
    return marshal(json,sdg_formatter_goal_country_goals_fields)
