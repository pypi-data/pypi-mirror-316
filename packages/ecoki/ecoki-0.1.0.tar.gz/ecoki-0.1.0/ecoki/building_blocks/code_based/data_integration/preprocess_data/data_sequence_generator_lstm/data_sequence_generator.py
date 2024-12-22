from ecoki.building_block_framework.building_block import BuildingBlock
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd


class DataSequenceGenerator(BuildingBlock):
    """Building block for generating time-step sequences of input and output features from a dataset."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.description = "Takes in the dataset and generates the time-step sequences for LSTM training"
        self.version = "1"
        self.category = "Transformer"
        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_inlet_port('input_and_target_features', list)
        self.add_outlet_port('output_data_sequences', list)
        self.add_outlet_port('output_data_sequences_timesteps', list)
        self.add_outlet_port('target_column', dict)

    def generate_sequences(self, dataset, target, ip_features):
        X, y, timesteps = list(), list(), list()
        for i in range(len(dataset)):
            # find the end of this pattern
            end_ix = i + int(self.settings['num_steps_in'])
            out_end_ix = end_ix + int(self.settings['num_steps_out'])
            # check if we are beyond the dataset
            if out_end_ix > len(dataset):
                break
            # gather timesteps for visualization later
            t_steps = dataset.index[i:out_end_ix].values.astype(str)
            # gather input and output parts of the pattern
            seq_x = dataset.loc[dataset.index[i:end_ix], ip_features]
            seq_y = dataset.loc[dataset.index[end_ix:out_end_ix], target]

            timesteps.append(t_steps)
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y), np.array(timesteps)

    def execute(self, input_data, input_and_target_features):
        ip_features = input_and_target_features[0]
        target = input_and_target_features[1]
        print(ip_features)
        print(target)
        X, y, timesteps = self.generate_sequences(input_data, target, ip_features)
        print(X.shape, y.shape)
        return {"output_data_sequences": [X, y], "output_data_sequences_timesteps": [timesteps],
                "target_column": { input_data.columns.get_loc(target): target }}
