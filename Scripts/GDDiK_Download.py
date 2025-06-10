import requests
import os
import xml.etree.ElementTree as ET
import datetime

from utils.const import DATA_GDDIK_PATH, DATA_GDDIK_TEMP_PATH, DATA_GDDIK_LOG_PATH, URL_GDDIK

def gddik_xml_downloading():

    def saving_xml(xml_file: requests.models.Response,data_path: str):
        try:
            gen = ""
            with open(DATA_GDDIK_TEMP_PATH, 'wb') as f:
                f.write(xml_file.content)
            
            tree = ET.parse(DATA_GDDIK_TEMP_PATH)
            root = tree.getroot()
            gen = root.attrib.get('gen')
            gen_file = gen.replace(":","")

            data_path = f'{DATA_GDDIK_PATH}\\GDDiK_data_{gen_file}'

            with open(data_path, 'wb') as f:
                f.write(xml_file.content)

            os.remove(DATA_GDDIK_TEMP_PATH)

            with open(DATA_GDDIK_LOG_PATH, 'a') as f:
                f.write(f'{datetime.datetime.now()}-{data_path}-saved\n')

        except Exception as e:
            with open(DATA_GDDIK_LOG_PATH, 'a') as f:
                f.write(f'ERROR-{datetime.datetime.now()}-{e}\n')

    try:
        latest_file = None
        latest_time = 0

        #deleting temp file
        if os.path.exists(DATA_GDDIK_TEMP_PATH):
            os.remove(DATA_GDDIK_TEMP_PATH)

        xml_file = requests.get(URL_GDDIK)
        if xml_file.status_code == 200:

            #scaning for lastest xml file form GDDiK
            with os.scandir(DATA_GDDIK_PATH) as entries:
                for entry in entries:
                    if entry.is_file():
                        mod_time = entry.stat().st_mtime
                        if mod_time > latest_time:
                            latest_time = mod_time
                            latest_file = entry.name


            #if not exists previous GDDiK xml file
            if latest_file == None:
                saving_xml(xml_file,DATA_GDDIK_PATH)
                        
            #if exists previous GDDiK xml file    
            else:
                data_path_l = f'{DATA_GDDIK_PATH}\\{latest_file}' #change this line to more flexible

                with open(DATA_GDDIK_TEMP_PATH,'wb') as f:
                    f.write(xml_file.content)

                tree_lastest = ET.parse(data_path_l)
                root_lastest = tree_lastest.getroot()
                gen_lastest = root_lastest.attrib.get('gen')

                tree_temp = ET.parse(DATA_GDDIK_TEMP_PATH)
                root_temp = tree_temp.getroot()
                gen_temp = root_temp.attrib.get('gen')


                #if GDDiK xml was download
                if gen_lastest == gen_temp:

                    with open(DATA_GDDIK_LOG_PATH, 'a') as f:
                        f.write(f'{datetime.datetime.now()}-{data_path_l}-exists\n')

                else:
                    saving_xml(xml_file,DATA_GDDIK_PATH)
        else:
            with open(DATA_GDDIK_LOG_PATH, 'a') as f:
                f.write(f'{datetime.datetime.now()}-{xml_file.status_code}-faild_connection')

    except Exception as e:
        with open(DATA_GDDIK_LOG_PATH, 'a') as f:
                f.write(f'ERROR-{datetime.datetime.now()}-{e}\n')




