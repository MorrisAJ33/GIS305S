import yaml
import arcpy
from etl.GSheetsEtl import GSheetsEtl

def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    return config_dict
