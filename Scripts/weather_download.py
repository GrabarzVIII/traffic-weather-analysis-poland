import pandas as pd
from datetime import datetime
from meteostat import Hourly, Point
from utils.const import DATA_WHEATHER_LOG_PATH

#lan = 17.090633
#lat = 51.178573
#data_string = '2025-03-24T18:36:00+0100'
#type_u = 'U'

def get_weather (lat: float, lan: float, data_str: str, type_utr:str) -> pd.core.frame.DataFrame:

    def log(message: str):
        with open(DATA_WHEATHER_LOG_PATH, 'a') as f:
                f.write(f'{datetime.now()} - {message}\n')
    
    try:

        y,m,d,h,min = int(data_str[:4]),int(data_str[5:7]),int(data_str[8:10]),int(data_str[11:13]),int(data_str[14:16])
        start = datetime(y,m,d,h,0)
        end = datetime(y,m,d,h+1,0)
        point = Point(lat,lan)
        weather = Hourly(point,start=start,end=end)
        weather_df = weather.fetch()

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
        
        weather_df['utr_index'] = f'{type_utr}{lat}{lan}{data_str}'
        
        if min < 20:
            return weather_df.loc[[start]]

        elif min >= 20 and min < 40:
            return weather_df.groupby('utr_index').mean()
        
        elif min >= 40:
            return weather_df.loc[[end]]


    except Exception as e:
        log(e)
        return None


#get_weather(lat=lat,lan=lan,data_str=data_string)