import numpy as np
import re
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
from shapely.geometry import Point,Polygon, box
from shapely.vectorized import contains
import osmnx as ox
from rasterio.warp import reproject
from rasterio.warp import Resampling
import rioxarray
import geopy.distance
import rasterio
import geopandas
import rioxarray
from rasterio.transform import Affine
from rasterio.warp import reproject
from rasterio.warp import Resampling
from osgeo import gdal
import tempfile
import os
import signal
from shapely.geometry import Point, MultiPoint
from geopy.distance import geodesic
import numpy as np
names = globals()

def count_edge(vertices, edge_orientations, edge_lengths, resolution):
    """
    Calculate the orientation and length of edges in a polygon.

    Parameters
    ----------
    vertices : ndarray
        List of vertex coordinates.
    edge_orientations : list
        List to store edge orientations (angles).
    edge_lengths : list
        List to store edge lengths.
    resolution : float
        Scaling factor for edge length.

    Returns
    -------
    edge_orientations : list
        Updated list of edge orientations.
    edge_lengths : list
        Updated list of edge lengths.
    """
    deltas = np.diff(vertices, axis=0)
    angles = np.rad2deg(np.arctan2(deltas[:, 1], deltas[:, 0] + 1e-10))
    distances = np.linalg.norm(deltas, axis=1) * resolution
    edge_orientations.extend(angles.tolist())
    edge_lengths.extend(distances.tolist())
    return edge_orientations, edge_lengths


def cal_entropy(edge_orientations, edge_lengths):
    """
    Calculate entropy based on edge orientations and lengths.

    Parameters
    ----------
    edge_orientations : list
        List of edge orientations (angles).
    edge_lengths : list
        List of edge lengths.

    Returns
    -------
    angle_groups : ndarray
        Unique angle groups (in radians).
    weighted_lengths : ndarray
        Total lengths associated with each angle group.
    """
    rounded_angles = np.zeros(np.shape(edge_orientations)[0])

    # Group angles by rounding to the nearest 10 degrees
    for i in range(np.shape(edge_orientations)[0]):
        rounded_angles[i] = np.round(edge_orientations[i] / 10) * 10

    # Sort angles and lengths together
    sorted_angles, sorted_lengths = zip(*sorted(zip(rounded_angles.flatten(), np.array(edge_lengths).flatten())))

    weighted_lengths = np.zeros(np.unique(rounded_angles).size)
    current_index = 0
    group_index = 0

    # Aggregate lengths for each group of angles
    while current_index < rounded_angles.size - 1:
        if sorted_angles[current_index] == sorted_angles[current_index + 1]:
            weighted_lengths[group_index] += sorted_lengths[current_index]
            current_index += 1
        else:
            weighted_lengths[group_index] += sorted_lengths[current_index]
            current_index += 1
            group_index += 1
    weighted_lengths[group_index] += sorted_lengths[-1]

    unique_angles = np.unique(rounded_angles)

    # Handle merging of angles -90 and 90 if present
    if (unique_angles[0] == -90) and (unique_angles[-1] == 90):

        # Combine data for -90 and 90 degrees
        weighted_lengths[-1] += weighted_lengths[0]
        weighted_lengths = np.delete(weighted_lengths, 0)
        unique_angles = np.delete(unique_angles, 0)

    # Convert angles to radians for polar plots
    angle_groups = np.deg2rad(unique_angles)
    return angle_groups, weighted_lengths

def cal_lp(topography):
    """
    Calculate the proportion of land in the given topography matrix.

    Parameters
    ----------
    topography : ndarray
        2D topography matrix.

    Returns
    -------
    float
        Proportion of land/building area.
    """
    return np.count_nonzero(topography) / topography.size


def cal_lf(domain, grid_spacing):
    """
    Calculate land fraction.

    Parameters
    ----------
    domain : ndarray
        2D domain matrix.
    grid_spacing : float
        Grid spacing.

    Returns
    -------
    float
        Land fraction.
    """
    total_fraction = 0

    for row in domain:
        non_zero_indices = np.nonzero(row)[0]
        if non_zero_indices.size > 0:
            contiguous_sections = []
            start_idx = non_zero_indices[0]

            for i in range(len(non_zero_indices) - 1):
                if non_zero_indices[i] + 1 != non_zero_indices[i + 1]:
                    contiguous_sections.append(row[start_idx:non_zero_indices[i] + 1])
                    start_idx = non_zero_indices[i + 1]
            contiguous_sections.append(row[start_idx:non_zero_indices[-1] + 1])  # Add the last section

            for section in contiguous_sections:
                total_fraction += np.max(section)

    return total_fraction * grid_spacing / (domain.size * grid_spacing**2)


def cal_lw(domain, grid_spacing):
    """
    Calculate land width.

    Parameters
    ----------
    domain : ndarray
        2D domain matrix.
    grid_spacing : float
        Grid spacing.

    Returns
    -------
    float
        Land width.
    """
    domain_with_nan = np.where(domain != 0, domain, np.nan)
    return (Lw(domain_with_nan, grid_spacing) +
            Lw(domain_with_nan.T, grid_spacing)) / (domain_with_nan.size * grid_spacing**2)


def cal_alignness(domain):
    """
    Calculate alignness of streets based on empty space.

    Parameters
    ----------
    domain : ndarray
        2D domain matrix.

    Returns
    -------
    alignness : float
        Mean alignness normalized by domain width.
    row_alignness : ndarray
        Array of alignness values for each row.
    """
    row_alignness = np.zeros(domain.shape[0])

    for row_idx, row in enumerate(domain):
        empty_indices = np.where(row == 0)[0]
        if empty_indices.size == 0:
            row_alignness[row_idx] = domain.shape[1]  # Entire row is empty
            continue

        boundary_condition = (empty_indices[0] == 0 and
                              empty_indices[-1] == domain.shape[1] - 1)
        longest_empty = 0
        start_idx = empty_indices[0]

        for i in range(len(empty_indices) - 1):
            if empty_indices[i] + 1 != empty_indices[i + 1]:
                longest_empty = max(longest_empty, empty_indices[i] - start_idx + 1)
                start_idx = empty_indices[i + 1]

        # Check the last stretch
        longest_empty = max(longest_empty, empty_indices[-1] - start_idx + 1)

        if boundary_condition:
            longest_empty = max(longest_empty, empty_indices[-1] - start_idx + 1 + empty_indices[0])

        row_alignness[row_idx] = longest_empty

    alignness = np.round(row_alignness.mean() / domain.shape[1], 4)
    return alignness, row_alignness / domain.shape[1]


def Lw(topography, grid_spacing):
    """
    Calculate total pressure on windward and leeward faces.

    Parameters
    ----------
    topography : ndarray
        2D topography matrix with empty spaces as NaN.
    grid_spacing : float
        Grid spacing.

    Returns
    -------
    float
        Total pressure on windward and leeward faces.
    """
    windward_faces, leeward_faces = [], []

    for column_idx in range(topography.shape[1]):
        front_faces = []
        back_faces = []

        for row_idx in range(1, topography.shape[0] - 1):
            if np.isnan(topography[row_idx, column_idx]):
                if not np.isnan(topography[row_idx - 1, column_idx]):  # Windward face
                    front_faces.append(topography[row_idx - 1, column_idx])
                if not np.isnan(topography[row_idx + 1, column_idx]):  # Leeward face
                    back_faces.append(topography[row_idx + 1, column_idx])

        windward_faces.extend(front_faces)
        leeward_faces.extend(back_faces)

    total_pressure = np.nansum(np.array(windward_faces) + np.array(leeward_faces))
    return total_pressure * grid_spacing

def extract_domain(resolution, default_height, bounding_box, output_name, rotation_angle):
    """
    Main function for extracting domain data.
    """
    res_x = resolution
    res_y = resolution
    default_height = default_height

    # Convert bounding box to format that OSM can read and download the building footprint as GeoDataFrame
    bbox_processed, bbox_coordinates = topo.select_region(bounding_box)

    # Download data from OSM with bounding box as input
    gdf = ox.geometries_from_bbox(
        bbox_coordinates[0], bbox_coordinates[1], bbox_coordinates[2], bbox_coordinates[3], {"building": True}
    )

    gdf.reset_index(level=0, inplace=True)

    # Extract the geometry and building levels
    geometries = gdf['geometry'].values

    # Extract and process the building height (can be "building levels" or "height")
    try:
        building_heights = gdf['height'].values
        building_heights = np.array([float(value) for value in building_heights])
    except:
        building_heights = np.zeros(geometries.size)

    try:
        building_levels = gdf['building:levels'].values
        building_levels = np.array([float(value) for value in building_levels]) * 3
    except:
        building_levels = np.zeros(geometries.size)

    # Calculate the centroid of each urban structure
    centroids = []
    for index in range(geometries.shape[0]):
        centroids.append(geometries[index].centroid)
    data = {'geometry': geometries, 'centroid': centroids}

    # Reproduce the DataFrame with centroids
    gdf = pd.DataFrame(data)

    x_multiplier, y_multiplier = topo.projection(bbox_coordinates, res_x, res_y)

    domain_original, domain_rotated, gdf, x_start, y_start = initialize(
        bbox_processed, gdf, x_multiplier, y_multiplier, bbox_coordinates, rotation_angle
    )

    edge_orientations = []  # Edge orientation
    edge_lengths = []  # Edge length
    total_area = []  # Total area
    realistic_area = []  # Area with realistic building height

    for polygon_idx in range(gdf.shape[0]):  # If centroid of the structure falls within the bounding box
        if Point(gdf['centroid'][polygon_idx][0][0], gdf['centroid'][polygon_idx][1][0]).within(Polygon(bbox_processed)):
            domain_rotated, realistic_area, total_area = process_building(
                edge_orientations, edge_lengths, domain_original, domain_rotated, polygon_idx, gdf, building_levels,
                building_heights, x_multiplier, y_multiplier, x_start, y_start, bbox_coordinates, default_height,
                total_area, realistic_area, resolution, rotation_angle
            )

    angle, weighted_values = cal_entropy(edge_orientations, edge_lengths)
    print_domain(domain_rotated)
    alignment_entropy = print_entropy(angle, weighted_values)
    print_results(alignment_entropy, domain_rotated, total_area, realistic_area, default_height)

    showDiagram(domain_rotated, angle, weighted_values, alignment_entropy, rotation_angle, np.array(total_area), output_name)

    return domain_rotated


def extract_domainKML(resolution, default_height, bounding_box, output_name, rotation_angle, extra_geometric_stats):
    res_x = resolution
    res_y = resolution
    default_height = default_height

    # Bounding box coordinates
    ymin = np.min([sum(bounding_box, [])[0], sum(bounding_box, [])[2], sum(bounding_box, [])[4], sum(bounding_box, [])[6]])
    ymax = np.max([sum(bounding_box, [])[0], sum(bounding_box, [])[2], sum(bounding_box, [])[4], sum(bounding_box, [])[6]])
    xmin = np.min([sum(bounding_box, [])[1], sum(bounding_box, [])[3], sum(bounding_box, [])[5], sum(bounding_box, [])[7]])
    xmax = np.max([sum(bounding_box, [])[1], sum(bounding_box, [])[3], sum(bounding_box, [])[5], sum(bounding_box, [])[7]])
    bbox_coordinates = np.array([xmax, xmin, ymin, ymax])

    # Download data from OSM with bounding box as input
    gdf = ox.geometries_from_bbox(
        bbox_coordinates[0], bbox_coordinates[1], bbox_coordinates[2], bbox_coordinates[3], {"building": True}
    )

    gdf.reset_index(level=0, inplace=True)

    # Extract the geometry and building levels
    geometries = gdf['geometry'].values

    # Extract and process the building height (can be "building levels" or "height")
    try:
        building_heights = gdf['height'].values
        building_heights = np.array([float(value) for value in building_heights])
    except:
        building_heights = np.zeros(geometries.size)

    try:
        building_levels = gdf['building:levels'].values
        building_levels = np.array([float(value) for value in building_levels]) * 3
    except:
        building_levels = np.zeros(geometries.size)

    # Calculate the centroid of each urban structure
    centroids = []
    for index in range(geometries.shape[0]):
        centroids.append(geometries[index].centroid)
    data = {'geometry': geometries, 'cent': centroids}  # Restored to 'cent'

    # Reproduce the DataFrame with centroids
    gdf = pd.DataFrame(data)

    x_multiplier, y_multiplier = projection(bbox_coordinates, res_x, res_y)

    domain_original, domain_rotated, gdf, x_start, y_start = initialize(
        bounding_box, gdf, x_multiplier, y_multiplier, bbox_coordinates, rotation_angle
    )

    edge_orientations = []  # Edge orientation
    edge_lengths = []  # Edge length
    total_area = []  # Total area
    realistic_area = []  # Area with realistic building height

    for polygon_idx in range(gdf.shape[0]):  # If centroid of the structure falls within the bounding box
        if Point(gdf['cent'][polygon_idx][0][0], gdf['cent'][polygon_idx][1][0]).within(Polygon(bounding_box)):
            domain_rotated, realistic_area, total_area = process_building(
                edge_orientations, edge_lengths, domain_original, domain_rotated, polygon_idx, gdf, building_levels,
                building_heights, x_multiplier, y_multiplier, x_start, y_start, bbox_coordinates, default_height,
                total_area, realistic_area, resolution, rotation_angle
            )

    print_domain(domain_rotated)

    if (extra_geometric_stats): 
        angle, weighted_values = cal_entropy(edge_orientations, edge_lengths)
        alignment_entropy = print_entropy(angle, weighted_values)
        print_results(alignment_entropy, domain_rotated, total_area, realistic_area, default_height)
        showDiagram(domain_rotated, angle, weighted_values, alignment_entropy, rotation_angle, np.array(total_area), output_name)

    return domain_rotated


def extract_domain_from_KML_wsf3d(bounding_box, resolution, bldH, output_name, angleRotate, extra_geometric_stats):
    """
    Extracts and processes building height data from WSF3D raster using KML geometries.

    Args:
        kml_file (str): Path to the KML file.
        resolution (float): Grid resolution for domain processing.
        default_height (float): Default building height when no data is available.
        output_name (str): Output file name prefix for saving results.
        rotation_angle (float): Angle for rotating the domain grid.

    Outputs:
        - Saves domain visualization and outputs.
    """
    try:    
        high_res = cal_maxmin(bounding_box)  # high res
        
        WSF3D = 'WSF3D_V02_BuildingHeight.tif'
        angleRotate = 0
        bldH = 16
        resx, resy, res = resolution, resolution, resolution

        # Bounding box coordinates
        ymin = np.min([sum(bounding_box, [])[0], sum(bounding_box, [])[2], sum(bounding_box, [])[4], sum(bounding_box, [])[6]])
        ymax = np.max([sum(bounding_box, [])[0], sum(bounding_box, [])[2], sum(bounding_box, [])[4], sum(bounding_box, [])[6]])
        xmin = np.min([sum(bounding_box, [])[1], sum(bounding_box, [])[3], sum(bounding_box, [])[5], sum(bounding_box, [])[7]])
        xmax = np.max([sum(bounding_box, [])[1], sum(bounding_box, [])[3], sum(bounding_box, [])[5], sum(bounding_box, [])[7]])
        bbox_coordinates = np.array([xmax, xmin, ymin, ymax])

        # Download data from OSM with bounding box as input
        gdf = ox.geometries_from_bbox(
            bbox_coordinates[0], bbox_coordinates[1], bbox_coordinates[2], bbox_coordinates[3], {"building": True}
        )
        gdf_ = ox.geometries_from_bbox(
            bbox_coordinates[0], bbox_coordinates[1], bbox_coordinates[2], bbox_coordinates[3], {"building": True}
        )

        gdf.reset_index(level=0, inplace=True)

        # Extract the geometry and building levels
        geom = gdf['geometry'].values
    
        # Extract and process the building height (can be "building levels" or "height")
        try:
            building_heights = gdf['height'].values
            building_heights = np.array([float(value) for value in building_heights])
        except:
            building_heights = np.zeros(geom.size)
    
        try:
            building_levels = gdf['building:levels'].values
            building_levels = np.array([float(value) for value in building_levels]) * 3
        except:
            building_levels = np.zeros(geom.size)

        high_res = gdal.Open('output.tif')
        HHmean = high_res.ReadAsArray()
        HHmean = HHmean.astype(np.float32) / 10
        HHmean[HHmean <= 0] = np.nan
        HHmean = np.nanmean(HHmean)

        centroid = []
        for idxP in range(geom.shape[0]):
            centroid.append(geom[idxP].centroid)
        data = {'geometry': geom, 'cent': centroid}

        gdf = pd.DataFrame(data)

        x_mul, y_mul = projection(bbox_coordinates, resx, resy)

        domain1, domain, gdf, x_start, y_start = initialize(bounding_box, gdf, x_mul, y_mul, bbox_coordinates, angleRotate)

        lineO = []
        lineL = []
        area = []
        areaH = []

        for idxP in range(gdf.shape[0]):
            if Point(gdf['cent'][idxP][0][0], gdf['cent'][idxP][1][0]).within(Polygon(bounding_box)):
                nx = []
                ny = []
                xy = []
                Pol = []

                for i in range(np.shape(gdf['geometry'][idxP])[1]):
                    xb = int(np.round((gdf['geometry'][idxP][0][i] - bbox_coordinates[1]) * x_mul)) - x_start
                    yb = int(np.round((gdf['geometry'][idxP][1][i] - bbox_coordinates[2]) * y_mul)) - y_start

                    xx, yy, _ = rotateS(xb, yb, domain1, angleRotate)

                    nx.append(xx + x_start)
                    ny.append(yy + y_start)
                    xy.append([xx + x_start, yy + y_start])
                    Pol.append((xx, yy))

                [lineO, lineL] = count_edge(xy, lineO, lineL, res)

                pol = Polygon(Pol)
                area.append(pol.area)

                building_levels[np.isnan(building_levels)] = 0
                building_heights[np.isnan(building_heights)] = 0

                if building_heights[idxP] == 0:
                    if building_levels[idxP] == 0:
                        HH = bldH
                    else:
                        HH = float(building_levels[idxP])
                        areaH.append(pol.area)
                else:
                    HH = float(building_heights[idxP])
                    areaH.append(pol.area)

                try:
                    a = gdf_['geometry'].values[idxP].bounds
                    single_high = gdal.Translate('new.tif', high_res, projWin=[a[0], a[3], a[2], a[1]]).ReadAsArray()
                    single_high = single_high.astype(np.float32) / 10
                    single_high[single_high <= 0] = np.nan
                    HH = np.nanmean(single_high)
                    if np.isnan(HH):
                        HH = HHmean
                except:
                    HH = HHmean
                    
                domain = construct(domain, HH, nx, ny, x_start, y_start, pol)
            
        print_domain(domain)
        
    finally:
        if high_res:
            high_res = None

def initialize(bounding_box, data_frame, x_multiplier, y_multiplier, bounding_box_coordinates, rotation_angle):
    """
    Initialize the computational domain.

    Parameters
    ----------
    bounding_box : ndarray
        Bounding box coordinates.
    data_frame : DataFrame
        DataFrame containing geometry and centroid data.
    x_multiplier, y_multiplier : float
        Multipliers to convert latitude/longitude to x/y.
    bounding_box_coordinates : list
        Bounding box limits [y_max, y_min, x_min, x_max].
    rotation_angle : float
        Rotation angle in degrees.

    Returns
    -------
    domain_original : ndarray
        Domain containing the topography before rotation.
    domain_rotated : ndarray
        Domain containing the topography after rotation.
    updated_data_frame : DataFrame
        DataFrame with geometry and centroids converted to x/y coordinates.
    min_x, min_y : int
        Minimum x and y values after conversion.
    """
    geometry_dict = {}
    i = 0
    x_min = bounding_box_coordinates[1]
    y_min = bounding_box_coordinates[2]

    # Extract geometry and centroids
    for polygon_idx in range(data_frame.shape[0]):
        try:
            geometry_dict[i] = {
                'geometry': data_frame['geometry'][polygon_idx].exterior.coords.xy,
                'cent': data_frame['cent'][polygon_idx].coords.xy  # Restored to 'cent'
            }
            i += 1
        except:
            pass

    updated_data_frame = pd.DataFrame.from_dict(geometry_dict, "index")

    # Convert lat/long to x/y 2D empty domain
    bounding_box_converted = np.zeros(np.shape(bounding_box))
    x_coords = []
    y_coords = []

    for i in range(np.shape(bounding_box)[0]):
        bounding_box_converted[i][0] = int(np.round((bounding_box[i][0] - x_min) * x_multiplier))
        bounding_box_converted[i][1] = int(np.round((bounding_box[i][1] - y_min) * y_multiplier))
        x_coords.append(int(np.round((bounding_box[i][0] - x_min) * x_multiplier)))
        y_coords.append(int(np.round((bounding_box[i][1] - y_min) * y_multiplier)))

    domain_original = np.zeros([np.max(x_coords) - np.min(x_coords), np.max(y_coords) - np.min(y_coords)])
    _, _, domain_rotated = rotateS(0, 0, domain_original, rotation_angle)

    return domain_original, domain_rotated, updated_data_frame, np.min(x_coords), np.min(y_coords)


def process_building(edge_orientations, edge_lengths, domain_original, domain_rotated, polygon_idx, geometry_data_frame, 
                     building_height_low, building_height_high, x_multiplier, y_multiplier, x_offset, y_offset, 
                     bounding_box_coordinates, default_height, building_areas, real_building_areas, resolution, rotation_angle):
    """
    Process a building to project its geometry onto the computational domain.

    Parameters
    ----------
    edge_orientations, edge_lengths : list
        Lists of edge orientations and lengths.
    domain_original, domain_rotated : ndarray
        Domains before and after rotation.
    polygon_idx : int
        Index of the polygon to process.
    geometry_data_frame : DataFrame
        DataFrame containing geometry data.
    building_height_low, building_height_high : ndarray
        Arrays of low and high building heights.
    x_multiplier, y_multiplier : float
        Multipliers to convert lat/long to x/y.
    x_offset, y_offset : int
        Offsets for x and y coordinates.
    bounding_box_coordinates : list
        Bounding box limits.
    default_height : float
        Default height of the buildings.
    building_areas, real_building_areas : list
        Lists of building areas and real building areas.
    resolution : float
        Resolution of the computational domain.
    rotation_angle : float
        Rotation angle in degrees.

    Returns
    -------
    domain_rotated : ndarray
        Updated rotated domain.
    real_building_areas, building_areas : list
        Updated lists of real building areas and total building areas.
    """
    x_coordinates = []
    y_coordinates = []
    projected_points = []
    polygon_points = []

    # Project points from geometry
    for vertex_idx in range(np.shape(geometry_data_frame['geometry'][polygon_idx])[1]):
        x_projected = int(np.round((geometry_data_frame['geometry'][polygon_idx][0][vertex_idx] - bounding_box_coordinates[1]) * x_multiplier)) - x_offset
        y_projected = int(np.round((geometry_data_frame['geometry'][polygon_idx][1][vertex_idx] - bounding_box_coordinates[2]) * y_multiplier)) - y_offset

        x_rotated, y_rotated, _ = rotateS(x_projected, y_projected, domain_original, rotation_angle)

        x_coordinates.append(x_rotated + x_offset)
        y_coordinates.append(y_rotated + y_offset)
        projected_points.append([x_rotated + x_offset, y_rotated + y_offset])
        polygon_points.append((x_rotated, y_rotated))

    # Count edges
    edge_orientations, edge_lengths = count_edge(projected_points, edge_orientations, edge_lengths, resolution)

    polygon = Polygon(polygon_points)
    building_areas.append(polygon.area)

    # Replace NaN values with 0
    building_height_low[np.isnan(building_height_low)] = 0
    building_height_high[np.isnan(building_height_high)] = 0

    # Determine building height
    if building_height_high[polygon_idx] == 0:
        if building_height_low[polygon_idx] == 0:
            height = default_height
        else:
            height = float(building_height_low[polygon_idx])
            real_building_areas.append(polygon.area)
    else:
        height = float(building_height_high[polygon_idx])
        real_building_areas.append(polygon.area)

    # Update domain with building height
    domain_rotated = construct(domain_rotated, height, x_coordinates, y_coordinates, x_offset, y_offset, polygon)

    return domain_rotated, real_building_areas, building_areas


def construct(domain, building_height, x_coords, y_coords, x_offset, y_offset, polygon):
    """
    Construct the computational domain by filling it with the building height.

    Parameters
    ----------
    domain : ndarray
        Computational domain.
    building_height : float
        Height of the building.
    x_coords, y_coords : list
        Lists of x and y coordinates of the building vertices.
    x_offset, y_offset : int
        Offsets for x and y coordinates.
    polygon : Polygon
        Polygon representing the building.

    Returns
    -------
    domain : ndarray
        Updated computational domain.
    """
    x_min = np.min(x_coords) - x_offset
    x_max = np.max(x_coords) - x_offset
    y_min = np.min(y_coords) - y_offset
    y_max = np.max(y_coords) - y_offset

    # Fill the interior of the polygon with the building height
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            point = Point(x, y)
            if point.within(polygon) or point.intersects(polygon):
                try:
                    domain[x, y] = building_height
                except:
                    continue
    return domain


xtick_font = {
    "family": "DejaVu Sans",
    "size": 10,
    "weight": "bold",
    "alpha": 1.0,
    "zorder": 3,
}

color="#003366"
edgecolor="k"
linewidth=0.5
alpha=0.7


def print_domain(domain):
    """
    Plot the computational domain and save it as a PDF file.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    image = ax.imshow(domain)
    colorbar = plt.colorbar(image)
    colorbar.set_label('Estimated building height [m]')
    plt.tight_layout()
    plt.savefig('domain.pdf')


def print_entropy(angles, radii):
    """
    Plot entropy in a polar plot and compute the alignment entropy coefficient.

    Parameters
    ----------
    angles : array-like
        Angles in radians for the polar plot.
    radii : array-like
        Values corresponding to each angle.

    Returns
    -------
    phi : float
        Alignment entropy coefficient (phi).
    """
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": "polar"})

    ax.set_theta_zero_location("N")
    ax.set_theta_direction("clockwise")
    ax.set_ylim(top=radii.max())

    # Configure the y-ticks and remove their labels
    ax.set_yticks(np.linspace(0, radii.max(), 5))
    ax.set_yticklabels(labels="")

    # Configure the x-ticks and their labels
    direction_labels = ["N", "", "E", "", "S", "", "W", ""]
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(labels=direction_labels)
    ax.tick_params(axis="x", which="major", pad=-2)

    ax.bar(
        angles,
        height=radii,
        width=0.1,
        align="center",
        bottom=0,
        zorder=2,
        color="#003366",
        edgecolor="k",
        linewidth=0.5,
        alpha=0.7,
    )
    ax.set_thetamin(-90)
    ax.set_thetamax(90)
    plt.tight_layout()
    plt.savefig('polarO.png', dpi=300)

    # Entropy calculations
    evenly_distributed_min = 2  # Edge evenly distributed to just 2 orientations
    h_min = 1 / evenly_distributed_min * np.log(1 / evenly_distributed_min) * evenly_distributed_min

    evenly_distributed_max = 18  # Edge evenly distributed to all 18 orientations
    h_max = 1 / evenly_distributed_max * np.log(1 / evenly_distributed_max) * evenly_distributed_max

    weighted_entropy = np.nansum(radii / sum(radii) * np.log(radii / sum(radii)))
    phi = 1 - (h_max - weighted_entropy) / (h_max - h_min)

    return phi


def print_results(phi, domain, building_areas, real_building_areas, default_building_height):
    """
    Display results including entropy, rasterization error, and building height recognition.

    Parameters
    ----------
    phi : float
        Alignment entropy coefficient (phi).
    domain : ndarray
        Computational domain.
    building_areas : list
        Areas of the buildings.
    real_building_areas : list
        Areas of the buildings with real heights.
    default_building_height : float
        Default building height used in the domain.
    """
    print('$\\phi=$' + str(phi))
    print(domain.shape)
    print('Rasterization error = ' +
          str((cal_lp(domain) - np.array(building_areas).sum() / domain.size) / cal_lp(domain) * 100)[:4] + '%')
    print('{}% real building height recognized, the rest is set to {} m'.format(
        str(np.array(real_building_areas).sum() / np.array(building_areas).sum() * 100)[:4], default_building_height))
    return ()


def showDiagram(domain, edge_angles, edge_weights, phi, rotation_angle, building_areas, output_name):
    """
    Plot diagrams for computational domain, edge orientations, and alignmentness.

    Parameters
    ----------
    domain : ndarray
        Computational domain.
    edge_angles : array-like
        Edge orientation angles.
    edge_weights : array-like
        Weights of edge orientations.
    phi : float
        Alignment entropy coefficient (phi).
    rotation_angle : float
        Rotation angle of the domain.
    building_areas : list
        Areas of the buildings.
    output_name : str
        Output filename prefix.
    """
    output_directory = ''
    fig = plt.figure(figsize=(12, 6))

    # Plot computational domain
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.contourf(domain)
    ax1.axis('equal')

    lambda_p = cal_lp(domain)
    scalar_value = (1 - lambda_p) * 0.001

    ax1.set_title('Computational domain ' + '$\\lambda_p$ = ' + str(lambda_p)[0:6] + '\n' + output_name +
                  ' Domain size = ' + str(domain.shape))

    np.savetxt(output_directory + output_name + '_topo', domain, fmt='%d')

    # Plot contours
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.contour(domain, linewidths=0.1, colors='r')
    ax2.axis('equal')
    ax2.set_title('Top sink of scalar = 1e-7*' + str(scalar_value)[5:9])

    # Plot edge orientations
    ax3 = fig.add_subplot(133, polar=True)

    xtick_font_config = {
        "family": "DejaVu Sans",
        "size": 15,
        "weight": "bold",
        "alpha": 1.0,
        "zorder": 3,
    }

    x_angles = np.unique(edge_angles) - rotation_angle
    x_angles = np.deg2rad(x_angles)
    y_weights = np.array(edge_weights)

    x_angles = np.concatenate((x_angles, x_angles + np.pi), axis=0)
    y_weights = np.concatenate((y_weights, y_weights), axis=0)

    ax3.set_theta_zero_location("N")
    ax3.set_theta_direction("clockwise")
    ax3.set_ylim(top=y_weights.max())

    # Configure the y-ticks and remove their labels
    ax3.set_yticks(np.linspace(0, y_weights.max(), 5))
    ax3.set_yticklabels(labels="")

    # Configure the x-ticks and their labels
    orientation_labels = ["N", "", "E", "", "S", "", "W", ""]
    ax3.set_xticks(ax3.get_xticks())
    ax3.set_xticklabels(labels=orientation_labels, fontdict=xtick_font_config)
    ax3.tick_params(axis="x", which="major", pad=-2)

    ax3.bar(
        x_angles,
        height=y_weights,
        width=0.1,
        align="center",
        bottom=0,
        zorder=2,
        color="#003366",
        edgecolor="k",
        linewidth=0.5,
        alpha=0.7,
    )

    gamma, alignment_profile = cal_alignness(domain)

    # Plot alignmentness
    ax4 = fig.add_subplot(8, 3, 24)
    title = 'Orientations of building edges \n Edge entropy $\\phi$ = ' + str(phi)[:6]
    title += '\n Rotation angle = ' + str(rotation_angle) + '$^{\\circ}$'
    title += '\n Average building size $A_0$ = ' + str(building_areas.mean())[:6] + '$m^2$'
    ax3.set_title(title)

    ax4.plot(alignment_profile, c='k')
    ax4.set_xlim(0, domain.shape[0])
    ax4.set_xlabel('Alignedness $\\gamma$ = ' + str(gamma)[0:6])

    plt.tight_layout()
    plt.savefig(output_directory + output_name + '.png', dpi=300)


def Parse_GE(coordinates):
    """
    Parse the longitude/latitude coordinates extracted from GE to osmnx input.
    
    Parameters
    ----------
    coordinates : list
        List of LL coordinates extracted from Google Earth.
    
    Returns
    -------
    parsed_value : float
        Converted coordinate value.
    """
    multiplier = 1 if coordinates[-1] in ['N', 'E'] else -1
    parsed_value = multiplier * sum(float(value) / 60 ** idx for idx, value in enumerate(re.split('°|\'|\"', coordinates[:-2])))
    return parsed_value


def parseKML(file_name):
    """
    Parse a KML file to extract longitude and latitude coordinates.
    
    Parameters
    ----------
    file_name : str
        Path to the KML file.
    
    Returns
    -------
    lat_lon_pairs : list
        List of [longitude, latitude] pairs.
    """
    with open(file_name) as file:
        lines = np.array(file.readlines())
    
    for line_idx in range(lines.size):
        if '<coordinates>\n' in lines[line_idx]:
            coordinates_array = np.array(lines[line_idx + 1].split(','))

    longitude_list, latitude_list = [], []
    for coord_idx in range(np.size(coordinates_array) - 1):
        (longitude_list if coord_idx % 2 == 0 else latitude_list).append(coordinates_array[coord_idx])

    longitude_list[0] = longitude_list[0][6:]  # Strip prefix from the first longitude
    longitude_list = [coord[2:] if idx > 0 else coord for idx, coord in enumerate(longitude_list)]  # Remove prefix for remaining
    
    lat_lon_pairs = [[float(lon), float(lat)] for lon, lat in zip(longitude_list, latitude_list)]
    return lat_lon_pairs


def cal_WGSdist(lon1, lon2, lat1, lat2):
    """
    Calculate real distance of two points with longitude and latitude.
    
    Parameters
    ----------
    lon1, lon2 : float
        Longitude of the two points.
    lat1, lat2 : float
        Latitude of the two points.
    
    Returns
    -------
    distance : float
        Distance in meters.
    """
    earth_radius = 6371  # Earth radius in km
    delta_lon, delta_lat = np.deg2rad(lon2 - lon1), np.deg2rad(lat2 - lat1)

    haversine_formula = np.sin(delta_lat / 2) ** 2 + np.cos(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.sin(delta_lon / 2) ** 2
    central_angle = 2 * np.arctan2(np.sqrt(haversine_formula), np.sqrt(1 - haversine_formula))

    distance = earth_radius * central_angle * 1000  # Convert to meters
    return distance


def shear(angle, x_coord, y_coord):
    """
    Apply shear transformation to coordinates.

    Parameters
    ----------
    angle : float
        Shear angle in radians.
    x_coord, y_coord : int
        Original coordinates.
    
    Returns
    -------
    transformed_y, transformed_x : int
        Transformed coordinates.
    """
    tangent = math.tan(angle / 2)
    transformed_x = round(x_coord - y_coord * tangent)
    transformed_y = y_coord

    # Shear 2
    transformed_y = round(transformed_x * math.sin(angle) + transformed_y)

    # Shear 3
    transformed_x = round(transformed_x - transformed_y * tangent)

    return transformed_y, transformed_x


def rotate(image, angle_degrees):
    """
    Rotate an image by a specified angle.
    
    Parameters
    ----------
    image : ndarray
        Input image array.
    angle_degrees : float
        Angle of rotation in degrees.
    
    Returns
    -------
    rotated_image : ndarray
        Rotated image array.
    """
    angle_radians = math.radians(angle_degrees)
    cosine, sine = math.cos(angle_radians), math.sin(angle_radians)
    height, width = image.shape

    new_height = round(abs(height * cosine) + abs(width * sine)) + 1
    new_width = round(abs(width * cosine) + abs(height * sine)) + 1

    rotated_image = np.zeros((new_height, new_width))
    original_center = ((height - 1) / 2, (width - 1) / 2)
    new_center = ((new_height - 1) / 2, (new_width - 1) / 2)

    for row_idx in range(height):
        for col_idx in range(width):
            y_rel, x_rel = row_idx - original_center[0], col_idx - original_center[1]
            new_y, new_x = shear(angle_radians, x_rel, y_rel)
            new_y += new_center[0]
            new_x += new_center[1]

            if 0 <= new_y < new_height and 0 <= new_x < new_width:
                rotated_image[int(new_y), int(new_x)] = image[row_idx, col_idx]

    plt.imshow(rotated_image)
    plt.axis('equal')
    return rotated_image


def rotateS(x_coord, y_coord, image_map, angle_degrees):
    """
    Rotate coordinates with respect to an image.

    Parameters
    ----------
    x_coord, y_coord : int
        Original coordinates.
    image_map : ndarray
        Input image array.
    angle_degrees : float
        Angle of rotation in degrees.
    
    Returns
    -------
    transformed_y, transformed_x, rotated_image : int, int, ndarray
        Transformed coordinates and rotated image.
    """
    angle_radians = math.radians(angle_degrees)
    cosine, sine = math.cos(angle_radians), math.sin(angle_radians)

    height, width = image_map.shape
    new_height = round(abs(height * cosine) + abs(width * sine)) + 1
    new_width = round(abs(width * cosine) + abs(height * sine)) + 1

    rotated_image = np.zeros([new_height, new_width])
    image_copy = rotated_image.copy()

    original_center_height = round(((height + 1) / 2) - 1)
    original_center_width = round(((width + 1) / 2) - 1)

    new_center_height = round(((new_height + 1) / 2) - 1)
    new_center_width = round(((new_width + 1) / 2) - 1)

    relative_y = image_map.shape[0] - 1 - x_coord - original_center_height
    relative_x = image_map.shape[1] - 1 - y_coord - original_center_width

    transformed_y, transformed_x = shear(angle_radians, relative_x, relative_y)

    transformed_y = new_center_height - transformed_y
    transformed_x = new_center_width - transformed_x

    return transformed_y, transformed_x, rotated_image



def projection(bbox_coordinates, resolution_x, resolution_y):
    """
    Calculate the projection multiplier.

    Parameters
    ----------
    bbox_coordinates : list
        Bounding box coordinates [y_max, y_min, x_min, x_max].
    resolution_x, resolution_y : int
        Resolution in x and y directions.
    
    Returns
    -------
    x_multiplier, y_multiplier : float
        Multipliers in x and y directions.
    """
    y_max, y_min, x_min, x_max = bbox_coordinates
    x_distance = cal_WGSdist(x_min, x_max, y_min, y_min) / resolution_x
    y_distance = cal_WGSdist(x_min, x_min, y_min, y_max) / resolution_y

    x_multiplier = x_distance / (x_max - x_min)
    y_multiplier = y_distance / (y_max - y_min)

    return x_multiplier, y_multiplier



def select_region(bbox_coordinates):
    """
    Project the longitude/latitude coordinates to osmnx input.

    Parameters
    ----------
    bbox_coordinates : list
        List of longitude and latitude coordinates extracted from Google Earth.
    
    Returns
    -------
    bbox_osm : list
        List of projected coordinates.
    bbox_bounds : ndarray
        Array of bounding box values [xmax, xmin, ymin, ymax].
    """
    bbox_osm = [[Parse_GE(coord[1]), Parse_GE(coord[0])] for coord in bbox_coordinates]
    all_coordinates = sum(bbox_osm, [])
    ymin, ymax = np.min(all_coordinates[::2]), np.max(all_coordinates[::2])
    xmin, xmax = np.min(all_coordinates[1::2]), np.max(all_coordinates[1::2])

    bbox_bounds = np.array([xmax, xmin, ymin, ymax])
    return bbox_osm, bbox_bounds



def pressureDefT(topography):
    """
    Identify windward and leeward grids for realistic irregular geometry.

    Parameters
    ----------
    topography : ndarray
        Transposed topography matrix.

    Returns
    -------
    frontal_pressures : ndarray
        Frontal face pressures.
    back_pressures : ndarray
        Back face pressures.
    distances : ndarray
        Distance between paired frontal and back faces.
    """
    def pressureDefPre(topography_matrix):
        """Count frontal and back face samples in the topography."""
        frontal_face_counts = np.zeros(topography_matrix.shape[1])
        back_face_counts = np.zeros(topography_matrix.shape[1])

        for col in range(topography_matrix.shape[1]):
            for row in range(topography_matrix.shape[0]):
                try:
                    if np.isnan(topography_matrix[row, col]) and ~np.isnan(topography_matrix[row - 1, col]):  # Frontal face
                        frontal_face_counts[col] += 1
                    if np.isnan(topography_matrix[row, col]) and ~np.isnan(topography_matrix[row + 1, col]):  # Back face
                        back_face_counts[col] += 1
                except IndexError:
                    pass
        return frontal_face_counts, back_face_counts

    topography = np.transpose(topography)
    frontal_face_counts, back_face_counts = pressureDefPre(topography)

    frontal_pressures, back_pressures, distances = [], [], []
    frontal_overlaps, back_overlaps, overlap_distances = [], [], []
    no_back_first_row, no_back_last_row, both_back_overlap = 0, 0, 0

    for col in range(topography.shape[1]):
        try:
            # Case: No B grid in the first and last rows
            if ~np.isnan(topography[0, col]) and ~np.isnan(topography[-1, col]):
                for row in range(topography.shape[0]):
                    if np.isnan(topography[row, col]) and ~np.isnan(topography[row - 1, col]):  # Frontal face
                        frontal_pressures.append(topography[row - 1, col])
                        temp_row = row
                    if np.isnan(topography[row, col]) and ~np.isnan(topography[row + 1, col]):  # Back face
                        back_pressures.append(topography[row + 1, col])
                        distances.append(row - temp_row + 1)

            # Case: No B grid in the first row but present in the last
            elif ~np.isnan(topography[0, col]) and np.isnan(topography[-1, col]):
                no_back_first_row += 1
                frontal_count = 0
                for row in range(topography.shape[0]):
                    if np.isnan(topography[row, col]) and ~np.isnan(topography[row - 1, col]):  # Frontal face
                        if frontal_count == frontal_face_counts[col] - 1:  # Last frontal face
                            frontal_pressures.append(topography[row - 1, col])
                            back_pressures.append(topography[0, col])
                            distances.append(topography.shape[0] - row)
                        else:
                            frontal_pressures.append(topography[row - 1, col])
                            frontal_count += 1
                            temp_row = row
                    if np.isnan(topography[row, col]) and ~np.isnan(topography[row + 1, col]):  # Back face
                        back_pressures.append(topography[row + 1, col])
                        distances.append(row - temp_row + 1)

            # Case: No B grid in the last row but present in the first
            elif np.isnan(topography[0, col]) and ~np.isnan(topography[-1, col]):
                no_back_last_row += 1
                first = True
                for row in range(topography.shape[0]):
                    if np.isnan(topography[row, col]) and ~np.isnan(topography[row - 1, col]):  # Frontal face
                        frontal_pressures.append(topography[row - 1, col])
                        temp_row = row
                    if np.isnan(topography[row, col]) and ~np.isnan(topography[row + 1, col]):  # Back face
                        if first:
                            back_pressures.append(topography[row + 1, col])
                            distances.append(row)
                            first = False
                        else:
                            back_pressures.append(topography[row + 1, col])
                            distances.append(row - temp_row + 1)

            # Case: B grid present in both the first and last rows
            elif np.isnan(topography[0, col]) and np.isnan(topography[-1, col]):
                both_back_overlap += 1
                frontal_count, first = 0, True
                for row in range(topography.shape[0]):
                    if np.isnan(topography[row, col]) and ~np.isnan(topography[row - 1, col]):  # Frontal face
                        if frontal_count == frontal_face_counts[col] - 1:  # Last frontal face
                            frontal_overlaps.append(topography[row - 1, col])
                            upper_size = topography.shape[0] - row
                        else:
                            frontal_pressures.append(topography[row - 1, col])
                            frontal_count += 1
                            temp_row = row
                for row in range(topography.shape[0]):
                    if np.isnan(topography[row, col]) and ~np.isnan(topography[row + 1, col]):  # Back face
                        if first:
                            back_overlaps.append(topography[row + 1, col])
                            lower_size = row
                            overlap_distances.append(lower_size + upper_size + 1)
                            first = False
                        else:
                            back_pressures.append(topography[row + 1, col])
                            distances.append(row - temp_row + 1)

        except IndexError:
            pass

    frontal_pressures.extend(frontal_overlaps)
    back_pressures.extend(back_overlaps)
    distances.extend(overlap_distances)

    return np.array(frontal_pressures), np.array(back_pressures), np.array(distances)


def cal_maxmin(bbox, output_filename="output.tif"):
    bbox_osm = []
    for i in range(np.shape(bbox)[0]):
        tmp = [bbox[i][1], bbox[i][0]]
        bbox_osm.append(tmp)

    ymin = np.min([sum(bbox_osm, [])[0], sum(bbox_osm, [])[2], sum(bbox_osm, [])[4], sum(bbox_osm, [])[6]])
    ymax = np.max([sum(bbox_osm, [])[0], sum(bbox_osm, [])[2], sum(bbox_osm, [])[4], sum(bbox_osm, [])[6]])
    xmin = np.min([sum(bbox_osm, [])[1], sum(bbox_osm, [])[3], sum(bbox_osm, [])[5], sum(bbox_osm, [])[7]])
    xmax = np.max([sum(bbox_osm, [])[1], sum(bbox_osm, [])[3], sum(bbox_osm, [])[5], sum(bbox_osm, [])[7]])
    bbox_osm_ = np.array([xmax, xmin, ymin, ymax])

    WSF3D = "WSF3D_V02_BuildingHeight.tif"

    factor = 0.0001
    ds = gdal.Open(WSF3D)
    ds = gdal.Translate(
        "new.tif",
        ds,
        projWin=[
            xmin - abs(xmin) * factor,
            ymax + abs(ymax) * factor,
            xmax + abs(xmax) * factor,
            ymin - abs(ymin) * factor,
        ],
    )

    with rasterio.open("new.tif") as dataset:
        profile = dataset.profile.copy()
        upscale_factor = 30 / 1

        data = dataset.read(
            out_shape=(
                dataset.count,
                int(dataset.height * upscale_factor),
                int(dataset.width * upscale_factor),
            ),
            resampling=Resampling.bilinear,
        )

        transform = dataset.transform * dataset.transform.scale(
            (1 / upscale_factor),
            (1 / upscale_factor),
        )

        profile.update(
            {
                "height": data.shape[-2],
                "width": data.shape[-1],
                "transform": transform,
            }
        )

    with rasterio.open(output_filename, "w", **profile) as dataset:
        dataset.write(data)

    with rasterio.open(output_filename) as final_dataset:
        cc = final_dataset.read(1).astype(np.float32) / 10
        cc[cc <= 0] = np.nan


    # Return the processed data
    return cc




def pointRadius45(LL,radius): # input longitude and latitude radius in KM
    # add and subtract on x and y axis to accompish a BBox for 
    Lat,Lon =  LL
    
    
    # raidus m to the east 
    LL1 = geopy.distance.distance(radius).destination((Lat, Lon), bearing=0+45)
    LL2 = geopy.distance.distance(radius).destination((Lat, Lon), bearing=90+45)
    LL3 = geopy.distance.distance(radius).destination((Lat, Lon), bearing=180+45)
    LL4 = geopy.distance.distance(radius).destination((Lat, Lon), bearing=270+45)
    
    bbox = [LL1[::-1][1:],LL2[::-1][1:],LL3[::-1][1:],LL4[::-1][1:]]
    
    
    return(bbox)

def extract_domain_from_points_wsf3d(df, dir_topo="topo", rradius=2):
    high_res = None  # Initialize GDAL resource reference
    num_entries = len(df.iloc[:, 0])
    
    try:
        for idxFF in range(num_entries):
            LL = [df.Lat[idxFF], df.Lon[idxFF]]
            bbox = pointRadius45(LL, rradius)
            bbox
            high_res = cal_maxmin(bbox)  # high res

            WSF3D = 'WSF3D_V02_BuildingHeight.tif'
            angleRotate = 0
            bldH = 16
            resx, resy, res = 1, 1, 1
            bbox_osm = []

            for i in range(np.shape(bbox)[0]):
                tmp = [bbox[i][1], bbox[i][0]]
                bbox_osm.append(tmp)

            ymin = np.min([sum(bbox_osm, [])[0], sum(bbox_osm, [])[2], sum(bbox_osm, [])[4], sum(bbox_osm, [])[6]])
            ymax = np.max([sum(bbox_osm, [])[0], sum(bbox_osm, [])[2], sum(bbox_osm, [])[4], sum(bbox_osm, [])[6]])
            xmin = np.min([sum(bbox_osm, [])[1], sum(bbox_osm, [])[3], sum(bbox_osm, [])[5], sum(bbox_osm, [])[7]])
            xmax = np.max([sum(bbox_osm, [])[1], sum(bbox_osm, [])[3], sum(bbox_osm, [])[5], sum(bbox_osm, [])[7]])
            bbox_osm_ = np.array([ymax, ymin, xmin, xmax])
            bbox_cor = bbox_osm_

            gdf = ox.geometries_from_bbox(bbox_cor[0], bbox_cor[1], bbox_cor[2], bbox_cor[3], {"building": True})
            gdf_ = ox.geometries_from_bbox(bbox_cor[0], bbox_cor[1], bbox_cor[2], bbox_cor[3], {"building": True})
            gdf.reset_index(level=0, inplace=True)

            geom = gdf['geometry'].values
            high_res = gdal.Open('output.tif')

            HHmean = high_res.ReadAsArray()
            HHmean = HHmean.astype(np.float32) / 10
            HHmean[HHmean <= 0] = np.nan
            HHmean = np.nanmean(HHmean)

            try:
                bHeightH = gdf['height'].values
                bHeightH = np.array([float(x) for x in bHeightH])
            except:
                bHeightH = np.zeros(geom.size)

            try:
                bHeightL = gdf['building:levels'].values
                bHeightL = np.array([float(x) for x in bHeightL]) * 3
            except:
                bHeightL = np.zeros(geom.size)

            centroid = []
            for idxP in range(geom.shape[0]):
                centroid.append(geom[idxP].centroid)
            data = {'geometry': geom, 'cent': centroid}

            gdf = pd.DataFrame(data)

            x_mul, y_mul = projection(bbox_cor, resx, resy)

            domain1, domain, gdf, x_start, y_start = initialize(bbox, gdf, x_mul, y_mul, bbox_cor, angleRotate)

            lineO = []
            lineL = []
            area = []
            areaH = []

            for idxP in range(gdf.shape[0]):
                if Point(gdf['cent'][idxP][0][0], gdf['cent'][idxP][1][0]).within(Polygon(bbox)):
                    nx = []
                    ny = []
                    xy = []
                    Pol = []

                    for i in range(np.shape(gdf['geometry'][idxP])[1]):
                        xb = int(np.round((gdf['geometry'][idxP][0][i] - bbox_cor[1]) * x_mul)) - x_start
                        yb = int(np.round((gdf['geometry'][idxP][1][i] - bbox_cor[2]) * y_mul)) - y_start

                        xx, yy, _ = rotateS(xb, yb, domain1, angleRotate)

                        nx.append(xx + x_start)
                        ny.append(yy + y_start)
                        xy.append([xx + x_start, yy + y_start])
                        Pol.append((xx, yy))

                    [lineO, lineL] = count_edge(xy, lineO, lineL, res)

                    pol = Polygon(Pol)
                    area.append(pol.area)

                    bHeightL[np.isnan(bHeightL)] = 0
                    bHeightH[np.isnan(bHeightH)] = 0

                    if bHeightH[idxP] == 0:
                        if bHeightL[idxP] == 0:
                            HH = bldH
                        else:
                            HH = float(bHeightL[idxP])
                            areaH.append(pol.area)
                    else:
                        HH = float(bHeightH[idxP])
                        areaH.append(pol.area)

                    try:
                        a = gdf_['geometry'].values[idxP].bounds
                        single_high = gdal.Translate('new.tif', high_res, projWin=[a[0], a[3], a[2], a[1]]).ReadAsArray()
                        single_high = single_high.astype(np.float32) / 10
                        single_high[single_high <= 0] = np.nan
                        HH = np.nanmean(single_high)
                        if np.isnan(HH):
                            HH = HHmean
                    except:
                        HH = HHmean

                    domain = construct(domain, HH, nx, ny, x_start, y_start, pol)

            t1 = 0
            t2 = 0
            for i in range(domain.shape[0]):
                for j in range(domain.shape[1]):
                    if domain[i, j] != 0:
                        t1 += 1
                        t2 += domain[i, j]

            fig, ax = plt.subplots(figsize=(8, 8))
            im = ax.imshow(domain)
            circle1 = plt.Circle((int(domain.shape[0] / 2), int(domain.shape[0] / 2)), 10, color='r')
            ax.add_patch(circle1)
            ax.set_title('Hmean=' + str(t2 / t1)[:5] + 'm' + ' @ a radius of ' + str(int(rradius * 1000)) + 'm around ' + df.Name[idxFF])
            cb = plt.colorbar(im)
            cb.set_label('Estimated building height from WSF90 [m]')
            plt.tight_layout()

            plt.savefig('domainRaw' + df.Name[idxFF] + str(int(rradius * 1000)) + '45.png', dpi=300)
            os.makedirs(dir_topo, exist_ok=True)
            np.savetxt(dir_topo + df.Name[idxFF] + '45_topo', domain, fmt='%d')
            if high_res:
                high_res = None

    except KeyboardInterrupt:
        print("Process interrupted by user.")
        raise

    finally:
        if high_res:
            high_res = None


def extract_domain_from_points_osm(df, rradius=2):
    """
    Processes OpenStreetMap (OSM) data to extract building information, calculate domains, 
    visualize data, and save outputs.

    Args:
        df (pd.DataFrame): DataFrame with 'Name', 'Lat', and 'Lon' columns.

    Outputs:
        - Prints processed information.
        - Saves visualization and raw data.
    """
    num_entries = len(df.iloc[:, 0])
    
    try:
        for idxFF in range(num_entries):
            LL = [df.Lat[idxFF], df.Lon[idxFF]]

            # Generate bounding box
            bbox = pointRadius45(LL, rradius)

            bbox_osm = []
            for i in range(np.shape(bbox)[0]):
                tmp = [bbox[i][1], bbox[i][0]]
                bbox_osm.append(tmp)

            ymin = np.min([sum(bbox_osm, [])[0], sum(bbox_osm, [])[2], sum(bbox_osm, [])[4], sum(bbox_osm, [])[6]])
            ymax = np.max([sum(bbox_osm, [])[0], sum(bbox_osm, [])[2], sum(bbox_osm, [])[4], sum(bbox_osm, [])[6]])
            xmin = np.min([sum(bbox_osm, [])[1], sum(bbox_osm, [])[3], sum(bbox_osm, [])[5], sum(bbox_osm, [])[7]])
            xmax = np.max([sum(bbox_osm, [])[1], sum(bbox_osm, [])[3], sum(bbox_osm, [])[5], sum(bbox_osm, [])[7]])
            bbox_cor = [ymax, ymin, xmin, xmax]

            # Fetch building data from OSM
            gdf = ox.geometries_from_bbox(bbox_cor[0], bbox_cor[1], bbox_cor[2], bbox_cor[3], {"building": True})
            if gdf.empty:
                print(f"No building data found for {df.Name[idxFF]} at radius {rradius} km.")
                continue

            gdf.reset_index(level=0, inplace=True)
            geom = gdf['geometry'].values

            # Extract height-related information
            try:
                bHeightH = gdf['height'].values
                bHeightH = np.array([float(x) for x in bHeightH])
            except:
                bHeightH = np.zeros(geom.size)

            try:
                bHeightL = gdf['building:levels'].values
                bHeightL = np.array([float(x) for x in bHeightL]) * 3
            except:
                bHeightL = np.zeros(geom.size)

            centroid = []
            for idxP in range(geom.shape[0]):
                centroid.append(geom[idxP].centroid)
            data = {'geometry': geom, 'cent': centroid}

            gdf = pd.DataFrame(data)

            # Projection setup
            x_mul, y_mul = projection(bbox_cor, 1, 1)  # Resolution: 1x1
            domain1, domain, gdf, x_start, y_start = initialize(bbox, gdf, x_mul, y_mul, bbox_cor, 0)

            lineO = []
            lineL = []
            area = []
            areaH = []

            for idxP in range(gdf.shape[0]):
                if Point(gdf['cent'][idxP][0][0], gdf['cent'][idxP][1][0]).within(Polygon(bbox)):
                    nx, ny, xy, Pol = [], [], [], []
                    for i in range(np.shape(gdf['geometry'][idxP])[1]):
                        xb = int(np.round((gdf['geometry'][idxP][0][i] - bbox_cor[1]) * x_mul)) - x_start
                        yb = int(np.round((gdf['geometry'][idxP][1][i] - bbox_cor[2]) * y_mul)) - y_start

                        xx, yy, _ = rotateS(xb, yb, domain1, 0)  # No rotation here

                        nx.append(xx + x_start)
                        ny.append(yy + y_start)
                        xy.append([xx + x_start, yy + y_start])
                        Pol.append((xx, yy))

                    [lineO, lineL] = count_edge(xy, lineO, lineL, 1)  # Resolution
                    pol = Polygon(Pol)
                    area.append(pol.area)

                    bHeightL[np.isnan(bHeightL)] = 0
                    bHeightH[np.isnan(bHeightH)] = 0

                    if bHeightH[idxP] == 0:
                        HH = bHeightL[idxP] if bHeightL[idxP] != 0 else 16  # Default height
                    else:
                        HH = bHeightH[idxP]
                    areaH.append(pol.area)

                    domain = construct(domain, HH, nx, ny, x_start, y_start, pol)

            t1, t2 = 0, 0
            for i in range(domain.shape[0]):
                for j in range(domain.shape[1]):
                    if domain[i, j] != 0:
                        t1 += 1
                        t2 += domain[i, j]

            # Visualization
            fig, ax = plt.subplots(figsize=(8, 8))
            im = ax.imshow(domain)
            circle1 = plt.Circle((int(domain.shape[0] / 2), int(domain.shape[0] / 2)), 10, color='r')
            ax.add_patch(circle1)
            ax.set_title(f'Hmean={t2 / t1:.2f}m @ radius {int(rradius * 1000)}m around {df.Name[idxFF]}')
            cb = plt.colorbar(im)
            cb.set_label('Estimated building height from OSM [m]')
            plt.tight_layout()

            # Save visualization and data
            plt.savefig(f"osm_domain_{df.Name[idxFF]}.png", dpi=300)
            np.savetxt(f"osm_domain_{df.Name[idxFF]}.txt", domain, fmt='%d')
            print(f"Saved OSM domain and visualization for {df.Name[idxFF]}.")

    except KeyboardInterrupt:
        print("Process interrupted by user.")
        raise

    except Exception as e:
        print(f"An error occurred: {e}")


def cal_std(topo):
    tmp = topo[np.nonzero(topo)].flatten()
    std = np.std(tmp)
    mean = np.mean(tmp)
    hmax = np.nanmax(tmp)
    hmin = np.nanmin(tmp)
    return(mean,std,hmax,hmin)
