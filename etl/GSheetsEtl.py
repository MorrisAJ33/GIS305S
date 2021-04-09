import arcpy
from etl.SpatialEtl import SpatialEtl

class GSheetsEtl(SpatialEtl):

    def __init__(self, remote, local_dir, data_format, destination):
        super().__init__(remote, local_dir, data_format, destination)

    def extract(self):
        print("Extracting addresses from google form spreadsheet")
        # file = urllib.request.urlopen("https://docs.google.com/spreadsheets/d/e/2PACX-1vTaJ_1xRhGQAOSITkgn_C1wfPSnPX0BA37XuftlXVfVrpjfj4J3BHPu1soGeUtNt3XjLI1G_HT2Fy69/pub?output=csv")

        r = requests.get(
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vTaJ_1xRhGQAOSITkgn_C1wfPSnPX0BA37XuftlXVfVrpjfj4J3BHPu1soGeUtNt3XjLI1G_HT2Fy69/pub?output=csv")
        r.encoding = "utf-8"
        data = r.text
        with open(r"C:\Users\morri\Downloads\addresses.csv", "w") as output_file:
            output_file.write(data)

    def load(self):
        # Description: Creates a point feature class from input table

        # Set environment settings
        arcpy.env.workspace = r"C:\Users\morri\Documents\Alex Morris\GIS 305\arcgis\westnileoutbreak\WestNileOutbreak\WestNileOutbreak.gdb\\"
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