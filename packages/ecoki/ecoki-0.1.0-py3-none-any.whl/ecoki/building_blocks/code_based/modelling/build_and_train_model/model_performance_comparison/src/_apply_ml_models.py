# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:55:52 2022

@author: eko
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import ekoAnalysis, norm, scores_df
from sklearn.feature_selection import RFE
import xgboost
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import cross_val_NN, NN_learning_curve
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import is_valid_file, copy_file, create_venv, save_dataframe
import argparse
import json
import os


def check_nn_requirements(parser, args):
    if (bool(args.neural_network_file is None) ^ bool(args.requirements_file is None)):
        parser.error("require --neural_network_file AND --requirements_file")
    elif(args.neural_network_file is None and args.requirements_file is None):
        return False
    else:
        return True

def gen_train_test_set(dataset, fraction):
    train_dataset = dataset.sample(frac=fraction,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    return train_dataset, test_dataset

def compute_training_stats(train_dataset):
    train_stats = train_dataset.describe()
    train_stats = train_stats.transpose()
    return train_stats

def get_final_features(num_features, x_train, y_train):
    estimator = xgboost.XGBRegressor()
    selector = RFE(estimator, step=1, n_features_to_select=num_features)
    selector = selector.fit(x_train, y_train)   
    selected = selector.get_support(1) # the most important features
    return selected  
    
def run_model_comparison(analysis_name, results_identifier, dataset, labels, num_features_list, savedir_path, include_neural_network=False,   
                         neural_network_script_path=None, req_txt_file_path = None, include_lc_analysis=True):

    if include_neural_network:
        print("\n -------------------------------Installing packages for neural network python script----------------------------------------")
        create_venv(savedir_path, analysis_name, req_txt_file_path)

    #Create training and test data
    train_dataset, test_dataset = gen_train_test_set(dataset, 0.8)

    # We first do a normalization including the labels, since this is needed to compare the beta coefficients of the multivariate linear 
    # regression, and the NN requires normalized labels
    ##########################################################################
    # Calculate basic statistics with the train data and normalize
    train_stats = compute_training_stats(train_dataset)
    normed_train_data = norm(train_dataset,train_stats)
    normed_test_data = norm(test_dataset,train_stats)

    # Seperate out response variable
    train_labels = train_dataset[labels]
    test_labels = test_dataset[labels]

    analysis = ekoAnalysis()

    num_features_labels = []
    dfs = []
    all_rfe_lc_scores = []

    for num_features in num_features_list:
        #plots = []
        lc_scores = []
        # Creates empty dataframe for storing the scores later
        df = scores_df(['Algorithm', 'Coeff. of Determination', 'Root Mean Square Error', 'Mean Absolute Error', 'Mean Absolute % Error'])
    
        x_train=normed_train_data.drop(columns=labels)
        x_test=normed_test_data.drop(columns=labels)
        y_train=normed_train_data.loc[:,labels]
        y_test=normed_test_data.loc[:,labels]

        # Combine test and train sets for doing cross validation later
        X = pd.concat([x_train,x_test])
        Y = pd.concat([y_train,y_test])

        # Compute noteworthiness threshold
        std_labels = pd.DataFrame(np.std(Y))
        std_sum_labels = std_labels[0].sum()
        std_avg_labels = std_sum_labels/len(labels)
        noteworthiness_threshold = round(0.05*std_avg_labels, 3)

        num_feature_label = ""
        if num_features != len(x_train.columns):
            print(f"--------------------------- Starting model comparison for {num_features} features (RFE) ---------------------------------------\n")
            num_feature_label = f'{num_features} features (RFE)'
            # RFE to select the number of most relevant features requested by the user
            selected = get_final_features(int(num_features), x_train, y_train)
            most_important_features = pd.DataFrame(X.columns[selected], columns=["Most important features"])
            save_dataframe(most_important_features, os.path.join(savedir_path, analysis_name, results_identifier, 'data', num_feature_label), "most_important_features.csv")
            X = X[X.columns[selected]] # final features
            x_train = x_train[x_train.columns[selected]]
            x_test = x_test[x_test.columns[selected]]
        else:
            print(f"--------------------------- Starting model comparison for {num_features} features (all features) ---------------------------------------\n")
            num_feature_label = f'All {num_features} features'
        num_features_labels.append(num_feature_label)

        # Do linear regression with normalized labels so that the coefficients can be generated and compared across labels
        # Apply linear regression
        lin_reg = LinearRegression()
        name = "Linear Regression"
        lin_reg.fit(x_train,y_train)

        # Get coefficients for each parameter
        coefficients = pd.DataFrame(np.transpose(lin_reg.coef_), x_test.columns, columns=test_labels.columns)
        save_dataframe(coefficients, os.path.join(savedir_path, analysis_name, results_identifier, 'data', num_feature_label), "coefficients.csv")
        #dfs.append(coefficients)
        ##########################################################################

        # Create and score all the models
        df, mae_values = analysis.model_and_score(x_train,y_train,X,Y,df)
        if include_lc_analysis:
            lr_lc_score = analysis.plot_learning_curve(LinearRegression())
            lc_scores.append(lr_lc_score)
            xg_lc_score = analysis.plot_learning_curve(xgboost.XGBRegressor())
            lc_scores.append(xg_lc_score)

        # Create NN model and calculate score, using a cross validation
        #NN_learning_curve_all_scores = None
        if include_neural_network:
            cv = 5
            NN_score = cross_val_NN(cv, x_train, x_test, y_train, y_test, savedir_path, analysis_name, neural_network_script_path) # Train and cross validate neural network model
            df = df.append(NN_score, ignore_index=True)
            mae_values.append(NN_score['Mean Absolute Error'])            
            #df = pd.concat([df, NN_score], ignore_index=True)
            # Create NN learning curve data
            #make optional. Make sure errors not created when saving dataframe
            if include_lc_analysis:
                NN_learning_curve_all_scores = NN_learning_curve(cv, x_train, x_test, y_train, y_test, savedir_path, analysis_name, neural_network_script_path)
                lc_scores.append(NN_learning_curve_all_scores)
                save_dataframe(NN_learning_curve_all_scores, os.path.join(savedir_path, analysis_name, results_identifier, 'data', num_feature_label), "NN learning curve.csv")              
        else:
            mae_values.append("")

        df_name = "df"
        if num_feature_label.startswith("All"):
            df_name = "df not normalized"
        save_dataframe(df, os.path.join(savedir_path, analysis_name, results_identifier, 'data', num_feature_label), "%s.csv"%(df_name))

        if include_lc_analysis:
            all_rfe_lc_scores.append(lc_scores)        
        dfs.append(df)

        print(f"--------------------------- Finished model comparison for {num_feature_label} ---------------------------------------\n")

    return dfs, all_rfe_lc_scores, num_features_labels, noteworthiness_threshold
