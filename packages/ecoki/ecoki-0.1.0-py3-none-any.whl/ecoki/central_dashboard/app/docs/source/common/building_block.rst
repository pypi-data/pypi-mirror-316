Building Block
==============

The ``BuildingBlock`` class is a fundamental component of the EcoKI framework, serving as the base class for all building blocks in the system. It provides a standardized structure and interface for creating modular, reusable components in machine learning pipelines.

.. automodule:: ecoki.building_block_framework.building_block
   :members:

Key Features
------------

- Abstract base class for all building blocks
- Inherits from ``BuildingBlockDataStructure``
- Supports inlet and outlet ports for data flow
- Configurable settings for each building block
- Integration with the pipeline manager

Usage
-----

To create a custom building block, inherit from the ``BuildingBlock`` class and implement the required methods:

.. code-block:: python

   from ecoki.building_block_framework.building_block import BuildingBlock

   class CustomBuildingBlock(BuildingBlock):
       def __init__(self, **kwargs):
           super().__init__(**kwargs)
           # Initialize custom attributes

       def execute(self):
           # Implement the main logic of the building block
           pass

Example
-------

Here's a simple example of how to use the ``BuildingBlock`` class:

.. code-block:: python

   from ecoki.building_block_framework.building_block import BuildingBlock
   from ecoki.pipeline_framework.pipeline_manager.pipeline_manager import PipelineManager

   # Create a custom building block
   class MyBuildingBlock(BuildingBlock):
       def __init__(self, **kwargs):
           super().__init__(**kwargs)

       def execute(self):
           # Implement the main logic
           pass

   # Initialize the building block
   my_bb = MyBuildingBlock(name="MyBlock", description="A custom building block", category="Processing")

   # Create a pipeline manager
   pipeline_manager = PipelineManager()

   # Attach the pipeline manager to the building block
   my_bb.attach_pipeline_manager(pipeline_manager)

   # Set the building block settings
   my_bb.set_settings({"param1": 10, "param2": "value"})

   # Execute the building block
   my_bb.execute()

API Reference
-------------

.. autoclass:: ecoki.building_block_framework.building_block.BuildingBlock
   :members:
   :inherited-members:
   :special-members: __init__

Methods
-------

.. automethod:: ecoki.building_block_framework.building_block.BuildingBlock.attach_pipeline_manager

   Registers the pipeline manager to the building block.

   Parameters
   ----------
   pipeline_manager : PipelineManager
       The pipeline manager object to be attached.

.. automethod:: ecoki.building_block_framework.building_block.BuildingBlock.set_settings

   Sets the building block settings.

   Parameters
   ----------
   settings : dict
       A dictionary containing the settings for the building block.

See Also
--------

- :class:`ecoki.common.base_classes.BuildingBlockDataStructure`
- :class:`ecoki.pipeline_framework.pipeline_manager.pipeline_manager.PipelineManager`
