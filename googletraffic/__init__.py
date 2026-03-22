"""
py-googletraffic: Python Package for Google Maps Traffic Data

Create georeferenced traffic rasters from Google Maps traffic information.
"""

from .core import (
    make_raster,
    make_raster_from_polygon,
    make_raster_from_bbox,
)

__version__ = "0.1.2"
__author__ = "py-googletraffic Contributors"
__all__ = [
    "make_raster",
    "make_raster_from_polygon",
    "make_raster_from_bbox",
]
