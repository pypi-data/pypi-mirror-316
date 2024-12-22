from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd
import requests
import json

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

class TimeSeriesWrapper(BuildingBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "ecoKI"
        self.description = "Dieser Baustein kann eine Zeitreihe zusammenfassen und sie zu einem Merkmal aggregieren. Dabei kann das MAXIMUM, der DURCHSCHNITT oder der MEDIAN als Aggregatsfunktion für jede Gruppierung spezifiziert werden. Auf diese Weise können Zeitreihen beispielsweise für die Nutzung im Optimierungsbaustein vorbereitet werden, sodass sie nur durch einen Wert charakterisiert werden kann. Außerdem wird eine Infereenz-Pipeline gestartet werden, die eine bestehende Inferenz-Pipeline mit den definierten Transformationen der Daten ausführen kann."
        self.version = "1"
        self.category = "data integration"

        self.add_inlet_port('input_data', object)
        self.add_outlet_port('output_data', object)

    def execute(self, input_data):

        # get input
        self.training_features = input_data[0]
        self.training_labels = input_data[2]

        self.test_features = input_data[1]
        self.test_labels = input_data[3]

        training_features_aggregated = self.training_features
        training_labels_aggregated = self.training_labels
        test_features_aggregated = self.test_features
        test_labels_aggregated = self.test_labels

        # iterate over agg features
        for agg_column_name in self.settings["feature_aggregations"]:

            # get data from settings
            agg_func = self.settings["feature_aggregations"][agg_column_name]["aggregation_function"]
            aggregated_columns = self.settings["feature_aggregations"][agg_column_name]["aggregated_columns"]

            # mean
            if agg_func == "mean":

                # training_features
                training_features_aggregated[agg_column_name] = self.training_features.loc[:,aggregated_columns].mean(axis = 1)
                training_features_aggregated = training_features_aggregated.drop(aggregated_columns,axis=1)

                # test_features
                test_features_aggregated[agg_column_name] = self.test_features.loc[:,aggregated_columns].mean(axis = 1)
                test_features_aggregated = test_features_aggregated.drop(aggregated_columns,axis=1)

            # max
            if agg_func == "max":

                # training_features
                training_features_aggregated[agg_column_name] = self.training_features.loc[:, aggregated_columns].max(axis=1)
                training_features_aggregated = training_features_aggregated.drop(aggregated_columns,axis=1)

                # test_features
                test_features_aggregated[agg_column_name] = self.test_features.loc[:,aggregated_columns].max(axis = 1)
                test_features_aggregated = test_features_aggregated.drop(aggregated_columns,axis=1)

            # median
            if agg_func == "median":

                # training_features
                training_features_aggregated[agg_column_name] = self.training_features.loc[:, aggregated_columns].median(axis=1)
                training_features_aggregated = training_features_aggregated.drop(aggregated_columns,axis=1)

                # test_features
                test_features_aggregated[agg_column_name] = self.test_features.loc[:,aggregated_columns].median(axis = 1)
                test_features_aggregated = test_features_aggregated.drop(aggregated_columns,axis=1)

        # iterate over agg labels
        for agg_column_name in self.settings["label_aggregations"]:

            # get data from settings
            agg_func = self.settings["label_aggregations"][agg_column_name]["aggregation_function"]
            aggregated_columns = self.settings["label_aggregations"][agg_column_name]["aggregated_columns"]

            # mean
            if agg_func == "mean":
                # training_labels
                training_labels_aggregated[agg_column_name] = self.training_labels.loc[:, aggregated_columns].mean(
                    axis=1)
                training_labels_aggregated = training_labels_aggregated.drop(aggregated_columns, axis=1)

                # test_labels
                test_labels_aggregated[agg_column_name] = self.test_labels.loc[:, aggregated_columns].mean(axis=1)
                test_labels_aggregated = test_labels_aggregated.drop(aggregated_columns, axis=1)

            # max
            if agg_func == "max":
                # training_labels
                training_labels_aggregated[agg_column_name] = self.training_labels.loc[:, aggregated_columns].max(
                    axis=1)
                training_labels_aggregated = training_labels_aggregated.drop(aggregated_columns, axis=1)

                # test_labels
                test_labels_aggregated[agg_column_name] = self.test_labels.loc[:, aggregated_columns].max(axis=1)
                test_labels_aggregated = test_labels_aggregated.drop(aggregated_columns, axis=1)

            # median
            if agg_func == "median":
                # training_labels
                training_labels_aggregated[agg_column_name] = self.training_labels.loc[:,
                                                                aggregated_columns].median(axis=1)
                training_labels_aggregated = training_labels_aggregated.drop(aggregated_columns, axis=1)

                # test_labels
                test_labels_aggregated[agg_column_name] = self.test_labels.loc[:, aggregated_columns].median(axis=1)
                test_labels_aggregated = test_labels_aggregated.drop(aggregated_columns, axis=1)

        # set output data
        #output_data = [self.training_features, self.test_features, self.training_labels, self.test_labels, input_data[4]]
        output_data = [training_features_aggregated, test_features_aggregated, training_labels_aggregated, test_labels_aggregated, input_data[4]]

        # start time series wrapped inference pipeline
        if self.settings["create_inference_wrapper_template"]:
            print("a")

            # get the inference pipeline template (already there as an ecoKI pipeline)
            inference_pipeline_template = get_pipeline_template("Inference_Time_Series_Wrapped_Model")

            # adjust the settings to the trained model
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["feature_aggregations"] = self.settings["feature_aggregations"]
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["label_aggregations"] = self.settings["label_aggregations"]
            inference_pipeline_template["topology"]["nodes"][0]["settings"]["wrapped_inference_pipeline"] = self.settings["wrapped_inference_pipeline"]


            # set the name of the pipeline (idea: do it in future dynamically based on the name of the train-pipeline?
            inference_pipeline_template["name"] = "Inference_Time_Series_Wrapped_Model_custom"

            # save new template as a custom pipeline template via api (TODO: delete first?)
            add_custom_pipeline(inference_pipeline_template)

            # stop it if theres already a pipeline with this name on the active/running pipelines
            if inference_pipeline_template["name"] in self.pipeline_manager.pipelines.keys():

                # stop pipeline
                delete_custom_pipeline(inference_pipeline_template["name"])

            # in case the pipeline should be started, start it
            if self.settings["create_inference_wrapper"]:

                # start pipeline
                start_custom_pipeline(inference_pipeline_template["name"])

        return {"output_data": output_data}