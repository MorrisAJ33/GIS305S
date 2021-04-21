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
            output_layer = buffer(d_base, lyr)
            print(output_layer, " has completed processing.")
        else:
            print("No Buffer")

    inFeatures = ["Lakes_Res_Buff.shp", "Mosquito_Buff.shp", "OSMP_Prop_Buff.shp", "Wetlands_Reg_Buff.shp"]
    intersect_save = input("Enter intersect description word:")
    arcpy.Intersect_analysis(inFeatures, f"{intersect_save}_intersect.shp", "ALL")
    arcpy.analysis.Erase("{intersect_save}_intersect.shp", 'avoid_points_Buff','spray_zone.shp')
    name_result = "spray_address.shp"
    target = 'Boulder_add.shp'
    arcpy.SpatialJoin_analysis(target, 'spray_zone.shp', name_result)
    arcpy.SelectLayerByAttribute_management(name_result, "NEW_SELECTION")
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
    global d_base
    out = rf"{d_base}\{out_layer}"
    map_disp.addDataFromPath(out)
    aprx.save()
def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    logging.basicConfig(filename=f"{config_dict.get('proj_dir')}wnv.log", filemode="w", level=logging.DEBUG)
    return config_dict
def etl():
    GSheetsEtl(config_dict)
    #etl_instance = GSheetsEtl(config_dict)
    #etl_instance.process()

if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()
    main()
