from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="py-googletraffic",
    version="0.1.0",
    author="py-googletraffic Contributors",
    description="Create georeferenced traffic rasters from Google Maps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/py-googletraffic",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.0.0",
        "Pillow>=9.0.0",
        "rasterio>=1.3.0",
        "numpy>=1.20.0",
        "geopandas>=0.10.0",
        "shapely>=1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "notebook>=6.4.0",
            "matplotlib>=3.5.0",
            "folium>=0.12.0",
        ],
    },
    keywords="google-maps traffic gis raster geospatial",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/py-googletraffic/issues",
        "Source": "https://github.com/yourusername/py-googletraffic",
    },
)
