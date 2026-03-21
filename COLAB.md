# Google Colab Setup Guide 📓

This guide provides step-by-step instructions for using **py-googletraffic** in Google Colab notebooks.

## Table of Contents
- [Overview](#overview)
- [One-Time Setup](#one-time-setup)
- [Complete Setup Code](#complete-setup-code)
- [Usage Example](#usage-example)
- [Common Issues](#common-issues)
- [Tips and Best Practices](#tips-and-best-practices)

## Overview

Google Colab is a free cloud-based Jupyter notebook environment. To use **py-googletraffic** in Colab, you need to:

1. Install Chrome and ChromeDriver
2. Install the py-googletraffic package and its dependencies
3. Configure Selenium for headless operation

The entire setup takes about 2-3 minutes on first run.

## One-Time Setup

Run this setup code **once** at the beginning of your Colab notebook:

### Step 1: Install System Dependencies

```python
# Install Chrome and ChromeDriver for Selenium
!apt-get update
!apt-get install -y chromium-chromedriver
!apt-get install -y chromium-browser

# Verify installation
!which chromium-browser
!which chromedriver
```

### Step 2: Install Python Packages

```python
# Install GDAL dependencies (required for rasterio)
!apt-get install -y gdal-bin libgdal-dev

# Set GDAL environment variables
import os
os.environ['GDAL_CONFIG'] = '/usr/bin/gdal-config'

# Install py-googletraffic from GitHub
!pip install git+https://github.com/kwahalf/py-googletraffic.git

# Alternative: Install from local clone
# !git clone https://github.com/kwahalf/py-googletraffic.git
# %cd py-googletraffic
# !pip install -e .
# %cd ..
```

### Step 3: Configure ChromeDriver Path

```python
# Add ChromeDriver to PATH (if not already available)
import sys
chromium_driver_path = '/usr/lib/chromium-browser/'
if chromium_driver_path not in sys.path:
    sys.path.insert(0, chromium_driver_path)
```

## Complete Setup Code

Copy and paste this complete setup block into your Colab notebook:

```python
# ============================================================================
# Google Colab Setup for py-googletraffic
# Run this cell once at the start of your notebook
# ============================================================================

# 1. Install Chrome and ChromeDriver
print("📦 Installing Chrome and ChromeDriver...")
!apt-get update -qq
!apt-get install -y chromium-chromedriver chromium-browser >/dev/null 2>&1

# 2. Install GDAL (required for geospatial operations)
print("📦 Installing GDAL...")
!apt-get install -y gdal-bin libgdal-dev >/dev/null 2>&1

# 3. Set environment variables
import os
os.environ['GDAL_CONFIG'] = '/usr/bin/gdal-config'

# 4. Install py-googletraffic
print("📦 Installing py-googletraffic...")
!pip install -q git+https://github.com/kwahalf/py-googletraffic.git

# 5. Verify installation
print("✅ Setup complete! Verifying installation...")
import googletraffic as gt
print(f"✅ py-googletraffic version: {gt.__version__}")
print("✅ Ready to use!")
```

## Usage Example

After running the setup, use **py-googletraffic** normally:

```python
import googletraffic as gt
import numpy as np
import matplotlib.pyplot as plt

# Set your Google Maps API key
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Create a traffic raster for New York City
print("🚦 Capturing traffic data...")
traffic_raster = gt.make_raster(
    location=(40.7580, -73.9855),  # Times Square, NYC
    height=800,
    width=800,
    zoom=14,
    google_key=GOOGLE_API_KEY,
    wait_time=3
)

print(f"✅ Raster shape: {traffic_raster.shape}")
print(f"✅ Traffic levels: {np.unique(traffic_raster)}")

# Visualize the traffic raster
plt.figure(figsize=(10, 10))
plt.imshow(traffic_raster, cmap='RdYlGn_r', interpolation='nearest')
plt.colorbar(label='Traffic Level (0=no data, 1=green, 2=orange, 3=red, 4=dark red)')
plt.title('Real-Time Traffic - Times Square, NYC')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()
```

### Save GeoTIFF to Google Drive

```python
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Create traffic raster and save to Drive
output_path = '/content/drive/MyDrive/traffic_nyc.tif'
gt.make_raster(
    location=(40.7580, -73.9855),
    height=1000,
    width=1000,
    zoom=14,
    google_key=GOOGLE_API_KEY,
    output_path=output_path
)

print(f"✅ Saved to: {output_path}")
```

### Create Traffic Raster from Bounding Box

```python
# Define a bounding box around Manhattan
bbox = {
    'xmin': -74.0479,  # West
    'xmax': -73.9067,  # East
    'ymin': 40.6829,   # South
    'ymax': 40.8820    # North
}

traffic_raster = gt.make_raster_from_bbox(
    bbox=bbox,
    height_px=1000,
    google_key=GOOGLE_API_KEY,
    zoom=12
)

# Visualize
plt.figure(figsize=(12, 8))
plt.imshow(traffic_raster, cmap='RdYlGn_r', interpolation='nearest')
plt.colorbar(label='Traffic Level')
plt.title('Manhattan Traffic Heatmap')
plt.tight_layout()
plt.show()
```

### Process Multiple Locations

```python
import time
from datetime import datetime

# Define multiple locations
locations = {
    'Times Square': (40.7580, -73.9855),
    'Central Park': (40.7829, -73.9654),
    'Brooklyn Bridge': (40.7061, -73.9969),
    'JFK Airport': (40.6413, -73.7781)
}

results = {}

for name, coords in locations.items():
    print(f"🚦 Capturing {name}...")
    
    raster = gt.make_raster(
        location=coords,
        height=500,
        width=500,
        zoom=14,
        google_key=GOOGLE_API_KEY
    )
    
    # Calculate average traffic level
    avg_traffic = raster[raster > 0].mean() if (raster > 0).any() else 0
    results[name] = avg_traffic
    
    print(f"   Average traffic level: {avg_traffic:.2f}")
    
    # Be respectful to Google's servers
    time.sleep(2)

# Visualize results
plt.figure(figsize=(10, 6))
plt.bar(results.keys(), results.values(), color=['green', 'orange', 'red', 'darkred'])
plt.ylabel('Average Traffic Level')
plt.title(f'Traffic Comparison - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

## Common Issues

### Issue 1: ChromeDriver Not Found

**Error:** `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solution:**
```python
# Reinstall ChromeDriver
!apt-get install -y chromium-chromedriver
!which chromedriver  # Verify installation
```

### Issue 2: GDAL Import Error

**Error:** `ImportError: libgdal.so.XX: cannot open shared object file`

**Solution:**
```python
# Reinstall GDAL
!apt-get install -y gdal-bin libgdal-dev
import os
os.environ['GDAL_CONFIG'] = '/usr/bin/gdal-config'
```

### Issue 3: Screenshot Size Mismatch

**Error:** Raster dimensions don't match requested size

**Solution:** This is automatically handled by the package. The image is resized to exact dimensions using high-quality interpolation.

### Issue 4: Timeout Waiting for Map to Load

**Error:** `TimeoutException: Message: Map did not load`

**Solution:**
```python
# Increase wait_time parameter
traffic_raster = gt.make_raster(
    location=(40.7580, -73.9855),
    height=1000,
    width=1000,
    zoom=14,
    google_key=GOOGLE_API_KEY,
    wait_time=5  # Increase from default 3 to 5 seconds
)
```

### Issue 5: API Key Issues

**Error:** `Error loading Google Maps` or blank screenshots

**Solution:**
1. Verify your API key is correct
2. Enable "Maps JavaScript API" in Google Cloud Console
3. Check API key restrictions and quotas
4. Ensure billing is enabled (Google requires it even for free tier)

### Issue 6: SessionNotCreatedException (Chrome Instance Exited)

**Error:** `selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome failed to start: exited normally`

**Cause:** Google Colab runs in a containerized environment that requires specific Chrome flags to prevent the browser from exiting prematurely.

**Solution:** The package automatically includes the necessary Chrome flags for Colab compatibility:
- `--disable-setuid-sandbox` - Required for containerized environments
- `--remote-debugging-port=9222` - Enables remote debugging in restricted environments
- `--disable-extensions` - Prevents extension-related crashes
- `--disable-software-rasterizer` - Improves stability in headless mode

These flags are already configured in the package (version 0.1.0+). If you're still experiencing this error:

```python
# Update to the latest version
!pip install --upgrade py-googletraffic

# Restart the runtime
# Runtime → Restart runtime
```

If the issue persists, verify Chrome and ChromeDriver are properly installed:

```python
!google-chrome --version
!chromedriver --version
```

## Tips and Best Practices

### 1. Store API Key Securely

Don't hardcode your API key in notebooks that you share:

```python
from google.colab import userdata

# Store in Colab Secrets (Settings → Secrets → Add new secret)
GOOGLE_API_KEY = userdata.get('GOOGLE_MAPS_API_KEY')
```

Or use environment variables:

```python
import os
from getpass import getpass

# Prompt for API key (won't be visible when typing)
if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = getpass('Enter Google Maps API Key: ')

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
```

### 2. Monitor API Usage

```python
# Track how many API calls you're making
import time

start_time = time.time()
api_calls = 0

for location in locations:
    raster = gt.make_raster(location=location, ...)
    api_calls += 1
    time.sleep(2)  # Rate limiting

elapsed = time.time() - start_time
print(f"Made {api_calls} API calls in {elapsed:.1f} seconds")
```

### 3. Cache Results

Save results to avoid repeated API calls:

```python
import pickle
from pathlib import Path

cache_file = '/content/traffic_cache.pkl'

# Load from cache if exists
if Path(cache_file).exists():
    with open(cache_file, 'rb') as f:
        traffic_raster = pickle.load(f)
    print("✅ Loaded from cache")
else:
    # Fetch new data
    traffic_raster = gt.make_raster(...)
    
    # Save to cache
    with open(cache_file, 'wb') as f:
        pickle.dump(traffic_raster, f)
    print("✅ Saved to cache")
```

### 4. Optimize for Colab's Runtime Limits

Google Colab sessions have time limits. For long-running analyses:

```python
# Save intermediate results to Google Drive
from google.colab import drive
drive.mount('/content/drive')

checkpoint_dir = '/content/drive/MyDrive/traffic_checkpoints/'
os.makedirs(checkpoint_dir, exist_ok=True)
```

### 5. Visualize with Interactive Maps

```python
import folium
from folium import plugins

# Create interactive map
m = folium.Map(location=[40.7580, -73.9855], zoom_start=14)

# Add traffic raster as overlay (requires conversion to image)
# For better interactivity, plot individual points instead

m
```

### 6. Export for Further Analysis

```python
# Export as CSV for analysis in other tools
import pandas as pd

# Convert raster to DataFrame
h, w = traffic_raster.shape
df = pd.DataFrame({
    'row': np.repeat(np.arange(h), w),
    'col': np.tile(np.arange(w), h),
    'traffic_level': traffic_raster.flatten()
})

df.to_csv('/content/drive/MyDrive/traffic_data.csv', index=False)
print("✅ Exported to CSV")
```

## Performance Considerations

### Memory Usage

Google Colab provides ~12-13 GB RAM. For large rasters:

```python
# Monitor memory usage
!free -h

# For very large areas, use tiling
traffic_raster = gt.make_raster_from_bbox(
    bbox=large_bbox,
    height_px=2000,  # Automatically split into tiles
    google_key=GOOGLE_API_KEY,
    zoom=15
)
```

### Processing Time

- Single 1000×1000 raster: ~5-10 seconds
- Bbox with tiling: ~20-60 seconds depending on size
- Multiple locations: Scale linearly + add delays

### Free Tier Limits

- Google Maps API: $200 free credit/month (~28,000 map loads)
- Colab GPU/TPU: Not needed for this package
- Colab session: 12 hours max runtime

## Complete Working Example

Here's a complete notebook you can copy and run:

```python
# ============================================================================
# Complete Google Colab Example - NYC Traffic Analysis
# ============================================================================

# 1. SETUP (Run once)
print("📦 Installing dependencies...")
!apt-get update -qq
!apt-get install -y chromium-chromedriver chromium-browser gdal-bin libgdal-dev >/dev/null 2>&1

import os
os.environ['GDAL_CONFIG'] = '/usr/bin/gdal-config'

!pip install -q git+https://github.com/kwahalf/py-googletraffic.git

# 2. IMPORTS
import googletraffic as gt
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 3. CONFIGURATION
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your key

# 4. CAPTURE TRAFFIC DATA
print("🚦 Capturing traffic data for Times Square...")
traffic_raster = gt.make_raster(
    location=(40.7580, -73.9855),
    height=1000,
    width=1000,
    zoom=14,
    google_key=GOOGLE_API_KEY
)

# 5. ANALYZE
print(f"✅ Raster shape: {traffic_raster.shape}")
print(f"✅ Traffic levels present: {np.unique(traffic_raster)}")
print(f"✅ Average traffic: {traffic_raster[traffic_raster > 0].mean():.2f}")

# Calculate statistics
total_pixels = traffic_raster.size
traffic_pixels = (traffic_raster > 0).sum()
coverage = 100 * traffic_pixels / total_pixels

print(f"\n📊 Statistics:")
print(f"   Total pixels: {total_pixels:,}")
print(f"   Traffic pixels: {traffic_pixels:,} ({coverage:.1f}%)")
for level in range(1, 5):
    count = (traffic_raster == level).sum()
    pct = 100 * count / traffic_pixels if traffic_pixels > 0 else 0
    print(f"   Level {level}: {count:,} pixels ({pct:.1f}%)")

# 6. VISUALIZE
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Traffic heatmap
im = axes[0].imshow(traffic_raster, cmap='RdYlGn_r', interpolation='nearest', vmin=0, vmax=4)
axes[0].set_title(f'Times Square Traffic - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
plt.colorbar(im, ax=axes[0], label='Traffic Level')

# Traffic distribution
levels = ['No data', 'Green', 'Orange', 'Red', 'Dark Red']
colors_viz = ['gray', 'green', 'orange', 'red', 'darkred']
counts = [np.sum(traffic_raster == i) for i in range(5)]

axes[1].bar(levels, counts, color=colors_viz)
axes[1].set_ylabel('Pixel Count')
axes[1].set_title('Traffic Level Distribution')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

print("\n✅ Analysis complete!")
```

## Additional Resources

- **Main Documentation:** [README.md](README.md)
- **Installation Guide:** [INSTALLATION.md](INSTALLATION.md)
- **Quick Start Guide:** [QUICKSTART.md](QUICKSTART.md)
- **API Documentation:** Coming soon
- **Example Notebooks:** [examples/](examples/)

## Getting Help

If you encounter issues:

1. Check [Common Issues](#common-issues) section above
2. Verify all setup steps were completed
3. Check the GitHub issues page
4. Create a new issue with:
   - Your Colab notebook code
   - Complete error message
   - Python version: `!python --version`
   - Package version: `import googletraffic as gt; print(gt.__version__)`

---

**Happy mapping! 🗺️🚦**
