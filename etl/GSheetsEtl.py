
import arcpy
import requests
import csv

# from etl folder use file spatial etl output
from etl.SpatialEtl import SpatialEtl


class GSheetsEtl(SpatialEtl):
    """
    Gsheets Etl is an extract, transform and load function. Data in .csv
    format is retrieved from google form through URL. Data must have street
    address.

    Parameters:
        config_dict (dictionary): A dictionary containing a remote_URL key to the
        google spreadsheet and web GeoCoding service.
    """
    # dictionary passed in to create instance
    config_dict = None

# from etl folder use file spatial etl output
    def __init__(self, config_dict):
        super().__init__(config_dict)

    def extract(self):
        """Extracting data from Google spreadsheet to write to local file"""

        print("Extracting addresses from google form spreadsheet")

        r = requests.get(self.config_dict.get('remote_url'))
        r.encoding = "utf-8"
        data = r.text
        with open(rf"{self.config_dict.get('proj_dir')}\addresses.csv", "w") as output_file:
            output_file.write(data)

    def transform(self):
        """
        Transform takes csv inputs address into geocoder, and records coordinates in new .csv
        """
        try:
            print("Add City, State")

            transformed_file = open(rf"{self.config_dict.get('proj_dir')}\new_addresses.csv", "w")
            transformed_file.write("X,Y,Type\n")
            with open(rf"{self.config_dict.get('proj_dir')}\addresses.csv", "r") as partial_file:
                csv_dict = csv.DictReader(partial_file, delimiter=',')
                for row in csv_dict:
                    address = row["Street Address"] + " Boulder CO"
                    print(address)
                    urladdress= address.replace(" ","+")
                    geo_concat = rf"{self.config_dict.get('geocoder_prefix_url')}{urladdress}{self.config_dict.get('geocoder_suffix_url')}"
                    print(geo_concat)
                    r = requests.get(geo_concat)
                    r.encoding = "utf-8"
                    #print(r.text)

                    resp_dict = r.json()
                    x = resp_dict['result']['addressMatches'][0]['coordinates']['x']
                    y = resp_dict['result']['addressMatches'][0]['coordinates']['y']
                    transformed_file.write(f"{x},{y},Residential\n")
            transformed_file.close()

        except Exception as e:
            print(f"Error in extract, transform and load {e}")


    def load(self):
        """
        New Point layer is created from geocoded csv
        """
        # Description: Creates a point feature class from input table

        # Set environment settings
        arcpy.env.workspace= rf"{self.config_dict.get('proj_dir')}\WestNileOutbreak.gdb\\"
        arcpy.env.overwriteOutput = True

        # Set the local variables
        in_table = rf"{self.config_dict.get('proj_dir')}\new_addresses.csv"
        out_feature_class = "avoid_points.shp"
        x_coords = "X"
        y_coords = "Y"

        # Make the XY event layer...
        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)

        # Print the total rows
        print(arcpy.GetCount_management(out_feature_class))


    def process(self):
        self.extract()
        self.transform()
        self.load()