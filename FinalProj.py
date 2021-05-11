import arcpy
import yaml
import logging
from etl.GSheetsEtl import GSheetsEtl


def main():
    """
    Arc GIS workspace with 5 files listed in read me, to construct spray addresses
    with an avoided area for homes returning form
    Output spray zone layer and spray address layer
    """

    logging.info('Starting West Nile Virus Simulation')
    arcpy.env.workspace = fr"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    find_lyr = arcpy.ListFeatureClasses()

   #buffer for loop
    try:
        for lyr in find_lyr:
            print(lyr)
            if lyr == "Lakes_and_Reservoirs-shp" or lyr == "Mosquito_Larval_sites-shp" or lyr == "OSMP_PropOSMP_Properties-shp" or lyr=="Wetlands_Regulatory" or lyr=="avoid_points":
                d_base= fr"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb"
                logging.debug('Starting Buffer')
                output_layer = buffer(d_base, lyr)
                logging.debug('End Buffer')
                print(output_layer, " has completed processing.")
            elif lyr == 'address_CO_N' or lyr == 'spray_CO_N':
                arcpy.Delete_management(lyr)
            else:
                print("No Buffer")
    except Exception as e:
        print(f"Error in Buffer Loop {e}")
    try:
        # buffered layers created from precceding loop
        inFeatures = ["Lakes_Res_Buff", "Mosquito_Buff", "OSMP_Prop_Buff", "Wetlands_Reg_Buff"]
        # Intersect identifier input
        intersect_save = input("Enter intersect description word:")
        # saved intersect layer with identifier
        int_out = f"{intersect_save}_intersect"

        logging.debug('Starting Intersect')
        # Intersect process with all above hazard layer buffers
        arcpy.Intersect_analysis(inFeatures, int_out, "ALL")
        logging.debug('End Intersect')


        logging.debug('Starting  Erase')
        # Avoid points are another buffer, but need to be removed from hazard intersect
        arcpy.Erase_analysis(int_out, 'avoid_points_Buff', 'spray_zone')
        logging.debug('End Erase')

        address_all = 'Boulder_add'
        name_result = "target_address"
        # Second intersect to get addresses that are within hazard area intersect
        logging.debug('Starting  intersect')
        arcpy.Intersect_analysis([address_all, int_out], name_result, "ALL")
        logging.debug('End Intersect')

        logging.debug('Starting  Select')
        arcpy.SelectLayerByAttribute_management(name_result, "NEW_SELECTION")
        logging.debug('End  Select')
        my_cnt = arcpy.GetCount_management(name_result)
        print(f"There are {my_cnt} selected features")

        arcpy.SelectLayerByAttribute_management(name_result, "CLEAR_SELECTION")
        proj_lyr = 'address_CO_N'
        spatialref = 2231
        arcpy.Project_management(name_result, proj_lyr, spatialref)
        arcpy.Project_management('spray_zone', 'spray_CO_N', spatialref)

        mapthis(proj_lyr, 'spray_CO_N', my_cnt)
        record_address('address_CO_N', config_dict)
    except Exception as e:
        print(f"Error in spray address creation {e}")

def buffer(gdb, shp):
    """Buffer is called from main loop, input is here that requires a value no less than 1000 ft, and no greater
    than 5000 ft. The resulting layer is saved and used within main geoprocessing."""

    import arcpy
    units = " Feet"
    dist1 = input(f"Enter a distance in feet to buffer {shp}, between 1,000 and 5,000 ft. ")
    chk = int(dist1)
    while chk < 1000 or chk > 5000:
        dist1 = input(f"Distance in feet to buffer {shp}, between 1,000 and 5,000 ft. ")
        chk = int(dist1)
    dist2 = dist1 + units
    output_layer = rf"{gdb}{shp}_Buff"
    print(output_layer)
    buff_lyr = rf"{gdb}{shp}"
    arcpy.Buffer_analysis(buff_lyr, output_layer, dist2, "FULL", "ROUND", "ALL")
    return output_layer


def mapthis(out_layer, layer2, count):
    """
    Input two layers returned from main and map them as well as include
    address count in sub-title
    """
    try:
        aprx = arcpy.mp.ArcGISProject(fr"{config_dict.get('proj_dir')}\WestNileOutbreak.aprx")
        map_disp = aprx.listMaps()[0]
        dbase = fr"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb"
        co_n = arcpy.SpatialReference(2231)
        map_disp.spatialReference = co_n
        map_disp.addDataFromPath(rf"{dbase}\{layer2}")
        lyr = map_disp.listLayers(layer2)[0]
        sym = lyr.symbology
        sym.renderer.symbol.color = {'RGB': [255, 0, 0, 100]}
        sym.renderer.symbol.outlineColor = {'RGB': [100, 100, 100, 100]}
        lyr.symbology = sym
        lyr.transparency = 50
        aprx.save()
        map_disp.addDataFromPath(rf"{dbase}\{out_layer}")
        aprx.save()
        lyt = aprx.listLayouts()[0]
        for el in lyt.listElements():
            print(el.name)
            if "Title" in el.name:
                sub_title = input("Enter custom map Sub-Title: ")
                el.text = f"{el.text}: {sub_title}, Address Count={count}"
        map = input("Enter layout sub name: ")
        lyt.exportToPDF(f"layout_{map}")
    except Exception as e:
        print(f"Error in map layout {e}")
def setup():
    """setup is a method that can call a yaml file configuration dictionary which can define environments like workspace
    the path to Gsheets form for avoid points, and geocoder URL to create avoid points shape file."""
    try:
        with open('config/wnvoutbreak.yaml') as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)
            logging.basicConfig(level=logging.DEBUG,
                                filename="wnv.log",
                                filemode='w',
                                format='%(name)s - '
                                       '%(levelname)s - '
                                       '%(message)s')
        return config_dict
    except Exception as e:
        print(f"Error in yaml config {e}")

def etl():
    """etl can be imported as base class definitions for use in extraction, transformation and loading data.
    these classes define objects written too and returned from created csv to then apply spatial information for
    further output processing."""
    try:
        GSheetsEtl(config_dict)
        etl_instance = GSheetsEtl(config_dict)
        etl_instance.process()
    except Exception as e:
        print(f"Error in extract, transform and load {e}")

def record_address(spray_add, config_dict):
    """
    Create a csv file, output_address that has all addresses to be sprayed for mosquitos
    """
    print("Creating CSV of final addresses")
    try:
    # Create a search cursor based on the shapefile
        Row = arcpy.SearchCursor(spray_add)

        # Loop through each row in the attributes
        for R in Row:
            # write value to file
            output_file = open(rf"{config_dict.get('proj_dir')}\output_addresses.csv", "w")
            output_file.write(f"{R}\n")

    except Exception as e:
        print(f"Error in extract, transform and load {e}")

if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()
    main()
