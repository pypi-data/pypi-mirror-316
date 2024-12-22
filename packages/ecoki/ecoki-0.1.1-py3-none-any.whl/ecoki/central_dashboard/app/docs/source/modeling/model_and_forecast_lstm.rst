ModelAndForecast LSTM
=====================

This module provides functionality for building, training, and making predictions using an LSTM (Long Short-Term Memory) model. It is designed as part of the EcoKI architecture and is implemented as a building block for time series forecasting tasks.

The main component of this module is the `ModelAndForecast` class, which encapsulates the process of:

1. Building an LSTM model with configurable complexity.
2. Training the model on provided time series data.
3. Making predictions on a test dataset.
4. Handling multi-step time series forecasting.

This module is particularly useful in machine learning pipelines where time series forecasting is required. It provides a flexible LSTM implementation that can be easily integrated into larger data processing and analysis workflows.

Key features of this module include:
- Seamless integration with the EcoKI building block framework.
- Support for configurable LSTM model complexity.
- Handling of multi-dimensional input features and multi-step output predictions.
- Automatic reshaping of input and output data to fit LSTM requirements.
- Customizable model architecture based on the specified complexity level.

The module leverages Keras and TensorFlow backend to implement the LSTM model, making it a powerful tool for sequence prediction tasks in the EcoKI ecosystem.

Detailed Functionality
----------------------

The `ModelAndForecast` class utilizes several components to perform its tasks:

1. Model Building:
   - Configurable LSTM architecture based on the specified complexity level.
   - Support for both basic and more complex LSTM configurations.

2. Data Handling:
   - Reshaping of input and output data to match LSTM requirements.
   - Support for multi-dimensional features and multi-step predictions.

3. Model Training:
   - Compilation of the LSTM model with MSE loss and Adam optimizer.
   - Training the model on the provided training data.

4. Prediction:
   - Making forecasts on the test dataset.
   - Handling of multi-step predictions.

The core functionality is implemented in the `build_model` method, which constructs and trains the LSTM model, and the `execute` method, which orchestrates the entire process of model building, training, and prediction.

Parameters
----------

.. autoclass:: ecoki.building_blocks.code_based.modelling.build_and_train_model.model_and_forecast_lstm.model_and_forecast.ModelAndForecast
   :members:

Key Components
--------------

The module consists of several key components:

1. `ModelAndForecast` class: The main class that encapsulates the LSTM model building and forecasting functionality.

2. `build_model` method: Responsible for constructing and training the LSTM model.

3. `execute` method: Orchestrates the entire process of data preparation, model building, training, and prediction.

Example
-------

Here's a basic example of how to use the :class:`ModelAndForecast` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_and_forecast_lstm.model_and_forecast import ModelAndForecast
   import numpy as np

   # Assuming you have your data prepared
   input_data = [...]  # Your input data list
   data_sequences_timesteps = [...]  # Your data sequences and timesteps
   target_column = {...}  # Your target column dictionary

   # Initialize the building block
   lstm_model = ModelAndForecast()

   # Set the required settings
   lstm_model.settings = {
       "nn_complexity": "Basic"  # or "Complex" for a more sophisticated model
   }

   # Execute the model building and forecasting
   result = lstm_model.execute(input_data, data_sequences_timesteps, target_column)

   # Access the results
   test_and_forecasted_data = result['test_and_forecasted_data']
   sequences_timesteps = result['sequences_timesteps']
   target = result['target']

This example demonstrates how to initialize the `ModelAndForecast` class, set the necessary settings, and execute the LSTM model building and forecasting process. The resulting data can then be used for further analysis or integration into a larger machine learning pipeline.

The `test_and_forecasted_data` will contain the predictions made by the LSTM model on the test dataset. The `sequences_timesteps` and `target` outputs provide information about the data structure used in the model.
