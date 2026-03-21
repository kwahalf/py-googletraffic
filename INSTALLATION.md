# Installation and Setup Guide

Complete guide to installing and setting up py-googletraffic.

## Quick Links

- 📓 **Google Colab Users:** Skip this guide and use the [Google Colab Setup Guide](COLAB.md) instead
- 💻 **Windows Users:** See platform-specific notes in the [Windows Setup Guide](WINDOWS.md)
- 🚀 **After installation:** Jump to the [Quick Start Guide](QUICKSTART.md)

---

## Prerequisites

### 1. Python Environment

Ensure you have Python 3.8 or higher:

```bash
python --version
# Should show 3.8 or higher
```

If you need to install Python:
- **macOS**: `brew install python3`
- **Ubuntu/Debian**: `sudo apt-get install python3 python3-pip`
- **Windows**: Download from [python.org](https://python.org)

### 2. Install ChromeDriver

ChromeDriver is required for Selenium browser automation.

#### macOS
```bash
# Using Homebrew
brew install chromedriver

# Verify installation
which chromedriver
```

#### Ubuntu/Debian
```bash
# Install chromium and chromedriver
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver

# Verify installation
which chromedriver
```

#### Windows
1. Download ChromeDriver from https://chromedriver.chromium.org/
   - Choose the version matching your Chrome browser
   - Download `chromedriver_win32.zip`

2. Extract to a folder (e.g., `C:\chromedriver`)

3. Add the folder to your PATH:
   - Open "Environment Variables" settings:
     - Press `Win + R`, type `sysdm.cpl`, press Enter
     - Click "Environment Variables"
   - Under "User variables" or "System variables", find "Path"
   - Click "Edit" → "New"
   - Add the path: `C:\chromedriver`
   - Click "OK" on all dialogs

4. Restart your command prompt/PowerShell

**Alternative: Add to project directory**
```powershell
# Download and place chromedriver.exe in your project folder
# Python will find it in the current directory
```

#### Verify ChromeDriver
```bash
# Command Prompt or PowerShell
chromedriver --version
# Should show version number

# If not found, test in project directory:
cd C:\path\to\py-googletraffic
.\chromedriver.exe --version
```

### 3. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Maps JavaScript API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Maps JavaScript API"
   - Click "Enable"
4. Create API key:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy your API key

#### Secure Your API Key

**Option 1: Environment Variable (Recommended)**

*macOS/Linux:*
```bash
# Add to ~/.bashrc or ~/.zshrc
export GOOGLE_MAPS_API_KEY="your_api_key_here"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

*Windows (Command Prompt - Permanent):*
```cmd
:: Set user environment variable
setx GOOGLE_MAPS_API_KEY "your_api_key_here"

:: Restart command prompt for changes to take effect
```

*Windows (PowerShell - Permanent):*
```powershell
# Set user environment variable
[System.Environment]::SetEnvironmentVariable('GOOGLE_MAPS_API_KEY', 'your_api_key_here', 'User')

# Restart PowerShell for changes to take effect
```

*Windows (Temporary - Current Session):*
```cmd
:: Command Prompt
set GOOGLE_MAPS_API_KEY=your_api_key_here

:: PowerShell
$env:GOOGLE_MAPS_API_KEY="your_api_key_here"
```

**Option 2: .env File**

```bash
# Create .env file in project root
echo "GOOGLE_MAPS_API_KEY=your_api_key_here" > .env

# In Python:
# from dotenv import load_dotenv
# import os
# load_dotenv()
# api_key = os.getenv('GOOGLE_MAPS_API_KEY')
```

**⚠️ Never commit API keys to version control!**

## Installation

### Option 1: Install from Source (Development)

#### macOS/Linux:
```bash
# Clone the repository
git clone https://github.com/kwahalf/py-googletraffic.git
cd py-googletraffic

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install package in development mode
pip install -e .
```

#### Windows (Command Prompt):
```cmd
:: Clone the repository
git clone https://github.com/kwahalf/py-googletraffic.git
cd py-googletraffic

:: Create virtual environment (recommended)
python -m venv venv

:: Activate virtual environment
venv\Scripts\activate.bat

:: Install package in development mode
pip install -e .
```

#### Windows (PowerShell):
```powershell
# Clone the repository
git clone https://github.com/kwahalf/py-googletraffic.git
cd py-googletraffic

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment (may need to enable scripts first)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1

# Install package in development mode
pip install -e .
```

### Option 2: Install from PyPI (When Available)

```bash
# Future: Once published to PyPI
pip install py-googletraffic
```

### Verify Installation

```bash
python -c "import googletraffic as gt; print(gt.__version__)"
# Should print: 0.1.0
```

## Quick Test

Create a test script to verify everything works:

```python
# test_installation.py
import googletraffic as gt
import os

# Get API key from environment
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

if not api_key:
    print("❌ GOOGLE_MAPS_API_KEY environment variable not set!")
    exit(1)

print("✓ Package imported successfully")
print(f"✓ Version: {gt.__version__}")
print(f"✓ API key found: {api_key[:10]}...")

# Try creating a small raster
try:
    print("\nTesting raster creation (this may take a few seconds)...")
    traffic = gt.make_raster(
        location=(40.7580, -73.9855),
        height=100,  # Small size for quick test
        width=100,
        zoom=14,
        google_key=api_key
    )
    print(f"✓ Test successful! Created raster with shape: {traffic.shape}")
except Exception as e:
    print(f"❌ Test failed: {e}")
```

Run the test:
```bash
python test_installation.py
```

## Jupyter Notebook Setup

### Install Jupyter

```bash
# If not already installed
pip install jupyter notebook ipykernel matplotlib

# Register kernel
python -m ipykernel install --user --name=googletraffic --display-name="Python (googletraffic)"
```

### Launch Jupyter

```bash
# Start Jupyter Notebook
jupyter notebook

# Or Jupyter Lab
jupyter lab
```

### Run Example Notebook

1. Navigate to `examples/` directory
2. Open `getting_started.ipynb`
3. Select the "Python (googletraffic)" kernel
4. Set your API key in the second cell
5. Run all cells

## Troubleshooting

### ChromeDriver Issues

**Error: chromedriver not found**
```bash
# Solution: Install ChromeDriver (see Prerequisites section)
```

**Error: ChromeDriver version mismatch**
```bash
# Check Chrome version
google-chrome --version  # Linux
# Or check in browser: chrome://settings/help

# Download matching ChromeDriver version
```

**Error: Permission denied**
```bash
# Make ChromeDriver executable (macOS/Linux)
chmod +x /path/to/chromedriver
```

### Import Errors

**Error: No module named 'googletraffic'**
```bash
# Solution: Install package
pip install -e .
```

**Error: No module named 'rasterio'**

*macOS:*
```bash
brew install gdal
pip install rasterio
```

*Ubuntu/Linux:*
```bash
sudo apt-get install gdal-bin libgdal-dev
pip install rasterio
```

*Windows:*
```powershell
# Option 1: Use pre-built wheels (easiest)
# Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
# Download matching GDAL and rasterio .whl files for your Python version
# Then:
pip install GDAL-3.x.x-cp3xx-cp3xx-win_amd64.whl
pip install rasterio-1.x.x-cp3xx-cp3xx-win_amd64.whl

# Option 2: Use conda (recommended for Windows)
conda install -c conda-forge rasterio gdal

# Option 3: Install OSGeo4W (advanced users)
# Download from: https://trac.osgeo.org/osgeo4w/
```

### API Key Issues

**Error: API key invalid**
- Verify key is correct (no extra spaces)
- Check Maps JavaScript API is enabled
- Ensure billing is enabled in Google Cloud Console

**Error: API quota exceeded**
- Check usage in Google Cloud Console
- Verify billing account is active
- Consider rate limiting your requests

### Browser Issues

**Error: Browser crashes or hangs**
```python
# Try with headless=False to see what's happening
traffic = gt.make_raster(..., headless=False)

# Or increase wait_time
traffic = gt.make_raster(..., wait_time=10)
```

### Memory Issues

**Error: Out of memory**
```python
# Reduce raster size
traffic = gt.make_raster(height=500, width=500, ...)  # Instead of 2000x2000

# Or reduce max_pixels for large areas
traffic = gt.make_raster_from_bbox(..., max_pixels=1000)
```

## Windows-Specific Troubleshooting

### PowerShell Script Execution Policy

**Error: Cannot run scripts**
```powershell
# Enable script execution for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass for single session
powershell -ExecutionPolicy Bypass
```

### Path Issues on Windows

**Error: chromedriver not found**
```cmd
:: Check if chromedriver is in PATH
where chromedriver

:: If not found, add to PATH or place in project folder
copy chromedriver.exe C:\path\to\py-googletraffic\
```

**Using chromedriver from project directory:**
```python
import os
# Add project directory to PATH temporarily
os.environ['PATH'] = os.getcwd() + os.pathsep + os.environ['PATH']

import googletraffic as gt
# Now it should find chromedriver.exe in current directory
```

### File Path Formatting

Windows users should use proper path formatting:

```python
# Option 1: Use forward slashes (works on Windows too)
output_path = "C:/Users/YourName/traffic_data/nyc_traffic.tif"

# Option 2: Use raw strings with backslashes
output_path = r"C:\Users\YourName\traffic_data\nyc_traffic.tif"

# Option 3: Use pathlib (recommended)
from pathlib import Path
output_path = Path("C:/Users/YourName/traffic_data/nyc_traffic.tif")
```

### Conda Environment (Recommended for Windows)

If you encounter multiple dependency issues, using Conda is often easier:

```cmd
:: Create conda environment
conda create -n googletraffic python=3.9
conda activate googletraffic

:: Install dependencies
conda install -c conda-forge selenium pillow rasterio geopandas

:: Install package
pip install -e .
```

### Long Path Issues (Windows 10/11)

If you encounter "path too long" errors:

```powershell
# Enable long path support (requires admin)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# Or use shorter folder names closer to drive root
# Instead of: C:\Users\YourName\Documents\Projects\py-googletraffic
# Use: C:\dev\py-googletraffic
```

### Chrome/ChromeDriver Version Mismatch

```cmd
:: Check your Chrome version
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version

:: Download matching ChromeDriver from:
:: https://chromedriver.chromium.org/downloads
```

### Firewall/Antivirus Blocking

If selenium/chromedriver is blocked:
1. Add exception for `chromedriver.exe` in Windows Defender
2. Add exception for `python.exe`
3. Check corporate firewall settings

## Docker Setup (Optional)

For a completely isolated environment:

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python package
WORKDIR /app
COPY . /app
RUN pip install -e .

CMD ["python"]
```

Build and run:
```bash
docker build -t py-googletraffic .
docker run -it -e GOOGLE_MAPS_API_KEY=your_key py-googletraffic
```

## Next Steps

1. ✅ Review the [README.md](../README.md) for usage examples
2. ✅ Try the [example notebook](examples/getting_started.ipynb)
3. ✅ Run the [simple example](examples/simple_example.py)
4. ✅ Read the [API documentation](docs/api.md) (when available)
5. ✅ Start building your own traffic analysis!

## Getting Help

- 📝 [GitHub Issues](https://github.com/kwahalf/py-googletraffic/issues)
- 📖 [Documentation](https://github.com/kwahalf/py-googletraffic)
- 💬 [Discussions](https://github.com/kwahalf/py-googletraffic/discussions)
