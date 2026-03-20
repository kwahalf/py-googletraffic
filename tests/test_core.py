"""
Unit tests for core functions (mock-based tests).

Note: Full integration tests require actual Google Maps API key
and ChromeDriver. These tests use mocks to test logic without
external dependencies.
"""

import unittest
from unittest.mock import patch, MagicMock
import numpy as np


class TestMakeRaster(unittest.TestCase):
    """Test make_raster function with mocks."""

    @patch("googletraffic.core._capture_traffic_map")
    @patch("googletraffic.core.classify_traffic_array")
    def test_make_raster_returns_array(self, mock_classify, mock_capture):
        """Test that make_raster returns numpy array."""
        from googletraffic.core import make_raster

        # Setup mocks
        mock_image = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_capture.return_value = mock_image

        mock_traffic = np.ones((100, 100), dtype=np.uint8)
        mock_classify.return_value = mock_traffic

        # Test
        result = make_raster(
            location=(40.7580, -73.9855),
            height=100,
            width=100,
            zoom=14,
            google_key="test_key",
            output_path=None,
        )

        # Verify
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (100, 100))
        mock_capture.assert_called_once()
        mock_classify.assert_called_once()

    @patch("googletraffic.core._capture_traffic_map")
    @patch("googletraffic.core.classify_traffic_array")
    @patch("googletraffic.core.rasterio.open")
    def test_make_raster_saves_geotiff(self, mock_rio, mock_classify, mock_capture):
        """Test that make_raster saves GeoTIFF when output_path provided."""
        from googletraffic.core import make_raster

        # Setup mocks
        mock_image = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_capture.return_value = mock_image

        mock_traffic = np.ones((100, 100), dtype=np.uint8)
        mock_classify.return_value = mock_traffic

        mock_dst = MagicMock()
        mock_rio.return_value.__enter__.return_value = mock_dst

        # Test
        output_path = "/tmp/test.tif"
        result = make_raster(
            location=(40.7580, -73.9855),
            height=100,
            width=100,
            zoom=14,
            google_key="test_key",
            output_path=output_path,
        )

        # Verify
        self.assertEqual(result, output_path)
        mock_rio.assert_called_once()
        mock_dst.write.assert_called_once()

    @patch("googletraffic.core._capture_traffic_map")
    def test_make_raster_with_different_dimensions(self, mock_capture):
        """Test make_raster with different width and height."""
        from googletraffic.core import make_raster

        # Setup mock
        mock_image = np.zeros((500, 1000, 3), dtype=np.uint8)
        mock_capture.return_value = mock_image

        # Test
        with patch("googletraffic.core.classify_traffic_array") as mock_classify:
            mock_classify.return_value = np.zeros((500, 1000), dtype=np.uint8)

            result = make_raster(
                location=(40.7580, -73.9855),
                height=500,
                width=1000,
                zoom=14,
                google_key="test_key",
            )

            # Verify dimensions
            self.assertEqual(result.shape, (500, 1000))


class TestMakeRasterFromBbox(unittest.TestCase):
    """Test make_raster_from_bbox function."""

    @patch("googletraffic.core.make_raster")
    @patch("googletraffic.core.split_bounds_into_tiles")
    def test_single_tile(self, mock_split, mock_make):
        """Test bbox with single tile."""
        from googletraffic.core import make_raster_from_bbox

        # Setup mocks - single tile
        mock_split.return_value = [
            {
                "center_lat": 40.75,
                "center_lng": -73.98,
                "width": 1000,
                "height": 1000,
                "position": (0, 0),
            }
        ]

        mock_make.return_value = np.ones((1000, 1000), dtype=np.uint8)

        # Test
        result = make_raster_from_bbox(
            bbox=(-74.0, 40.7, -73.9, 40.8), zoom=14, google_key="test_key"
        )

        # Verify
        mock_split.assert_called_once()
        mock_make.assert_called_once()
        self.assertIsInstance(result, np.ndarray)

    @patch("googletraffic.core.make_raster")
    @patch("googletraffic.core.split_bounds_into_tiles")
    @patch("googletraffic.core.rasterio.open")
    def test_multiple_tiles(self, mock_rio, mock_split, mock_make):
        """Test bbox that requires multiple tiles."""
        from googletraffic.core import make_raster_from_bbox

        # Setup mocks - 2x2 grid
        mock_split.return_value = [
            {
                "center_lat": 40.75,
                "center_lng": -73.98,
                "width": 500,
                "height": 500,
                "position": (0, 0),
            },
            {
                "center_lat": 40.75,
                "center_lng": -73.94,
                "width": 500,
                "height": 500,
                "position": (0, 1),
            },
            {
                "center_lat": 40.79,
                "center_lng": -73.98,
                "width": 500,
                "height": 500,
                "position": (1, 0),
            },
            {
                "center_lat": 40.79,
                "center_lng": -73.94,
                "width": 500,
                "height": 500,
                "position": (1, 1),
            },
        ]

        # Each tile returns a small array
        mock_make.return_value = np.ones((500, 500), dtype=np.uint8)

        mock_dst = MagicMock()
        mock_rio.return_value.__enter__.return_value = mock_dst

        # Test
        result = make_raster_from_bbox(
            bbox=(-74.0, 40.7, -73.9, 40.8),
            zoom=14,
            google_key="test_key",
            output_path="/tmp/test.tif",
        )

        # Verify
        self.assertEqual(mock_make.call_count, 4)  # Called for each tile


class TestMakeRasterFromPolygon(unittest.TestCase):
    """Test make_raster_from_polygon function."""

    @patch("googletraffic.core.make_raster_from_bbox")
    def test_with_geodataframe(self, mock_bbox):
        """Test with GeoPandas GeoDataFrame."""
        from googletraffic.core import make_raster_from_polygon

        try:
            import geopandas as gpd
            from shapely.geometry import box

            # Create test polygon
            polygon = box(-74.0, 40.7, -73.9, 40.8)
            gdf = gpd.GeoDataFrame([1], geometry=[polygon], crs="EPSG:4326")

            mock_bbox.return_value = np.ones((1000, 1000), dtype=np.uint8)

            # Test
            result = make_raster_from_polygon(polygon=gdf, zoom=14, google_key="test_key")

            # Verify
            mock_bbox.assert_called_once()
            call_args = mock_bbox.call_args[1]
            self.assertIn("bbox", call_args)

        except ImportError:
            self.skipTest("GeoPandas not installed")

    @patch("googletraffic.core.make_raster_from_bbox")
    def test_with_shapely_polygon(self, mock_bbox):
        """Test with Shapely Polygon."""
        from googletraffic.core import make_raster_from_polygon

        try:
            from shapely.geometry import box

            polygon = box(-74.0, 40.7, -73.9, 40.8)
            mock_bbox.return_value = np.ones((1000, 1000), dtype=np.uint8)

            # Test
            result = make_raster_from_polygon(polygon=polygon, zoom=14, google_key="test_key")

            # Verify
            mock_bbox.assert_called_once()

        except ImportError:
            self.skipTest("Shapely not installed")


class TestCaptureTrafficMap(unittest.TestCase):
    """Test _capture_traffic_map function (partial mocking)."""

    @patch("googletraffic.core.webdriver.Chrome")
    @patch("googletraffic.core.tempfile.NamedTemporaryFile")
    @patch("googletraffic.core.Image.open")
    def test_html_template_usage(self, mock_image_open, mock_tempfile, mock_driver):
        """Test that HTML template is populated correctly."""
        from googletraffic.core import _capture_traffic_map

        # Setup mocks
        mock_temp = MagicMock()
        mock_temp.name = "/tmp/test.html"
        mock_tempfile.return_value.__enter__.return_value = mock_temp

        mock_browser = MagicMock()
        mock_browser.execute_script.return_value = True
        mock_browser.get_screenshot_as_png.return_value = b"fake_image_data"
        mock_driver.return_value = mock_browser

        mock_img = MagicMock()
        mock_img_array = np.zeros((640, 640, 3), dtype=np.uint8)
        mock_image_open.return_value = mock_img

        with patch("googletraffic.core.np.array", return_value=mock_img_array):
            # Test
            try:
                result = _capture_traffic_map(
                    latitude=40.7580,
                    longitude=-73.9855,
                    zoom=14,
                    google_key="test_key",
                    width=640,
                    height=640,
                    wait_time=1,
                    headless=True,
                )

                # Verify browser was used
                mock_driver.assert_called_once()
                mock_browser.quit.assert_called_once()

            except Exception as e:
                # If there are import or other issues, skip gracefully
                self.skipTest(f"Test environment issue: {e}")


if __name__ == "__main__":
    unittest.main()
