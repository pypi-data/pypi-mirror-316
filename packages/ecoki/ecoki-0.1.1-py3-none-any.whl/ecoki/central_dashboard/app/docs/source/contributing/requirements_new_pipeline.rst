Requirements for Pipelines
============================

When creating a new Pipeline in EcoKI, you must follow specific requirements to ensure consistency and compatibility across the framework. This document outlines the technical requirements, best practices, and integration guidelines for new Pipelines.
Everyone creating a new Pipeline in EcoKI must follow these requirements. The requirements are organized into:

* Technical requirements for pipeline structure and configuration
* Best practices for error handling and testing
* Integration guidelines for ports and building blocks
* Example pipeline configuration

Technical Requirements
----------------------

Pipeline Structure
~~~~~~~~~~~~~~~~~~~

#. Must be defined in a settings.json file
#. Must have a unique name and description 
#. Must specify building blocks and their connections
#. Should follow a clear data flow structure

Settings.json Structure
~~~~~~~~~~~~~~~~~~~~~~~

The settings.json file must contain:

#. "nodes" array defining building blocks
#. "connections" array defining port connections
#. Each node must specify:

   * name: Unique identifier for the building block
   * building_block_module: Python module path
   * building_block_class: Class name
   * execution_mode: Usually "local"
   * settings: Dictionary of block-specific settings
   * visualizer_module: Module path for visualizer (if any)
   * visualizer_class: Class name for visualizer (if any)
   * interactive_configuration: Boolean flag
   * visualizer_input: Dictionary/list of visualization inputs

Connection Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Each connection in the settings.json must specify:

#. name: Unique connection identifier
#. from_node: Source building block name
#. from_port: Source port name
#. to_node: Target building block name
#. to_port: Target port name

Best Practices
--------------

Error Handling
~~~~~~~~~~~~~~~

#. Validate settings.json schema
#. Check for missing required fields
#. Verify module and class paths exist
#. Validate port compatibility

Testing
~~~~~~~~~~~

#. Test building block instantiation
#. Verify port connections
#. Test complete pipeline execution

Integration Guidelines
----------------------

Port Management
~~~~~~~~~~~~~~~~

#. Define clear inlet/outlet port names
#. Document port data types
#. Handle data type conversions
#. Validate port connections

Building Block Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

#. Use consistent naming conventions
#. Document required settings
#. Provide default values
#. Include setting descriptions

Example Pipeline Configuration
------------------------------      

Here's a real-world example of a pipeline settings.json:

.. code-block:: json

    {
        "nodes": [
            {
                "name": "ecoKI_data_reader",
                "building_block_module": "ecoki.building_blocks.code_based.data_integration.acquire_data.ecoki_data_reader.ecoki_data_reader",
                "building_block_class": "EcoKIDataReader",
                "execution_mode": "local",
                "settings": {},
                "visualizer_module": "",
                "visualizer_class": "",
                "visualizer_input": {},
                "interactive_configuration": true
            },
            {
                "name": "data_selector",
                "building_block_module": "ecoki.building_blocks.code_based.data_integration.preprocess_data.data_selector.data_selector",
                "building_block_class": "DataSelector",
                "execution_mode": "local",
                "settings": {},
                "visualizer_module": "",
                "visualizer_class": "",
                "visualizer_input": {},
                "interactive_configuration": true
            }
        ],
        "connections": [
            {
                "name": "1",
                "from_node": "ecoKI_data_reader", 
                "from_port": "output_data",
                "to_node": "data_selector",
                "to_port": "input_data"
            }
        ]
    }

.. seealso::
   For more detailed examples and implementation guidelines, refer to the existing pipeline settings files in the EcoKI framework.
