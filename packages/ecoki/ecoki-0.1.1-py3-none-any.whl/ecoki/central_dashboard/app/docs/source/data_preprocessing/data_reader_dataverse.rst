DataReaderDataverse
===================

This module provides functionality for reading data from the EcoKI Dataverse repository. It is designed as part of the EcoKI architecture and is implemented as a building block for data integration pipelines.

The main component of this module is the `DataReaderDataverse` class, which encapsulates the process of:

1. Connecting to the Dataverse API using provided credentials.
2. Downloading specified data files from the Dataverse repository.
3. Loading the downloaded data into a pandas DataFrame.
4. Providing the data as an output for further processing in the EcoKI pipeline.

This module is particularly useful for integrating data stored in Dataverse repositories into EcoKI workflows, allowing seamless access to datasets for various analysis and modeling tasks.

Key features of this module include:
- Integration with the EcoKI building block framework.
- Support for both interactive and non-interactive settings.
- Flexible data file selection using either file ID or dataset DOI and filename.
- Automatic conversion of downloaded data to pandas DataFrame format.

The module leverages the pyDataverse library for interacting with the Dataverse API, making it a robust tool for data acquisition in the EcoKI ecosystem.



Parameters
-----------


.. autoclass:: ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_dataverse.data_reader_dataverse.DataReaderDataverse
   :members:

Example
-------

Here's a basic example of how to use the :class:`DataReaderDataverse` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_dataverse.data_reader_dataverse import DataReaderDataverse

   # Initialize the building block
   dataverse_reader = DataReaderDataverse()

   # Set up the connection parameters
   base_url = "https://your-dataverse-url.com"
   api_token = "your-api-token"
   doi = "10.5072/FK2/ABCDEF"  # Example DOI
   file_name = "example_data.csv"

   # Configure the settings
   dataverse_reader.settings = {
       "base_url": base_url,
       "token": api_token,
       "doi": doi,
       "name": file_name
   }

   # Execute the data reading process
   result = dataverse_reader.execute()

   # Access the downloaded data
   data = result['output_data']

.. seealso::
   :class:`pyDataverse.api.NativeApi`
   :class:`pyDataverse.api.DataAccessApi`