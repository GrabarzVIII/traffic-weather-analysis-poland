import requests
import os
import xml.etree.ElementTree as ET
import datetime

def saving_xml(xml_file,data_path):
    gen = ""
    with open(data_temp_path, 'wb') as f:
        f.write(xml_file.content)
    
    tree = ET.parse(data_temp_path)
    root = tree.getroot()
    gen = root.attrib.get('gen')
    gen_file = gen.replace(":","")

    data_path = f'{data_path}\\GDDiK_data_{gen_file}'

    with open(data_path, 'wb') as f:
        f.write(xml_file.content)

    os.remove(data_temp_path)

    with open(log_path, 'a') as f:
        f.write(f'{time}-{data_path}-saved\n')

data_path = r"Data\GDDiK_data"
data_temp_path = r"Data\GDDiK_data\temp_xml\temp.xml"
log_path = r"logs\GDDiK_download.log"
url = r"https://www.archiwum.gddkia.gov.pl/dane/zima_html/utrdane.xml"
time = datetime.datetime.now()

latest_file = None
latest_time = 0

#deleting temp file
if os.path.exists(data_temp_path):
    os.remove(data_temp_path)

xml_file = requests.get(url)
if xml_file.status_code == 200:

    #scaning for lastest xml file form GDDiK
    with os.scandir(data_path) as entries:
        for entry in entries:
            if entry.is_file():
                mod_time = entry.stat().st_mtime
                if mod_time > latest_time:
                    latest_time = mod_time
                    latest_file = entry.name


    #if not exists previous GDDiK xml file
    if latest_file == None:
        saving_xml(xml_file,data_path)
                
    #if exists previous GDDiK xml file    
    else:
        data_path_l = f'{data_path}\\{latest_file}'

        with open(data_temp_path,'wb') as f:
            f.write(xml_file.content)

        tree_lastest = ET.parse(data_path_l)
        root_lastest = tree_lastest.getroot()
        gen_lastest = root_lastest.attrib.get('gen')

        tree_temp = ET.parse(data_temp_path)
        root_temp = tree_temp.getroot()
        gen_temp = root_temp.attrib.get('gen')

        print(gen_lastest)
        print(gen_temp)
        #if GDDiK xml was download
        if gen_lastest == gen_temp:

            with open(log_path, 'a') as f:
                f.write(f'{time}-{data_path}-exists\n')

        else:
            saving_xml(xml_file,data_path)
else:
    with open(log_path, 'a') as f:
                f.write(f'{time}-{xml_file.status_code}-faild_connection')
            




