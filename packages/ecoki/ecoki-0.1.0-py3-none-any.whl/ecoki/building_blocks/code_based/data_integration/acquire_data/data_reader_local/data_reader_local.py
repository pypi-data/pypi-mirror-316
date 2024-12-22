from ecoki.building_block_framework.building_block import BuildingBlock
from io import StringIO
import pandas as pd
import time

class DataReaderLocal(BuildingBlock):
    
    """
    A building block for reading CSV data from local files.

    This class extends the BuildingBlock class and provides functionality
    to read CSV data from local files and process it into a pandas DataFrame.

    Attributes:
        architecture (str): The architecture of the building block.
        description (str): A brief description of the building block's functionality.
        version (str): The version of the building block.
        category (str): The category of the building block.
        data (pd.DataFrame): The DataFrame to store the read data.

    """


    def __init__(self, **kwargs):
        
        """
        Initialize the DataReaderLocal building block.

        Args:
            **kwargs: Additional keyword arguments to pass to the parent class.

        """

        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Read csv data from local"
        self.version = "1"
        self.category = "Transformer"

        self.add_outlet_port('output_data', pd.DataFrame)

        self.dataset = None
        self.data_num = None
        self.start_index = 0
        self.data = None

        self.interval = 1

    def upload_local_dataset(self, file_path, columns_separator=None):

        if columns_separator:
            self.dataset = pd.read_csv(file_path, sep=columns_separator)
        else:
            self.dataset = pd.read_csv(file_path)

    def execute(self):
        
        """
        Execute the data reading process.

        This method reads the CSV data from the specified file path,
        sets the index if specified, and returns the processed DataFrame.

        Returns:
            dict: A dictionary containing the output DataFrame.

        """

        if self.interactive_settings:
            if self.settings["index_name"]:
                if self.settings["index_name"].isdigit():
                    self.settings["index_name"] = int(self.settings["index_name"])
                self.data = self.dataset.set_index(self.settings["index_name"])
        else:
            if not self.data_num:
                file_path = self.settings["data_file_path"]
                columns_separator = self.settings["columns_separator"]
                self.upload_local_dataset(file_path, columns_separator)

                if self.settings["index_name"]:
                    if self.settings["index_name"].isdigit():
                        self.settings["index_name"] = int(self.settings["index_name"])
                    self.dataset.set_index(self.settings["index_name"], inplace=True)

                if self.settings["invert_data"]:
                    self.dataset = self.dataset * -1
                self.data_num = self.settings["data_num"]
                self.interval = self.settings["interval"]

            self.data = self.dataset.iloc[self.start_index: self.start_index + self.data_num]
            self.start_index += self.data_num
            time.sleep(self.interval)

        return {"output_data": self.data}
