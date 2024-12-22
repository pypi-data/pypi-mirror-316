# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd


class DataSelector(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.version = "1"
        self.description = "With this building block, the user can select and rename the column of Dataframe."
        self.category = "preprocess_data"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', pd.DataFrame)

    def execute(self, input_data):
        try:

            column_name = [i for i in self.settings["columns"].keys()]

            selected_dataframe = input_data.loc[:, column_name]

            rename_dict = {}

            for original_name, new_name in self.settings["columns"].items():
                if new_name:
                    rename_dict[original_name] = new_name
                else:
                    name_splits = original_name.split('.')
                    if len(name_splits) == 6:
                        if name_splits[-1] == "value":
                            rename_dict[original_name] = name_splits[1] + ' ' + name_splits[3]
                        else:
                            rename_dict[original_name] = name_splits[1] + ' ' + name_splits[3] + ' ' + name_splits[-1]

            selected_dataframe.rename(columns=rename_dict, inplace=True)

            # reindex with timestamp
            #if "timestamp" in selected_dataframe.columns:
            #    selected_dataframe["timestamp"] = pd.to_datetime(selected_dataframe["timestamp"])
            #    selected_dataframe = selected_dataframe.set_index("timestamp")

            if "file_path" in self.settings.keys():
                file_path = self.settings["file_path"]
                selected_dataframe.to_csv(file_path)

            return {"output_data": selected_dataframe}

        except Exception as exc:
            self.logger.logger.error(f'Cannot execute building block {self.name}')
            self.logger.logger.error(exc, exc_info=True)

