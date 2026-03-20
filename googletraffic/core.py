"""
Core functions for creating georeferenced traffic rasters.
"""

import os
import io
import tempfile
import time
from typing import Tuple, Optional, Union
import numpy as np
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    raise ImportError(
        "Selenium is required. Install with: pip install selenium"
    )

try:
    from PIL import Image
except ImportError:
    raise ImportError(
        "Pillow is required. Install with: pip install Pillow"
    )

try:
    import rasterio
    from rasterio.transform import from_bounds
except ImportError:
    raise ImportError(
        "Rasterio is required. Install with: pip install rasterio"
    )

from .constants import GOOGLE_MAPS_HTML_TEMPLATE, TILE_SIZE
from .utils import (
    classify_traffic_array,
    calculate_bounds,
    create_geotransform,
    split_bounds_into_tiles,
)


def _setup_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Set up Chrome WebDriver for capturing maps.
    
    Parameters
    ----------
    headless : bool
        Whether to run browser in headless mode
    
    Returns
    -------
    webdriver.Chrome
        Configured Chrome driver
    """
    options = Options()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(f'--window-size={TILE_SIZE},{TILE_SIZE}')
    
    driver = webdriver.Chrome(options=options)
    return driver


def _capture_traffic_map(
    latitude: float,
    longitude: float,
    zoom: int,
    google_key: str,
    width: int = 640,
    height: int = 640,
    wait_time: int = 3,
    headless: bool = True,
) -> np.ndarray:
    """
    Capture a screenshot of Google Maps with traffic layer.
    
    Parameters
    ----------
    latitude : float
        Center latitude
    longitude : float
        Center longitude
    zoom : int
        Google Maps zoom level (0-20)
    google_key : str
        Google Maps API key
    width : int
        Screenshot width in pixels
    height : int
        Screenshot height in pixels
    wait_time : int
        Time to wait for traffic layer to load (seconds)
    headless : bool
        Whether to run browser in headless mode
    
    Returns
    -------
    np.ndarray
        Image array with shape (height, width, 3)
    """
    driver = None
    temp_file = None
    
    try:
        # Create HTML file
        html_content = GOOGLE_MAPS_HTML_TEMPLATE.format(
            lat=latitude,
            lng=longitude,
            zoom=zoom,
            api_key=google_key
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            temp_file = f.name
        
        # Set up driver
        driver = _setup_driver(headless=headless)
        driver.set_window_size(width, height)
        
        # Load page
        driver.get(f'file://{temp_file}')
        
        # Wait for map to be ready
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return window.mapReady === true')
        )
        
        # Additional wait for traffic layer
        time.sleep(wait_time)
        
        # Take screenshot
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        image_array = np.array(image)
        
        return image_array
        
    finally:
        if driver:
            driver.quit()
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)


def make_raster(
    location: Tuple[float, float],
    height: int,
    width: int,
    zoom: int,
    google_key: str,
    output_path: Optional[str] = None,
    wait_time: int = 3,
    headless: bool = True,
) -> Union[np.ndarray, str]:
    """
    Create a traffic raster centered at a specific location.
    
    This function captures Google Maps traffic data and converts it into
    a georeferenced raster with traffic levels (1-4).
    
    Parameters
    ----------
    location : tuple
        Center coordinates as (latitude, longitude)
    height : int
        Raster height in pixels
    width : int
        Raster width in pixels
    zoom : int
        Google Maps zoom level (0-20). Higher values = more detail.
        Recommended: 14-16 for city-level, 11-13 for regional
    google_key : str
        Google Maps JavaScript API key
    output_path : str, optional
        If provided, saves raster as GeoTIFF to this path
    wait_time : int
        Seconds to wait for traffic layer to load (default: 3)
    headless : bool
        Run browser in headless mode (default: True)
    
    Returns
    -------
    np.ndarray or str
        If output_path is None, returns numpy array with traffic levels.
        If output_path is provided, saves GeoTIFF and returns the path.
    
    Examples
    --------
    >>> import googletraffic as gt
    >>> # Create raster around New York City
    >>> raster = gt.make_raster(
    ...     location=(40.7128, -74.0060),
    ...     height=1000,
    ...     width=1000,
    ...     zoom=14,
    ...     google_key="YOUR_API_KEY"
    ... )
    >>> print(raster.shape)  # (1000, 1000)
    """
    import io  # Import here to avoid issues
    
    latitude, longitude = location
    
    # Capture traffic map
    image_array = _capture_traffic_map(
        latitude=latitude,
        longitude=longitude,
        zoom=zoom,
        google_key=google_key,
        width=width,
        height=height,
        wait_time=wait_time,
        headless=headless,
    )
    
    # Classify pixels to traffic levels
    traffic_array = classify_traffic_array(image_array)
    
    if output_path is None:
        return traffic_array
    
    # Save as GeoTIFF
    bounds = calculate_bounds(latitude, longitude, width, height, zoom)
    transform = from_bounds(
        bounds['west'], bounds['south'],
        bounds['east'], bounds['north'],
        width, height
    )
    
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=traffic_array.dtype,
        crs='EPSG:4326',
        transform=transform,
    ) as dst:
        dst.write(traffic_array, 1)
    
    return output_path


def make_raster_from_bbox(
    bbox: Tuple[float, float, float, float],
    zoom: int,
    google_key: str,
    output_path: Optional[str] = None,
    max_pixels: int = 2000,
    wait_time: int = 3,
    headless: bool = True,
) -> Union[np.ndarray, str]:
    """
    Create a traffic raster from a bounding box.
    
    For large areas, this function automatically splits the region into
    multiple tiles to stay within reasonable pixel dimensions.
    
    Parameters
    ----------
    bbox : tuple
        Bounding box as (west, south, east, north) in decimal degrees
    zoom : int
        Google Maps zoom level (0-20)
    google_key : str
        Google Maps JavaScript API key
    output_path : str, optional
        If provided, saves raster as GeoTIFF
    max_pixels : int
        Maximum dimension for a single tile (default: 2000)
    wait_time : int
        Seconds to wait for traffic layer to load per tile
    headless : bool
        Run browser in headless mode
    
    Returns
    -------
    np.ndarray or str
        Traffic raster or path to saved GeoTIFF
    
    Examples
    --------
    >>> import googletraffic as gt
    >>> # Create raster for Manhattan bbox
    >>> bbox = (-74.02, 40.70, -73.97, 40.80)  # (west, south, east, north)
    >>> raster = gt.make_raster_from_bbox(
    ...     bbox=bbox,
    ...     zoom=14,
    ...     google_key="YOUR_API_KEY",
    ...     output_path="manhattan_traffic.tif"
    ... )
    """
    west, south, east, north = bbox
    bounds = {
        'west': west,
        'south': south,
        'east': east,
        'north': north,
    }
    
    # Split into tiles if necessary
    center_lat = (north + south) / 2
    center_lng = (east + west) / 2
    
    tiles = split_bounds_into_tiles(bounds, zoom, max_pixels)
    
    if len(tiles) == 1:
        # Single tile - use make_raster directly
        tile = tiles[0]
        return make_raster(
            location=(tile['center_lat'], tile['center_lng']),
            height=tile['height'],
            width=tile['width'],
            zoom=zoom,
            google_key=google_key,
            output_path=output_path,
            wait_time=wait_time,
            headless=headless,
        )
    
    # Multiple tiles - capture and mosaic
    print(f"Creating {len(tiles)} tiles to cover area...")
    
    # Capture all tiles
    tile_arrays = []
    for idx, tile in enumerate(tiles, 1):
        print(f"  Capturing tile {idx}/{len(tiles)}...")
        tile_array = make_raster(
            location=(tile['center_lat'], tile['center_lng']),
            height=tile['height'],
            width=tile['width'],
            zoom=zoom,
            google_key=google_key,
            output_path=None,
            wait_time=wait_time,
            headless=headless,
        )
        tile_arrays.append((tile, tile_array))
    
    # Mosaic tiles
    # Determine grid dimensions
    max_i = max(t['position'][0] for t, _ in tile_arrays) + 1
    max_j = max(t['position'][1] for t, _ in tile_arrays) + 1
    
    # Create empty mosaic
    total_height = sum(t['height'] for t, _ in tile_arrays if t['position'][1] == 0)
    total_width = sum(t['width'] for t, _ in tile_arrays if t['position'][0] == 0)
    mosaic = np.zeros((total_height, total_width), dtype=np.uint8)
    
    # Fill mosaic
    for tile, tile_array in tile_arrays:
        i, j = tile['position']
        # Calculate position in mosaic
        start_i = sum(t['height'] for t, _ in tile_arrays 
                     if t['position'][0] < i and t['position'][1] == 0)
        start_j = sum(t['width'] for t, _ in tile_arrays 
                     if t['position'][1] < j and t['position'][0] == 0)
        
        mosaic[start_i:start_i+tile['height'], 
               start_j:start_j+tile['width']] = tile_array
    
    if output_path is None:
        return mosaic
    
    # Save as GeoTIFF
    transform = from_bounds(west, south, east, north, total_width, total_height)
    
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=total_height,
        width=total_width,
        count=1,
        dtype=mosaic.dtype,
        crs='EPSG:4326',
        transform=transform,
    ) as dst:
        dst.write(mosaic, 1)
    
    return output_path


def make_raster_from_polygon(
    polygon,
    zoom: int,
    google_key: str,
    output_path: Optional[str] = None,
    max_pixels: int = 2000,
    wait_time: int = 3,
    headless: bool = True,
) -> Union[np.ndarray, str]:
    """
    Create a traffic raster covering a polygon area.
    
    Parameters
    ----------
    polygon : shapely.geometry.Polygon or geopandas.GeoDataFrame
        Polygon defining the area of interest
    zoom : int
        Google Maps zoom level (0-20)
    google_key : str
        Google Maps JavaScript API key
    output_path : str, optional
        If provided, saves raster as GeoTIFF
    max_pixels : int
        Maximum dimension for a single tile
    wait_time : int
        Seconds to wait for traffic layer to load per tile
    headless : bool
        Run browser in headless mode
    
    Returns
    -------
    np.ndarray or str
        Traffic raster or path to saved GeoTIFF
    
    Examples
    --------
    >>> import googletraffic as gt
    >>> import geopandas as gpd
    >>> # Load polygon (e.g., city boundary)
    >>> gdf = gpd.read_file("city_boundary.geojson")
    >>> raster = gt.make_raster_from_polygon(
    ...     polygon=gdf,
    ...     zoom=14,
    ...     google_key="YOUR_API_KEY",
    ...     output_path="city_traffic.tif"
    ... )
    """
    try:
        import geopandas as gpd
        from shapely.geometry import Polygon
    except ImportError:
        raise ImportError(
            "GeoPandas and Shapely are required. Install with: "
            "pip install geopandas shapely"
        )
    
    # Handle GeoDataFrame
    if isinstance(polygon, gpd.GeoDataFrame):
        polygon = polygon.geometry.unary_union
    
    # Get bounding box
    bounds = polygon.bounds  # (minx, miny, maxx, maxy)
    bbox = (bounds[0], bounds[1], bounds[2], bounds[3])  # (west, south, east, north)
    
    return make_raster_from_bbox(
        bbox=bbox,
        zoom=zoom,
        google_key=google_key,
        output_path=output_path,
        max_pixels=max_pixels,
        wait_time=wait_time,
        headless=headless,
    )
