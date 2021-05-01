import arcpy
import yaml
import logging
from etl.GSheetsEtl import GSheetsEtl


def main():
    logging.info('Starting West Nile Virus Simulation')
    arcpy.env.workspace = fr"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    find_lyr= arcpy.ListFeatureClasses()
    for lyr in find_lyr:
        print(lyr)
        if  lyr == "Lakes_Res" or lyr == "Mosquito" or lyr == "OSMP_Prop" or lyr == "Wetlands_Reg" or lyr == 'avoid_points':
            d_base = fr"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb\\"
            logging.debug('Starting Buffer')
            output_layer = buffer(d_base, lyr)
            logging.debug('End Buffer')
            print(output_layer, " has completed processing.")
        else:
            print("No Buffer")

    inFeatures = ["Lakes_Res_Buff", "Mosquito_Buff", "OSMP_Prop_Buff", "Wetlands_Reg_Buff"]
    intersect_save = input("Enter intersect description word:")
    int_out = f"{intersect_save}_intersect"
    logging.debug('Starting Intersect')
    arcpy.Intersect_analysis(inFeatures, int_out, "ALL")
    logging.debug('End Intersect')
    logging.debug('Starting  Erase')
    arcpy.Erase_analysis(int_out, 'avoid_points_Buff', 'spray_zone')
    logging.debug('End Erase')
    address_all = 'Boulder_add'
    name_result = "spray_address"
    arcpy.Intersect_analysis([address_all, int_out], name_result, "ALL")
    logging.debug('Starting  Select')
    arcpy.SelectLayerByAttribute_management(name_result, "NEW_SELECTION")
    logging.debug('End  Select')
    my_cnt = arcpy.GetCount_management(name_result)
    print(f"There are {my_cnt} selected features")
    mapthis(name_result)
def buffer(gdb, shp):
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
def mapthis(out_layer):
    aprx = arcpy.mp.ArcGISProject(fr"{config_dict.get('proj_dir')}\WestNileOutbreak.aprx")
    map_disp = aprx.listMaps()[0]
    dbase= fr"{config_dict.get('proj_dir')}\WestNileOutbreak.gdb"
    map_disp.addDataFromPath(rf"{dbase}\{out_layer}")
    aprx.save()
    lyt = aprx.listLayouts()[0]
    for el in lyt.listElements():
        print(el.name)
        if "Title" in el.name:
            sub_title= input("Enter custom map Sub-Title: ")
            el.text = el.text + sub_title
    map = input("Enter layout sub name: ")
    lyt.exportToPDF(f"layout_{map}")
def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
        logging.basicConfig(level=logging.DEBUG,
                            filename= "wnv.log",
                            filemode='w',
                            format='%(name)s - '
                                '%(levelname)s - '
                                '%(message)s')
    return config_dict
def etl():
    GSheetsEtl(config_dict)
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()

if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    #etl()
    main()
