# Nave Visualization

This Python package provides functions for visualizing environmental data, such as evapotranspiration, leaching risk, and precipitation/irrigation data. It works with geospatial datasets, processes them, and generates maps and visualizations, primarily outputting results as PDF files.

## Package components

This package contains the following modules:

- `nave_visualization_core`: Main module, including functions for date generation, loading datasets, and creating environmental maps.
- `test`: A jupyter notebook that demos all the functions in nave_visualization_core.



### Example Usage

```python
import nave_visualization_core as nave

# Example function call
nave.functions.build_evapotranspiration_map(twr_block, output)

```


Prerequisites
-----
This package is compatible with Python 3.6 and above. You can download the latest version of Python from [python.org](https://www.python.org/downloads/).
This package depends on several Python libraries. You can install them using pip:

- geopandas — For working with geospatial data.
- matplotlib — For creating static, animated, and interactive visualizations in Python.
- numpy — A library for numerical operations.
- pandas — For data manipulation and analysis.
- shapely — For geometric operations and analysis.
- xarray — For working with labeled multi-dimensional arrays.
- rasterio — For reading and writing geospatial raster data.

To install the dependencies, you can install them manually:
 - Install them manually:

     ```bash
     pip install geopandas 
     pip install matplotlib 
     pip install numpy 
     pip install pandas 
     pip install shapely 
     pip install xarray 
     pip install rasterio
     ```


Installing nave_visualization
-----------------------

Packages can only be imported if they are located in a directory on the PYTHONPATH (which you can view in python using ``sys.path()``).

Packages installed using the command line tool ``pip`` are added to this path.


```bash
pip install nave-visualization

```


License
-------
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

