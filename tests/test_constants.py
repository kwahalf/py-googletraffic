"""
Unit tests for constants module.
"""

import unittest
from googletraffic.constants import (
    TRAFFIC_LEVELS,
    TRAFFIC_COLORS,
    ZOOM_SCALES,
    TILE_SIZE,
    GOOGLE_MAPS_HTML_TEMPLATE,
)


class TestTrafficLevels(unittest.TestCase):
    """Test traffic level definitions."""

    def test_traffic_levels_exist(self):
        """Test that all traffic levels are defined."""
        self.assertIn(1, TRAFFIC_LEVELS)
        self.assertIn(2, TRAFFIC_LEVELS)
        self.assertIn(3, TRAFFIC_LEVELS)
        self.assertIn(4, TRAFFIC_LEVELS)

    def test_traffic_levels_have_descriptions(self):
        """Test that traffic levels have descriptions."""
        for level in [1, 2, 3, 4]:
            self.assertIsInstance(TRAFFIC_LEVELS[level], str)
            self.assertGreater(len(TRAFFIC_LEVELS[level]), 0)

    def test_traffic_levels_correct_count(self):
        """Test that there are exactly 4 traffic levels."""
        self.assertEqual(len(TRAFFIC_LEVELS), 4)


class TestTrafficColors(unittest.TestCase):
    """Test traffic color definitions."""

    def test_traffic_colors_exist(self):
        """Test that all traffic color levels are defined."""
        for level in [1, 2, 3, 4]:
            self.assertIn(level, TRAFFIC_COLORS)

    def test_color_structure(self):
        """Test that each color definition has required fields."""
        required_fields = ["name", "rgb_center", "tolerance"]

        for level, color_info in TRAFFIC_COLORS.items():
            for field in required_fields:
                self.assertIn(field, color_info, f"Level {level} missing field: {field}")

    def test_color_names(self):
        """Test color names are strings."""
        for level, color_info in TRAFFIC_COLORS.items():
            self.assertIsInstance(color_info["name"], str)
            self.assertGreater(len(color_info["name"]), 0)

    def test_rgb_values(self):
        """Test RGB center values are valid tuples."""
        for level, color_info in TRAFFIC_COLORS.items():
            rgb = color_info["rgb_center"]

            # Should be tuple of 3 values
            self.assertIsInstance(rgb, tuple)
            self.assertEqual(len(rgb), 3)

            # All values should be 0-255
            for value in rgb:
                self.assertIsInstance(value, int)
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 255)

    def test_tolerance_values(self):
        """Test tolerance values are reasonable."""
        for level, color_info in TRAFFIC_COLORS.items():
            tolerance = color_info["tolerance"]

            self.assertIsInstance(tolerance, (int, float))
            self.assertGreater(tolerance, 0)
            self.assertLess(tolerance, 500)  # Reasonable upper bound

    def test_green_color(self):
        """Test green traffic color definition."""
        green = TRAFFIC_COLORS[1]
        self.assertEqual(green["name"], "green")
        self.assertEqual(green["rgb_center"], (99, 197, 124))

    def test_orange_color(self):
        """Test orange traffic color definition."""
        orange = TRAFFIC_COLORS[2]
        self.assertEqual(orange["name"], "orange")
        self.assertEqual(orange["rgb_center"], (242, 139, 52))

    def test_red_color(self):
        """Test red traffic color definition."""
        red = TRAFFIC_COLORS[3]
        self.assertEqual(red["name"], "red")
        self.assertEqual(red["rgb_center"], (240, 70, 70))

    def test_dark_red_color(self):
        """Test dark red traffic color definition."""
        dark_red = TRAFFIC_COLORS[4]
        self.assertEqual(dark_red["name"], "dark_red")
        self.assertEqual(dark_red["rgb_center"], (129, 31, 31))


class TestZoomScales(unittest.TestCase):
    """Test zoom scale definitions."""

    def test_zoom_levels_count(self):
        """Test that zoom levels 0-20 are defined."""
        self.assertEqual(len(ZOOM_SCALES), 21)

        for zoom in range(21):
            self.assertIn(zoom, ZOOM_SCALES)

    def test_zoom_scale_values(self):
        """Test that zoom scale values are positive."""
        for zoom, scale in ZOOM_SCALES.items():
            self.assertIsInstance(scale, (int, float))
            self.assertGreater(scale, 0)

    def test_zoom_scale_progression(self):
        """Test that zoom scales decrease as zoom increases."""
        for zoom in range(20):
            self.assertGreater(ZOOM_SCALES[zoom], ZOOM_SCALES[zoom + 1])

    def test_zoom_scale_doubling(self):
        """Test that each zoom level approximately halves the scale."""
        for zoom in range(19):
            ratio = ZOOM_SCALES[zoom] / ZOOM_SCALES[zoom + 1]
            # Should be approximately 2.0
            self.assertAlmostEqual(ratio, 2.0, places=1)

    def test_zoom_0_scale(self):
        """Test zoom level 0 scale (world view)."""
        self.assertAlmostEqual(ZOOM_SCALES[0], 156543.03, places=2)

    def test_zoom_20_scale(self):
        """Test zoom level 20 scale (building level)."""
        self.assertAlmostEqual(ZOOM_SCALES[20], 0.15, places=2)


class TestTileSize(unittest.TestCase):
    """Test tile size constant."""

    def test_tile_size_is_integer(self):
        """Test that tile size is an integer."""
        self.assertIsInstance(TILE_SIZE, int)

    def test_tile_size_is_positive(self):
        """Test that tile size is positive."""
        self.assertGreater(TILE_SIZE, 0)

    def test_tile_size_value(self):
        """Test expected tile size value."""
        self.assertEqual(TILE_SIZE, 640)


class TestGoogleMapsTemplate(unittest.TestCase):
    """Test Google Maps HTML template."""

    def test_template_exists(self):
        """Test that template is defined."""
        self.assertIsInstance(GOOGLE_MAPS_HTML_TEMPLATE, str)
        self.assertGreater(len(GOOGLE_MAPS_HTML_TEMPLATE), 0)

    def test_template_has_placeholders(self):
        """Test that template has required placeholders."""
        required_placeholders = ["{lat}", "{lng}", "{zoom}", "{api_key}"]

        for placeholder in required_placeholders:
            self.assertIn(
                placeholder,
                GOOGLE_MAPS_HTML_TEMPLATE,
                f"Template missing placeholder: {placeholder}",
            )

    def test_template_is_html(self):
        """Test that template contains HTML structure."""
        self.assertIn("<!DOCTYPE html>", GOOGLE_MAPS_HTML_TEMPLATE)
        self.assertIn("<html>", GOOGLE_MAPS_HTML_TEMPLATE)
        self.assertIn("<head>", GOOGLE_MAPS_HTML_TEMPLATE)
        self.assertIn("<body>", GOOGLE_MAPS_HTML_TEMPLATE)
        self.assertIn("</html>", GOOGLE_MAPS_HTML_TEMPLATE)

    def test_template_has_map_div(self):
        """Test that template has map container."""
        self.assertIn('<div id="map">', GOOGLE_MAPS_HTML_TEMPLATE)

    def test_template_has_google_maps_script(self):
        """Test that template loads Google Maps API."""
        self.assertIn("maps.googleapis.com", GOOGLE_MAPS_HTML_TEMPLATE)
        self.assertIn("TrafficLayer", GOOGLE_MAPS_HTML_TEMPLATE)

    def test_template_formatting(self):
        """Test that template can be formatted with values."""
        try:
            formatted = GOOGLE_MAPS_HTML_TEMPLATE.format(
                lat=40.7580, lng=-73.9855, zoom=14, api_key="test_key"
            )

            # Check values were inserted (note: Python formats 40.7580 as 40.758)
            self.assertIn("40.758", formatted)  # Trailing zero removed by Python
            self.assertIn("-73.9855", formatted)
            self.assertIn("14", formatted)
            self.assertIn("test_key", formatted)

        except KeyError as e:
            self.fail(f"Template formatting failed: {e}")


if __name__ == "__main__":
    unittest.main()
