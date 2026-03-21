# Changelog

All notable changes to py-googletraffic will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Integration tests with real Google Maps API
- Support for time-series traffic data collection
- Additional export formats (PNG, CSV)
- Docker container support
- Command-line interface (CLI)

## [0.1.0] - 2026-03-21

### Added
- Initial release of py-googletraffic
- Core functionality for creating traffic rasters from Google Maps
- Three main functions:
  - `make_raster()` - Create raster around a point location
  - `make_raster_from_bbox()` - Create raster from bounding box
  - `make_raster_from_polygon()` - Create raster from polygon
- Traffic classification into 4 levels (green, orange, red, dark red)
- GeoTIFF export with proper georeferencing
- Automatic image resizing to exact dimensions
- Support for Python 3.8, 3.9, 3.10, 3.11
- Cross-platform support (Windows, macOS, Linux)
- Google Colab support with dedicated setup guide
- Comprehensive documentation:
  - README with quick start guide
  - Complete installation guide (INSTALLATION.md)
  - Quick start guide (QUICKSTART.md)
  - Windows-specific guide (WINDOWS.md)
  - Google Colab guide (COLAB.md)
  - Contributing guidelines (CONTRIBUTING.md)
- Example notebooks and scripts:
  - Getting started Jupyter notebook
  - Google Colab example notebook
  - Simple Python script example
- Comprehensive test suite with 35+ test methods
- GitHub Actions CI/CD pipeline:
  - Multi-OS testing (Ubuntu, macOS, Windows)
  - Multi-Python version testing (3.8-3.11)
  - Automated linting and formatting checks
  - Automated contributor recognition
- Automated contributor tracking via git history
- Code quality tools:
  - Black for code formatting
  - Flake8 for linting
  - nose2 and pytest for testing
  - Coverage reporting

### Fixed
- Overflow warning in color distance calculations
- Screenshot dimension mismatch (now auto-resizes to exact dimensions)
- NumPy boolean compatibility across Python versions
- Windows encoding issues in setup.py
- Pillow resampling compatibility (9.x and 10.x)

### Technical Details
- Uses Selenium WebDriver for browser automation
- ChromeDriver for capturing Google Maps screenshots
- Pillow for image processing and color classification
- Rasterio for GeoTIFF creation
- GeoPandas/Shapely for geospatial operations
- NumPy for efficient array operations

## Version History

- **0.1.0** (2026-03-21) - Initial public release

---

## How to Update This File

When making changes:

1. Add items to "Unreleased" section
2. Use categories: Added, Changed, Deprecated, Removed, Fixed, Security
3. When releasing, move items under a new version heading
4. Link version numbers to git tags/releases

## Release Process

1. Update version in:
   - `googletraffic/__init__.py`
   - `setup.py`
   - `pyproject.toml`
2. Update CHANGELOG.md (move Unreleased to new version)
3. Commit changes: `git commit -m "Release v0.X.Y"`
4. Create tag: `git tag -a v0.X.Y -m "Version 0.X.Y"`
5. Push: `git push && git push --tags`
6. GitHub Actions will automatically publish to PyPI

---

For more details on each version, see the [GitHub Releases page](https://github.com/kwahalf/py-googletraffic/releases).
