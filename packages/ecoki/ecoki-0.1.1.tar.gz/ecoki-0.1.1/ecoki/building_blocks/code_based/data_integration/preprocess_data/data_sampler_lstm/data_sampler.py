from ecoki.building_block_framework.building_block import BuildingBlock
import pandas as pd
import os
from numpy import nan, isnan
from pandas import read_csv


class DataSampler(BuildingBlock):
    """Building block for sampling dataset based on time(minutes, hours, etc.)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.description = "Sample dataset based on time(minutes, hours, etc.)"
        self.version = "1"
        self.category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', pd.DataFrame)
 
    def execute(self, input_data):
        data = input_data

        print(self.settings['datetime_sampling_resolution'])
        daily_groups = data.resample(self.settings['datetime_sampling_resolution'])
        daily_data = daily_groups.sum()
        daily_data.index = daily_data.index.to_period(self.settings['datetime_sampling_resolution'])
        # Set the processed data to the output port
        return {"output_data": daily_data}
