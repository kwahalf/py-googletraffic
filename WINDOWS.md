# Windows Setup Guide for py-googletraffic

Complete guide for installing and using py-googletraffic on Windows 10/11.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step-by-Step Installation](#step-by-step-installation)
- [Setting Up API Key](#setting-up-api-key)
- [Running Your First Example](#running-your-first-example)
- [Common Windows Issues](#common-windows-issues)
- [Using Conda (Recommended)](#using-conda-recommended)

## Prerequisites

### 1. Python Installation

Download and install Python 3.8 or higher from [python.org](https://www.python.org/downloads/):

1. Download the Windows installer (64-bit recommended)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation:

```cmd
python --version
pip --version
```

### 2. Google Chrome

Ensure Google Chrome is installed: https://www.google.com/chrome/

Check your Chrome version:
- Open Chrome
- Go to `chrome://settings/help`
- Note the version number (e.g., "121.0.6167.85")

### 3. ChromeDriver

Download ChromeDriver matching your Chrome version:

**Option A: Manual Installation (Simple)**

1. Go to https://chromedriver.chromium.org/downloads
2. Download the version matching your Chrome browser
3. Download `chromedriver_win32.zip`
4. Extract `chromedriver.exe`
5. Choose one of these options:

   **Option 1: Add to PATH**
   - Create folder: `C:\chromedriver`
   - Copy `chromedriver.exe` to `C:\chromedriver`
   - Add to PATH:
     - Press `Win + R`, type `sysdm.cpl`, press Enter
     - Click "Advanced" tab → "Environment Variables"
     - Under "User variables", select "Path" → "Edit"
     - Click "New" → Add `C:\chromedriver`
     - Click OK on all dialogs
     - Restart Command Prompt

   **Option 2: Place in Project Folder**
   - Copy `chromedriver.exe` to your project folder
   - No PATH configuration needed

6. Verify:
```cmd
chromedriver --version
```

**Option B: Using Chocolatey**

If you have [Chocolatey](https://chocolatey.org/) installed:

```cmd
choco install chromedriver
```

## Step-by-Step Installation

### Using Command Prompt (Recommended for Beginners)

1. **Open Command Prompt**
   - Press `Win + R`
   - Type `cmd`
   - Press Enter

2. **Choose installation location**
```cmd
:: Create a folder for your projects (use a short path)
mkdir C:\dev
cd C:\dev
```

3. **Clone the repository**

If you have Git:
```cmd
git clone https://github.com/kwahalf/py-googletraffic.git
cd py-googletraffic
```

Or download ZIP from GitHub and extract to `C:\dev\py-googletraffic`

4. **Create virtual environment**
```cmd
python -m venv venv
```

5. **Activate virtual environment**
```cmd
venv\Scripts\activate.bat
```

You should see `(venv)` at the start of your command prompt.

6. **Install package**
```cmd
pip install -e .
```

7. **Verify installation**
```cmd
python -c "import googletraffic as gt; print('Success! Version:', gt.__version__)"
```

### Using PowerShell

1. **Open PowerShell**
   - Press `Win + X`
   - Select "Windows PowerShell"

2. **Enable script execution** (first time only)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. **Navigate to installation location**
```powershell
mkdir C:\dev
cd C:\dev
```

4. **Clone or download repository**
```powershell
git clone https://github.com/kwahalf/py-googletraffic.git
cd py-googletraffic
```

5. **Create and activate virtual environment**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

6. **Install package**
```powershell
pip install -e .
```

## Setting Up API Key

### Get Your API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Maps JavaScript API":
   - Navigate to "APIs & Services" → "Library"
   - Search for "Maps JavaScript API"
   - Click "Enable"
4. Create API credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy your API key

### Set Environment Variable

**Method 1: Permanent (Recommended)**

Using Command Prompt:
```cmd
setx GOOGLE_MAPS_API_KEY "YOUR_API_KEY_HERE"
```

Using PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY_HERE', 'User')
```

**Important:** Restart your Command Prompt or PowerShell after setting the variable.

**Method 2: Session Only**

Command Prompt:
```cmd
set GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
```

PowerShell:
```powershell
$env:GOOGLE_MAPS_API_KEY="YOUR_API_KEY_HERE"
```

**Method 3: .env File (Best Practice)**

1. Create `.env` file in project root:
```
GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
```

2. Install python-dotenv:
```cmd
pip install python-dotenv
```

3. In your Python code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GOOGLE_MAPS_API_KEY')
```

### Verify API Key

```cmd
echo %GOOGLE_MAPS_API_KEY%
```

Or in PowerShell:
```powershell
echo $env:GOOGLE_MAPS_API_KEY
```

## Running Your First Example

Create a test file `test_traffic.py`:

```python
import googletraffic as gt
import os

# Get API key from environment
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

if not api_key:
    print("ERROR: GOOGLE_MAPS_API_KEY not set!")
    print("Set it with: setx GOOGLE_MAPS_API_KEY your_key_here")
    exit(1)

print("Creating traffic raster for Times Square, NYC...")
print("This will take about 10-15 seconds...")

# Create traffic raster
traffic = gt.make_raster(
    location=(40.7580, -73.9855),  # Times Square
    height=500,
    width=500,
    zoom=14,
    google_key=api_key,
    output_path="nyc_traffic.tif"
)

print(f"Success! Created: {traffic}")
print("Open nyc_traffic.tif in QGIS or other GIS software to view!")
```

Run it:
```cmd
python test_traffic.py
```

## Common Windows Issues

### Issue 1: chromedriver not found

**Error:** `'chromedriver' is not recognized as an internal or external command`

**Solutions:**
1. Verify ChromeDriver is in PATH:
   ```cmd
   where chromedriver
   ```

2. If not found, place `chromedriver.exe` in project folder:
   ```cmd
   copy C:\path\to\chromedriver.exe C:\dev\py-googletraffic\
   ```

3. Or add to PATH (see Prerequisites section)

### Issue 2: PowerShell Script Execution Error

**Error:** `cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 3: GDAL/Rasterio Installation Fails

**Error:** `Failed to build rasterio` or GDAL-related errors

**Solution 1 - Use Conda (Easiest):**
```cmd
conda install -c conda-forge rasterio
```

**Solution 2 - Use Pre-built Wheels:**
1. Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/
2. Download `GDAL` wheel matching your Python version (e.g., `GDAL‑3.4.3‑cp39‑cp39‑win_amd64.whl` for Python 3.9)
3. Download `rasterio` wheel
4. Install:
```cmd
pip install GDAL‑3.4.3‑cp39‑cp39‑win_amd64.whl
pip install rasterio‑1.2.10‑cp39‑cp39‑win_amd64.whl
```

### Issue 4: Path Too Long

**Error:** `OSError: [Errno 22] Invalid argument` (path too long)

**Solutions:**
1. Move project to shorter path (e.g., `C:\dev\py-googletraffic`)
2. Enable long paths (requires admin PowerShell):
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```
3. Restart computer

### Issue 5: SSL Certificate Errors

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution:**
```cmd
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -e .
```

### Issue 6: Firewall/Antivirus Blocking

If Chrome or Selenium is blocked:

1. Add exceptions in Windows Defender:
   - Settings → Privacy & Security → Windows Security → Virus & threat protection
   - Manage settings → Add or remove exclusions
   - Add: `C:\dev\py-googletraffic\venv\`
   - Add: `C:\chromedriver\chromedriver.exe`

2. Check corporate firewall settings

### Issue 7: Chrome Version Mismatch

**Error:** `session not created: This version of ChromeDriver only supports Chrome version XX`

**Solution:**
1. Check Chrome version: `chrome://version`
2. Download matching ChromeDriver from: https://chromedriver.chromium.org/downloads
3. Replace old `chromedriver.exe`

## Using Conda (Recommended)

If you encounter many dependency issues, Conda is easiest:

### Install Miniconda

1. Download: https://docs.conda.io/en/latest/miniconda.html
2. Run installer (use default options)
3. Open "Anaconda Prompt" from Start Menu

### Setup with Conda

```cmd
:: Create environment
conda create -n googletraffic python=3.9
conda activate googletraffic

:: Install dependencies (much easier on Windows!)
conda install -c conda-forge selenium pillow rasterio geopandas shapely matplotlib jupyter

:: Install package
cd C:\dev\py-googletraffic
pip install -e .

:: Verify
python -c "import googletraffic as gt; print('Success!', gt.__version__)"
```

### Using Jupyter with Conda

```cmd
:: Activate environment
conda activate googletraffic

:: Install Jupyter
conda install -c conda-forge jupyter notebook

:: Start Jupyter
jupyter notebook

:: Open examples/getting_started.ipynb
```

## Running Examples

### Command Line Example

```cmd
cd C:\dev\py-googletraffic
python examples\simple_example.py
```

### Jupyter Notebook

```cmd
:: Activate virtual environment
venv\Scripts\activate.bat

:: Start Jupyter
jupyter notebook

:: Opens in browser - navigate to examples/getting_started.ipynb
```

## File Paths in Python

Windows uses backslashes, but Python works with both:

```python
# Option 1: Forward slashes (recommended, cross-platform)
output = "C:/Users/YourName/Documents/traffic.tif"

# Option 2: Raw strings with backslashes
output = r"C:\Users\YourName\Documents\traffic.tif"

# Option 3: Pathlib (best practice)
from pathlib import Path
output = Path("C:/Users/YourName/Documents/traffic.tif")
```

## Getting Help

### Check Logs

```python
# Run with headless=False to see browser
traffic = gt.make_raster(
    location=(40.7580, -73.9855),
    height=500,
    width=500,
    zoom=14,
    google_key=api_key,
    headless=False  # Watch what's happening
)
```

### Enable Debug Output

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Resources

- 📖 [Full Documentation](README.md)
- 🔧 [Installation Guide](INSTALLATION.md)
- 🚀 [Quick Start](QUICKSTART.md)
- 🐛 [GitHub Issues](https://github.com/kwahalf/py-googletraffic/issues)

## Next Steps

1. ✅ Try the [Jupyter notebook](examples/getting_started.ipynb)
2. ✅ Run [simple_example.py](examples/simple_example.py)
3. ✅ Read the [full README](README.md)
4. ✅ Start analyzing traffic data!

## Tips for Windows Users

- Use short paths (avoid deep nested folders)
- Use Conda for easier dependency management
- Keep Chrome and ChromeDriver versions in sync
- Use forward slashes in file paths
- Check antivirus/firewall if browser automation fails
- Restart terminal after setting environment variables

Happy mapping! 🗺️🚦
