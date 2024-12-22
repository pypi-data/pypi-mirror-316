<b><u>Module: TrainAndPredictLinReg</u></b>

This module is designed for training a linear regression model using the input data. Once the model is trained, it makes predictions on the test dataset and calculates the mean absolute error (MAE) between the predicted and actual values.

######

## Short description

The TrainAndPredictLinReg class wraps around a basic statistical analysis model - Linear Regression. Linear Regression is a linear approach to modeling the relationship between a dependent variable and one or more independent variables.

This model assumes a linear relationship between the input variables (X) and the single output variable (Y). More specifically, that Y can be calculated from a linear combination of the input variables (X).

The algorithm fits multiple lines on the data points and returns the line that results in the least error. This simple, yet powerful, method can provide a useful prediction in many simple and complex regression problems.

This Building Block trains a Linear Regression model on provided data, makes predictions on a test dataset, and then calculates the Mean Absolute Error (MAE), a straightforward and easy-to-interpret metric of prediction error.

## inputs
### Necessary:
- "input_data": A list of pandas DataFrames. The list should contain four elements in the following order: x_train, x_valid, y_train, y_valid.

### Optional:
none

## exits
In case of any exceptions during the model training, prediction, or MAE calculation, None is returned and a status code of 1 is set on the output port.

### Expected results:
The output of this module is a pandas DataFrame containing the actual and predicted values from the test dataset.

### Output format:
The output format is a pandas DataFrame.

## parameters
There are no parameters to set in the settings.json file for this module.

## History
1.0.0 -> Initial release
