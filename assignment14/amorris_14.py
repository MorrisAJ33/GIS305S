import arcpy
srs= arcpy.ListSpatialReferences("*utm/north america*")
for sr_string in srs:
    sr_object = arcpy.SpatialReference(sr_string)
    print("{0.centralMeridian} {0.name} {0.PCSCode}".format(sr_object))
aprx = arcpy.mp.ArcGISProject(r"C:\Users\morri\Documents\Alex Morris\GIS 305\arcgis\westnileoutbreak\WestNileOutbreak\WestNileOutbreak.aprx")
map_doc = aprx.listMaps()[0]
print(map_doc)
utm13 = arcpy.SpatialReference(3743)
map_doc.spatialReference = utm13
lyr = map_doc.listLayers("U.S. States (Generalized)")[0]
sym = lyr.symbology
sym.renderer.symbol.color ={'RGB' : [255,0,0,100] }
sym.renderer.symbol.outlineColor ={'RGB' : [100,100,100,100] }
lyr.symbology = sym
lyr.transparency = 50
aprx.save()