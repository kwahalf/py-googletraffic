# 🚀 Quick Start Guide

Get up and running with py-googletraffic in 5 minutes!

> **� Google Colab Users:** Use the [Google Colab Setup Guide](COLAB.md) and skip Steps 1-2  
> **💻 Windows Users:** For a complete Windows-specific guide, see [WINDOWS.md](WINDOWS.md)

## Step 1: Install Dependencies (2 minutes)

**macOS:**
```bash
brew install chromedriver
chromedriver --version  # Verify
```

**Ubuntu/Debian:**
```bash
sudo apt-get install chromium-chromedriver
chromedriver --version  # Verify
```

**Windows:**
1. Download ChromeDriver: https://chromedriver.chromium.org/
2. Extract `chromedriver.exe` to `C:\chromedriver`
3. Add `C:\chromedriver` to your PATH (see [detailed instructions](INSTALLATION.md))
4. Or place `chromedriver.exe` in your project folder
5. Verify in Command Prompt: `chromedriver --version`

## Step 2: Install Package (1 minute)

**macOS/Linux:**
```bash
cd /path/to/py-googletraffic
source venv/bin/activate  # If using virtual environment
pip install -e .
python -c "import googletraffic as gt; print('✓ Installed version:', gt.__version__)"
```

**Windows (Command Prompt):**
```cmd
cd C:\path\to\py-googletraffic
venv\Scripts\activate.bat
pip install -e .
python -c "import googletraffic as gt; print('✓ Installed version:', gt.__version__)"
```

**Windows (PowerShell):**
```powershell
cd C:\path\to\py-googletraffic
venv\Scripts\Activate.ps1
pip install -e .
python -c "import googletraffic as gt; print('✓ Installed version:', gt.__version__)"
```

## Step 3: Get Google Maps API Key (1 minute)

1. Go to https://console.cloud.google.com/
2. Create/select project
3. Enable "Maps JavaScript API"
4. Create API key
5. Set environment variable:

**macOS/Linux:**
```bash
export GOOGLE_MAPS_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
setx GOOGLE_MAPS_API_KEY "your_api_key_here"
:: Restart command prompt
```

**Windows (PowerShell):**
```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_MAPS_API_KEY', 'your_api_key_here', 'User')
# Restart PowerShell
```

## Step 4: Run Your First Example (1 minute)

Create a file `test.py`:

```python
import googletraffic as gt
import os

# Get your API key
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Create traffic raster for Times Square
traffic = gt.make_raster(
    location=(40.7580, -73.9855),  # Times Square, NYC
    height=500,
    width=500,
    zoom=14,
    google_key=api_key
)

print(f"✓ Success! Created traffic raster: {traffic.shape}")
print(f"✓ Traffic levels found: {set(traffic.flatten())}")
```

Run it:
```bash
python test.py
```

## Step 5: Try Jupyter Notebook

```bash
# Launch Jupyter
jupyter notebook

# Open: examples/getting_started.ipynb
# Set your API key in cell 3
# Run all cells!
```

## Common First Commands

### Create and Save Traffic Map
```python
import googletraffic as gt

# Save as GeoTIFF
gt.make_raster(
    location=(40.7128, -74.0060),  # NYC
    height=1000,
    width=1000,
    zoom=14,
    google_key="YOUR_KEY",
    output_path="nyc_traffic.tif"
)
```

### Visualize in Matplotlib
```python
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

traffic = gt.make_raster(
    location=(40.7128, -74.0060),
    height=1000,
    width=1000,
    zoom=14,
    google_key="YOUR_KEY"
)

colors = ['white', 'green', 'orange', 'red', 'darkred']
plt.imshow(traffic, cmap=ListedColormap(colors), vmin=0, vmax=4)
plt.colorbar(label='Traffic Level')
plt.title('NYC Traffic')
plt.show()
```

### Analyze Traffic Patterns
```python
import numpy as np

# Get traffic statistics
traffic_pixels = traffic[traffic > 0]
print(f"Mean traffic: {traffic_pixels.mean():.2f}")
print(f"Congested: {(traffic >= 3).sum() / (traffic > 0).sum() * 100:.1f}%")

# Count by level
for level in range(1, 5):
    count = (traffic == level).sum()
    print(f"Level {level}: {count} pixels")
```

## Troubleshooting

❌ **"chromedriver not found"**  
→ Install ChromeDriver (see Step 1)

❌ **"API key invalid"**  
→ Check key is correct, Maps JavaScript API is enabled

❌ **"No module named 'googletraffic'"**  
→ Run `pip install -e .` in project directory

❌ **Browser crashes**  
→ Try increasing `wait_time=10` or `headless=False`

## What's Next?

✅ Review [README.md](README.md) for detailed documentation  
✅ Check [INSTALLATION.md](INSTALLATION.md) for advanced setup  
✅ Explore [examples/getting_started.ipynb](examples/getting_started.ipynb)  
✅ Run [examples/simple_example.py](examples/simple_example.py)

## Quick Reference

### Zoom Levels
- 10-12: Regional (metro areas)
- 13-15: City (neighborhoods) ⭐ **Recommended**
- 16-18: Street level

### Traffic Levels
- 1 = 🟢 Green (no traffic)
- 2 = 🟠 Orange (medium)
- 3 = 🔴 Red (high)
- 4 = 🔴 Dark Red (heavy)

### Key Functions
- `make_raster()` - Traffic around a point
- `make_raster_from_bbox()` - Traffic in bounding box
- `make_raster_from_polygon()` - Traffic in polygon

## Need Help?

- 📖 Full docs: [README.md](README.md)
- 🐛 Issues: https://github.com/yourusername/py-googletraffic/issues
- 💬 Questions: Open a discussion on GitHub

Happy mapping! 🗺️🚦
