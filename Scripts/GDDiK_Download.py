import requests
import os
import xml.etree.ElementTree as ET

data_path = r"Data\GDDiK_data"
data_temp_path = r"Data\GDDiK_data\temp_xml\temp.xml"
log_path = r"logs\GDDiK_download.log"
url = r"https://www.archiwum.gddkia.gov.pl/dane/zima_html/utrdane.xml"

latest_file = None
latest_time = 0

if os.path.exists(data_temp_path):
    os.remove(data_temp_path)

with os.scandir(data_path) as entries:
    for entry in entries:
        if entry.is_file():
            mod_time = entry.stat().st_mtime
            if mod_time > latest_time:
                latest_time = mod_time
                latest_file = entry.name

if latest_file == None:
    xml_file = requests.get(url)
    print(xml_file.status_code)
    if xml_file.status_code == 200:
        
        gen = ""
        with open(data_temp_path, 'wb') as f:
            f.write(xml_file.content)
        
        #with open(data_temp_path, 'r', encoding='utf-8') as f:
        #    first_line = f.readline().strip()
        tree = ET.parse(data_temp_path)
        root = tree.getroot()

        gen = root.attrib.get('gen')
        print(gen)
            
    
else:
    file_path = data_path + '\\' + latest_file

