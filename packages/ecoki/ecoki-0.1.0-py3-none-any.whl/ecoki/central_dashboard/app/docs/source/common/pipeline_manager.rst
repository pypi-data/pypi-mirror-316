Pipeline Manager
================

The Pipeline Manager module is responsible for managing and executing data processing pipelines within the Ecoki Central Dashboard. It provides a flexible and extensible framework for creating, configuring, and running complex data workflows.

.. py:module:: ecoki.pipeline_manager

Classes
-------

.. py:class:: PipelineManager

   The main class for managing pipelines.

   .. py:method:: __init__(config)

      Initialize the PipelineManager.

      :param dict config: Configuration dictionary for the pipeline manager.

   .. py:method:: create_pipeline(name, steps)

      Create a new pipeline.

      :param str name: Name of the pipeline.
      :param list steps: List of pipeline steps.
      :return: The created pipeline object.
      :rtype: Pipeline

   .. py:method:: run_pipeline(pipeline_name)

      Run a pipeline by its name.

      :param str pipeline_name: Name of the pipeline to run.
      :return: The result of the pipeline execution.
      :rtype: dict

   .. py:method:: get_pipeline_status(pipeline_name)

      Get the status of a pipeline.

      :param str pipeline_name: Name of the pipeline.
      :return: The current status of the pipeline.
      :rtype: str

.. py:class:: Pipeline

   Represents a single pipeline in the system.

   .. py:method:: __init__(name, steps)

      Initialize a Pipeline object.

      :param str name: Name of the pipeline.
      :param list steps: List of steps in the pipeline.

   .. py:method:: add_step(step)

      Add a step to the pipeline.

      :param BuildingBlock step: The building block to add as a step.

   .. py:method:: remove_step(step_index)

      Remove a step from the pipeline.

      :param int step_index: Index of the step to remove.

   .. py:method:: execute()

      Execute the pipeline.

      :return: The result of the pipeline execution.
      :rtype: dict

Functions
---------

.. py:function:: validate_pipeline_config(config)

   Validate the configuration of a pipeline.

   :param dict config: The pipeline configuration to validate.
   :return: True if the configuration is valid, False otherwise.
   :rtype: bool

.. py:function:: optimize_pipeline(pipeline)

   Optimize the given pipeline for better performance.

   :param Pipeline pipeline: The pipeline to optimize.
   :return: The optimized pipeline.
   :rtype: Pipeline

Usage Example
-------------

Here's a basic example of how to use the Pipeline Manager:

.. code-block:: python

   from ecoki.pipeline_manager import PipelineManager
   from ecoki.building_blocks import DataLoader, DataTransformer, DataExporter

   # Initialize the Pipeline Manager
   config = {"max_concurrent_pipelines": 5, "log_level": "INFO"}
   manager = PipelineManager(config)

   # Create a new pipeline
   steps = [
       DataLoader(source="database"),
       DataTransformer(operation="normalize"),
       DataExporter(destination="file")
   ]
   pipeline = manager.create_pipeline("my_pipeline", steps)

   # Run the pipeline
   result = manager.run_pipeline("my_pipeline")

   # Check the status
   status = manager.get_pipeline_status("my_pipeline")
   print(f"Pipeline status: {status}")

This module provides a powerful and flexible way to manage data processing workflows in the Ecoki Central Dashboard.
