from setuptools import setup, find_packages

DESCRIPTION = """A Python package for visualizing environmental data, specifically evapotranspiration, leaching risk,
and precipitation/irrigation data. The package includes functions to generate time-series date lists, 
load datasets into dictionaries, and create various types of maps for visualizing environmental phenomena, 
such as evapotranspiration and leaching risk, using geospatial data. 
Outputs are typically saved as PDF files with detailed visualizations."""

NAVE_GRANULE_V = 1.0

setup(
    name="nave_visualization",  
    version=NAVE_GRANULE_V,  
    description=DESCRIPTION,  
    author_email="<nic@naveanalytics.com>",  
    packages=find_packages(),  
    install_requires=[ 
        'geopandas',
        'matplotlib',
        'numpy',
        'pandas',
        'shapely',
        'xarray',
        'rasterio',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
)
