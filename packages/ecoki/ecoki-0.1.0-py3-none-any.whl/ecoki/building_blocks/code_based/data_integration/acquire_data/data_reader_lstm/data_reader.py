from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd
import os
from pandas import read_csv
import io


class DataReader(BuildingBlock):
    """Building block for reading csv data from local time series dataset."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Read csv data from local time series dataset"
        self.version = "1"
        self.category = "Transformer"

        self.add_outlet_port('output_data', pd.DataFrame)
        self.add_outlet_port('features', list)
 
    def execute(self):
        # Load data
        absolute_path = os.path.abspath(self.settings['dataset_path'])
        print(absolute_path)
        dataset = read_csv(absolute_path, sep=self.settings['col_separator'], header=0, low_memory=False,
                           infer_datetime_format=True, parse_dates=self.settings['parse_cols_as_date'],
                           index_col=self.settings['index_col'])
        return {"output_data": dataset, "features": [self.settings['ip_features'], self.settings['target']]}
