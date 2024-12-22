SplitTrainTestLabel
===================

This module provides functionality for splitting a pre-processed input dataset into training and test datasets. It is designed as part of the EcoKI architecture and is implemented as a building block for preparing data for machine learning tasks.

The main component of this module is the `SplitTrainTestLabel` class, which encapsulates the process of:

1. Taking a pre-processed dataset as input.
2. Splitting the dataset into training and test sets, with the test set being 20% of the original dataset.
3. Handling both feature columns and label columns separately.
4. Providing an option to control data shuffling during the split.

This module is particularly useful in data preparation pipelines, where consistent and reproducible data splitting is crucial for model training and evaluation.

Key features of this module include:
- Seamless integration with the EcoKI building block framework.
- Flexible handling of multiple feature and label columns.
- Optional control over data shuffling during the split.
- Comprehensive output including separated feature and label datasets for both training and testing.

The module leverages scikit-learn's `train_test_split` function for reliable and efficient data splitting, making it a versatile tool for preparing datasets in the EcoKI ecosystem.

Parameters
----------

.. autoclass:: ecoki.building_blocks.code_based.modelling.build_and_train_model.split_traintest_label.split_traintest_label.SplitTrainTestLabel
   :members:

Example
-------

Here's a basic example of how to use the :class:`SplitTrainTestLabel` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.modelling.build_and_train_model.split_traintest_label.split_traintest_label import SplitTrainTestLabel
   import pandas as pd

   # Assuming you have your data prepared
   input_data = pd.DataFrame(...)  # Your input DataFrame

   # Initialize the building block
   splitter = SplitTrainTestLabel()

   # Set the required settings
   splitter.settings = {
       "selected_columns_label": ["target_column"],
       "selected_columns": ["feature1", "feature2", "feature3"],
       "shuffle": True
   }

   # Execute the splitting
   result = splitter.execute(input_data)

   # Access the split datasets
   x_train, x_valid, y_train, y_valid, label_column = result['output_data']

This example demonstrates how to initialize the `SplitTrainTestLabel` class, set the necessary settings, and execute the data splitting process. The resulting split datasets can then be used for further model training and evaluation tasks.
