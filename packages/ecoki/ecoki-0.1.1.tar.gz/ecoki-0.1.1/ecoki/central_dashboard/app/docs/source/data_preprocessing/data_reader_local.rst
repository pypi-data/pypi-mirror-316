Data Reader Local
=================

The Data Reader Local module provides functionality for reading CSV data from local files within the EcoKI architecture. This module is implemented in the ``ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_local.data_reader_local`` package.

Key Features
------------

- Integration with the EcoKI building block framework
- Reading CSV data from local files
- Processing data into pandas DataFrames
- Support for both interactive and non-interactive settings

The main component of this module is the ``DataReaderLocal`` class, which extends the ``BuildingBlock`` class from the EcoKI framework.

Detailed Functionality
----------------------

The ``DataReaderLocal`` class provides the following core functionalities:

1. Local File Reading:
   - Reads CSV data from specified local file paths
   - Converts the data into pandas DataFrames for further processing

2. Interactive and Non-interactive Modes:
   - Supports both interactive GUI-based file selection and non-interactive file path specification

3. Output Management:
   - Provides a standardized output port for the read data (pandas DataFrame)

Parameters
----------

.. autoclass:: ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_local.data_reader_local.DataReaderLocal
   :members:

Example
-------

Here's a basic example of how to use the ``DataReaderLocal`` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_local.data_reader_local import DataReaderLocal

   # Initialize the DataReaderLocal
   data_reader = DataReaderLocal()

   # Configure the settings
   data_reader.settings = {
       "data_file_path": "/path/to/your/local/file.csv"
   }

   # Execute the data reading process
   result = data_reader.execute()

   # Access the read data
   data = result['output_data']

This example demonstrates how to initialize the ``DataReaderLocal``, set the necessary settings, and execute the data reading process. The resulting data can then be used for further processing or analysis within the EcoKI ecosystem.

.. Extending the Data Reader Local
.. -------------------------------

.. To extend or modify the functionality of the ``DataReaderLocal`` class:

.. 1. Subclass the ``DataReaderLocal`` class to add new methods or override existing ones.
.. 2. Ensure that any new functionality maintains compatibility with the EcoKI building block framework.
.. 3. Update the documentation to reflect any changes or additions to the class.

.. This extensible design allows for easy customization and enhancement of the local data reading capabilities within the EcoKI ecosystem.
