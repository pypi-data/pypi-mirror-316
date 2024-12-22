# Project Imports
from ecoki.building_block_framework.building_block import BuildingBlock

# Library Imports
import pandas as pd
from pandas import DataFrame
from typing import Dict
import json
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
import pickle
import requests
import numpy as np

def get_pipeline_template(template_name):
    """
    Retrieves a pipeline template from the server.

    Args:
        template_name (str): The name of the template to retrieve.

    Returns:
        dict: The pipeline template payload if successful, empty list otherwise.
    """
    try:
        #TODO: replace host and port
        collected = requests.get('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/ecoki/'+str(template_name)+'/content/')
        if collected.status_code == 200:
            # parse the JSON response and retrieve the pipeline topology
            result = collected.json()["payload"]
    except:
        result = []
    return result

def add_custom_pipeline(template):
    """
    Adds a custom pipeline template to the server.

    Args:
        template (dict): The pipeline template to add.

    Returns:
        None
    """
    try:
        #TODO: replace host and port
        collected = requests.post('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/custom/add/'+str(template["name"])+'/content/?overwrite=true', json.dumps(template))
        if collected.status_code == 200:
            print("success")
    except:
        print("failed")
    return

def delete_custom_pipeline(name):
    """
    Deletes a custom pipeline from the server.

    Args:
        name (str): The name of the pipeline to delete.

    Returns:
        None
    """
    try:
        #TODO: replace host and port
        collected = requests.delete('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/?pipeline_name='+str(name)+'')
        if collected.status_code == 200:
            print("success")
    except:
        print("failed")
    return

def start_custom_pipeline(name):
    """
    Starts a custom pipeline on the server.

    Args:
        name (str): The name of the pipeline to start.

    Returns:
        None
    """
    try:
        #TODO: replace host and port
        collected = requests.put('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/?pipeline_type=custom&pipeline_name='+str(name)+'')
        if collected.status_code == 200:
            print("success")
    except:
        print("failed")
    return

warnings.filterwarnings("ignore")

class TrainAndPredictXGBoostMultioutput(BuildingBlock):
    """
    A class for training and predicting with an XGBoost model in a multi-output configuration.

    This class handles the training of an XGBoost model using MultiOutputRegressor for multi-output regression tasks.
    It includes functionality for model training, prediction, and evaluation, including root mean squared error calculation
    and feature importance extraction.

    Attributes:
        architecture (str): The architecture name.
        version (str): The version of the building block.
        category (str): The category of the building block.
        description (str): A brief description of the building block functionality.
    """

    def __init__(self, **kwargs):
        """
        Initializes the TrainAndPredictXGBoostMultioutput building block with specified keyword arguments.

        Args:
            **kwargs: Keyword arguments for the BuildingBlock superclass.
        """
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.version = "1"
        self.category = "Transformer"
        self.description = "Building Block to train a MultiOutputRegressor in combination with XGBoost regression model. Also predict values on the test set (10% of dataset) and calculate the root mean squared error(rmse)"

        self.add_inlet_port('input_data', list)
        self.add_outlet_port('output_data_preds', DataFrame)
        self.add_outlet_port('output_data_featimp', DataFrame)
        self.add_outlet_port('output_data_metrics', dict)
        self.add_outlet_port('output_data_hyperparameters', DataFrame)
        self.add_outlet_port('output_data_labels', DataFrame)

    def execute(self, input_data):
        """
        Executes the training and prediction process using XGBoost with MultiOutputRegressor on the provided input data.

        Args:
            input_data (list): A list containing the input data for the model. Expected to contain [X_train, X_test, y_train, y_test, label_column].

        Returns:
            dict: A dictionary containing the results of the XGBoost model predictions, feature importances, evaluation metrics, default hyperparameters, and label columns.

        The returned dictionary includes:
            - output_data_preds: DataFrame containing the predicted values and the true values.
            - output_data_featimp: DataFrame containing the feature importances.
            - output_data_metrics: DataFrame containing the evaluation metrics.
            - output_data_hyperparameters: DataFrame containing the default hyperparameters of the model.
            - output_data_labels: DataFrame containing the label columns.
        """
        # Split the input data into train and test sets
        X_train, X_test, y_train, y_test, label_column = input_data

        # Create the XGBoost regressor model
        xgb_regressor = xgb.XGBRegressor()

        # Create the multi-output regressor model using XGBoost
        multi_output_regressor = MultiOutputRegressor(xgb_regressor)

        # Train the multi-output model
        multi_output_regressor.fit(X_train, y_train)

        # Save the model to disk
        filename = 'trained_model.sav'
        pickle.dump(multi_output_regressor, open(filename, 'wb'))

        # Load the model from disk
        multi_output_regressor = pickle.load(open(filename, 'rb'))

        # Make predictions
        y_pred = multi_output_regressor.predict(X_test)
        
        # Ensure predictions are non-negative
        y_pred = np.maximum(y_pred, 0)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
        rmse = np.sqrt(mse)
        # Print the root mean squared error for each label column
        for i, rmse_value in enumerate(rmse):
            print(f"Root Mean Squared Error for {label_column[i]}: {rmse_value:.4f}")

        # Save results in a dataframe
        results = pd.DataFrame()
        for i, label in enumerate(label_column):
            results[f"True_{label}"] = y_test[label].values
            results[f"Predicted_{label}"] = y_pred[:, i]

        # Save the results
        results.to_csv("predictions.csv")
        print("Prediction results saved")

        # Get feature importance for each output model
        feature_importances = pd.DataFrame(index=X_train.columns)
        for i, estimator in enumerate(multi_output_regressor.estimators_):
            feature_importances[f'{label_column[i]}'] = estimator.feature_importances_
        feature_importances.sort_values(by=f'{label_column[0]}', ascending=False, inplace=True)
        feature_importances.to_csv('feature_importances.csv')

        # Create a dictionary with the root mean squared error for each label column
        metrics = {f"rmse_{label_column[i]}": rmse_value for i,rmse_value in enumerate(rmse)}

        # Retrieve default hyperparameters from the XGBoost regressor class / documentation
        default_params = {
            'n_estimators': 100,
            'max_depth': 3,
            'validate_parameters': False,
            'nthread': "default to maximum number of threads available if not set",
            'objective': 'reg:squarederror',
            'base_score': 0.5,
            'booster': 'gbtree',
            'colsample_bylevel': 1,
            'colsample_bynode': 1,
            'colsample_bytree': 1,
            'gamma': 0,
            'gpu_id': -1,
            'importance_type': 'gain',
            'interaction_constraints': 'Check documentation for details',
            'learning_rate': 0.300000012,
            'max_delta_step': 0,
            'min_child_weight': 1,
            'missing': "None",
            'monotone_constraints': 'Check documentation for details',
            'n_jobs': 1,
            'num_parallel_tree': 1,
            'random_state': 0,
            'reg_alpha': 0,
            'reg_lambda': 1,
            'scale_pos_weight': 1,
            'subsample': 1,
            'tree_method': 'auto',
            'verbosity': 1
        }

        # Convert the dictionary to a DataFrame
        hyperparameters_df = pd.DataFrame(default_params.items(), columns=['Hyperparameter', 'Default Value'])

        # Save the DataFrame to a CSV file
        hyperparameters_df.to_csv('hyperparameters.csv', index=False)

        # create inference pipeline
        if self.settings["create_inference_pipeline_template"]:
            print("a")

            # get the inference pipeline template (already there as an ecoKI pipeline)
            inference_pipeline_template = get_pipeline_template("Inference_Xgboost_Multi")

            # adjust the settings to the trained model
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["label_names"] = y_test.columns.values.tolist()
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["feature_names"] = X_test.columns.values.tolist()
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["model_file_path"] = "trained_model.sav"

            # set the name of the pipeline (idea: do it in future dynamically based on the name of the train-pipeline?
            inference_pipeline_template["name"] = "Inference_Xgboost_Multi_custom"

            # save new template as a custom pipeline template via api
            add_custom_pipeline(inference_pipeline_template)

            # stop it if theres already a pipeline with this name on the active/running pipelines
            if inference_pipeline_template["name"] in self.pipeline_manager.pipelines.keys():

                # stop pipeline
                delete_custom_pipeline(inference_pipeline_template["name"])

            # in case the pipeline should be started, start it
            if self.settings["create_inference_pipeline"]:

                # start pipeline
                start_custom_pipeline(inference_pipeline_template["name"])

        return {"output_data_preds": results, "output_data_featimp": feature_importances, "output_data_metrics": pd.DataFrame(metrics, index=[0]),
                "output_data_hyperparameters": hyperparameters_df, "output_data_labels": label_column}

