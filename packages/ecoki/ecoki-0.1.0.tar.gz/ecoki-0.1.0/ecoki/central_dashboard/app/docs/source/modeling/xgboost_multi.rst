TrainAndPredictXGBoostMultioutput
=================================


This module provides functionality for training and predicting with an XGBoost model in a multi-output configuration. It is designed as part of the EcoKI architecture and is implemented as a building block for machine learning pipelines.

The main component of this module is the `TrainAndPredictXGBoostMultioutput` class, which encapsulates the process of:

1. Training an XGBoost model using `MultiOutputRegressor` for handling multiple output variables.
2. Making predictions on test data.
3. Evaluating the model's performance using root mean squared error (RMSE).
4. Extracting feature importance information.
5. Providing comprehensive documentation using NumPy-style docstrings.

This module is particularly useful for regression tasks with multiple target variables, where the relationships between input features and multiple outputs need to be modeled simultaneously.

Key features of this module include:
- Seamless integration with the EcoKI building block framework.
- Automatic handling of multi-output regression scenarios.
- Model persistence for later use.
- Comprehensive output including predictions, feature importances, evaluation metrics, and model hyperparameters.

The module leverages the power of XGBoost for high performance and the flexibility of scikit-learn's `MultiOutputRegressor` for handling multiple outputs, making it a versatile tool for complex regression tasks in the EcoKI ecosystem.



Parameters
-----------

.. autoclass:: ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_xgboost_multioutput.train_and_predict_xgboost_multioutput.TrainAndPredictXGBoostMultioutput
   :members:


Other Methods
-------------

The module also includes several utility functions that support the main `TrainAndPredictXGBoostMultioutput` class:

.. autofunction:: ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_xgboost_multioutput.train_and_predict_xgboost_multioutput.get_pipeline_template

   Retrieves a pipeline template from the server.

.. autofunction:: ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_xgboost_multioutput.train_and_predict_xgboost_multioutput.add_custom_pipeline

   Adds a custom pipeline template to the server.

.. autofunction:: ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_xgboost_multioutput.train_and_predict_xgboost_multioutput.delete_custom_pipeline

   Deletes a custom pipeline from the server.

.. autofunction:: ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_xgboost_multioutput.train_and_predict_xgboost_multioutput.start_custom_pipeline

   Starts a custom pipeline on the server.

These utility functions are primarily used for managing pipeline templates and operations on the server. They provide functionality for retrieving, adding, deleting, and starting custom pipelines, which can be useful when working with more complex modeling workflows.



Example
-------

Here's a basic example of how to use the :class:`TrainAndPredictXGBoostMultioutput` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_xgboost_multioutput.train_and_predict_xgboost_multioutput import TrainAndPredictXGBoostMultioutput

   # Assuming you have your data prepared
   X_train, X_test, y_train, y_test, label_column = prepare_your_data()

   # Initialize the building block
   xgboost_multioutput = TrainAndPredictXGBoostMultioutput()

   # Execute the training and prediction
   results = xgboost_multioutput.execute([X_train, X_test, y_train, y_test, label_column])

   # Access the results
   predictions = results['output_data_preds']
   feature_importance = results['output_data_featimp']
   metrics = results['output_data_metrics']


.. seealso::
   :class:`sklearn.multioutput.MultiOutputRegressor`
   :class:`xgboost.XGBRegressor`
