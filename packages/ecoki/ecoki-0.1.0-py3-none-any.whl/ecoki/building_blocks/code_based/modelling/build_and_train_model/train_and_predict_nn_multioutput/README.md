<b><u>Module: TrainAndPredictNNMultioutput</u></b>

This module is designed to perform hyperparameter tuning (if the size of the dataset is large, i.e., greater than 10,000 records) using GridSearchCV, train an XGBoost regression model with MultiOutputRegressor on the input data, predict values on the test set (10% of the dataset), and calculate the Mean Squared Error (MSE) between the predicted and actual values.

######

## Short description

The TrainAndPredictXGBoostMultioutput class encapsulates the functionality of XGBoost, a powerful gradient boosting algorithm, used in combination with a MultiOutputRegressor from Scikit-learn. This combination is used to handle multi-output (multiple target variables) regression tasks.

The class leverages the MultiOutputRegressor wrapper that takes a regressor as input and creates a new regressor that uses the underlying regressor to predict each of the outputs separately. This helps in the prediction of multiple dependent variables simultaneously.

In the context of XGBoost, the class trains a model for each of the target variables independently, while using a single set of features. The MultiOutputRegressor uses the fit and predict methods for each target variable independently.

Similar to the previous classes, if the dataset size is large (>10k records), hyperparameter tuning is applied using GridSearchCV. Predictions are made on the test dataset and performance metrics (Mean Squared Error in this case) are computed for evaluation.

This Building Block additionally provides feature importance data, which represents the contribution of each feature in the predictive model. This can be particularly helpful in understanding the influence of different features on the predictive model. Feature importance data is usually obtained from the feature_importances_ attribute of the XGBoost model.

Furthermore, the class also saves and provides the hyperparameters used in the XGBoost model. This can be useful in future debugging or optimization tasks.

## Inputs
### Necessary:
- "input_data": A list of pandas DataFrames. The list should contain four elements in the following order: x_train, x_test, y_train, y_test.

### Optional:
none

## Exits
In case of any exceptions during the model training, prediction, or MSE calculation, None is returned and a status code of 1 is set on the output port.

### Expected results:
The output of this module is a pandas DataFrame containing the actual and predicted values from the test dataset. It also includes the feature importance and hyperparameters used in the XGBoost model.

### Output format:
The output format is a pandas DataFrame.

## Parameters
"label_column": List containing the names of the label columns.

## History
1.0.0 -> Initial release