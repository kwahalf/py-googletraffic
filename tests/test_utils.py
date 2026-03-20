"""
Unit tests for utility functions.
"""

import unittest
import numpy as np
from googletraffic.utils import (
    color_distance,
    classify_traffic_pixel,
    classify_traffic_array,
    get_meters_per_pixel,
    calculate_bounds,
    create_geotransform,
    split_bounds_into_tiles,
)


class TestColorDistance(unittest.TestCase):
    """Test color distance calculations."""
    
    def test_identical_colors(self):
        """Test distance between identical colors is zero."""
        color = (255, 128, 64)
        self.assertEqual(color_distance(color, color), 0.0)
    
    def test_different_colors(self):
        """Test distance between different colors."""
        distance = color_distance((255, 0, 0), (0, 255, 0))
        self.assertGreater(distance, 0)
        # Distance should be sqrt(255^2 + 255^2) = ~360.6
        self.assertAlmostEqual(distance, 360.624, places=2)
    
    def test_black_white(self):
        """Test distance between black and white."""
        distance = color_distance((0, 0, 0), (255, 255, 255))
        # Distance should be sqrt(3 * 255^2) = ~441.67
        self.assertAlmostEqual(distance, 441.673, places=2)


class TestClassifyTrafficPixel(unittest.TestCase):
    """Test traffic pixel classification."""
    
    def test_green_traffic(self):
        """Test classification of green (no traffic)."""
        # Green traffic color
        rgb = (99, 197, 124)
        level = classify_traffic_pixel(rgb)
        self.assertEqual(level, 1)
    
    def test_orange_traffic(self):
        """Test classification of orange (medium traffic)."""
        rgb = (242, 139, 52)
        level = classify_traffic_pixel(rgb)
        self.assertEqual(level, 2)
    
    def test_red_traffic(self):
        """Test classification of red (high traffic)."""
        rgb = (240, 70, 70)
        level = classify_traffic_pixel(rgb)
        self.assertEqual(level, 3)
    
    def test_dark_red_traffic(self):
        """Test classification of dark red (heavy traffic)."""
        rgb = (129, 31, 31)
        level = classify_traffic_pixel(rgb)
        self.assertEqual(level, 4)
    
    def test_non_traffic_color(self):
        """Test classification of non-traffic color."""
        # Blue color (not a traffic color)
        rgb = (0, 0, 255)
        level = classify_traffic_pixel(rgb)
        self.assertEqual(level, 0)
    
    def test_near_green(self):
        """Test color close to green threshold."""
        # Slightly different from green center
        rgb = (110, 200, 130)
        level = classify_traffic_pixel(rgb)
        self.assertEqual(level, 1)


class TestClassifyTrafficArray(unittest.TestCase):
    """Test traffic array classification."""
    
    def test_single_color_array(self):
        """Test array with single color."""
        # Create 3x3 array of green traffic
        array = np.full((3, 3, 3), [99, 197, 124], dtype=np.uint8)
        result = classify_traffic_array(array)
        
        self.assertEqual(result.shape, (3, 3))
        self.assertTrue(bool(np.all(result == 1)))
    
    def test_mixed_colors_array(self):
        """Test array with multiple traffic levels."""
        array = np.zeros((2, 2, 3), dtype=np.uint8)
        
        # Green
        array[0, 0] = [99, 197, 124]
        # Orange
        array[0, 1] = [242, 139, 52]
        # Red
        array[1, 0] = [240, 70, 70]
        # Dark red
        array[1, 1] = [129, 31, 31]
        
        result = classify_traffic_array(array)
        
        self.assertEqual(result[0, 0], 1)
        self.assertEqual(result[0, 1], 2)
        self.assertEqual(result[1, 0], 3)
        self.assertEqual(result[1, 1], 4)
    
    def test_non_traffic_array(self):
        """Test array with non-traffic colors."""
        # White array (pure white, clearly not a traffic color)
        array = np.full((2, 2, 3), [255, 255, 255], dtype=np.uint8)
        result = classify_traffic_array(array)
        
        # Check that all pixels are classified as 0 (no traffic)
        unique_values = np.unique(result)
        self.assertEqual(len(unique_values), 1, 
                        f"Expected only value 0, but got: {unique_values}")
        self.assertEqual(unique_values[0], 0,
                        f"Expected 0, but got: {unique_values[0]}")
    
    def test_non_traffic_color_blue(self):
        """Test that blue color (common in maps) is not classified as traffic."""
        # Blue color - should not match any traffic colors
        blue = (0, 0, 255)
        level = classify_traffic_pixel(blue)
        self.assertEqual(level, 0, 
                        f"Blue should be classified as 0 (no traffic), got {level}")


class TestGetMetersPerPixel(unittest.TestCase):
    """Test meters per pixel calculations."""
    
    def test_equator_zoom_0(self):
        """Test meters per pixel at equator, zoom 0."""
        meters = get_meters_per_pixel(0, 0)
        self.assertAlmostEqual(meters, 156543.03, places=2)
    
    def test_equator_zoom_10(self):
        """Test meters per pixel at equator, zoom 10."""
        meters = get_meters_per_pixel(0, 10)
        self.assertAlmostEqual(meters, 152.87, places=2)
    
    def test_latitude_effect(self):
        """Test that higher latitudes have smaller meters per pixel."""
        equator = get_meters_per_pixel(0, 10)
        high_lat = get_meters_per_pixel(60, 10)
        
        # At 60° latitude, should be cos(60°) = 0.5 times equator
        self.assertLess(high_lat, equator)
        self.assertAlmostEqual(high_lat / equator, 0.5, places=1)
    
    def test_invalid_zoom(self):
        """Test that invalid zoom raises error."""
        with self.assertRaises(ValueError):
            get_meters_per_pixel(0, 25)
        
        with self.assertRaises(ValueError):
            get_meters_per_pixel(0, -1)
    
    def test_zoom_progression(self):
        """Test that zoom levels double in detail."""
        zoom_10 = get_meters_per_pixel(0, 10)
        zoom_11 = get_meters_per_pixel(0, 11)
        
        # Each zoom level should halve the meters per pixel
        self.assertAlmostEqual(zoom_11, zoom_10 / 2, places=2)


class TestCalculateBounds(unittest.TestCase):
    """Test geographic bounds calculations."""
    
    def test_bounds_at_equator(self):
        """Test bounds calculation at equator."""
        bounds = calculate_bounds(
            center_lat=0,
            center_lng=0,
            width=1000,
            height=1000,
            zoom=10
        )
        
        self.assertIn('north', bounds)
        self.assertIn('south', bounds)
        self.assertIn('east', bounds)
        self.assertIn('west', bounds)
        
        # Bounds should be symmetric around center
        self.assertAlmostEqual(bounds['north'], -bounds['south'], places=4)
        self.assertAlmostEqual(bounds['east'], -bounds['west'], places=4)
    
    def test_bounds_positive_values(self):
        """Test that bounds are calculated correctly."""
        bounds = calculate_bounds(40.7580, -73.9855, 1000, 1000, 14)
        
        # North should be greater than south
        self.assertGreater(bounds['north'], bounds['south'])
        # East should be greater than west
        self.assertGreater(bounds['east'], bounds['west'])
        
        # Bounds should contain the center point
        self.assertTrue(bounds['south'] < 40.7580 < bounds['north'])
        self.assertTrue(bounds['west'] < -73.9855 < bounds['east'])
    
    def test_different_dimensions(self):
        """Test bounds with different width and height."""
        bounds = calculate_bounds(40.0, -74.0, 2000, 1000, 14)
        
        lat_range = bounds['north'] - bounds['south']
        lng_range = bounds['east'] - bounds['west']
        
        # Width is 2x height, so lng_range should be ~2x lat_range
        # (approximately, considering latitude correction)
        self.assertGreater(lng_range, lat_range)


class TestCreateGeotransform(unittest.TestCase):
    """Test GDAL geotransform creation."""
    
    def test_geotransform_format(self):
        """Test geotransform tuple format."""
        bounds = {
            'north': 41.0,
            'south': 40.0,
            'east': -73.0,
            'west': -74.0
        }
        
        transform = create_geotransform(bounds, 1000, 1000)
        
        # Should return 6-element tuple
        self.assertEqual(len(transform), 6)
        
        # Check components
        self.assertEqual(transform[0], bounds['west'])  # x_min
        self.assertGreater(transform[1], 0)  # pixel_width (positive)
        self.assertEqual(transform[2], 0)  # rotation
        self.assertEqual(transform[3], bounds['north'])  # y_max
        self.assertEqual(transform[4], 0)  # rotation
        self.assertLess(transform[5], 0)  # pixel_height (negative)
    
    def test_pixel_size_calculation(self):
        """Test pixel size calculation in geotransform."""
        bounds = {
            'north': 40.0,
            'south': 39.0,
            'east': -73.0,
            'west': -74.0
        }
        
        transform = create_geotransform(bounds, 100, 100)
        
        pixel_width = transform[1]
        pixel_height = abs(transform[5])
        
        # Pixel width should be (east - west) / width
        expected_width = (bounds['east'] - bounds['west']) / 100
        self.assertAlmostEqual(pixel_width, expected_width, places=6)
        
        # Pixel height should be (north - south) / height
        expected_height = (bounds['north'] - bounds['south']) / 100
        self.assertAlmostEqual(pixel_height, expected_height, places=6)


class TestSplitBoundsIntoTiles(unittest.TestCase):
    """Test bounds splitting into tiles."""
    
    def test_small_area_single_tile(self):
        """Test that small area returns single tile."""
        bounds = {
            'north': 40.01,
            'south': 40.00,
            'east': -73.99,
            'west': -74.00
        }
        
        tiles = split_bounds_into_tiles(bounds, zoom=14, max_pixels=2000)
        
        # Should return single tile
        self.assertEqual(len(tiles), 1)
        
        tile = tiles[0]
        self.assertIn('center_lat', tile)
        self.assertIn('center_lng', tile)
        self.assertIn('width', tile)
        self.assertIn('height', tile)
        self.assertIn('position', tile)
    
    def test_large_area_multiple_tiles(self):
        """Test that large area is split into multiple tiles."""
        bounds = {
            'north': 41.0,
            'south': 40.0,
            'east': -73.0,
            'west': -74.0
        }
        
        tiles = split_bounds_into_tiles(bounds, zoom=14, max_pixels=500)
        
        # Should return multiple tiles
        self.assertGreater(len(tiles), 1)
        
        # All tiles should have required fields
        for tile in tiles:
            self.assertIn('center_lat', tile)
            self.assertIn('center_lng', tile)
            self.assertIn('width', tile)
            self.assertIn('height', tile)
            self.assertIn('position', tile)
            
            # Dimensions should not exceed max_pixels
            self.assertLessEqual(tile['width'], 500)
            self.assertLessEqual(tile['height'], 500)
    
    def test_tile_positions_unique(self):
        """Test that tiles have unique positions."""
        bounds = {
            'north': 41.0,
            'south': 40.0,
            'east': -73.0,
            'west': -74.0
        }
        
        tiles = split_bounds_into_tiles(bounds, zoom=14, max_pixels=500)
        
        positions = [tile['position'] for tile in tiles]
        unique_positions = set(positions)
        
        # All positions should be unique
        self.assertEqual(len(positions), len(unique_positions))
    
    def test_tile_coverage(self):
        """Test that tiles cover the entire bounds."""
        bounds = {
            'north': 40.1,
            'south': 40.0,
            'east': -73.9,
            'west': -74.0
        }
        
        tiles = split_bounds_into_tiles(bounds, zoom=14, max_pixels=1000)
        
        # All tile centers should be within bounds
        for tile in tiles:
            self.assertTrue(bounds['south'] <= tile['center_lat'] <= bounds['north'])
            self.assertTrue(bounds['west'] <= tile['center_lng'] <= bounds['east'])


if __name__ == '__main__':
    unittest.main()
