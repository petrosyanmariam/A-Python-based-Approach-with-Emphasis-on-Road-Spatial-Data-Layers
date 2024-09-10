import arcpy

# Set the path to the feature class (road centerlines)
link_fc = r"Path_to_Your_Geodatabase\Roads_Line"

# Set the workspace (generic path for sharing)
arcpy.env.workspace = r"Path_to_Your_Geodatabase"

# Set the connectivity tolerance (in meters)
connectivity_tolerance = 5.0  # Adjust as necessary

# Create a feature layer from the road centerlines
arcpy.MakeFeatureLayer_management(link_fc, "link_lyr")

# Function to check the distance between two points
def check_distance(point1, point2):
    point_geom1 = arcpy.PointGeometry(point1)
    point_geom2 = arcpy.PointGeometry(point2)
    return point_geom1.distanceTo(point_geom2)

# Function to evaluate the connectivity cases
def evaluate_connectivity(link_ends):
    distances = [check_distance(link_ends[i], link_ends[j]) for i in range(len(link_ends)) for j in range(i+1, len(link_ends))]
    
    # Case 1: Perfect case where all share the same coordinates
    if all(dist == 0 for dist in distances):
        return "Perfect case where all link ends share the same coordinates."
    
    # Case 2: All link ends are within the connectivity tolerance
    if all(dist <= connectivity_tolerance for dist in distances):
        if len(set(distances)) == 1:
            return "All link ends are within the connectivity tolerance - Perfect Case."
        else:
            return "All link ends are within the connectivity tolerance."
    
    # Case 3: One link end lies within the tolerance from one link end but greater from others
    for i, dist1 in enumerate(distances):
        for j, dist2 in enumerate(distances):
            if i != j and dist1 <= connectivity_tolerance and dist2 > connectivity_tolerance:
                return "Link end lies within a distance of less than the connectivity tolerance from another link end, but greater from others."
    
    # Case 4: One link end is not connected (dangle)
    if any(dist > connectivity_tolerance for dist in distances):
        return "One link end is at a distance greater than the tolerance from all other link ends. It will be considered not connected (dangle)."

    return "Undefined case."

# Iterate through each link and assess the connectivity at its endpoints
with arcpy.da.SearchCursor("link_lyr", ["SHAPE@"]) as link_cursor:
    for link_row in link_cursor:
        # Get the start and end points of the link (line)
        link_start = link_row[0].firstPoint
        link_end = link_row[0].lastPoint
        
        # Assuming there are other links that share endpoints, we will collect those points
        link_ends = [link_start, link_end]
        
        # Select other links that share the same endpoints
        arcpy.SelectLayerByLocation_management("link_lyr", "INTERSECT", link_row[0], selection_type="NEW_SELECTION")
        
        with arcpy.da.SearchCursor("link_lyr", ["SHAPE@"]) as intersect_cursor:
            for intersect_row in intersect_cursor:
                # Add the endpoints of intersecting links
                intersect_start = intersect_row[0].firstPoint
                intersect_end = intersect_row[0].lastPoint
                if intersect_start not in link_ends:
                    link_ends.append(intersect_start)
                if intersect_end not in link_ends:
                    link_ends.append(intersect_end)
        
        # Evaluate connectivity
        if len(link_ends) >= 2:
            result = evaluate_connectivity(link_ends)
            print(result)
