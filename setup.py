from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="py-googletraffic",
    version="0.1.1",
    author="Denis Juma",
    author_email="kwanusud@gmail.com",
    description="Create georeferenced traffic rasters from Google Maps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kwahalf/py-googletraffic",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
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
        "test": [
            "nose2>=0.12.0",
            "coverage>=6.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.6.0",
            "mock>=4.0.3",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "notebook>=6.4.0",
            "matplotlib>=3.5.0",
            "folium>=0.12.0",
        ],
    },
    keywords="google-maps traffic gis raster geospatial selenium",
    project_urls={
        "Homepage": "https://github.com/kwahalf/py-googletraffic",
        "Bug Reports": "https://github.com/kwahalf/py-googletraffic/issues",
        "Source": "https://github.com/kwahalf/py-googletraffic",
        "Documentation": "https://github.com/kwahalf/py-googletraffic#readme",
        "Changelog": "https://github.com/kwahalf/py-googletraffic/blob/main/CHANGELOG.md",
    },
)
