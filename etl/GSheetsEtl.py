import arcpy
import requests
import csv

from etl.SpatialEtl import SpatialEtl

config_dict = None
class GSheetsEtl(SpatialEtl):

    def __init__(self, config_dict):
        super().__init__(self.config_dict)

    def extract(self):
        print("Extracting addresses from google form spreadsheet")
        # file = urllib.request.urlopen("https://docs.google.com/spreadsheets/d/e/2PACX-1vTaJ_1xRhGQAOSITkgn_C1wfPSnPX0BA37XuftlXVfVrpjfj4J3BHPu1soGeUtNt3XjLI1G_HT2Fy69/pub?output=csv")

        r = requests.get(
            self.config_dict.get('remote_url'))
        r.encoding = "utf-8"
        data = r.text
        with open(f"{self.config_dict.get('proj_dir')}addresses.csv", "w") as output_file:
            output_file.write(data)

    def load(self):
        # Description: Creates a point feature class from input table

        # Set environment settings
        arcpy.env.workspace = rf"{config_dict.get('proj_dir')}WestNileOutbreak.gdb\\"
        arcpy.env.overwriteOutput = True

        # Set the local variables
        in_table = r"C:\Users\morri\Downloads\new_addresses.csv"
        out_feature_class = "avoid_points"
        x_coords = "X"
        y_coords = "Y"

        # Make the XY event layer...
        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)

        # Print the total rows
        print(arcpy.GetCount_management(out_feature_class))

    def process(self):
        super().extract()
        super().transform()
        super().load()