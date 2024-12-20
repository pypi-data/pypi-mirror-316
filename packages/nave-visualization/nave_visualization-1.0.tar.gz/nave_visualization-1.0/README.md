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


Installing your package
-----------------------

Packages can only be imported if they are located in a directory on the PYTHONPATH (which you can view in python using ``sys.path()``).

Packages installed using the command line tool ``pip`` are added to this path.
This is preferable to manually adding paths to ``sys.path`` in your scripts.
You can install local packages that you are working on in develop mode, by pointing pip the **directory** that contains `setup.py` and your package folder:

.. code-block:: console

    pip install -e local_path/example-package-python

This creates a temporary reference to your local package files - you'll see an `.egg-info` file has been created next to your package.
When packages are installed without the ``-e`` flag, they're installed in `site-packages` next to your python installation.

Be sure to uninstall your package once you've finished - don't delete the `.egg-info` reference.
Use the name of the package when deleting it, like so:

.. code-block:: console

    pip uninstall examplepackage






License
-------
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Distributing
------------

Storing your source code in an open repository allows others to view and critique your code. Python code can be distributed in a number of formats, as described by this `overview of python packages <https://packaging.python.org/overview/>`_.

To allow others to install and use your code more easily, consider uploading your package to the Python Package Index (PyPI).
PyPI is an online repository of python packages and is the default repository used by ``pip``.

Please see this `guide to packaging projects <https://packaging.python.org/tutorials/packaging-projects/>`_ for instructions on uploading your package to PyPI.