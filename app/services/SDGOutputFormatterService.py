from flask_restful import fields, marshal
from typing import Any

import pandas as pd
import json as JSON

# Declare the formatting fields for the big API endpoint
data_fields = {
    'time period' : fields.Integer,
    'value' : fields.String,
    'extra data' : fields.List(fields.String)
}

topic_fields = {
    'topic code' : fields.String,
    'topic description' : fields.String,
    'unit' : fields.String,
    'source' : fields.String,
    'data' : fields.List(fields.Nested(data_fields))
}

json_fields = {
    'country' : fields.String,
    'country code' : fields.Integer,
    'topics' : fields.List(fields.Nested(topic_fields))
}

def sdg_formatter(df: pd.DataFrame) -> Any:
    json = {}
    json['country'] = df['GeoAreaName'].values[0]
    json['country code'] = df['GeoAreaCode'].values[0]
    json['topics'] = []
    df_serieCode = df.drop(columns=['GeoAreaName', 'GeoAreaCode'])
    for serieCode in df_serieCode.SeriesCode.unique():
        topic = {}
        df_topic = df_serieCode[df_serieCode['SeriesCode'] == serieCode]
        topic['topic code'] = df_topic['SeriesCode'].values[0]
        topic['topic description'] = df_topic['SeriesDescription'].values[0]
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
                if not(col == 'TimePeriod' or col == 'Value'):
                    s = "NULL" if str(row[col] == "nan") else str(row[col])
                    data['extra data'].append("{}:{}".format(col,s))
            topic['data'].append(data)
        json['topics'].append(topic)
    return marshal(json, json_fields)

country_field = {
    'country' : fields.String,
    'country code' : fields.String
}

countries_fields = {
    'countries' : fields.List(fields.Nested(country_field))
}

def sdg_formatter_countries(df: pd.DataFrame) -> Any:
    json = {}
    json['countries'] = []
    for _, row in df.iterrows():
        data = {}
        data['country'] = row['GeoAreaName']
        data['country code'] = row['GeoAreaCode']
        json['countries'].append(data)
    return marshal(json, countries_fields)

goal_field = {
    'goal' : fields.String,
    'goal code' : fields.String
}

goals_fields = {
    'goals' : fields.List(fields.Nested(goal_field))
}

def sdg_formatter_goals(df: pd.DataFrame) -> Any:
    json = {}
    json['goals'] = []
    for _, row in df.iterrows():
        data = {}
        data['goal'] = row['SeriesDescription']
        data['goal code'] = row['SeriesCode']
        json['goals'].append(data)
    return marshal(json, goals_fields)
