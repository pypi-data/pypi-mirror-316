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


class Optimization2DVisualizer(BuildingBlock):
    """
    A building block for visualizing 2D optimization results.

    This class provides functionality to create an interactive 2D plot showing model predictions
    for labels and ratings based on optimized parameters. It helps users understand the decision-making
    process of the optimization algorithm in adjusting process parameters.

    Attributes:
        architecture (str): The name of the architecture (ecoKI).
        version (str): The version of the building block.
        category (str): The category of the building block (Transformer).
        description (str): A detailed description of the building block's functionality.

    """

    def __init__(self, **kwargs):
        """
        Initialize the Optimization2DVisualizer building block.

        Args:
            **kwargs: Additional keyword arguments to be passed to the parent BuildingBlock class.
        """
        super().__init__(**kwargs)

        self.architecture = "ecoKI"
        self.version = "1"
        self.category = "Transformer"
        self.description = "Dieser Baustein zeigt einen interaktiven 2D-Plot, der für die zu optimierenden Parameter die Vorhersage des Modells für die Labels und das Rating angibt. Auf diese Weise kann dem Nutzer geholfen werden, die Entscheidung des Optimierungsalgorithmus zur Anpassung der Prozessparameter nachzuvollziehen. Auf die X- und Y-Achse des Plots können die zu optimierenden Prozessparameter gesetzt werden. Bei mehr als zwei Prozessparametern können somit unterschiedliche 2D-Kombinationen erzeugt werden. Über 'Output_Name' kann das Label des Modells gewählt werden, für das der Nutzer eine farblich gekennzeichnete Kontur geplottet haben möchte. Hier stehen alle Ausgänge des Modells sowie das Rating des Optimierers entstanden durch die Optimierungsfunktion zur Auswahl. Über den 'Testdaten_Index' kann das Sample des Testdatensatzes ausgewählt werden, für das der Plot erstellt wird. Außerdem sind sowohl die originale Parameterkombination des Testdatensatzes (weiß) als auch der optimierte Parametervorschlag (rot) dargestellt. Außerdem ist es möglich, über den Button 'Zeige_Trainingsdatensatz_Kombinationen' alle vorkommenden Parameterkombinationen des Trainingsdatensatzes anzuzeigen. Denn der Optimierer schlägt nur neue Kombinationen vor, die sich in direkter Nähe zu einer festgelegten Mindestzahl an bekannten Kombinationen befindet. So kann nachvollzogen werden, warum nicht aussichtsreichere Parameterkombinationen im 2D-Raum vorgeschlagen wurden."

        self.add_inlet_port('input_data', object)
        self.add_inlet_port('input_data_split_train_test', object)
        self.add_inlet_port('input_data_settings', object)

        self.add_outlet_port('input_data', object)
        self.add_outlet_port('input_data_split_train_test', object)
        self.add_outlet_port('input_data_settings', object)
        #self.add_outlet_port("model", object)
        self.add_outlet_port("pp_manager", object)

        # # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
        #self.model = self.load_model('trained_model.sav')


    # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
    # def load_model(self,filename):
    #     # Load the model from disk
    #     multi_output_regressor = pickle.load(open(filename, 'rb'))
    #     return multi_output_regressor

    # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
    def execute(self, input_data, input_data_split_train_test, input_data_settings):
        """
        Execute the Optimization2DVisualizer building block.

        This method processes the input data and returns it along with the pipeline manager.

        Args:
            input_data (object): The input data for visualization.
            input_data_split_train_test (object): The split train-test data.
            input_data_settings (object): The settings for input data.

        Returns:
            dict: A dictionary containing the following keys:
                - input_data (object): The original input data.
                - input_data_split_train_test (object): The split train-test data.
                - input_data_settings (object): The settings for input data.
                - pp_manager (object): The pipeline manager.

        """
        # get input data
        return {"input_data": input_data, "input_data_split_train_test": input_data_split_train_test, "input_data_settings": input_data_settings, "pp_manager": self.pipeline_manager}
