.. EcoKI Developer Docs master file, created by
   sphinx-quickstart on Thu Sep 26 11:06:54 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EcoKI Developer Docs
====================

`EcoKI <https://www.ecoki.de/>`_ is an innovative low code platform for developing and deploying machine learning pipelines, with a focus on energy efficiency. EcoKI offers a collection of pre-built pipeline components, example projects, and utilities for data visualization, model training, and optimization. It is designed to streamline the development process for energy-related machine learning applications and promote sustainable AI practices.


Key features of EcoKI include:

- A modular architecture for creating flexible and reusable machine learning pipelines
- Support for various machine learning algorithms, including XGBoost, neural networks and optimation algorithms
- Integration with energy efficiency scenarios and sustainability metrics
- A user-friendly dashboard for managing and monitoring pipelines
- Extensive documentation and developer resources



.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   getting_started/installation


.. toctree::
   :maxdepth: 1
   :caption: Data Processing

   data_preprocessing/data_reader_dataverse
   data_preprocessing/ecoki_data_reader
   data_preprocessing/data_reader_local
   data_preprocessing/data_imputer

.. toctree::
   :maxdepth: 1
   :caption: Modeling

   modeling/xgboost_multi
   modeling/lin_reg
   modeling/rfe
   modeling/split_train_test
   modeling/model_comparision
   modeling/model_and_forecast_lstm

.. toctree::
   :maxdepth: 1
   :caption: Optimization

   optimization/process_parameter_optimizer
   optimization/optimization_2d_visualizer
   optimization/optimization_2d_visualizer_visualizer

.. toctree::
   :maxdepth: 1
   :caption: Common

   common/building_block
   common/pipeline_manager

.. toctree::
   :maxdepth: 1
   :caption: Custom Building Blocks and Pipelines

   custom_building_blocks_and_pipelines/custom_building_block

.. toctree::
   :maxdepth: 1
   :caption: Contributing

   contributing/contributions
   contributing/requirements_new_bb
   contributing/requirements_new_pipeline

.. toctree::   
   :maxdepth: 1
   :caption: FAQs

   FAQs/FAQs

.. toctree::
   :maxdepth: 1
   :caption: UML diagrams

   uml_diagrams/uml_diagram

Indices and tables
-------------------

* :ref:`genindex`
* :ref:`search`
* :ref:`modindex`

