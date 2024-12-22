Requirements for Building Blocks
================================

When creating a new Building Block (BB) in EcoKI, you must follow specific requirements to ensure consistency and compatibility across the framework. This document outlines the technical requirements, best practices, and integration guidelines for new Building Blocks.
Everyone creating a new Building Block (BB) in EcoKI must follow these requirements. The requirements are organized into:

* Technical requirements for class structure and configuration 
* Best practices for documentation and testing
* Integration guidelines for data and visualization
* Example building block implementation

Technical Requirements
----------------------

Class Structure
~~~~~~~~~~~~~~~

#. Must inherit from ``BuildingBlock`` base class
#. Must implement ``execute()`` method
#. Must call parent constructor using ``super().__init__(**kwargs)``
#. Must define class attributes:

   * architecture: str
   * version: str
   * category: str 
   * description: str

#. Class naming must follow conventions:

   * Use CamelCase style (e.g., DataLoader)
   * Name should indicate functionality
   * Use common abbreviations only (e.g., CSV)
   * Use consistent prefixes/suffixes (e.g., TrainModel, EvaluateModel)

Port Configuration 
~~~~~~~~~~~~~~~~~~

#. Must define inlet/outlet ports in __init__ using:

   * add_inlet_port()
   * add_outlet_port()

#. Common inlet ports include:

   * input_data: Main input (list, DataFrame, array)

#. Common outlet ports include:

   * output_data: Processed data
   * metrics: Performance metrics
   * visualizations: Generated plots

#. Port naming conventions:

   * Use lowercase with underscores
   * Be descriptive but concise
   * Follow common patterns across blocks

Best Practices
--------------

Documentation
~~~~~~~~~~~~~

#. Use docstrings for all classes/methods
#. Document all attributes and parameters
#. Include clear functionality descriptions
#. Document input/output data formats

Testing
~~~~~~~

#. Include pytest unit tests
#. Test with various input types
#. Verify expected outputs
#. Test edge cases and errors

Integration Guidelines
----------------------

Data Compatibility
~~~~~~~~~~~~~~~~~~

#. Support common formats:

   * pandas DataFrame
   * numpy arrays
   * Python lists

#. Handle data type conversions
#. Process missing values properly

Visualization Standards
~~~~~~~~~~~~~~~~~~~~~~~

#. Use consistent styling
#. Enable interactive features
#. Include proper labels/titles

Third-Party Requirements
------------------------

Licensing
~~~~~~~~~

#. Include clear license info
#. Ensure EcoKI compatibility
#. Document dependencies
#. Provide attributions

Example Implementation
----------------------

Here's a template for creating a new Building Block:

.. code-block:: python

    from ecoki.building_block_framework.building_block import BuildingBlock
    
    class NewBuildingBlock(BuildingBlock):
        """
        A generic building block template.

        This class provides a starting point for creating new building blocks in the EcoKI framework.
        Implement the required functionality by overriding the execute method and configuring
        appropriate inlet and outlet ports.

        Attributes:
            architecture (str): The architecture name.
            version (str): The version of the building block.
            category (str): The category of the building block.
            description (str): A brief description of the building block functionality.
        """

        def __init__(self, **kwargs):
            """
            Initializes the building block with specified keyword arguments.

            Args:
                **kwargs: Keyword arguments for the BuildingBlock superclass.
            """
            super().__init__(**kwargs)

            self.architecture = "EcoKI"
            self.version = "1"
            self.category = "Processing"  # Choose appropriate category
            self.description = "Description of building block functionality..."

            # Configure required ports
            self.add_inlet_port('input_data', list)  # Add inlet ports as needed
            self.add_outlet_port('output_data', dict)  # Add outlet ports as needed

        def execute(self, input_data):
            """
            Executes the main functionality of the building block.

            Args:
                input_data: Input data received through inlet port.

            Returns:
                bool: True if execution successful, False otherwise.
            """
            # Implement building block logic here
            return True

.. seealso::
   For more detailed examples and implementation guidelines, refer to the existing building block files in the EcoKI framework.
