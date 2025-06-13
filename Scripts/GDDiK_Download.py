import requests
import os
import xml.etree.ElementTree as ET
import datetime

from typing import Tuple, Optional
from utils.const import DATA_GDDIK_PATH, DATA_GDDIK_TEMP_PATH, DATA_GDDIK_LOG_PATH, URL_GDDIK

def gddik_xml_downloading():

    def log(message: str):
        with open(DATA_GDDIK_LOG_PATH, 'a') as f:
                f.write(f'{datetime.datetime.now()} - {message}\n')

    def get_gen_from_xml(path: str) -> Optional[str]:
        tree = ET.parse(path)
        root = tree.getroot()
        return root.attrib.get('gen') 

    def saving_xml(xml_file: requests.models.Response):
        try:
            with open(DATA_GDDIK_TEMP_PATH, 'wb') as f:
                f.write(xml_file.content)
            
            gen = get_gen_from_xml(DATA_GDDIK_TEMP_PATH)
            if gen is None:
                raise ValueError("Brak atrybutu 'gen' w XML")
            gen_file = gen.replace(":", "")

            file_name = f'GDDiK_data_{gen_file}.xml'
            save_path = os.path.join(DATA_GDDIK_PATH, file_name)

            with open(save_path, 'wb') as f:
                f.write(xml_file.content)

            log(f'{save_path} - saved')


        except Exception as e:
            log(e)

    def get_xml_file(url: str) -> Tuple[requests.models.Response, Optional[str]]:
        try:
            latest_file = None
            latest_time = 0
            xml_file = requests.get(url)
            xml_file.raise_for_status()

        # Scanning for the latest XML file from GDDKiA
            with os.scandir(DATA_GDDIK_PATH) as entries:
                for entry in entries:
                    if entry.is_file():
                        mod_time = entry.stat().st_mtime
                        if mod_time > latest_time:
                            latest_time = mod_time
                            latest_file = entry.name

            return xml_file, latest_file
        except Exception as e:
            log(e)
            return None,None




    try:
        
        xml_file, latest_file = get_xml_file(URL_GDDIK)

        if xml_file is None:
            log('nieudalo_sie_pobrac_pliku_xml')
            return
        
        #deleting temp file
        if os.path.exists(DATA_GDDIK_TEMP_PATH):
            os.remove(DATA_GDDIK_TEMP_PATH)


        #if not exists previous GDDiK xml file
        if latest_file == None:
            saving_xml(xml_file)
                    
        #if exists previous GDDiK xml file    
        else:

            latest_file_path = os.path.join(DATA_GDDIK_PATH, latest_file)

            with open(DATA_GDDIK_TEMP_PATH,'wb') as f:
                f.write(xml_file.content)

            gen_latest = get_gen_from_xml(latest_file_path)

            gen_temp = get_gen_from_xml(DATA_GDDIK_TEMP_PATH)


            #if GDDiK xml was download
            if gen_latest == gen_temp:
                
                log(f'{latest_file_path} - exists')

            else:
                saving_xml(xml_file)


    except Exception as e:
        log(e)

    finally:
        if os.path.exists(DATA_GDDIK_TEMP_PATH):
            os.remove(DATA_GDDIK_TEMP_PATH)




