# Project Imports
from ecoki.building_block_framework.building_block import BuildingBlock

# Library Imports
import pandas as pd
from pandas import DataFrame
import json
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings("ignore")
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error

import numpy as np
warnings.filterwarnings("ignore")


class TrainAndPredictXGBoost(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.version = "1"
        self.category = "Transformer"
        self.description = "Building Block to do hyperparameter tuning (if dataset is large (>10k) using GridSearchCV, and Trains a XGBoost regression model. Also predict\
                values on the test set (10% of dataset) and calculate the mean average error (mae)"

        self.add_inlet_port('input_data', list)
        self.add_outlet_port('output_data_preds', DataFrame)
        self.add_outlet_port('output_data_featimp', DataFrame)


    def execute(self, input_data):

        label_column = self.settings["label_column"]
        print("label_column is", label_column)
        label_column = label_column[0]
        x_train = input_data[0]

        x_valid = input_data[1]
        y_train = pd.DataFrame()

        y_train[label_column] = input_data[2]

        y_train = y_train.astype(float)
        y_valid = pd.DataFrame()

        y_valid[label_column] = input_data[3]
        y_valid = y_valid.astype(float)

        # Regression model
        xgb1 = xgb.XGBRegressor(verbosity=0)

        # Do hyperparameter tuning if length of train dataset is >10k
        if len(x_train) > 10000:
            
            print("Hyperparameter tuning using GridSearchCV is being done since the length of train dataset is >10k")
            # chose the parameter pool to do grid search
            parameters = {'nthread': [4],  # when use hyperthread, xgboost may become slower
                            'objective': ['reg:squarederror'],
                            'learning_rate': [.3, 0.5],  # so called `eta` value
                            'max_depth': [5, 6],
                            'min_child_weight': [4],
                            'silent': [1],
                            'subsample': [0.7],
                            'colsample_bytree': [0.7, 0.8, 0.9],
                            'n_estimators': [1000, 1200],
                            'eval_metric': ['mae']}

            # grid search to find the best parameter combination
            xgb1 = GridSearchCV(xgb1, parameters, cv=2, n_jobs=1, verbose=False)

        model = xgb1

        # train the model
        model.fit(x_train, y_train)

        # predict on test set using trained model
        y_pred = model.predict(x_valid)
        
                
        # Ensure predictions are non-negative
        y_pred = np.maximum(y_pred, 0)

        # calculate mean absolute error
        mae = mean_absolute_error(y_valid, y_pred)

        print("Mean Absolute Error:", mae)

        # save results in a dataframe
        results = pd.DataFrame()
        results["True_components"] = y_valid[label_column].values
        results["Predicted_components"] = y_pred

        feature_important = model.get_booster().get_score(importance_type='weight')
        keys = list(feature_important.keys())
        values = list(feature_important.values())

        data = pd.DataFrame(data=values, index=keys, columns=["score"]).sort_values(by="score", ascending=False)

        return {"output_data_preds": results, "output_data_featimp": data}




