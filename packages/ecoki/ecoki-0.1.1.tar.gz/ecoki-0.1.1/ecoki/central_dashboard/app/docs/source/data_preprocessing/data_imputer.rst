Data Imputer
============

The Data Imputer module provides functionality for imputing missing data within the EcoKI architecture. This module is implemented in the ``ecoki.building_blocks.code_based.data_integration.preprocess_data.data_imputer.data_imputer`` package.

Key Features
------------

- Integration with the EcoKI building block framework
- Imputation of missing values in numerical and categorical columns
- Support for different imputation strategies
- Flexible configuration options

The main component of this module is the ``DataImputer`` class, which extends the ``BuildingBlock`` class from the EcoKI framework.

Detailed Functionality
----------------------

The ``DataImputer`` class provides the following core functionalities:

1. Missing Data Imputation:
   - Imputes missing values in numerical columns using specified strategy (default: median)
   - Imputes missing values in categorical columns using specified strategy (default: most frequent)

2. Flexible Configuration:
   - Allows customization of imputation strategies for numerical and categorical data
   - Supports specifying custom fill values
   - Option to exclude certain columns (labels) from imputation

3. Input/Output Management:
   - Accepts input data as a pandas DataFrame
   - Provides imputed data as output in the same DataFrame format

Parameters
----------

.. autoclass:: ecoki.building_blocks.code_based.data_integration.preprocess_data.data_imputer.data_imputer.DataImputer
   :members:

Example
-------

Here's a basic example of how to use the ``DataImputer`` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.data_integration.preprocess_data.data_imputer.data_imputer import DataImputer
   import pandas as pd

   # Create a sample DataFrame with missing values
   data = pd.DataFrame({
       'A': [1, 2, None, 4],
       'B': ['x', None, 'z', 'x'],
       'C': [0.1, 0.2, 0.3, None]
   })

   # Initialize the DataImputer
   imputer = DataImputer()

   # Configure the settings (optional)
   imputer.settings = {
       "strategy_num": "mean",
       "strategy_cat": "most_frequent"
   }

   # Execute the imputation process
   result = imputer.execute(data)

   # Access the imputed data
   imputed_data = result['output_data']

This example demonstrates how to initialize the ``DataImputer``, set the imputation strategies, and execute the imputation process on a DataFrame with missing values. The resulting imputed data can then be used for further processing or analysis within the EcoKI ecosystem.
