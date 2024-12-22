# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:31:13 2022

@author: eko
"""

# This script contains various function to preprocess data, train and score models and generate and save output. It is used by the three 

# Note: check the various file locations and destinations as well as system paths before running on your computer.


import pandas as pd
from sklearn.linear_model import LinearRegression
import xgboost
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.dummy import DummyRegressor
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import ComputeMetrics
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import PlotDiagnostics


def norm(x,train_stats):
    # x: dataframe that should be normalized
    # train_stats: dataframe of the data set statistics
    
    normed_data = (x - train_stats['min']) / (train_stats['max'] - train_stats['min'])
    
    # Replace NA due to std of 0, with 0
    normed_data.fillna(0, inplace=True)
    return normed_data

def scores_df(column_names):
    # Creates empty dataframe for storing the scores later
    df = pd.DataFrame([], columns = column_names)
    return df

class ekoAnalysis(ComputeMetrics, PlotDiagnostics):

    def model_and_score(self, x_train,y_train,X,Y,df):
        # train the models, score the models and generate learning curves
    
        mae_values = [] 
        self.X = X
        self.Y = Y
    
        # Apply baseline "dummy" regression, only using the mean of the dataset for each prediciton
        name = "Naive Baseline"
        self.model = DummyRegressor(strategy="mean")
        self.kf = KFold(n_splits=5, shuffle=True, random_state=1) # 5 folds NOT selected because this causes extremely high error scores for the first fold for the linear regression
        self.X_validate() # Cross validate
        df = self.stats(name, df) # Print the metrics
    
        # Apply linear regression
        name = "Linear Regression"
        self.model = LinearRegression()
        self.kf = KFold(n_splits=5, shuffle=True, random_state=1)
        self.X_validate() # Cross validate
        df = self.stats(name, df) # Print the metrics
        mae_values.append(self.mae)

        # Apply xgboost
        name = "XGBoost Regression"
        self.model = xgboost.XGBRegressor()
        self.model.fit(x_train,y_train)
        self.kf = KFold(n_splits=5, shuffle=True, random_state=1)
        self.X_validate() # Cross validate
        df = self.stats(name, df) # Print the metrics
        mae_values.append(self.mae)
		
        # Plot of most important features in xgboost
        #self.plot_important_xgboost_features()

        return df, mae_values
