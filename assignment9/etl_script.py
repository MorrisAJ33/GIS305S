import arcpy
import csv
import requests

def extract():
    print("Extracting addresses from google form spreadsheet")
    r =requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vTaJ_1xRhGQAOSITkgn_C1wfPSnPX0BA37XuftlXVfVrpjfj4J""3BHPu1soGeUtNt3XjLI1G_HT2Fy69/pub?output=csv")
    r.encoding = "utf-8"
    data = r.text
    with open(r"C:\Users\morri\Downloads\addresses.csv", "w") as output_file:
        output_file.write(data)
def transform():
    print('Add City, State')
    transformed_file = open(r"C:\Users\morri\Downloads\new_addresses.csv", "w")
    transformed_file.write('X, Y, Type\n')
    with open(r"C:\Users\morri\Downloads\addresses.csv", "r") as partial_file:
        csv_dictionary = csv.DictReader(partial_file, delimiter = ',')
        for row in csv_dictionary:
            addrress = row["Street Address"] + " Boulder CO"
            print(addrress)
            geocode_url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=" + addrress +"&benchmark=2020&format=json"
            print(geocode_url)
            r = requests.get(geocode_url)
            resp_dict = r.json()
            print(resp_dict)
            x = resp_dict['result']['addressMatches'][0]['coordinates']['x']
            y = resp_dict['result']['addressMatches'][0]['coordinates']['y']
            transformed_file.write(f'{x},{y},Residential\n')
def load():
    arcpy.env.workspace = r'C:\Users\morri\Documents\Alex Morris\GIS 305\arcgis\westnileoutbreak\WestNileOutbreak\WestNileOutbreak.gdb\\'
    arcpy.env.overwriteOutput = True
    in_table = r"C:\Users\morri\Downloads\new_addresses.csv"
    out_feature_class = "avoid_points"
    x_coords = 'x'
    y_coords = 'y'
    arcpy.management.XYTableToPoint(in_table,out_feature_class,x_coords,y_coords)
    print(arcpy.GetCount_management(out_feature_class))
if __name__ == "__main__":
    extract()
    transform()
    load()