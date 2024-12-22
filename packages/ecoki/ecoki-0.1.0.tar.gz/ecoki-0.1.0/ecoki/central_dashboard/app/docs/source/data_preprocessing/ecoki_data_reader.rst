EcoKI Data Reader
=================

The EcoKI Data Reader module provides a flexible and extensible framework for reading data from various sources within the EcoKI architecture. This module is implemented in the ``ecoki.building_blocks.code_based.data_integration.acquire_data.ecoki_data_reader.ecoki_data_reader`` package.

Key Features
------------

- Integration with the EcoKI building block framework
- Dynamic registration of multiple data readers
- Support for both interactive and non-interactive settings
- Flexible execution of different data readers based on user settings

The main component of this module is the ``EcoKIDataReader`` class, which serves as a central hub for managing and executing various data readers.

Detailed Functionality
----------------------

The ``EcoKIDataReader`` class provides the following core functionalities:

1. Data Reader Registration:
   - Automatically registers data readers from the ``DataReaderRegister``
   - Supports easy addition of new data readers to the system

2. Data Reader Execution:
   - Executes the selected data reader based on user settings
   - Handles both interactive and non-interactive modes

3. Output Management:
   - Provides a standardized output port for the read data (pandas DataFrame)

Parameters
----------

.. autoclass:: ecoki.building_blocks.code_based.data_integration.acquire_data.ecoki_data_reader.ecoki_data_reader.EcoKIDataReader
   :members:

Example
-------

Here's a basic example of how to use the ``EcoKIDataReader`` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.data_integration.acquire_data.ecoki_data_reader.ecoki_data_reader import EcoKIDataReader

   # Initialize the EcoKIDataReader
   data_reader = EcoKIDataReader()

   # Configure the settings
   data_reader.settings = {
       "data_reader": "DataReaderLocal",  # or any other registered data reader
       # Add any specific settings for the chosen data reader
   }

   # Execute the data reading process
   result = data_reader.execute()

   # Access the read data
   data = result['output_data']

This example demonstrates how to initialize the ``EcoKIDataReader``, set the necessary settings, and execute the data reading process. The resulting data can then be used for further processing or analysis within the EcoKI ecosystem.

Registered Data Readers
-----------------------

The following data readers are currently registered and available for use:

1. DataReaderLocal
2. DataReaderDataverse
3. MongoDBDataReader

To use a specific data reader, set the "data_reader" key in the settings dictionary to the corresponding name.

Extending the EcoKI Data Reader
-------------------------------

To add a new data reader to the system:

1. Implement the new data reader class, ensuring it follows the required interface.
2. Add the new data reader to the ``DataReaderRegister`` enum in the ``data_reader_register.py`` file.
3. The ``EcoKIDataReader`` will automatically register and make the new data reader available for use.

This extensible design allows for easy integration of new data sources and reading methods into the EcoKI ecosystem.
