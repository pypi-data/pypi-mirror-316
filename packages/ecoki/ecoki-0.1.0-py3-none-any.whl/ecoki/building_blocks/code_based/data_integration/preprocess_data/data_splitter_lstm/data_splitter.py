from ecoki.building_block_framework.building_block import BuildingBlock
from sklearn.model_selection import train_test_split
import pandas as pd

class DataSplitter(BuildingBlock):
    """Building block for splitting the dataset into training and testing datasets."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.description = "Splits the dataset into training and testing datasets"
        self.version = "1"
        self.category = "Transformer"
        self.add_inlet_port('input_data_train_test', list)  # Inlet port to receive data
        self.add_outlet_port('output_data_train_test', list)  # Outlet port to send processed data

    def split_dataset(self, X, y):
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=float(self.settings['test_dataset_size']), shuffle=False)
        return x_train, x_test, y_train, y_test

    def execute(self, input_data_train_test):
        output_data_port = self.get_port('output_data_train_test', 'outlet')

        X, y = input_data_train_test
        x_train, x_test, y_train, y_test = self.split_dataset(X, y)
        print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

        output_data = [x_train, y_train, x_test, y_test]
        return {"output_data_train_test": output_data}
