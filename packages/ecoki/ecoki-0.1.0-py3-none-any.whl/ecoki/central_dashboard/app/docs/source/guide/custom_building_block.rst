Creating a Custom Building Block
================================

This guide will walk you through the process of creating a custom building block for the Ecoki Central Dashboard.

Prerequisites
-------------

Before creating a custom building block, ensure you have:

1. Access to the Ecoki Central Dashboard codebase
2. Familiarity with Python programming
3. Understanding of the existing building block structure

Steps to Create a Custom Building Block
---------------------------------------

1. Define the Building Block Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new Python file in the appropriate directory (e.g., `ecoki/building_blocks/`) and define your custom building block class:

.. code-block:: python

   from ecoki.building_blocks.base import BuildingBlock

   class MyCustomBuildingBlock(BuildingBlock):
       def __init__(self, name, description):
           super().__init__(name, description)
           # Add any custom initialization here

2. Implement Required Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implement the required methods for your building block:

.. code-block:: python

   class MyCustomBuildingBlock(BuildingBlock):
       # ... (previous code)

       def process(self, input_data):
           # Implement the main processing logic
           # This method should return the processed data
           pass

       def validate_input(self, input_data):
           # Implement input validation logic
           # Return True if input is valid, False otherwise
           pass

       def get_output_schema(self):
           # Define and return the output schema
           pass

3. Add Custom Functionality
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add any custom methods or attributes specific to your building block:

.. code-block:: python

   class MyCustomBuildingBlock(BuildingBlock):
       # ... (previous code)

       def custom_method(self):
           # Implement custom functionality
           pass

4. Register the Building Block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Register your custom building block in the appropriate registry file (e.g., `ecoki/building_blocks/registry.py`):

.. code-block:: python

   from ecoki.building_blocks.my_custom_block import MyCustomBuildingBlock

   def register_building_blocks():
       # ... (existing registrations)
       register_building_block(MyCustomBuildingBlock)

5. Create Documentation
^^^^^^^^^^^^^^^^^^^^^^^

Add documentation for your custom building block, including:

- Purpose and functionality
- Input and output specifications
- Usage examples
- Any configuration options

6. Test the Building Block
^^^^^^^^^^^^^^^^^^^^^^^^^^

Create unit tests for your custom building block to ensure it functions correctly:

.. code-block:: python

   import unittest
   from ecoki.building_blocks.my_custom_block import MyCustomBuildingBlock

   class TestMyCustomBuildingBlock(unittest.TestCase):
       def test_process(self):
           # Implement test cases for the process method
           pass

       def test_validate_input(self):
           # Implement test cases for input validation
           pass

       # Add more test methods as needed

7. Integrate with the Dashboard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the necessary parts of the Ecoki Central Dashboard to include your custom building block, such as:

- User interface for configuring the building block
- Pipeline integration
- Visualization components (if applicable)

Best Practices
--------------

- Follow the existing coding style and conventions in the Ecoki codebase
- Write clear and concise documentation for your building block
- Ensure your building block is modular and reusable
- Handle errors and edge cases gracefully
- Optimize for performance, especially for data-intensive operations

By following these steps and best practices, you can create a custom building block that seamlessly integrates with the Ecoki Central Dashboard and extends its functionality.
