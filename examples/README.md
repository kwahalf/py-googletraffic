# Examples 📚

This directory contains example code and notebooks demonstrating how to use **py-googletraffic**.

## Available Examples

### 1. Simple Python Script ([simple_example.py](simple_example.py))

Basic Python script showing the core functionality:
- Capture traffic data for a single location
- Save as GeoTIFF
- Minimal dependencies

**Best for:** Quick testing, automation scripts, production code

**Run it:**
```bash
python examples/simple_example.py
```

### 2. Getting Started Notebook ([getting_started.ipynb](getting_started.ipynb))

Comprehensive Jupyter notebook with:
- All three main functions (point, bbox, polygon)
- Visualization examples
- Data analysis techniques
- Best practices

**Best for:** Learning the package, local development, data exploration

**Run it:**
```bash
jupyter notebook examples/getting_started.ipynb
```

### 3. Google Colab Example ([google_colab_example.ipynb](google_colab_example.ipynb)) ☁️

Cloud-ready notebook specifically designed for Google Colab:
- Complete Colab setup instructions included
- No local installation required
- Google Drive integration
- Multi-location comparison examples
- Time series analysis

**Best for:** Cloud-based analysis, sharing with collaborators, no local setup

**Run it:**
1. Upload to Google Colab or open directly:
   - **Option A:** Go to [Google Colab](https://colab.research.google.com/)
   - Click **File → Upload notebook**
   - Upload `google_colab_example.ipynb`
   
2. **Option B:** Direct link (if you've published the notebook):
   ```
   https://colab.research.google.com/github/kwahalf/py-googletraffic/blob/main/examples/google_colab_example.ipynb
   ```

3. Run all cells in order
4. Enter your Google Maps API key when prompted

> **📓 See the complete [Google Colab Setup Guide](../COLAB.md) for detailed instructions**

## Prerequisites

### For Local Examples (simple_example.py, getting_started.ipynb)

1. **Install py-googletraffic:**
   ```bash
   # Option A: From PyPI (recommended)
   pip install py-googletraffic
   
   # Option B: From source (for development)
   pip install -e .  # From the repository root
   ```

2. **Get a Google Maps API Key:**
   - Visit: https://developers.google.com/maps/get-started
   - Enable "Maps JavaScript API"
   - Copy your API key

3. **Set your API key in the examples:**
   - Edit the example file
   - Replace `"YOUR_API_KEY_HERE"` with your actual key

### For Google Colab Example (google_colab_example.ipynb)

1. **Google account** (for Colab access)
2. **Google Maps API Key** (see above)
3. No local installation required!

## Usage Tips

### Secure API Key Storage

Don't hardcode your API key in shared code. Instead:

**Option 1: Environment Variable**
```python
import os
GOOGLE_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
```

Set it before running:
```bash
export GOOGLE_MAPS_API_KEY="your_key_here"
python examples/simple_example.py
```

**Option 2: Config File** (don't commit to git)
```python
# config.py (add to .gitignore)
GOOGLE_API_KEY = "your_key_here"

# In your script
from config import GOOGLE_API_KEY
```

**Option 3: Colab Secrets** (for Google Colab)
```python
from google.colab import userdata
GOOGLE_API_KEY = userdata.get('GOOGLE_MAPS_API_KEY')
```

### Customize Examples

All examples are designed to be modified:

1. **Change locations:**
   ```python
   location = (YOUR_LAT, YOUR_LNG)  # Your city
   ```

2. **Adjust resolution:**
   ```python
   height=2000,  # Higher = more detail
   width=2000,
   zoom=16,      # 11-13=city, 14-16=neighborhood, 17-20=street
   ```

3. **Modify wait time:**
   ```python
   wait_time=5  # Increase if traffic layer loads slowly
   ```

## Example Output

All examples produce:
- **NumPy arrays** with traffic levels (0-4)
- **GeoTIFF files** (if `output_path` specified)
- **Visualizations** (in notebooks)

Example output structure:
```
traffic_raster
├── shape: (1000, 1000)
├── dtype: uint8
└── values: 0=no data, 1=green, 2=orange, 3=red, 4=dark red
```

## Troubleshooting

### Common Issues

**Error: `No module named 'googletraffic'`**
```bash
# Install the package first
pip install py-googletraffic

# Or from source:
# cd /path/to/py-googletraffic
# pip install -e .
```

**Error: `'chromedriver' executable needs to be in PATH`**
- See [INSTALLATION.md](../INSTALLATION.md) for ChromeDriver setup
- Or use [Google Colab](google_colab_example.ipynb) (no ChromeDriver needed)

**Error: `Error loading Google Maps`**
- Verify your API key is correct
- Enable "Maps JavaScript API" in Google Cloud Console
- Check API quotas/billing

**Blank or incorrect raster**
- Increase `wait_time` parameter (try 5-10 seconds)
- Check internet connection
- Verify location coordinates are correct

## Next Steps

After trying the examples:

1. **Read the guides:**
   - [Quick Start Guide](../QUICKSTART.md)
   - [Installation Guide](../INSTALLATION.md)
   - [Google Colab Guide](../COLAB.md)

2. **Explore advanced features:**
   - Custom polygons with `make_raster_from_polygon()`
   - Time series analysis (capture same location multiple times)
   - Integration with GeoPandas/Shapely

3. **Build your own analysis:**
   - Traffic monitoring dashboards
   - Route optimization
   - Urban planning studies
   - Real estate analysis

## Contributing

Have a cool example? We'd love to include it!

1. Create your example script/notebook
2. Add documentation in the code
3. Test it thoroughly
4. Submit a pull request

## Support

- 📖 [Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/kwahalf/py-googletraffic/issues)
- 💬 [Discussions](https://github.com/kwahalf/py-googletraffic/discussions)

---

**Happy mapping! 🗺️🚦**
