import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#GDDiK data paths
DATA_GDDIK_PATH = os.path.join(BASE_DIR,"Data","GDDiK_data") #r"Data\GDDiK_data"
DATA_GDDIK_TEMP_PATH = os.path.join(BASE_DIR,"Data","GDDiK_data","temp_xml","temp.xml") #r"Data\GDDiK_data\temp_xml\temp.xml"

#GDDiK logs path
DATA_GDDIK_LOG_PATH = os.path.join(BASE_DIR,"logs","GDDiK_download.log") #r"logs\GDDiK_download.log"
DATA_WHEATHER_LOG_PATH = os.path.join(BASE_DIR,"logs","weather_download.log")

#External URLs
URL_GDDIK = r"https://www.archiwum.gddkia.gov.pl/dane/zima_html/utrdane.xml"

#Parsed data
PARASED_GDDIK = os.path.join(BASE_DIR,"Data","Parased","GDDiK")
PARASED_WEATHER = os.path.join(BASE_DIR,"Data","Parased","Weather")