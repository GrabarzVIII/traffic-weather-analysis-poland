import os
import pandas as pd
import xml.etree.ElementTree as ET

from GDDiK_Download import gddik_xml_downloading
from weather_download import get_weather
from utils.const import DATA_GDDIK_PATH, DATA_PARSING_LOG_PATH, PARASED_GDDIK, PARASED_WEATHER

def data_parsing():

    def get_gen_from_xml(path: str) -> str:
        tree = ET.parse(path)
        root = tree.getroot()
        return root.attrib.get('gen') 

    try:
        ######################################################################
        #checking last GDDiK xml
        ######################################################################

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
        gen = get_gen_from_xml(latest_file_dir)

        gddik_df = pd.read_xml(latest_file_dir, xpath='utr')
        

        ######################################################################
        #downloding weather to GDDiK frame
        ######################################################################

        weather_df = pd.DataFrame()
        gddik_df_final = pd.DataFrame()

        for i, col in gddik_df.iterrows():
            
            if col['typ'] == 'U' or col['typ'] == 'I':
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
            gddik_df_final = pd.concat([gddik_df_final,col.to_frame().T],ignore_index=True)

            mask = (
                (gddik_df_final['geo_long'] == col['geo_long']) &
                (gddik_df_final['geo_lat'] == col['geo_lat']) &
                (gddik_df_final['data_powstania'] == col['data_powstania']) &
                (gddik_df_final['typ'] == col['typ'])
            )

            if 'utr_index' not in gddik_df_final.columns:
                gddik_df_final['utr_index'] = None

            gddik_df_final.loc[mask, 'utr_index'] = weather_df['utr_index'].values[0]
            

        ######################################################################
        #saving weather DataFrame and GDDiK DataFrame to CSV
        ###################################################################### 
        print('generowanie plikow')

        os.makedirs(PARASED_WEATHER, exist_ok=True)
        os.makedirs(PARASED_GDDIK, exist_ok=True)
        gen = gen.replace(':','')
        
        weather_file = os.path.join(PARASED_WEATHER,f'weather_{gen}.csv')
        print(weather_file)
        weather_df.to_csv(weather_file,sep=";")

        gddik_file = os.path.join(PARASED_GDDIK,f'GDDiK_{gen}.csv')
        print(gddik_file)
        gddik_df_final.to_csv(gddik_file,sep=";")

    except Exception as e:
        print(e)
        return None
    

data_parsing()