import arcpy

# Set the paths to the feature classes (use relative paths for GitHub)
centerline_fc = r"Path_to_Your_Geodatabase\Roads_Line"
polygon_fc = r"Path_to_Your_Geodatabase\Roads"

# Set the workspace (use relative path)
arcpy.env.workspace = r"Path_to_Your_Geodatabase"

# Create a feature layer from the centerline and polygon features
arcpy.MakeFeatureLayer_management(centerline_fc, "centerline_lyr")
arcpy.MakeFeatureLayer_management(polygon_fc, "polygon_lyr")

# Select centerlines that do not intersect the polygons
arcpy.SelectLayerByLocation_management(
    "centerline_lyr", "INTERSECT", "polygon_lyr", invert_spatial_relationship=True
)

# Count the number of selected centerlines
count = int(arcpy.GetCount_management("centerline_lyr")[0])

# Check if there are any centerlines that fall outside the polygon
if count > 0:
    print(f"There are {count} centerline(s) that fall outside the road polygons.")
    # Optionally, export these to a new feature class (use relative path)
    arcpy.CopyFeatures_management("centerline_lyr", r"Path_to_Your_Geodatabase\Roads_Line_Outside")
else:
    print("All centerlines are within the road polygons.")
