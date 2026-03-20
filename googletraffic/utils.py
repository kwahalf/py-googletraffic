"""
Utility functions for traffic data processing.
"""

import numpy as np
from typing import Tuple
from .constants import TRAFFIC_COLORS, ZOOM_SCALES
import math


def color_distance(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    """
    Calculate Euclidean distance between two RGB colors.

    Parameters
    ----------
    color1 : tuple
        First RGB color as (r, g, b)
    color2 : tuple
        Second RGB color as (r, g, b)

    Returns
    -------
    float
        Euclidean distance between colors
    """
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


def classify_traffic_pixel(rgb: Tuple[int, int, int]) -> int:
    """
    Classify a pixel's RGB value into a traffic level.

    Parameters
    ----------
    rgb : tuple
        RGB values as (r, g, b)

    Returns
    -------
    int
        Traffic level (1-4) or 0 if no traffic color detected
    """
    min_distance = float("inf")
    best_level = 0

    for level, color_info in TRAFFIC_COLORS.items():
        distance = color_distance(rgb, color_info["rgb_center"])
        if distance < color_info["tolerance"] and distance < min_distance:
            min_distance = distance
            best_level = level

    return best_level


def classify_traffic_array(image_array: np.ndarray) -> np.ndarray:
    """
    Classify an entire image array into traffic levels.

    Parameters
    ----------
    image_array : np.ndarray
        Image array with shape (height, width, 3) containing RGB values

    Returns
    -------
    np.ndarray
        Array with shape (height, width) containing traffic levels (0-4)
    """
    height, width = image_array.shape[:2]
    traffic_array = np.zeros((height, width), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            rgb = tuple(image_array[i, j, :3])
            traffic_array[i, j] = classify_traffic_pixel(rgb)

    return traffic_array


def get_meters_per_pixel(latitude: float, zoom: int) -> float:
    """
    Calculate meters per pixel at a given latitude and zoom level.

    Parameters
    ----------
    latitude : float
        Latitude in degrees
    zoom : int
        Google Maps zoom level (0-20)

    Returns
    -------
    float
        Meters per pixel
    """
    if zoom not in ZOOM_SCALES:
        raise ValueError(f"Zoom level must be between 0 and 20, got {zoom}")

    # Adjust for latitude (Mercator projection)
    meters_per_pixel = ZOOM_SCALES[zoom] * math.cos(math.radians(latitude))
    return meters_per_pixel


def calculate_bounds(
    center_lat: float, center_lng: float, width: int, height: int, zoom: int
) -> dict:
    """
    Calculate geographic bounds for a raster centered at given coordinates.

    Parameters
    ----------
    center_lat : float
        Center latitude
    center_lng : float
        Center longitude
    width : int
        Width in pixels
    height : int
        Height in pixels
    zoom : int
        Zoom level

    Returns
    -------
    dict
        Dictionary with 'north', 'south', 'east', 'west' bounds
    """
    meters_per_pixel = get_meters_per_pixel(center_lat, zoom)

    # Calculate offset in degrees
    # Approximate: 1 degree latitude ≈ 111,111 meters
    # 1 degree longitude varies with latitude
    lat_offset = (height / 2 * meters_per_pixel) / 111111
    lng_offset = (width / 2 * meters_per_pixel) / (111111 * math.cos(math.radians(center_lat)))

    bounds = {
        "north": center_lat + lat_offset,
        "south": center_lat - lat_offset,
        "east": center_lng + lng_offset,
        "west": center_lng - lng_offset,
    }

    return bounds


def create_geotransform(bounds: dict, width: int, height: int) -> Tuple:
    """
    Create a GDAL geotransform tuple from bounds.

    The geotransform is (x_min, pixel_width, 0, y_max, 0, -pixel_height)

    Parameters
    ----------
    bounds : dict
        Geographic bounds with 'north', 'south', 'east', 'west'
    width : int
        Raster width in pixels
    height : int
        Raster height in pixels

    Returns
    -------
    tuple
        GDAL geotransform (x_origin, pixel_width, 0, y_origin, 0, -pixel_height)
    """
    x_min = bounds["west"]
    y_max = bounds["north"]
    pixel_width = (bounds["east"] - bounds["west"]) / width
    pixel_height = (bounds["north"] - bounds["south"]) / height

    return (x_min, pixel_width, 0, y_max, 0, -pixel_height)


def split_bounds_into_tiles(bounds: dict, zoom: int, max_pixels: int = 2000) -> list:
    """
    Split large geographic bounds into multiple tiles for API efficiency.

    Parameters
    ----------
    bounds : dict
        Geographic bounds with 'north', 'south', 'east', 'west'
    zoom : int
        Zoom level
    max_pixels : int
        Maximum dimension for a single tile

    Returns
    -------
    list
        List of dictionaries, each containing center coordinates and dimensions
    """
    # Calculate total area dimensions
    center_lat = (bounds["north"] + bounds["south"]) / 2

    meters_per_pixel = get_meters_per_pixel(center_lat, zoom)

    # Calculate dimensions in pixels
    lat_diff = bounds["north"] - bounds["south"]
    lng_diff = bounds["east"] - bounds["west"]

    height_pixels = int((lat_diff * 111111) / meters_per_pixel)
    width_pixels = int((lng_diff * 111111 * math.cos(math.radians(center_lat))) / meters_per_pixel)

    # Calculate number of tiles needed
    tiles_x = math.ceil(width_pixels / max_pixels)
    tiles_y = math.ceil(height_pixels / max_pixels)

    tiles = []

    for i in range(tiles_y):
        for j in range(tiles_x):
            # Calculate tile bounds
            tile_lat_min = bounds["south"] + (lat_diff / tiles_y) * i
            tile_lat_max = bounds["south"] + (lat_diff / tiles_y) * (i + 1)
            tile_lng_min = bounds["west"] + (lng_diff / tiles_x) * j
            tile_lng_max = bounds["west"] + (lng_diff / tiles_x) * (j + 1)

            tile_center_lat = (tile_lat_min + tile_lat_max) / 2
            tile_center_lng = (tile_lng_min + tile_lng_max) / 2

            tile_width = min(max_pixels, width_pixels - j * max_pixels)
            tile_height = min(max_pixels, height_pixels - i * max_pixels)

            tiles.append(
                {
                    "center_lat": tile_center_lat,
                    "center_lng": tile_center_lng,
                    "width": tile_width,
                    "height": tile_height,
                    "position": (i, j),
                }
            )

    return tiles
