# Project Imports
from ecoki.building_block_framework.building_block import BuildingBlock
# Library Imports
import json
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import LinearRegression
from scipy.optimize import differential_evolution
import pickle
import itertools
import sys
from sklearn.neighbors import BallTree
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import json
import panel as pn
from panel.interact import interact, fixed

# dependency import


class AsTimeseriesVisualizer(BuildingBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "ecoKI"
        self.version = "1"
        self.category = "Transformer"
        self.description = "Dieser Baustein kann Features, die Zeitreihen darstellen (Beispiel: f1_T-1, ... , f1_T-10) anhand eines vorgegebenen Patterns (regular expression) identifizieren sowie visualisieren."


        self.add_inlet_port('input_data', object)
        self.add_outlet_port('output_data', object)
        self.add_outlet_port('regex_pattern', object)


        # # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
        #self.model = self.load_model('trained_model.sav')


    # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
    # def load_model(self,filename):
    #     # Load the model from disk
    #     multi_output_regressor = pickle.load(open(filename, 'rb'))
    #     return multi_output_regressor

    # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
    def execute(self, input_data):

        # get input data
        return {"output_data": input_data, "regex_pattern":self.settings["regex_pattern"]}
