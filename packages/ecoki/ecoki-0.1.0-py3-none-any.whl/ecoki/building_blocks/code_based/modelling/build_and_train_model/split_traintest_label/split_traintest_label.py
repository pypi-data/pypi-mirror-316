import pandas as pd
from ecoki.building_block_framework.building_block import BuildingBlock
from sklearn.model_selection import train_test_split

class SplitTrainTestLabel(BuildingBlock):
    """
    A BuildingBlock class for splitting a pre-processed input dataset into training and test datasets.

    This class takes a pre-processed dataset as input and splits it into training and test datasets, 
    with the test dataset size being 20% of the original dataset. It is designed to prepare data for 
    further training and prediction tasks.

    Args:
        **kwargs: Additional keyword arguments to pass to the parent class.

    Attributes:
        architecture (str): The name of the architecture.
        description (str): A brief description of the class functionality.
        version (str): The version of the class.
        category (str): The category of the class.
    """

    def __init__(self, **kwargs):
        """
        Initializes the SplitTrainTestLabel class with specified keyword arguments.

        Args:
            **kwargs: Keyword arguments for the BuildingBlock superclass.
        """
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Splits a pre-processed input dataset into training and test datasets."
        self.version = "1"
        self.category = "Transformer"

        self.add_inlet_port('input_data', pd.DataFrame)
        self.add_outlet_port('output_data', list)

    def execute(self, input_data):
        """
        Splits the input dataset into training and test datasets based on the specified settings.

        Args:
            input_data (pd.DataFrame): The input dataset to be split.

        Returns:
            dict: A dictionary containing the training and test datasets, the label column, and other relevant information.
                The dictionary has the following structure:
                {
                    'output_data': [x_train, x_valid, y_train, y_valid, label_column]
                }
                Where:
                - x_train: Features of the training set
                - x_valid: Features of the validation (test) set
                - y_train: Labels of the training set
                - y_valid: Labels of the validation (test) set
                - label_column: Name(s) of the label column(s)
        """
        
        label_column = self.settings["selected_columns_label"]

        print("\n")
        print("label column(s) are", label_column)
        print("\n")
        
        selected_columns = self.settings["selected_columns"]
        print("selected features are", selected_columns)

        input_data.reset_index(drop=True, inplace=True)

        Data_X = input_data.loc[:, input_data.columns.isin(selected_columns)]
        Data_Y = input_data.loc[:, label_column]

        # hotfix for adding a settings that we are able to disable shuffling
        try:
            shuffle = self.settings["shuffle"]
            x_train, x_valid, y_train, y_valid = train_test_split(
                Data_X, Data_Y, test_size=0.2, random_state=0, shuffle=shuffle
            )
        except:
            x_train, x_valid, y_train, y_valid = train_test_split(
                Data_X, Data_Y, test_size=0.2, random_state=0
            )

        output_data = [x_train, x_valid, y_train, y_valid, label_column]

        return {"output_data": output_data}

