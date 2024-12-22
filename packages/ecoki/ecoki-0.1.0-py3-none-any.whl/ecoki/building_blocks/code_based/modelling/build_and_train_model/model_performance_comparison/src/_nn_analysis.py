# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:03:23 2023

@author: eko
"""

"""
Created on Fri Oct 20 10:21:27 2017

@author: bod

vKBP modellierung und optimierung. Das Ergebnis wird als CSV und Excel File gespeichert
"""

import pandas as pd
from sklearn.model_selection import KFold
import math
import subprocess
import os
import json
from ecoki.building_blocks.code_based.modelling.build_and_train_model.model_performance_comparison.src import save_dataframe


def run_NN(save_dir, nn_script_path, analysis_type, dict_length):
    """
	This function connects the user's neural script with the main code. 
	Subprocess is used to call an external program or command from main code
	save_dir: This is the name of the folder in which the packages for running the neural network script are installed for the respective analysis
	nn_script_path: This is the path for the user's neural network script
	analysis_type: Whether to use cross validation or learning for analyis. Values can be 'cv' or 'lc'
	dict_length: Length of score dictionary variable returned by user's script. Should be 5 for cv and 3 for lc
	"""
	
    python_exe = os.path.join("Scripts", "python.exe")
    python_bin = os.path.join(save_dir, 'venv', python_exe) # User's package install dir
    command = [python_bin, nn_script_path, "-a", analysis_type, "-s", os.path.join(save_dir, 'misc')]    
    p = subprocess.run(command, capture_output=True)   # subprocess to call external program or command, the user's script in this case
    if p.returncode:
        raise Exception(p.stderr.decode())

    output = p.stdout.decode()      # score output from script
    output = os.linesep.join([s for s in output.splitlines() if s])
    output_arr = output.split("\n")
    dict_str = output_arr[-1].replace("'", "\"")
    score = json.loads(dict_str)

	# Check whether the dictionary is of correct size, else throw error
    valid_dict = (True if len(score)==5 else False) if analysis_type=='cv' else (True if len(score)==3 else False)
    if not valid_dict:
        raise Exception(f"For {analysis_type} analyis, required length of score dictionary variable is {dict_length}, but {len(score)} was provided instead.")

    return score

def cross_val_NN(cv, x_train, x_test, y_train, y_test, savedir_path, analysis_name, nn_script_path):

    kf = KFold(n_splits=cv, shuffle=True, random_state=1)
    acc_score = pd.DataFrame()

    # Cross validation inputs and function
    X = pd.concat([x_train, x_test])
    Y = pd.concat([y_train, y_test])

    i = 0
    for train_index, test_index in kf.split(X):
        i += 1
        print("------------------------------------ Fold #%i"%(i), "--------------------------------------")
        X_train, X_test = X.iloc[train_index, :], X.iloc[test_index, :]
        Y_train, Y_test = Y.iloc[train_index, :], Y.iloc[test_index, :]

        for name, dataset in {"x_train":X_train, "x_test":X_test, "y_train":Y_train, "y_test":Y_test}.items():
            save_dataframe(dataset, os.path.join(savedir_path, analysis_name, "misc"), "%s.csv"%(name))

        NN_score = run_NN(os.path.join(savedir_path, analysis_name), nn_script_path, 'cv', 5)

        acc_score = acc_score.append(NN_score,ignore_index=True)
        #acc_score = pd.concat([acc_score, NN_score], ignore_index=True)

    avg_acc_score = acc_score.mean()
    
    avg_acc_score = pd.concat([pd.Series(["Neural Network"]), avg_acc_score]) # format so it can be appended to the other scores
    avg_acc_score.rename({0: "Algorithm"}, inplace = True) # format so it can be appended to the other scores

    return avg_acc_score

def NN_learning_curve(cv, x_train, x_test, y_train, y_test, savedir_path, analysis_name, nn_script_path):

    kf = KFold(n_splits=cv, shuffle=True, random_state=1)
    learning_curve_score = pd.DataFrame()

    # Cross validation inputs and function
    X = pd.concat([x_train, x_test])
    Y = pd.concat([y_train, y_test])
    
    # Set the training data sizes that will be plotted in the learning curves
    max_size = math.floor(X.shape[0]*0.8) # max size of data set is that of the full training data set
    training_sizes = [10,math.floor(max_size*0.2),math.floor(max_size*0.40),math.floor(max_size*0.6),math.floor(max_size*0.80),max_size]
    
    learning_curve_all_scores = pd.DataFrame()
    learning_curve_score = pd.DataFrame()
    
    i = 0
    for n in training_sizes:
        i += 1
        print("------------------------------------ Learning curve #%i"%(i), " of %i"%(len(training_sizes)), "in progress --------------------------------------")
        for train_index, test_index in kf.split(X):
            X_train, X_test = X.iloc[train_index, :], X.iloc[test_index, :]
            Y_train, Y_test = Y.iloc[train_index, :], Y.iloc[test_index, :]
            
            # Make training set size to that needed by the learning curve
            X_train = X_train.sample(n = n, random_state = 1)
            Y_train = Y_train.sample(n = n, random_state = 1)
 
            for name, dataset in {"x_train":X_train, "x_test":X_test, "y_train":Y_train, "y_test":Y_test}.items():
                save_dataframe(dataset, os.path.join(savedir_path, analysis_name, "misc"), "%s.csv"%(name))

            one_learning_curve_score = run_NN(os.path.join(savedir_path, analysis_name), nn_script_path, 'lc', 3)

            #learning_curve_score = pd.concat([learning_curve_score, one_learning_curve_score], ignore_index=True)
            learning_curve_score = learning_curve_score.append(one_learning_curve_score,ignore_index=True)
            
        avg_learning_curve_score = learning_curve_score.mean()
        
        #learning_curve_all_scores = pd.concat([learning_curve_all_scores, avg_learning_curve_score], ignore_index=True)
        learning_curve_all_scores = learning_curve_all_scores.append(avg_learning_curve_score,ignore_index=True)
        learning_curve_score = pd.DataFrame()# clear the variables so that the new average for the next training set size calculations can be stored
        
    return learning_curve_all_scores
