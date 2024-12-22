# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock

# External library imports
import pandas as pd
import time
import json
import datetime


class DataConverter(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "convert data from data model to dataframe"
        self.version = "1"
        self.category = "preprocess_data"

        self.reset_attributes()

        self.add_inlet_port('input_data', list)
        self.add_outlet_port('output_data', pd.DataFrame)

    def reset_attributes(self):
        self.numeric_columns = []

    def convert_mongodb_docs_to_df(self, mongoDB_documents):

        def apply_component(df_series):
            nested_dict = {}
            for i in range(len(df_series)):

                if "subcomponents" in df_series[i].keys():
                    subcomponent_dict = {}
                    sub_nested_dict = apply_subcomponent(df_series[i]["subcomponents"], subcomponent_dict)
                    df_series[i]["subcomponents"] = sub_nested_dict
                try:
                    nested_dict[df_series[i]["property"].pop("name")] = df_series[i]
                except KeyError:
                    nested_dict[i] = df_series[i]
            return {"components": nested_dict}

        def apply_subcomponent(subcomponent, sub_dict):
            for i in range(len(subcomponent)):
                if "subcomponents" in subcomponent[i].keys():
                    if subcomponent[i]["subcomponents"]:
                        subcomponent_dict = {}
                        sub_nested_dict = apply_subcomponent(subcomponent[i]["subcomponents"], subcomponent_dict)
                        subcomponent[i]["subcomponents"] = sub_nested_dict
                    else:
                        subcomponent[i].pop("subcomponents")

                try:
                    sub_dict[subcomponent[i]["property"].pop("name")] = subcomponent[i]
                except KeyError:
                    sub_dict[i] = subcomponent[i]
            return sub_dict

        normalized_df = pd.json_normalize(mongoDB_documents)
        normalized_df["components"] = normalized_df["components"].apply(apply_component)
        components_df = pd.json_normalize(normalized_df["components"].tolist())

        df = pd.concat([normalized_df, components_df], axis=1)
        df.drop(["components"], axis=1, inplace=True)

        #if self.settings["index_name"]:
        #    df.set_index(self.settings["index_name"], inplace=True)

        return df

    def execute(self, input_data):
        try:
            df = self.convert_mongodb_docs_to_df(input_data)

            if self.settings["column_type"] == "numeric":  # only return the numeric columns
                if not self.numeric_columns:
                    for col in df.columns:
                        if col == self.settings["index_name"] or col.split(".")[-1] == "value":
                            self.numeric_columns.append(col)

                df = df[self.numeric_columns]  # dataset that only contains numeric columns

            if self.settings["index_name"]:
                df[self.settings["index_name"]] = pd.to_datetime(df[self.settings["index_name"]])
                df.set_index(self.settings["index_name"], inplace=True)
            else:
                # toDO: throw error is index_name is not given
                pass

            return {"output_data": df}  # dataset with customized index column

        except Exception as exc:
            self.logger.logger.error(f'Cannot execute building block {self.name}')
            self.logger.logger.error(exc, exc_info=True)
