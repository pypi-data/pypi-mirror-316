# Project imports
from abc import ABC
from ecoki.building_block_framework.building_block import BuildingBlock

# System imports
import threading
import pandas as pd
import json


class DataTransformationAndPresentationDataWriter(BuildingBlock):
    """Building block for converting tabular data (ata frame) to data model."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.version = "1"
        self.description = "Given the name of a database in a MongoDB client, read the data from csv file and " \
                            "return it in data model format."
        self.category = "DataTransformationAndPresentation"

        self.database_config = None
        self.csv_file_path = None
        self.data_writer_config_path = None
        self.data_writer_config = None

        self.add_outlet_port('output_data', dict)

    def handle_data_writer_configuration(self):
        data_writer_config = self.settings['write_data']
        database_url = data_writer_config["database"]["url"]
        database_name = data_writer_config["database"]['database_name']
        collection_name = list(data_writer_config["database"]['collections'][0].keys())[0]
        self.database_config = {"url": database_url, "name": database_name, "collection": collection_name}
        self.csv_file_path = list(data_writer_config["database"]['collections'][0].values())[0][0]["file"]
        self.data_writer_config_path = list(data_writer_config["database"]['collections'][0].values())[0][0]["mapping"]

    def execute(self):
        self.handle_data_writer_configuration()

        data_frame = pd.read_csv(self.csv_file_path)
        with open(self.data_writer_config_path) as f:
            self.data_writer_config = json.load(f)

        df_columns = data_frame.columns.to_list()

        def process_components(df, config):

            data_model = {"timestamp": str(df[config["timestamp"]])}
            components = config["components"]
            components_list = []
            for component in components:
                processed_property = process_component_property(component["property"], df)
                processed_component = {"property": processed_property}
                if component["subcomponents"]:
                    processed_component["subcomponents"] = process_subcomponents(component["subcomponents"], df)
                components_list.append(processed_component)
            data_model["components"] = components_list
            return data_model

        def process_component_property(component_property, df):
            property_dict = {}
            for key, value in component_property.items():
                if value in df_columns:
                    if key == "value":
                        property_dict[key] = float(df[value])
                    else:
                        property_dict[key] = str(df[value])
                else:
                    property_dict[key] = value

            return property_dict

        def process_subcomponents(subcomponents, df):
            processed_subcomponents_list = []

            for subcomponent in subcomponents:
                processed_subcomponent = {}
                processed_sub_property = process_component_property(subcomponent["property"], df)
                processed_subcomponent["property"] = processed_sub_property
                if subcomponent["subcomponents"]:
                    process_subcomponents(subcomponent["subcomponents"], df)
                processed_subcomponents_list.append(processed_subcomponent)
            return processed_subcomponents_list

        df_data_model = data_frame.apply(process_components, axis=1, args=(self.data_writer_config,))

        df_data_model_list = df_data_model.tolist()

        results = {"database_config": self.database_config, "processed_data": df_data_model_list}
        return {"output_data": results}

