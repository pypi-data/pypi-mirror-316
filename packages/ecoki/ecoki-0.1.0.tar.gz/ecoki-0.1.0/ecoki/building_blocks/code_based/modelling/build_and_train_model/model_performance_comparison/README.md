<b><u>Module: ModelPerformanceComparison</u></b>

The ModelPerformanceComparison module is designed to apply machine and non-machine learning techniques to a given dataset, compare their performance and make a recommendation about the best suited technique by balancing model complexity and prediction accuracy.

######

## Short description

Performance comparison of machine and non-machine learning techniques:

The ModelPerformanceComparison module is designed to apply machine and non-machine learning techniques to a given dataset, compare their performance and make a recommendation about the best suited technique by balancing model complexity and prediction accuracy.

The `ModelPerformanceComparison` class, part of the `BuildingBlock` suite, implements the functionality of training and testing simple non-ML(linear Regression), Simple ML(xgboost) and Complex ML(neural network) models with most relevant features selected via Recursive Feature Elimination(RFE). The user has the option of providing multiple values for the number of features to be selected via RFE. Using these features, the models are trained, evaluated and a series of error metrics and learning curve plots are generated to help the user visualize how the performance of the models changed with the number of features selected via RFE. Based on this information, a recommendation is also made about the best suited technique. For analysing a complex ML model such as a neural network, the users must provide the path of their own python script that trains and tests the model.

## Inputs
### Required:
- "input_data": A pandas DataFrame where features are in columns and each row is an observation.
- "savedir_path": Path to the folder in which the results(plots and dataframes) and other important(dependencies for neural networks, etc) data will be stored.
- "analysis_name": Folder created within savedir_path to help user identify results of current analysis from other.
- "results_folder_name": Folder created within analysis_name folder. This is helpful for the user if for a specific analysis, multiple datasets are used and the results for each dataset must have a separate folder.
- "labels_list": List of labels for supervised learning tasks.
- "numbers_list_rfe": List of numbers of features to be selected via RFE method.
- "plot_learning_curves": Whether to generate learning curves for viewing training and validation error against training set size.
- "include_neural_network": Whether to include a custom python script for training and testing complex ML model such as a neural network.

### Optional:
- "neural_network_python_script_path": Path to python script for training neural network. It is not required if include_neural_network is False, otherwise required.
- "neural_network_requirements_txt_path": Path to requirements.txt file for installing dependencies of the python script. It is not required if include_neural_network is False, otherwise required.

### Expected results:
1. Dataframes representing scores of various error metrics computed for non-ML and simple ML and complex ML models.
2. Learning curve scores (Training and Validation error) of non-ML and simple ML and complex ML models computed for various training set sizes.
3. List of labels for the numbers selected for RFE method. The plots of a respective number can be stored in a folder named with this label.
4. Value of noteworthiness threshold that is used to determine whether a simpler model can be recommended instead of a complex one.
5. Directory path to the results folder where images of model performance plots can be saved.

### Output format:
1. List of dataframes. Each dataframe has values for various error metrics applied to a specific model
2. List of data for plotting learning curves. Each list index represents the learning curve data of one number from the list of numbers selected for RFE method.
3. String name
4. Float value
5. String path

## History
1.0.0 -> Initial release