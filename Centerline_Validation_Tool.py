import arcpy

# Set the paths to the feature classes (generic paths for sharing)
centerline_fc = r"Path_to_Your_Geodatabase\Roads_Line"
polygon_fc = r"Path_to_Your_Geodatabase\Roads"

# Set the workspace (generic path)
arcpy.env.workspace = r"Path_to_Your_Geodatabase"

# Create feature layers from the centerline and polygon features
arcpy.MakeFeatureLayer_management(centerline_fc, "centerline_lyr")
arcpy.MakeFeatureLayer_management(polygon_fc, "polygon_lyr")

# Step 1: Check if the centerline falls outside the polygon
arcpy.SelectLayerByLocation_management(
    "centerline_lyr", "INTERSECT", "polygon_lyr", invert_spatial_relationship=True
)
outside_count = int(arcpy.GetCount_management("centerline_lyr")[0])

# If there are any centerlines outside the polygons, these are "Not accepted"
if outside_count > 0:
    print(f"There are {outside_count} centerline(s) that fall outside the road polygons - Not accepted.")
    # Optionally export these for further analysis (generic path)
    arcpy.CopyFeatures_management("centerline_lyr", r"Path_to_Your_Geodatabase\Roads_Line_Outside")
else:
    print("All centerlines are within the road polygons.")

    # Step 2: Check how well the centerline follows the shape of the polygon

    # Calculate the length of the centerline and the length of the line's portion within the polygon
    arcpy.AddGeometryAttributes_management("centerline_lyr", "LENGTH", "KILOMETERS")
    arcpy.SelectLayerByLocation_management("centerline_lyr", "WITHIN", "polygon_lyr")
    arcpy.AddGeometryAttributes_management("centerline_lyr", "LENGTH", "KILOMETERS")
    
    with arcpy.da.SearchCursor("centerline_lyr", ["SHAPE@LENGTH"]) as cursor:
        for row in cursor:
            centerline_length = row[0]
    
    # Buffer the polygon slightly to account for acceptable deviations
    buffer_distance = "5 Meters"  # Adjust the buffer distance as needed
    buffered_polygon = arcpy.Buffer_analysis(polygon_fc, "in_memory/buffered_polygon", buffer_distance)
    
    arcpy.SelectLayerByLocation_management(
        "centerline_lyr", "WITHIN", buffered_polygon
    )
    buffered_length = 0
    with arcpy.da.SearchCursor("centerline_lyr", ["SHAPE@LENGTH"]) as cursor:
        for row in cursor:
            buffered_length += row[0]

    if buffered_length == centerline_length:
        print("All centerlines fall inside the real-world object and follow the shape faithfully - Accepted.")
    elif buffered_length < centerline_length and buffered_length > 0:
        print("The centerline falls inside the real-world object, but does not follow the shape faithfully - Not accepted.")
    else:
        print("The centerline falls inside the real-world object and, while it does not follow the exact centerline, it is acceptable - Accepted.")
