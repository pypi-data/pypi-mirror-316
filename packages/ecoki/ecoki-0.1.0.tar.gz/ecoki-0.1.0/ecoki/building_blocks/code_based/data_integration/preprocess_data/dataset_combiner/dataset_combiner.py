# System imports
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock


class DatasetCombiner(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._architecture = "EcoKI"
        self._version = "1"
        self._description = "Combine (i.e. concatenate) multiple tabular datasets passed as input.\
        Depending on the chosen axis, datasets are concatenated vertically (more rows) or horizontally (more columns)."
        self._category = "Transformer"

        self.add_inlet_port('input_data', list)
        self.add_outlet_port('output_data', pd.DataFrame)

    def execute(self, input_data):
        axis = 0
        if 'axis' in self.settings:
            if self.settings['axis'] == "0":
                axis = 0
            elif self.settings['axis'] == "1":
                axis = 1

        join = 'outer'
        if 'join' in self.settings:
            join = self.settings['join']

        ignore_index = False
        if 'ignore_index' in self.settings:
            if self.settings['ignore_index'] == "True":
                ignore_index = True

        # Throw error if arguments aren't of the expected type
        if not axis == 0 and not axis == 1:
            raise TypeError("axis should be 0 or 1")
        if not isinstance(join, str) and list is not None:
            raise TypeError("join should be a string.")
        if not isinstance(ignore_index, bool):
            raise TypeError("ignore_index should be a boolean.")

        # TODO: There exist other, more advanced, dataset combination options in pandas (pandas.merge(), pandas.join())
        #  analogous to SQL database operations that we might want to include in the future, depending on
        #  the encountered use cases.

        combined_data = pd.concat(input_data, axis=axis, join=join,
                         ignore_index=ignore_index)
        return {'output_data': combined_data}
