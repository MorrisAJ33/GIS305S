# GIS305S  Alex Morris Spring 2021
For my FRCC GIS Programming Class

This script needs to have an ArcGIS workspace defined in the yaml file.
Yaml file file needs to include URL to form .csv for avoid addresses
Yaml file needs a URL split for inserting address inside two halves of geocoding URL.

The goal is to take layers that can be identified as breeding grounds
for mosquitos.

Layers needed:  Boulder_Addresses
		OSMP_Properties-shp
		Lakes_and_Reservoirs-shp
		Mosquito_Larval_sites-shp
		Wetlands_Regulatory

Spatial ETL defines config dictionary in extract transform and load.
Gsheets ETL take config object and uses the key value pairs in dictionary to extract csv data, write to a new file, then use file to insert into geocoding url.
The geocoded points are written to new .csv to then be converted XY points in table to shape file, this becomes Avoid_points layer.

Main function includes most arcpy Geoprossesing. Initially looping through layers, first to identify layers
    requiring an input for buffer, also if previous output layers exist, delete them. All buffers are combined in intersect,
    except avoid points buffer which will erase from intersect layer. Output area is then overlaid by address' to
     find the resulting address' that we would like to spray in hazardous zones. Finally output layers are projected
     to state plane.

4 layers defined above (exclude Boulder_Addresses), and created Avoid_points layer are all passed to buffer function.
4 layers are combined with an intersect. 5th buffer (Avoid_points) is erased from the intersect.
The result is the spray area, of hazard area without the avoided buffer.

The spray area needs to be intersected withBoulder_Addresses to determine addresses to spray for mosquito control.

The spray area and spray addresses are converted to stateplane coordinate system.
This is the set spatial reference of map frame in code.

Finally, resulting layers are mapped to a layout, the layout requires two user inputs, a sub-title, and unique file identifier.
Count of addresses included.