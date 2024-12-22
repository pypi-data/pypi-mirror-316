# Project Imports
from ecoki.building_block_framework.building_block import BuildingBlock

# Library Imports
import pandas as pd
from pandas import DataFrame
from typing import Dict
import json
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
import numpy as np

warnings.filterwarnings("ignore")

class TrainAndPredictLinReg(BuildingBlock):
    """A class for training and predicting with a linear regression model in a single output configuration.

    This class handles the training of a linear regression model for single-output regression tasks.
    It includes functionality for model training, prediction, and evaluation, including root mean squared error calculation.

    Attributes:
        architecture: The architecture name.
        version: The version of the building block.
        category: The category of the building block.
        description: A brief description of the building block functionality.
    """

    def __init__(self, **kwargs):
        """Initializes the TrainAndPredictLinReg building block with specified keyword arguments.

        Args:
            **kwargs: Keyword arguments for the BuildingBlock superclass.
        """
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.version = "1"
        self.category = "Transformer"
        self.description = "Building Block to LinearRegression model and calculate the root mean squared error (rmse)"

        self.add_inlet_port('input_data', list)
        self.add_outlet_port('output_data_preds', DataFrame)
        self.add_outlet_port('output_data_metrics', dict)
        self.add_outlet_port('output_data_hyperparameters', DataFrame)
        self.add_outlet_port('output_data_labels', DataFrame)

    def execute(self, input_data):
        """Executes the training and prediction process using Linear Regression on the provided input data.

        Args:
            input_data: A list containing the input data for the model. Expected to contain [X_train, X_test, y_train, y_test, label_column].

        Returns:
            A dictionary containing the results of the linear regression model predictions, evaluation metrics, default hyperparameters, and label columns.
            The dictionary includes:
            - output_data_preds: DataFrame containing the predicted values and the true values.
            - output_data_metrics: DataFrame containing the evaluation metrics.
            - output_data_hyperparameters: DataFrame containing the default hyperparameters of the model.
            - output_data_labels: DataFrame containing the label columns.
        """
        

        # Split the input data into train and test sets
        X_train = input_data[0]
        X_test = input_data[1]
        y_train = input_data[2]
        y_test = input_data[3]
        label_column = input_data[4]
        
        print("label_column is", label_column)
        print("\n")

        # Create the Regression model
        LinReg = LinearRegression()
        model = LinReg

        # train the model
        model.fit(X_train, y_train)
        
        # Save the model to disk
        filename = 'linear_regression_model.sav'
        pickle.dump(model, open(filename, 'wb'))

        # Load the model from disk
        model = pickle.load(open(filename, 'rb'))

        # predict on test set using trained model
        y_pred = model.predict(X_test)
        
                
        # Ensure predictions are non-negative
        y_pred = np.maximum(y_pred, 0)

        # calculate mean absolute error
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print("Root Mean Squared Error is:", rmse)

        # save results in a dataframe
        results = pd.DataFrame()
        
        for i, label in enumerate(label_column):
            results[f"True_{label}"] = y_test[label].values
            results[f"Predicted_{label}"] = y_pred[:, i]

        # Save the results
        results.to_csv("predictions.csv")
        print("Prediction results saved")



        # Create a dictionary with the mean squared error for each label column
        label = label_column[0] # Assuming label_column is a list with a single value
        metrics = {f"rmse_{label}": rmse}

        # Retrieve default hyperparameters from the linear regression class / documentation
        default_params = {
            'fit_intercept': True,
            'normalize': False,
            'copy_X': True,
            'n_jobs': None,
            'positive': False
        }


        # Convert the dictionary to a DataFrame
        hyperparameters_df = pd.DataFrame(default_params.items(), columns=['Hyperparameter', 'Default Value'])

        # Save the DataFrame to a CSV file
        hyperparameters_df.to_csv('hyperparameters.csv', index=False)

        return {"output_data_preds": results, "output_data_metrics": pd.DataFrame(metrics, index=[0]),
                "output_data_hyperparameters": hyperparameters_df, "output_data_labels": label_column}

