"""
Design Document for Pytest of TrainAndPredictLinReg Module
===========================================================

Objective
---------
To ensure the TrainAndPredictLinReg module functions correctly by validating its behavior against expected outcomes using a test dataset.

Components to Test
------------------
1. Initialization:
   - Test if the TrainAndPredictLinReg class initializes correctly with the expected default properties.

2. Execution:
   - Test if the `execute` method processes input data correctly and returns the expected output structure.
   - Validate the correctness of the model training by checking if the model is saved and loaded correctly.
   - Verify the prediction results by comparing the predicted values against known outcomes from the test dataset.
   - Ensure the calculation of the root mean squared error (RMSE) is accurate.
   - Check if the results, metrics, hyperparameters, and labels are correctly saved into their respective dataframes and files.

3. Output Data:
   - Ensure the output dictionary contains all expected keys (`output_data_preds`, `output_data_metrics`, `output_data_hyperparameters`, `output_data_labels`).
   - Validate the format and integrity of the dataframes within the output dictionary.

Test Dataset
------------
The test dataset located at "ecoki/tests/test_dataset.csv" will be used for testing. It should be split into training and testing sets to simulate a real-world scenario.

Pytest Structure
----------------
1. Fixture for Setup:
   - A fixture that loads the test dataset, splits it into training and testing sets, and prepares the input format expected by the `execute` method.

2. Test Initialization:
   - A test function to verify the initialization of the TrainAndPredictLinReg class.

3. Test Execution:
   - A test function to verify the `execute` method's behavior and output structure.
   - Sub-tests to validate model saving and loading, prediction accuracy, RMSE calculation, and output data integrity.

4. Test Output Data:
   - Test functions to validate the presence and correctness of each key in the output dictionary.
   - Sub-tests to check the integrity and format of the dataframes within the output dictionary.

"""

from ecoki.building_blocks.code_based.modelling.build_and_train_model.train_and_predict_lin_reg.train_and_predict_lin_reg import TrainAndPredictLinReg
import pytest
import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np
import os
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def test_initialization():
    """
    Tests the initialization of the TrainAndPredictLinReg class.

    This test verifies if the TrainAndPredictLinReg class initializes with the expected default properties and correctly sets up its inlet and outlet ports.

    """
    # Initialize the TrainAndPredictLinReg instance
    lin_reg_block = TrainAndPredictLinReg(name='linreg_init_test')

    # Assertions to verify correct initialization properties
    assert lin_reg_block.architecture == "EcoKI", "Architecture property not initialized as expected."
    assert lin_reg_block.version == "1", "Version property not initialized as expected."
    assert lin_reg_block.category == "Transformer", "Category property not initialized as expected."
    assert lin_reg_block.description == "Building Block to LinearRegression model and calculate the root mean squared error (rmse)", "Description property not initialized as expected."
    
    # Assertions to verify the correct setup of inlet and outlet ports
    assert lin_reg_block.check_port_exists('input_data', 'inlet'), "Inlet port 'input_data' is missing."
    assert lin_reg_block.check_port_exists('output_data_preds', 'outlet'), "Outlet port 'output_data_preds' is missing."
    assert lin_reg_block.check_port_exists('output_data_metrics', 'outlet'), "Outlet port 'output_data_metrics' is missing."
    assert lin_reg_block.check_port_exists('output_data_hyperparameters', 'outlet'), "Outlet port 'output_data_hyperparameters' is missing."
    assert lin_reg_block.check_port_exists('output_data_labels', 'outlet'), "Outlet port 'output_data_labels' is missing."
    

@pytest.fixture
def setup_data():
    """
    Loads the test dataset and splits it into training and testing sets.

    Returns
    -------
    tuple
        A tuple containing the training and testing datasets and the label column.
    """
    # Load the dataset
    data = pd.read_csv('ecoki/tests/test_dataset.csv')
    X = data.drop(['Appliances', 'date'], axis=1)
    y = data[['Appliances']]
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test, ['Appliances']

def test_execute(setup_data):
    """
    Tests the `execute` method of the TrainAndPredictLinReg class.
    """
    X_train, X_test, y_train, y_test, label_column = setup_data
    
    # Initialize the TrainAndPredictLinReg instance
    lin_reg_block = TrainAndPredictLinReg(name='linreg_execute_test')
    
    # Execute the method
    output = lin_reg_block.execute([X_train, X_test, y_train, y_test, label_column])
    
    # Assertions to ensure correct execution
    assert 'output_data_preds' in output, "Missing output_data_preds in output"
    assert 'output_data_metrics' in output, "Missing output_data_metrics in output"
    assert 'output_data_hyperparameters' in output, "Missing output_data_hyperparameters in output"
    assert 'output_data_labels' in output, "Missing output_data_labels in output"
    
    # Validate the format and integrity of the dataframes within the output dictionary
    assert isinstance(output['output_data_preds'], pd.DataFrame), "output_data_preds is not a DataFrame"
    assert isinstance(output['output_data_metrics'], pd.DataFrame), "output_data_metrics is not a DataFrame"
    assert isinstance(output['output_data_hyperparameters'], pd.DataFrame), "output_data_hyperparameters is not a DataFrame"
    assert isinstance(output['output_data_labels'], list), "output_data_labels is not a list"
    
    # Validate prediction accuracy and RMSE calculation
    true_values = y_test[label_column[0]].values
    predicted_values = output['output_data_preds'][f"Predicted_{label_column[0]}"].values
    rmse = np.sqrt(mean_squared_error(true_values, predicted_values))
    assert rmse == output['output_data_metrics']['rmse_Appliances'].values[0], "RMSE calculation is incorrect"

    # Test model saving and loading
    saved_model_path = 'linear_regression_model.sav'
    assert os.path.exists(saved_model_path), "Model file was not saved"
    
    # Load the model and ensure it's of the correct type
    loaded_model = pickle.load(open(saved_model_path, 'rb'))
    assert isinstance(loaded_model, LinearRegression), "Loaded model is not a LinearRegression instance"
    
    # Ensure the loaded model can make predictions
    loaded_model_predictions = loaded_model.predict(X_test)
    assert len(loaded_model_predictions) == len(y_test), "Loaded model predictions length mismatch with test labels length"
    
    # Clean up saved model file
    os.remove(saved_model_path)

def test_prediction_accuracy(setup_data):
    """
    Tests the prediction accuracy of the TrainAndPredictLinReg model by comparing
    the predicted values against the known outcomes from the test dataset.
    """
    X_train, X_test, y_train, y_test, label_column = setup_data

    # Initialize the TrainAndPredictLinReg instance
    lin_reg_block = TrainAndPredictLinReg(name='linreg_prediction_accuracy_test')

    # Execute the method
    output = lin_reg_block.execute([X_train, X_test, y_train, y_test, label_column])

    # Extract true and predicted values
    true_values = y_test[label_column[0]].values
    predicted_values = output['output_data_preds'][f"Predicted_{label_column[0]}"].values

    # Calculate the accuracy of the predictions
    accuracy = np.mean(np.abs(true_values - predicted_values) / true_values) * 100

    # Assert that the accuracy is within an acceptable range
    assert accuracy <= 10, f"Prediction accuracy is not within acceptable range. Found: {accuracy}%"

def test_output_data_integrity_and_format(setup_data):
    """
    Tests the integrity and format of the dataframes within the output dictionary
    to ensure they meet the expected structure and data types.
    """
    X_train, X_test, y_train, y_test, label_column = setup_data

    # Initialize the TrainAndPredictLinReg instance
    lin_reg_block = TrainAndPredictLinReg(name='linreg_output_data_test')

    # Execute the method
    output = lin_reg_block.execute([X_train, X_test, y_train, y_test, label_column])

    # Test for the integrity and format of the output data predictions
    preds_df = output['output_data_preds']
    assert isinstance(preds_df, pd.DataFrame), "Predictions output is not a DataFrame"
    assert f"Predicted_{label_column[0]}" in preds_df.columns, "Predictions DataFrame missing expected column"
    assert preds_df[f"Predicted_{label_column[0]}"].dtype == np.float64, "Predictions column data type is incorrect"

    # Test for the integrity and format of the output data metrics
    metrics_df = output['output_data_metrics']
    assert isinstance(metrics_df, pd.DataFrame), "Metrics output is not a DataFrame"
    assert 'rmse_Appliances' in metrics_df.columns, "Metrics DataFrame missing expected column"
    assert metrics_df['rmse_Appliances'].dtype == np.float64, "Metrics column data type is incorrect"

    # Test for the integrity and format of the output data hyperparameters
    hyperparams_df = output['output_data_hyperparameters']
    assert isinstance(hyperparams_df, pd.DataFrame), "Hyperparameters output is not a DataFrame"
    assert all(isinstance(item, str) for item in hyperparams_df.columns), "Hyperparameters DataFrame columns are not all strings"

    # Test for the integrity and format of the output data labels
    labels_df = output['output_data_labels']
    assert isinstance(labels_df, list), "Labels output is not a list"
    assert label_column[0] in labels_df, "Labels list missing expected label"
