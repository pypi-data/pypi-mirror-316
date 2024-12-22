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
import requests

# dependency import
from ecoki.building_blocks.code_based.optimization.run_optimization.process_parameter_optimizer.third_parties.differential_evolution_adapted import differential_evolution_adapted
from ecoki.building_blocks.code_based.optimization.run_optimization.process_parameter_optimizer.third_parties.ball_tree import BIKScaledBallTree

#pn.extension()

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

def myround(x, base):
    """Round to given intervals
        Parameters
        ----------
        x : numpy array
            the values to be rounded
        base : float
            the interval of values to be rounded to

        Returns
        -------
        rounded values : numpy array
        Notes
        -----
    """
    return base * np.round(x / base)

def optimisation_function(pp, *params):
    """Optimisation function"""

    # get additional information
    f_single, names, ball_tree, model ,optimisation_resolution_dict,optimisation_neighbours = params

    # repeat feature df len(pp) times
    f = pd.DataFrame(pd.np.repeat(f_single.values, len(pp), axis=0), columns=f_single.columns)

    # round values integration
    round_bases = optimisation_resolution_dict
    for i in range(len(names)):
        f.loc[:, names[i]] = myround(pp[:, i], round_bases[names[i]])

    # combination_list = ball_tree.get_near_combinations(f)
    dist, number = ball_tree.get_near_radius(f, optimisation_neighbours)

    # predict quality features
    predictions = model.predict(f)

    # rate quality features
    qr = model.rate_quality_results(predictions)

    # penalize combinations far away from neighbous (factor 100)
    qr = np.asarray(
        [qr[i] if dist[i, optimisation_neighbours - 1] < 1 else qr[i]*100 * dist[i, optimisation_neighbours - 1] for i in
         range(len(pp))])

    # return overall rating
    return qr

class ProcessParameterOptimizer(BuildingBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "ecoKI"
        self.version = "1"
        self.category = "Transformer"
        self.description = "Dieser Baustein führt eine Black-Box-Optimierung auf Basis eines maschinell erlernten Modells durch. Die Optimierungsfunktion wird basierend auf den Augangs-Labels des verwendeten Modells definiert. Alle Einstellungen können in den Pipeline-Settings vorgenommen werden. Bei diesem Baustein handelt es sich um eine statische Analyse. Dabei wird für die ersten 100 Beispiele des Trainingsdatensatzes jeweils eine Optimierung der festgelegten Prozessparameter innerhalb definierter Grenzen vorgenommen. Als Ergebnis sind in folgender Visualisierung sowohl die originalen als auch die optimierten ('_optimized') Prozessparameter aufgelistet. Außerdem sind für beide Fälle die Vorhersagen des Modells für die Ausgangs-Labels dargestellt. Zuletzt ist auch das Rating-verfügbar, nach dem der Black-Box-Optimierer die Optimierung der Prozessparameter vorgenommen hat. In der Visualisierung können sowohl die Werte geplotte werden als auch unter 'Descriptive Statistics' die KPIs wie beispielsweise der Mittelwert der optimierten Labels eingesehen und verglichen weren. Mehrere Spalten können durch das Gedrückt-Halten von 'Strg' ausgewählt werden"
        self.add_inlet_port('input_data', object)
        self.add_outlet_port('output_data', object)
        self.add_outlet_port('output_data_split_train_test', object)
        self.add_outlet_port('output_data_settings', object)
        self.add_outlet_port('output_data_unwrapped', object)


        self.training_data = None
        self.test_features = None
        self.test_data = None

        self.inference_pipeline_created = False
        # # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
        # self.model = self.load_model('trained_model.sav')

        # test visualisation
        #self.start_panel_visu()

    # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
    #def load_model(self,filename):
        # Load the model from disk
    #    multi_output_regressor = pickle.load(open(filename, 'rb'))
    #    return multi_output_regressor

    # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
    def predict(self, features):

        # start inference pipeline at the first call
        if not self.inference_pipeline_created:

            # if already existing, stop first
            if self.settings['prediction_pipeline_name'] in self.pipeline_manager.pipelines.keys():
                delete_custom_pipeline(self.settings['prediction_pipeline_name'])

            # start it
            start_custom_pipeline(self.settings['prediction_pipeline_name'])
            self.inference_pipeline_created = True

        inner_loop_args = {
            "inputs": [
                {
                    "building_block": "Inference_BuildingBlock",
                    "inlet": "input_data",
                    "value": features
                }
            ],
            "outputs": [
                {
                    "building_block": "Inference_BuildingBlock",
                    "outlet": "output_data"
                }
            ]
        }

        y_pred = self.pipeline_manager.get_pipeline_executor(self.settings['prediction_pipeline_name']).run_with_args(
            inner_loop_args, self.pipeline_manager)

        return pd.DataFrame(columns=self.column_names, data=y_pred[0]['value'])

    def rate_quality_results(self,predictions):
        # return only the rating column as an array in shape 'ndarray(len,)'
        rated_predictions = self.objective_function(predictions)
        return rated_predictions.loc[:,"Rating"].values

    # def objective_function(self, predictions, include_predictions=True, only_rating=False):
    #
    #     # define columns
    #     quality = predictions.loc[:, 'apple_juice_quality'].values
    #     energie = predictions.loc[:, 'energy_consumption_production'].values
    #
    #     # calculate costs
    #     predictions['Rating'] = np.where(quality < 4, (1 + 4 - quality) * energie,
    #                                      energie)
    #
    #     return predictions

    def objective_function(self, predictions, include_predictions=True, only_rating=False):

        # set optimization target column
        minimization_value = predictions.loc[:, self.settings['objective_function']['optimization_target']].values

        rating = minimization_value

        # iterate over boundary conditions
        for condition,condition_value in self.settings['objective_function']['boundary_conditions'].items():

            if condition_value['operator'] == "greater":
                boundary_penalty_term = np.where(predictions.loc[:, condition_value['label_name']].values < condition_value['boundary'], 1 + condition_value['boundary'] - predictions.loc[:, condition_value['label_name']].values, 1)

            elif condition_value['operator'] == "less":
                boundary_penalty_term = np.where(predictions.loc[:, condition_value['label_name']].values > condition_value['boundary'], 1 + predictions.loc[:, condition_value['label_name']].values - condition_value['boundary'], 1)

            else:
                print("Optimization boundary operator not valid")
                continue

            # multiply
            rating = rating*boundary_penalty_term

        # set rating
        predictions['Rating'] = rating

        return predictions

    def execute(self, input_data):

        # get input data
        # input_data = self.get_port('input_data', 'inlet').get_port_value()
        #output_data_port = self.get_port('output_data', 'outlet')
        #output_data_split_train_test = self.get_port('output_data_split_train_test', 'outlet')
        #output_data_settings = self.get_port('output_data_settings', 'outlet')

        # set training and test data, features and labels from the input
        self.training_features = input_data[0]
        self.training_labels = input_data[2]
        self.training_data = pd.concat([self.training_features, self.training_labels], axis=1)
        self.test_features = input_data[1]
        self.test_labels = input_data[3]
        self.test_data = pd.concat([self.test_features, self.test_labels], axis=1)

        # replace this in the future (just needed for model prediction workaround. Once triggering pipelines from pipelines work, the prediction functionality should be a seperate pipeline
        self.column_names = self.test_labels.columns

        # settings
        self.confidence_radius_names = [name for name in self.settings['optimisation_parameters'].keys()]
        self.confidence_radius_values = [name["exploration_radius"] for name in self.settings['optimisation_parameters'].values()]

        self.optimisation_features_names = [name for name in self.settings['optimisation_parameters'].keys()]
        self.optimisation_bounds_left = [name["left_bound"] for name in self.settings['optimisation_parameters'].values()]

        self.optimisation_bounds_right = [name["right_bound"] for name in self.settings['optimisation_parameters'].values()]


        self.optimisation_parameter_discrete_names = []
        self.optimisation_resolution_dict = {key: inner_dict["resolution"] for key, inner_dict in self.settings['optimisation_parameters'].items() if "resolution" in inner_dict}

        self.optimisation_population_size = self.settings["optimisation_population_size"]
        self.optimisation_max_iterations = self.settings["optimisation_max_iterations"]
        self.optimisation_neighbours = self.settings["optimisation_neighbours"]
        self.ball_tree_leaf_size = self.settings["ball_tree_leaf_size"]

        # create ball tree
        self.ball_tree = BIKScaledBallTree(self.training_data, self.confidence_radius_names,
                                           self.confidence_radius_values, self.ball_tree_leaf_size)

        # optimize, take only the first 100 features
        optim_features = self.test_features.iloc[:self.settings["number_of_test_data_optimisations"], :]
        test_optimized_parameters = self.optimize_batch(optim_features)

        # insert the optimized parameters in the feature dataset (a copy)
        # test_optimized_parameters = optim_test_1
        self.optim_features_optimized = optim_features.copy()
        self.optim_features_optimized.loc[:, test_optimized_parameters.columns.tolist()] = test_optimized_parameters

        # get predictions for original and optimized features
        self.optim_predictions = self.predict(optim_features)
        self.optim_predictions_optimized = self.predict(self.optim_features_optimized)

        # get the rating for the predictions
        self.optim_predictions_rated = self.objective_function(self.optim_predictions)
        self.optim_predictions_optimized_rated = self.objective_function(self.optim_predictions_optimized)

        # save the complete feature df before dropping columns
        optim_features_complete = optim_features.copy()
        self.optim_features_optimized_complete = self.optim_features_optimized.copy()

        # drop all other features except the optimized ones
        optim_features = optim_features.loc[:,self.optimisation_features_names]
        self.optim_features_optimized = self.optim_features_optimized.loc[:, self.optimisation_features_names]

        # rename columns
        self.optim_features_optimized.columns = [col + str("_optimized") for col in
                                                 self.optim_features_optimized.columns]
        self.optim_predictions_optimized.columns = [col + str("_optimized") for col in
                                                    self.optim_predictions_optimized.columns]
        #self.optim_predictions_optimized_rated.columns = [col + str("_optimized") for col in self.optim_predictions_optimized_rated.columns]

        # concatenate result dataframe
        result_df = pd.concat(
            [optim_features.reset_index(drop=True), self.optim_features_optimized.reset_index(drop=True),
             self.optim_predictions_rated.reset_index(drop=True),
             self.optim_predictions_optimized_rated.reset_index(drop=True)], axis=1)

        ########################################
        # check in case there was a wrapper building block (e.g. for time series in between -> if yes, then also output the unwrapped data (endpoint in inference pipeline)
        output_data_unwrapped = pd.DataFrame()

        try:
            inner_loop_args = {
                "inputs": [
                    {
                        "building_block": "Inference_BuildingBlock",
                        "inlet": "input_data",
                        "value": optim_features_complete
                    }
                ],
                "outputs": [
                    {
                        "building_block": "Inference_BuildingBlock",
                        "outlet": "unwrapped_output_data"
                    }
                ]
            }

            # get unwrapped predictions of the non optimized samples
            y_pred_unwrapped = self.pipeline_manager.get_pipeline_executor(self.settings['prediction_pipeline_name']).run_with_args(
                inner_loop_args, self.pipeline_manager)[0]['value']

            # get unwrapped predictions of the optimized samples
            inner_loop_args["inputs"][0]["value"] = self.optim_features_optimized_complete
            y_pred_unwrapped_optimized = self.pipeline_manager.get_pipeline_executor(self.settings['prediction_pipeline_name']).run_with_args(
                inner_loop_args, self.pipeline_manager)[0]['value']

            # get unwrapped input of the non optimized samples
            inner_loop_args["inputs"][0]["value"] = optim_features_complete
            inner_loop_args["outputs"][0]["outlet"] = "unwrapped_input_data"
            x_unwrapped = self.pipeline_manager.get_pipeline_executor(self.settings['prediction_pipeline_name']).run_with_args(
                inner_loop_args, self.pipeline_manager)[0]['value']

            # get unwrapped input of the  optimized samples
            inner_loop_args["inputs"][0]["value"] = self.optim_features_optimized_complete
            x_unwrapped_optimized = self.pipeline_manager.get_pipeline_executor(self.settings['prediction_pipeline_name']).run_with_args(
                inner_loop_args, self.pipeline_manager)[0]['value']

            # add _optimized to columns names
            new_columns_x = [col+"_optimized" for col in x_unwrapped_optimized.columns]
            x_unwrapped_optimized.columns = new_columns_x

            # add _optimized to columns names
            new_columns_y = [col+"_optimized_predicted" for col in y_pred_unwrapped_optimized.columns]
            y_pred_unwrapped_optimized.columns = new_columns_y

            new_columns_y = [col+"_predicted" for col in y_pred_unwrapped.columns]
            y_pred_unwrapped.columns = new_columns_y

            # combine
            output_data_unwrapped = pd.concat([x_unwrapped.reset_index().drop('index',axis=1),x_unwrapped_optimized.reset_index().drop('index',axis=1),y_pred_unwrapped.reset_index().drop('index',axis=1),y_pred_unwrapped_optimized.reset_index().drop('index',axis=1)],axis=1)

        except:
            print("No inference pipeline used, therefore there is no unwrapped_data")


        # save results
        result_df.to_csv("optimisations.csv")

        # set port value
        """output_data_port.set_port_value(result_df)
        output_data_port.set_status_code(0)

        output_data_split_train_test.set_port_value(input_data)
        output_data_split_train_test.set_status_code(0)

        output_data_settings.set_port_value(self.settings)
        output_data_settings.set_status_code(0)"""

        return {"output_data": result_df, "output_data_split_train_test": input_data, "output_data_settings": self.settings, 'output_data_unwrapped':output_data_unwrapped}

    def optimize_batch(self, features):

        """Optimize a batch of samples due to a given cost function by either a genetic algorithm or a brute force grid search.
            Parameters
            ----------
            features : Pandas dataframe
                The features of the samples that shall be optimized (shape=(number of samples,number of features)
            bik_model : BIKModel
                A BIKModel instance that is used to predict the outputs (quality features of process and product) for a given set of features (process parameters + disturbances

            Returns
            -------
            optimized_df_ret : Pandas dataframe
                Returns a pandas dataframe that contains the proposed parameter proposals shape=(number of samples,number of optimied parameters)
            Notes
            -----
        """

        #features_df = pd.read_json(features)

        # create dataframe for storage of optimisation proposals
        optimized_df = pd.DataFrame()

        for i in range(len(features)):
            current_feature = features.iloc[[i], :]

            # optimize instance
            optimized_df = optimized_df.append(self.optimize_sample(current_feature))

            print("Sample Nr.  ", i, " optimized")

        # get only relevant pp
        optimized_df_ret = optimized_df[self.optimisation_features_names]

        return optimized_df_ret


    def optimize_sample(self, feature):

        """Optimize a single sample based on information from the ModelFeatureStructure Excel-sheet.
            Parameters
            ----------
            feature : Pandas dataframe
                The features of the samples that shall be optimized (shape=(1,number of features)
            bik_model : BIKModel
                A BIKModel instance that is used to predict the outputs (quality features of process and product) for a given set of features (process parameters + disturbances

            Returns
            -------
            best_comb : Pandas dataframe
                Returns a pandas dataframe that contains the proposed parameter proposal shape=(1,number of optimied parameters)
            Notes
            -----
        """

        # define optimisation bounds
        names = self.optimisation_features_names
        bounds = [(lb, rb) for lb, rb in zip(self.optimisation_bounds_left,
                                             self.optimisation_bounds_right)]

        # define combinsations for discrete process parameters
        optimisation_parameter_discrete_names = self.optimisation_parameter_discrete_names  # and parameter = True....
        if len(optimisation_parameter_discrete_names) > 0:
            value_dict = [self.training_data.loc[:, fname].unique() for fname in
                          optimisation_parameter_discrete_names.values]

            mgrid = np.asarray(list(itertools.product(*value_dict)))
            feature_wiederholungen = pd.concat([feature] * len(mgrid))
            feature_wiederholungen[optimisation_parameter_discrete_names] = mgrid

        else:
            feature_wiederholungen = feature

        # ffor all discrete parameter combinations
        for i in range(len(feature_wiederholungen)):

            # get features
            f = feature_wiederholungen.iloc[[i], :]

            # check if combination is at least n times in training data and therefore has an own ball tree instance (in case of BIKOptimisationBallTree with key
            if self.ball_tree.valid_key(feature_wiederholungen):

                # füge zusätzliche Informationen zusammen
                optim_arguments = (f.copy(), names, self.ball_tree, self, self.optimisation_resolution_dict,self.optimisation_neighbours)

                optim_results = differential_evolution_adapted(optimisation_function, bounds, args=optim_arguments,
                                                               popsize=self.optimisation_population_size,
                                                               maxiter=self.optimisation_max_iterations, disp=True,
                                                               polish=False,
                                                               updating='deferred')  # biba adapted version, only deferred works

                # round parameter to given resolution from the excel sheet
                round_bases = self.optimisation_resolution_dict
                for i in range(len(names)):
                    optim_results.x[i] = myround(optim_results.x[i].reshape(1), round_bases[names[i]])

                # speichere Parametervector und q_ges
                feature_wiederholungen.loc[f.index, names] = optim_results.x
                feature_wiederholungen.loc[f.index, 'Optimizer_Rating'] = optim_results.fun

            else:
                print("No valid key for sample", file=sys.stderr)
                feature_wiederholungen.loc[f.index, names] = np.nan
                feature_wiederholungen.loc[f.index, 'Optimizer_Rating'] = np.nan

        # get combination with best rating (minimum)
        best_comb = feature_wiederholungen.loc[
                    feature_wiederholungen['Optimizer_Rating'] == feature_wiederholungen['Optimizer_Rating'].min(),
                    :]  # nan is not returned
        return best_comb
