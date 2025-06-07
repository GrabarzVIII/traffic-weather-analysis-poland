import requests
import os

data_path = r"Data\GDDiK_data"
log_path = r"logs\GDDiK_download.log"
url = r"https://www.archiwum.gddkia.gov.pl/dane/zima_html/utrdane.xml"

latest_file = None
latest_time = 0

with os.scandir(data_path) as entries:
    for entry in entries:
        if entry.is_file():
            mod_time = entry.stat().st_mtime
            if mod_time > latest_time:
                latest_time = mod_time
                latest_file = entry.name

file_path = data_path + '\\' + latest_file

