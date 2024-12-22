# System imports
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock


class DuplicatesRemover(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._architecture = "EcoKI"
        self._version = "1"
        self._description = "Remove duplicate rows & columns from a tabular dataset passed as input. \
        Columns with duplicate names and columns with different names but duplicate values are removed."
        self._category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', pd.DataFrame)

    def execute(self, input_data):
        subset = None
        if 'subset' in self.settings:
            subset = self.settings['subset']

        keep = 'first'
        if 'keep' in self.settings:
            keep = self.settings['keep']
            if self.settings['keep'] == "False":
                keep = False

        # Throw error if arguments aren't of the expected type
        if not isinstance(subset, list) and subset is not None:
            raise TypeError("subset should be a list of column names or 'None'.")
        if not isinstance(keep, str) and keep is not False:
            raise TypeError("keep should be first, last or False.")

        df = input_data

        # Remove columns with duplicate names
        df = df.loc[:, ~df.columns.duplicated()].copy()  # TODO: Double-check if copy() is necessary

        # Remove columns with duplicate values
        df = df.loc[:, ~df.apply(lambda x: x.duplicated(), axis=1).all()].copy()

        # Remove duplicate rows & return result as json string
        df = df.drop_duplicates(subset=subset, keep=keep)

        return {"output_data": df}
