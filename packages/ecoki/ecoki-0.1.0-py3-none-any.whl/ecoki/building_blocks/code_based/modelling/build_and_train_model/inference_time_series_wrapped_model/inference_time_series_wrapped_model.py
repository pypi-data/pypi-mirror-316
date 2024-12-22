from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd
import pickle
import xgboost as xgb
from sklearn.multioutput import MultiOutputRegressor

from keras.models import Sequential, Model
from keras.layers import Input, LSTM, Dense, Concatenate, Dropout, Masking, Flatten, TimeDistributed
from keras.models import load_model

import requests
import json


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
class InferenceTimeSeriesWrappedModel(BuildingBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "ecoKI"
        self.description = "Dieser Baustein kann eine bestehende Inferenz-Pipeline mit den vorgenommenen Transformationen durch Aggregatsfunktionen auf den Feature ausführen. Zuvor müssen diese Aggregatsfunktionen im Baustein TimeSeriesWrapper definiert worden sein, der auch eine Inferenzpipeline mit diesem Baustein startet."
        self.version = "1"
        self.category = "Modeling"

        self.add_inlet_port('input_data', object)
        self.add_outlet_port('output_data', object)
        self.add_outlet_port('unwrapped_output_data', object)
        self.add_outlet_port('unwrapped_input_data', object)

        self.inference_pipeline_created = False

    def predict(self, features):

        # start inference pipeline at the first call
        if not self.inference_pipeline_created:

            # if already existing, stop first
            if self.settings['wrapped_inference_pipeline'] in self.pipeline_manager.pipelines.keys():
                delete_custom_pipeline(self.settings['wrapped_inference_pipeline'])

            # start it
            start_custom_pipeline(self.settings['wrapped_inference_pipeline'])
            self.inference_pipeline_created = True

        inner_loop_args = {
            "inputs": [
                {
                    "building_block": "Inference_BuildingBlock2",
                    "inlet": "input_data",
                    "value": features
                }
            ],
            "outputs": [
                {
                    "building_block": "Inference_BuildingBlock2",
                    "outlet": "output_data"
                }
            ]
        }

        y_pred = self.pipeline_manager.get_pipeline_executor(self.settings['wrapped_inference_pipeline']).run_with_args(inner_loop_args, self.pipeline_manager)

        return y_pred[0]['value']

    def execute(self, input_data):

        # do wrapping of the features
        input_data_unwrapped = input_data.copy()

        # iterate over agg features
        for agg_column_name in self.settings["feature_aggregations"]:

            print(agg_column_name)

            # get data from settings
            aggregated_columns = self.settings["feature_aggregations"][agg_column_name]["aggregated_columns"]

            # do the inverse aggregation
            input_data_unwrapped = input_data_unwrapped.assign(**{name: input_data_unwrapped[agg_column_name] for name in aggregated_columns})
            input_data_unwrapped = input_data_unwrapped.drop([agg_column_name],axis=1)

        # get predictions
        predictions = self.predict(input_data_unwrapped)

        predictions_wrapped = predictions.copy()

        # unwrap labels
        for agg_column_name in self.settings["label_aggregations"]:

            # get data from settings
            agg_func = self.settings["label_aggregations"][agg_column_name]["aggregation_function"]
            aggregated_columns = self.settings["label_aggregations"][agg_column_name]["aggregated_columns"]

            # mean
            if agg_func == "mean":
                # training_labels
                predictions_wrapped[agg_column_name] = predictions_wrapped.loc[:, aggregated_columns].mean(axis=1)
                predictions_wrapped = predictions_wrapped.drop(aggregated_columns, axis=1)

            # max
            if agg_func == "max":
                # training_labels
                predictions_wrapped[agg_column_name] = predictions_wrapped.loc[:, aggregated_columns].max(axis=1)
                predictions_wrapped = predictions_wrapped.drop(aggregated_columns, axis=1)

            # median
            if agg_func == "median":
                # training_labels
                predictions_wrapped[agg_column_name] = predictions_wrapped.loc[:, aggregated_columns].median(axis=1)
                predictions_wrapped = predictions_wrapped.drop(aggregated_columns, axis=1)

        return {"output_data": predictions_wrapped, "unwrapped_input_data": input_data_unwrapped, "unwrapped_output_data": predictions}