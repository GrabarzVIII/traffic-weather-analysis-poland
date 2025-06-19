import pandas as pd
from datetime import datetime
from meteostat import Hourly, Point
from utils.const import DATA_WHEATHER_LOG_PATH

def get_weather (lat: float, lon: float, data_str: str, type_utr:str) -> pd.core.frame.DataFrame:

    def log(message: str):
        with open(DATA_WHEATHER_LOG_PATH, 'a') as f:
                f.write(f'{datetime.now()} - {message}\n')
    
    try:

        y,m,d,h,min = int(data_str[:4]),int(data_str[5:7]),int(data_str[8:10]),int(data_str[11:13]),int(data_str[14:16])
        start = datetime(y,m,d,h,0)
        end = datetime(y,m,d,h+1,0)
        point = Point(lat,lon)
        weather = Hourly(point,start=start,end=end)
        weather_df = weather.fetch()

        if weather_df.empty:
            log(f'no_weather_data_for_{type_utr}{lat}{lon}{data_str}')
            return pd.DataFrame()

        weather_df = weather_df.rename(columns={
            'temp': 'temperature',
            'dwpt': 'dew_point',
            'rhum': 'relative_humidity',
            'prcp': 'precipitation',
            'snow': 'snowfall',
            'wdir': 'wind_direction',
            'wspd': 'wind_speed',
            'wpgt': 'wind_gust',
            'pres': 'pressure',
            'tsun': 'sunshine_duration',
            'coco': 'weather_condition_code'
        })
        
        weather_df['utr_index'] = f'{type_utr}{lat}{lon}{data_str}'
        
        if min < 20 and start in weather_df.index:
            return weather_df.loc[[start]]

        elif min >= 20 and min < 40:
            return weather_df.groupby('utr_index').mean(numeric_only=True)
        
        elif min >= 40 and end in weather_df.index:
            return weather_df.loc[[end]]
        
        else:
            return weather_df.iloc[[0]]


    except Exception as e:
        log(e)
        return pd.DataFrame()
