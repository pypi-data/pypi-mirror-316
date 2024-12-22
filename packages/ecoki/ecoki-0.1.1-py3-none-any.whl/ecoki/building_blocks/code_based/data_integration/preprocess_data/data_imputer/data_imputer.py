# System imports
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock


class DataImputer(BuildingBlock):
    """A building block for imputing missing data in a DataFrame.

    This class extends the BuildingBlock class and provides functionality
    to impute missing values in numerical and categorical columns of a
    pandas DataFrame.

    Attributes:
        architecture (str): The architecture of the building block.
        description (str): A brief description of the building block's functionality.
        version (str): The version of the building block.
        category (str): The category of the building block.

    """

    def __init__(self, **kwargs):
        """Initialize the DataImputer building block.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent class.
        """
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.description = "Impute missing data"
        self.version = "1"
        self.category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', pd.DataFrame)

    def execute(self, input_data):
        
        strategy_num = 'median'
        if 'strategy_num' in self.settings:
            strategy_num = self.settings['strategy_num']

        strategy_cat = 'most_frequent'
        if 'strategy_cat' in self.settings:
            strategy_cat = self.settings['strategy_cat']

        fill_value = None
        if 'fill_value' in self.settings:
            fill_value = self.settings['fill_value']

        labels = None
        if 'labels' in self.settings:
            labels = self.settings['labels']

        # Get list of columns with numerical data (float & int)
        num_columns = list(input_data.select_dtypes(include=['float64', 'int64'], exclude=labels).columns)
        num_imputer = None
        if len(num_columns) > 0:
            # Replace missing numerical data
            num_imputer = SimpleImputer(missing_values=np.nan, strategy=strategy_num, fill_value=fill_value)
            num_imputer.fit(input_data[num_columns])  # Fit num. imputer on data
            input_data[num_columns] = num_imputer.transform(input_data[num_columns])  # Impute missing train data

        # Get list of columns with categorical data
        cat_columns = list(input_data.select_dtypes(include=['category', 'object'], exclude=labels).columns)
        cat_imputer = None
        if len(cat_columns) > 0:
            # Replace missing categorical data
            cat_imputer = SimpleImputer(missing_values=np.nan, strategy=strategy_cat, fill_value=fill_value)
            cat_imputer.fit(input_data[cat_columns])  # Fit cat. imputer on data
            input_data[cat_columns] = cat_imputer.transform(input_data[cat_columns])  # Impute missing train data

        return {"output_data": input_data}