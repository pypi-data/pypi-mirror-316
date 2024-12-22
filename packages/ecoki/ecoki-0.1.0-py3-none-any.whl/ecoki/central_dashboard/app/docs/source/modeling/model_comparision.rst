ModelPerformanceComparison
==========================

This module provides functionality for comparing the performance of various machine learning models. It is designed as part of the EcoKI architecture and is implemented as a building block for evaluating and comparing different modeling approaches.

The main component of this module is the `ModelPerformanceComparison` class, which encapsulates the process of:

1. Training and testing multiple machine learning models, including non-ML, simple ML, and complex ML models.
2. Handling multiple labels for multi-output scenarios.
3. Performing recursive feature elimination (RFE) if specified.
4. Optionally including neural network models in the comparison.
5. Generating error metrics and learning curves for each model and label.
6. Saving performance plots and results.

This module is particularly useful in machine learning pipelines where model selection and performance evaluation are crucial steps. It provides a comprehensive comparison of different modeling approaches, allowing users to make informed decisions about which models to use for their specific use cases.

Key features of this module include:
- Seamless integration with the EcoKI building block framework.
- Support for multiple labels and multi-output scenarios.
- Flexible inclusion of various model types, including neural networks.
- Comprehensive output including error metrics, learning curves, and RFE results.
- Automatic generation and saving of performance plots.

The module leverages various machine learning algorithms and evaluation techniques to provide a thorough comparison of model performances, making it a valuable tool for model selection and evaluation in the EcoKI ecosystem.

Detailed Functionality
----------------------

The `ModelPerformanceComparison` class utilizes several components to perform its tasks:

1. Model Training and Testing:
   - Non-ML models: Linear Regression
   - Simple ML models: Random Forest, XGBoost
   - Complex ML models: Neural Networks (optional)

2. Performance Metrics:
   - Root Mean Squared Error (RMSE)
   - Mean Absolute Error (MAE)
   - R-squared (R2) score

3. Feature Selection:
   - Recursive Feature Elimination (RFE) with cross-validation

4. Visualization:
   - Learning curves for each model and label
   - Feature importance plots
   - Error distribution plots

5. Results Processing:
   - Calculation of noteworthiness threshold for highlighting significant results
   - Compilation of error metrics and learning curve data

The core functionality is implemented in the `run_model_comparison` function, which orchestrates the entire comparison process. This function handles data preprocessing, model training, evaluation, and results compilation.

Parameters
----------

.. autoclass:: ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.model_performance_comparison.ModelPerformanceComparison
   :members:

Key Components
--------------

The module consists of several key components:

1. `src/run_model_comparison.py`: Contains the main `run_model_comparison` function that orchestrates the entire comparison process.

2. `src/models.py`: Defines the model classes for Linear Regression, Random Forest, and XGBoost.

3. `src/neural_network.py`: Handles the integration and execution of neural network models if included in the comparison.

4. `src/plotting.py`: Provides functions for generating various plots, including learning curves and feature importance visualizations.

5. `src/utils.py`: Contains utility functions for data processing, error calculation, and result formatting.

Example
-------

Here's a basic example of how to use the :class:`ModelPerformanceComparison` class:

.. code-block:: python

   from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.model_performance_comparison import ModelPerformanceComparison
   import pandas as pd

   # Assuming you have your data prepared
   input_data = pd.DataFrame(...)  # Your input DataFrame

   # Initialize the building block
   model_comparison = ModelPerformanceComparison()

   # Set the required settings
   model_comparison.settings = {
       "analysis_name": "my_analysis",
       "results_folder_name": "comparison_results",
       "labels_list": ["target1", "target2"],
       "numbers_list_rfe": [5, 10, 15],
       "savedir_path": "/path/to/save/results",
       "include_neural_network": True,
       "neural_network_python_script_path": "/path/to/nn_script.py",
       "neural_network_requirements_txt_path": "/path/to/requirements.txt",
       "plot_learning_curves": True
   }

   # Execute the model comparison
   result = model_comparison.execute(input_data)

   # Access the comparison results
   error_metrics = result['error_metrics_data']
   learning_curves = result['learning_curves_data']
   rfe_results = result['rfe_number_labels']
   noteworthiness_threshold = result['noteworthiness_threshold']
   plots_directory = result['plots_save_dir']

This example demonstrates how to initialize the `ModelPerformanceComparison` class, set the necessary settings, and execute the model comparison process. The resulting comparison data can then be used for further analysis and decision-making in the model selection process.

The `error_metrics_data` will contain detailed performance metrics for each model and label, while `learning_curves_data` provides information about model performance across different training set sizes. The `rfe_number_labels` result shows the optimal number of features selected by the Recursive Feature Elimination process for each label. The `noteworthiness_threshold` helps identify particularly significant results, and `plots_save_dir` indicates where the generated visualizations are stored.
