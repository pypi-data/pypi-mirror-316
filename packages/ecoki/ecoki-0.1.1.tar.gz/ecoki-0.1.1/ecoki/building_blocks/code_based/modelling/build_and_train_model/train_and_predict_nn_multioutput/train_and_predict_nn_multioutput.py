# Project Imports
from ecoki.building_block_framework.building_block import BuildingBlock

# Library Imports
import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import Dict
import json
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
import pickle
import requests

from numpy import array
from keras.models import Sequential, Model
from keras.layers import Input, LSTM, Dense, Concatenate, Dropout, Masking, Flatten, TimeDistributed
from keras.callbacks import ReduceLROnPlateau,ModelCheckpoint,TensorBoard
from time import time, sleep
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras.optimizers import Adam

def get_pipeline_template(template_name):
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
    try:
        #TODO: replace host and port
        collected = requests.post('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/custom/add/'+str(template["name"])+'/content/?overwrite=true', json.dumps(template))
        if collected.status_code == 200:
            print("sucess")
            # parse the JSON response and retrieve the pipeline topology
            #result = collected.json()["payload"]
    except:
        print("failed")
        #result = []
    return

def delete_custom_pipeline(name):
    try:
        #TODO: replace host and port
        collected = requests.delete('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/?pipeline_name='+str(name)+'')
        if collected.status_code == 200:
            print("sucess")
    except:
        print("failed")

    return

def start_custom_pipeline(name):
    try:
        #TODO: replace host and port
        collected = requests.put('http://'+str("localhost")+':'+str(5000)+'/api/v1/pipelines/?pipeline_type=custom&pipeline_name='+str(name)+'')
        if collected.status_code == 200:
            print("sucess")
    except:
        print("failed")

    return

warnings.filterwarnings("ignore")

class TrainAndPredictNNMultioutput(BuildingBlock):
    """
    "Dieser Baustein trainiert ein neuronales Netz (Regressor) basierend auf Trainings. und Testdatensatz"

    Inlets:
    - input_data: list

    Outlets:
    - output_data_preds: DataFrame
    - output_data_featimp: DataFrame
    - output_data_metrics: dict
    - output_data_hyperparameters: DataFrame
    - output_data_labels: DataFrame
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.version = "1"
        self.category = "Transformer"
        self.description = "Dieser Baustein trainiert ein neuronales Netz (Regressor) basierend auf Trainings. und Testdatensatz"

        self.add_inlet_port('input_data', list)
        self.add_outlet_port('output_data_preds', DataFrame)
        self.add_outlet_port('output_data_featimp', DataFrame)
        self.add_outlet_port('output_data_metrics', dict)
        self.add_outlet_port('output_data_hyperparameters', DataFrame)
        self.add_outlet_port('output_data_labels', DataFrame)
        self.add_outlet_port('output_data_all', DataFrame)

    def execute(self, input_data):

        # Split the input data into train and test sets
        X_train = input_data[0]
        X_test = input_data[1]
        y_train = input_data[2]
        y_test = input_data[3]
        label_column = input_data[4]

        # build model
        input_layer = Input(shape=(X_train.shape[1]))

        # define dense layers with x units according to the settings
        first_layer = True
        for units in self.settings["dense_layers"]:
            if first_layer:
                combined_output = Dense(units, activation='relu')(input_layer)

                if self.settings["dropout"]>0:
                    combined_output = Dropout(self.settings["dropout"])(combined_output)

                first_layer= False
            else:
                combined_output = Dense(units, activation='relu')(combined_output)

                if self.settings["dropout"] > 0:
                    combined_output = Dropout(self.settings["dropout"])(combined_output)

        # define last layer
        x = Dense(y_train.shape[1])(combined_output)

        # create the model
        model = Model(inputs=[input_layer], outputs=x)

        # Initialisieren Sie den Adam-Optimierer mit der definierten Lernrate
        optimizer = Adam(learning_rate=self.settings["learning_rate"])

        # compile the model with an optimizer and a loss function
        model.compile(optimizer=optimizer, loss='mse')

        # defne callbacks
        filepath = "nn_weights.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=20, min_lr=0.00001)
        #tbCallBack = TensorBoard(log_dir="C:/tmp/logs/{}".format(time()), histogram_freq=0, write_graph=True, write_images=True)

        # scale
        feature_scaler = MinMaxScaler()
        feature_scaler = feature_scaler.fit(X_train)
        X_train_scaled = feature_scaler.transform(X_train)
        X_test_scaled = feature_scaler.transform(X_test)

        label_scaler = MinMaxScaler()
        label_scaler = label_scaler.fit(y_train)
        y_train_scaled = label_scaler.transform(y_train)
        y_test_scaled = label_scaler.transform(y_test)

        # fit model
        history = model.fit(X_train_scaled, y_train_scaled, batch_size=self.settings["batch_size"], epochs=self.settings["epochs"], verbose=1, validation_data=(X_test_scaled, y_test_scaled), callbacks=[reduce_lr, checkpoint], shuffle=True)

        # load best weights
        model.load_weights("nn_weights.hdf5")

        # save whole model and scaler
        model.save('nn_model.h5')
        pickle.dump(feature_scaler, open('nn_model_feature_scaler.sav', 'wb'))
        pickle.dump(label_scaler, open('nn_model_label_scaler.sav', 'wb'))

        # load it again
        new_model = load_model('nn_model.h5')
        feature_scaler_new = pickle.load(open('nn_model_feature_scaler.sav', 'rb'))
        label_scaler_new = pickle.load(open('nn_model_label_scaler.sav', 'rb'))

        #
        # # Create the XGBoost regressor model
        # xgb_regressor = xgb.XGBRegressor()
        #
        # # Create the multi-output regressor model using XGBoost
        # multi_output_regressor = MultiOutputRegressor(xgb_regressor)
        #
        # # Train the multi-output model
        # multi_output_regressor.fit(X_train, y_train)
        #
        # # Save the model to disk
        # filename = 'trained_model.sav'
        # pickle.dump(multi_output_regressor, open(filename, 'wb'))
        #
        # # Load the model from disk
        # multi_output_regressor = pickle.load(open(filename, 'rb'))

        # Make predictions
        y_pred_scaled = new_model.predict(X_test_scaled)
        y_pred = label_scaler_new.inverse_transform(y_pred_scaled)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')

        # Print the mean squared error for each label column
        for i, mse_value in enumerate(mse):
            print(f"Mean Squared Error for {label_column[i]}: {mse_value:.4f}")

        # save results in a dataframe
        results = pd.DataFrame()
        for i, label in enumerate(label_column):
            results[f"True_{label}"] = y_test[label].values
            results[f"Predicted_{label}"] = y_pred[:, i]

        # save the results
        results.to_csv("predictions.csv")
        print("prediction results saved")

        # # Get feature importance for each output model
        # # Initialize an empty DataFrame with columns as features
        # feature_importances = pd.DataFrame(index=X_train.columns)
        #
        # # Get feature importance for each output model
        # for i, estimator in enumerate(multi_output_regressor.estimators_):
        #     # Add the feature importances as a new column to the DataFrame
        #     feature_importances[f'{label_column[i]}'] = estimator.feature_importances_
        #
        # # Sort the DataFrame by importance for the first label column
        # feature_importances.sort_values(by=f'{label_column[0]}', ascending=False, inplace=True)
        #
        # # Save to a CSV file
        # feature_importances.to_csv('feature_importances.csv')

        # Create a dictionary with the mean squared error for each label column
        metrics = {}
        for i, mse_value in enumerate(mse):
            metrics[f"mse_{label_column[i]}"] = mse_value

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
            inference_pipeline_template = get_pipeline_template("Inference_Neural_Network_Multi")

            # adjust the settings to the trained model
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["label_names"] = y_test.columns.values.tolist()
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["feature_names"] = X_test.columns.values.tolist()
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["model_file_path"] = "nn_model.h5"
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["feature_scaler_file_path"] = "nn_model_feature_scaler.sav"
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["label_scaler_file_path"] = "nn_model_label_scaler.sav"


            # set the name of the pipeline (idea: do it in future dynamically based on the name of the train-pipeline?
            inference_pipeline_template["name"] = "Inference_Neural_Network_Multi_custom"

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

        # create results data
        output_data_all = pd.concat([X_test.reset_index().drop(labels = 'index',axis=1),results.reset_index().drop(labels = 'index',axis=1)],axis=1)

        return {"output_data_preds": results, "output_data_featimp": None, "output_data_metrics": pd.DataFrame(metrics, index=[0]),
                "output_data_hyperparameters": hyperparameters_df, "output_data_labels": label_column,'output_data_all':output_data_all}


