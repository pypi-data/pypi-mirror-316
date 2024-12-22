TrainAndPredictLinReg
=====================

This module provides functionality for training and predicting with a Linear Regression model in a single-output configuration. It is designed as part of the EcoKI architecture and is implemented as a building block for machine learning pipelines.

The main component of this module is the `TrainAndPredictLinReg` class, which encapsulates the process of:

1. Training a Linear Regression model for single-output regression tasks.
2. Making predictions on test data.
3. Evaluating the model's performance using root mean squared error (RMSE).
4. Saving and loading the trained model.
5. Providing comprehensive documentation using NumPy-style docstrings.

This module is particularly useful for simple regression tasks where a linear relationship between input features and a single output variable needs to be modeled.

Key features of this module include:
- Seamless integration with the EcoKI building block framework.
- Automatic handling of single-output regression scenarios.
- Model persistence for later use.
- Comprehensive output including predictions, evaluation metrics, and model hyperparameters.

The module leverages the simplicity and interpretability of Linear Regression, making it a useful tool for baseline modeling and scenarios where model explainability is crucial in the EcoKI ecosystem.

Parameters
-----------

.. autoclass:: ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_lin_reg.train_and_predict_lin_reg.TrainAndPredictLinReg
   :members:

Example
-------

Here's a basic example of how to use the :class:`TrainAndPredictLinReg` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_lin_reg.train_and_predict_lin_reg import TrainAndPredictLinReg

   # Assuming you have your data prepared
   X_train, X_test, y_train, y_test, label_column = prepare_your_data()

   # Initialize the building block
   lin_reg = TrainAndPredictLinReg()

   # Execute the training and prediction
   results = lin_reg.execute([X_train, X_test, y_train, y_test, label_column])

   # Access the results
   predictions = results['output_data_preds']
   metrics = results['output_data_metrics']
   hyperparameters = results['output_data_hyperparameters']

.. seealso::
   :class:`sklearn.linear_model.LinearRegression`

