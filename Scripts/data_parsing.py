import os
import pandas as pd

from GDDiK_Download import gddik_xml_downloading
from weather_download import get_weather
from utils.const import DATA_GDDIK_PATH

def data_parsing():

    latest_file = ''
    latest_time = 0
    with os.scandir(DATA_GDDIK_PATH) as entries:
        for entry in entries:
            if entry.is_file():
                mod_time = entry.stat().st_mtime
                if mod_time > latest_time:
                    latest_time = mod_time
                    latest_file = entry.name

    latest_file_dir = os.path.join(DATA_GDDIK_PATH,latest_file)
    
    gddik_df = pd.read_xml(latest_file_dir, xpath='utr')

    weather_df = pd.DataFrame()

    for i, col in gddik_df.iterrows():
        
        if col['typ'] == 'U':
            continue

        if pd.isna(col['geo_long']) or pd.isna(col['geo_lat']) or pd.isna(col['data_powstania']):
            continue 

        weather_row = get_weather(
                                lon = col['geo_long'],
                                lat=col['geo_lat'],
                                data_str=col['data_powstania'],
                                type_utr=col['typ'])
        
        if weather_row.empty:
            continue

        weather_df = pd.concat([weather_df,weather_row],ignore_index=True)

    
    print(weather_df)

data_parsing()