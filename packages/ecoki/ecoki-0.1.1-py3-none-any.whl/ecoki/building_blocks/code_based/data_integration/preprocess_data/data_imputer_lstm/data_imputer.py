from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd
import os
from numpy import nan, isnan
from pandas import read_csv
from functools import reduce


class DataImputer(BuildingBlock):
    """Building block for imputing missing data in a training dataset."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.description = "Impute missing data"
        self.version = "1"
        self.category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', pd.DataFrame)
    
    def fill_missing(self, dataset):
        num_rows_history = int(self.settings['row_history'])
        for row in range(dataset.values.shape[0]):
            for col in range(dataset.values.shape[1]):
                if isnan(dataset.values[row, col]):
                    dataset.values[row, col] = dataset.values[row - num_rows_history, col]
        return dataset
 
    def execute(self, input_data):
        dataset = input_data
        dataset.replace('?', nan, inplace=True)
        dataset = dataset.astype('float32')
        dataset = self.fill_missing(dataset)
        # Set the processed data to the output port
        return {"output_data": dataset}
