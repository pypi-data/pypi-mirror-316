import pandas as pd
from ecoki.building_block_framework.building_block import BuildingBlock

from sklearn.model_selection import train_test_split


class SplitTrainTest(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Split the input dataset (pre-processed) into Train and test datasets (10'%' size of the original) for further training and prediction."
        self.version = "1"
        self.category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', list)

    def execute(self, input_data):
        value_columns = [col for col in input_data.columns if col.endswith('.value')]
        input_data = input_data[value_columns].copy()
        input_data.reset_index(drop=True, inplace=True)
        label_column_string = self.settings["label_column"][0]
        label_column = [col for col in input_data.columns if label_column_string in col]
        Data_X = input_data.loc[:, ~input_data.columns.isin(label_column)]
        Data_Y = input_data.loc[:, label_column]
        x_train, x_valid, y_train, y_valid = train_test_split(
            Data_X, Data_Y, test_size=0.2, random_state=0
        )
        output_data = [x_train, x_valid, y_train, y_valid]

        return {"output_data": output_data}

        # except Exception as exc:
        # output_data_port.set_port_value([])
        # output_data_port.set_status_code(1)
