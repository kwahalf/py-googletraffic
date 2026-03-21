# py-googletraffic 🚦

Python package for creating georeferenced traffic rasters from Google Maps traffic data.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Colab](https://img.shields.io/badge/Google%20Colab-Supported-orange.svg)](COLAB.md)

## Overview

**py-googletraffic** is a Python package that extracts real-time traffic information from Google Maps and converts it into georeferenced raster datasets. This enables spatial analysis of traffic patterns, integration with other geospatial data, and visualization in GIS software or Jupyter notebooks.

Inspired by the R package [googletraffic](https://github.com/dime-worldbank/googletraffic), this Python implementation provides:

- 🗺️ **Georeferenced rasters** from Google Maps traffic data
- 🎨 **4-level traffic classification** (no traffic, medium, high, heavy)
- 📦 **GeoTIFF export** for use in QGIS, ArcGIS, etc.
- 📊 **Jupyter notebook integration** for interactive analysis
- 🌍 **Flexible spatial inputs** (points, bounding boxes, polygons)

### Traffic Levels

Traffic is classified into 4 levels based on Google Maps colors:

| Level | Color | Description |
|-------|-------|-------------|
| 1 | 🟢 Green | No traffic delays |
| 2 | 🟠 Orange | Medium traffic |
| 3 | 🔴 Red | High traffic |
| 4 | 🔴 Dark Red | Heavy traffic |

## Platform Support

**py-googletraffic** works on multiple platforms:

- 💻 **Local Development:** Windows, macOS, Linux
- 📓 **Jupyter Notebooks:** Local or JupyterHub environments  
- ☁️ **Google Colab:** Full cloud-based support ([Setup Guide](COLAB.md))
- 🐳 **Docker:** Can be containerized for deployment

> **📓 Google Colab Users:** See the complete [Google Colab Setup Guide](COLAB.md) for cloud-based installation and usage examples.

## Installation

> **📌 Platform-Specific Guides:**
> - **Windows:** [Windows Setup Guide](WINDOWS.md)
> - **Google Colab:** [Colab Setup Guide](COLAB.md)  
> - **General:** [Complete Installation Guide](INSTALLATION.md)

### Prerequisites

> **Note:** Google Colab users can skip this section and follow the [Colab Setup Guide](COLAB.md) instead.

1. **Python 3.8+**
2. **ChromeDriver** (for Selenium browser automation):
   ```bash
   # macOS
   brew install chromedriver
   
   # Ubuntu/Debian
   sudo apt-get install chromium-chromedriver
   
   # Windows: Download from https://chromedriver.chromium.org/
   # Extract chromedriver.exe and add to PATH
   # See detailed instructions: WINDOWS.md or INSTALLATION.md
   ```

3. **Google Maps API Key** with Maps JavaScript API enabled:
   - Get one at: https://developers.google.com/maps/get-started
   - Enable the "Maps JavaScript API" for your project

### Install Package

```bash
# Clone the repository
git clone https://github.com/yourusername/py-googletraffic.git
cd py-googletraffic

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows (Command Prompt):
# venv\Scripts\activate.bat
# Windows (PowerShell):
# venv\Scripts\Activate.ps1

# Install in development mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

## Try It Now! 🚀

**Want to try without installing anything?** Open our interactive Google Colab notebook:

👉 **[Open in Google Colab](examples/google_colab_example.ipynb)** 👈

The Colab notebook includes:
- ✅ Complete setup instructions (no local installation needed)
- ✅ Interactive examples with visualizations
- ✅ Multi-location traffic comparison
- ✅ Save results to Google Drive

See the [Google Colab Setup Guide](COLAB.md) for more details.

## Quick Start

### Basic Example

```python
import googletraffic as gt

# Set your Google Maps API key
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Create a traffic raster around Times Square, NYC
traffic_raster = gt.make_raster(
    location=(40.7580, -73.9855),  # (latitude, longitude)
    height=1000,
    width=1000,
    zoom=14,
    google_key=GOOGLE_API_KEY
)

print(traffic_raster.shape)  # (1000, 1000)
```

### Save as GeoTIFF

```python
# Create and save as georeferenced GeoTIFF
output_path = gt.make_raster(
    location=(40.7580, -73.9855),
    height=1000,
    width=1000,
    zoom=14,
    google_key=GOOGLE_API_KEY,
    output_path="nyc_traffic.tif"
)
```

### Visualize in Jupyter

```python
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Define colors matching Google Maps
colors = ['white', 'green', 'orange', 'red', 'darkred']
cmap = ListedColormap(colors)

plt.figure(figsize=(10, 10))
plt.imshow(traffic_raster, cmap=cmap, vmin=0, vmax=4)
plt.colorbar(label='Traffic Level')
plt.title('Traffic Conditions')
plt.show()
```

## Usage

### 1. Traffic Raster Around a Point

Create a traffic raster centered at specific coordinates:

```python
traffic = gt.make_raster(
    location=(latitude, longitude),
    height=2000,          # Height in pixels
    width=2000,           # Width in pixels
    zoom=16,              # Zoom level (0-20)
    google_key=API_KEY,
    output_path=None,     # Return numpy array
    wait_time=3,          # Seconds to wait for traffic layer
    headless=True         # Run browser in headless mode
)
```

**Zoom Level Guidelines:**
- **10-12**: Regional view (metro areas)
- **13-15**: City-level (neighborhoods)
- **16-18**: Street-level detail

### 2. Traffic Raster from Bounding Box

Create a traffic raster for a specific geographic area:

```python
# Define bounding box (west, south, east, north)
bbox = (-74.02, 40.70, -73.97, 40.73)

traffic = gt.make_raster_from_bbox(
    bbox=bbox,
    zoom=14,
    google_key=API_KEY,
    output_path="area_traffic.tif"
)
```

For large areas, the function automatically splits the region into multiple tiles.

### 3. Traffic Raster from Polygon

Create a traffic raster covering a polygon area:

```python
import geopandas as gpd

# Load polygon (e.g., city boundary)
gdf = gpd.read_file("city_boundary.geojson")

traffic = gt.make_raster_from_polygon(
    polygon=gdf,
    zoom=14,
    google_key=API_KEY,
    output_path="city_traffic.tif"
)
```

## Examples

Check out the Jupyter notebook in [examples/getting_started.ipynb](examples/getting_started.ipynb) for comprehensive examples including:

- Creating and visualizing traffic rasters
- Statistical analysis of traffic patterns
- Time-series traffic monitoring
- Integration with other geospatial data
- Working with GeoTIFFs in rasterio

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes (all platforms)
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide (macOS/Linux/Windows)
- **[WINDOWS.md](WINDOWS.md)** - 🪟 Complete Windows setup guide with troubleshooting
- **[examples/getting_started.ipynb](examples/getting_started.ipynb)** - Interactive Jupyter tutorial
- **[examples/simple_example.py](examples/simple_example.py)** - Simple Python script example

**Which guide should I read?**
- First time user? → Start with [QUICKSTART.md](QUICKSTART.md)
- Windows user? → Follow [WINDOWS.md](WINDOWS.md)
- Installation issues? → Check [INSTALLATION.md](INSTALLATION.md)
- Want to learn features? → Try [getting_started.ipynb](examples/getting_started.ipynb)

## API Costs

Google Maps API pricing:
- **Cost**: $7 per 1,000 queries (Maps JavaScript API)
- **Free tier**: $200/month credit = ~28,571 free queries
- **Note**: Large areas require multiple API calls

To minimize costs:
- Use appropriate zoom levels (lower zoom = fewer tiles needed)
- Adjust `max_pixels` parameter
- Cache results for repeated analyses

Learn more: https://mapsplatform.google.com/pricing/

## Advanced Usage

### Time Series Analysis

Capture traffic at different times:

```python
from datetime import datetime
import time

timestamps = []
traffic_snapshots = []

for i in range(24):  # Capture every hour for a day
    timestamp = datetime.now()
    traffic = gt.make_raster(
        location=(40.7580, -73.9855),
        height=1000,
        width=1000,
        zoom=14,
        google_key=API_KEY
    )
    
    timestamps.append(timestamp)
    traffic_snapshots.append(traffic)
    
    time.sleep(3600)  # Wait 1 hour
```

### Custom Traffic Analysis

```python
import numpy as np

# Calculate congestion statistics
traffic_pixels = traffic_raster[traffic_raster > 0]
mean_traffic = traffic_pixels.mean()
congestion_percentage = (np.sum(traffic_raster >= 3) / 
                         np.sum(traffic_raster > 0)) * 100

print(f"Mean traffic level: {mean_traffic:.2f}")
print(f"Congested areas: {congestion_percentage:.1f}%")
```

### Integration with Other Data

```python
import rasterio
import geopandas as gpd

# Load traffic raster
with rasterio.open("traffic.tif") as src:
    traffic = src.read(1)
    transform = src.transform

# Load points of interest
pois = gpd.read_file("restaurants.geojson")

# Extract traffic values at POI locations
from rasterio.transform import rowcol
traffic_at_pois = []

for idx, poi in pois.iterrows():
    row, col = rowcol(transform, poi.geometry.x, poi.geometry.y)
    if 0 <= row < traffic.shape[0] and 0 <= col < traffic.shape[1]:
        traffic_at_pois.append(traffic[row, col])

pois['traffic_level'] = traffic_at_pois
```

## How It Works

1. **HTML Generation**: Creates an HTML page with Google Maps JavaScript API
2. **Browser Automation**: Uses Selenium to load the page with traffic layer
3. **Screenshot Capture**: Takes a screenshot of the map with traffic overlay
4. **Color Classification**: Identifies traffic colors (green, orange, red, dark red)
5. **Georeferencing**: Converts pixel coordinates to geographic coordinates
6. **Raster Creation**: Generates a georeferenced raster in GeoTIFF format

## Comparison to R Package

| Feature | py-googletraffic (Python) | googletraffic (R) |
|---------|---------------------------|-------------------|
| Language | Python | R |
| Output Format | NumPy array, GeoTIFF | R raster object |
| Jupyter Support | ✅ Native | ⚠️ Via IRkernel |
| Dependencies | Selenium, Rasterio | rvest, magick |
| Polygon Support | ✅ GeoPandas | ✅ sf/sp |
| API Efficiency | Similar | Similar |

## Alternatives

### Mapbox Traffic API

The [mapboxapi](https://walker-data.com/mapboxapi/) package (R) and Mapbox API provide vector traffic data:

**Pros:**
- Vector format (polylines)
- Speed information available
- More detailed road network

**Cons:**
- Requires more API calls for large areas
- Different pricing model
- Different data format

## Troubleshooting

### ChromeDriver Issues

**macOS/Linux:**
```bash
# Check if ChromeDriver is installed
which chromedriver

# If not found, install it:
# macOS
brew install chromedriver

# Ubuntu
sudo apt-get install chromium-chromedriver
```

**Windows:**
```cmd
:: Check if ChromeDriver is in PATH
where chromedriver

:: If not found:
:: 1. Download from https://chromedriver.chromium.org/
:: 2. Extract chromedriver.exe to C:\chromedriver
:: 3. Add C:\chromedriver to PATH
:: Or place chromedriver.exe in your project folder
```

**Version mismatch:**
- Check Chrome version: `chrome://version` in browser
- Download matching ChromeDriver version
- On Windows, ensure no spaces in installation path

### API Key Issues

- Ensure Maps JavaScript API is enabled in Google Cloud Console
- Check API key restrictions and quotas
- Verify billing is enabled for your project
- **Windows**: Check for extra spaces when setting environment variable

### Traffic Layer Not Loading

- Increase `wait_time` parameter (try 5-10 seconds)
- Use `headless=False` to see what's happening in the browser
- Check internet connection and Google Maps availability
- **Windows**: Check if firewall/antivirus is blocking Chrome

### Memory Issues with Large Areas

- Reduce `max_pixels` parameter
- Process area in smaller chunks
- Use lower zoom levels

### Windows-Specific Issues

**PowerShell script execution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path too long errors:**
- Move project closer to drive root (e.g., `C:\dev\py-googletraffic`)
- Or enable long path support (requires admin)

**GDAL/Rasterio installation:**
- Use Conda: `conda install -c conda-forge rasterio`
- Or download pre-built wheels from: https://www.lfd.uci.edu/~gohlke/pythonlibs/

**See [INSTALLATION.md](INSTALLATION.md) for detailed Windows troubleshooting.**

## Testing

py-googletraffic includes a comprehensive test suite using nose2/pytest.

### Running Tests

**Quick start:**
```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
nose2

# Run with coverage
nose2 --with-coverage

# Or use pytest
pytest --cov=googletraffic
```

**Using the test runner:**
```bash
# Run with test script
python run_tests.py --coverage

# Run specific tests
python run_tests.py --pattern test_utils

# Use different runner
python run_tests.py --runner pytest
```

**Using Make:**
```bash
# Run tests
make test

# Run with coverage
make test-cov

# Run with pytest
make test-pytest
```

### Test Structure

- `tests/test_constants.py` - Tests for traffic colors and constants
- `tests/test_utils.py` - Tests for utility functions and calculations
- `tests/test_core.py` - Tests for core functions (using mocks)

See [tests/README.md](tests/README.md) for detailed testing documentation.

### Continuous Integration

Tests run automatically on GitHub Actions for every push and pull request. See `.github/workflows/tests.yml` for configuration.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`make test` or `nose2`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/py-googletraffic.git
cd py-googletraffic

# Install with dev dependencies
pip install -e ".[dev,test]"

# Run tests
make test

# Format code
make format

# Run linter
make lint
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{py-googletraffic,
  title = {py-googletraffic: Python Package for Google Maps Traffic Data},
  author = {{py-googletraffic Contributors}},
  year = {2026},
  url = {https://github.com/yourusername/py-googletraffic}
}
```

## Acknowledgments

- Inspired by the [googletraffic R package](https://github.com/dime-worldbank/googletraffic) by DIME World Bank
- Uses the Google Maps JavaScript API
- Built with Selenium, Rasterio, and GeoPandas

## Related Projects

- [googletraffic](https://github.com/dime-worldbank/googletraffic) - Original R implementation
- [mapboxapi](https://walker-data.com/mapboxapi/) - R package for Mapbox traffic data
- [OSMnx](https://github.com/gboeing/osmnx) - Python for street networks from OpenStreetMap

## Contact

For questions, issues, or suggestions, please [open an issue](https://github.com/yourusername/py-googletraffic/issues) on GitHub.
Create Georeferenced Traffic Data from the Google Maps  API
