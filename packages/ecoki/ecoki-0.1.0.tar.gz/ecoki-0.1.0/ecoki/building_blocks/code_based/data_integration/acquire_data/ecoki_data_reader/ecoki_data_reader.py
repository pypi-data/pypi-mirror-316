from ecoki.building_block_framework.building_block import BuildingBlock
from ecoki.building_blocks.code_based.data_integration.acquire_data.ecoki_data_reader.data_reader_register import DataReaderRegister
from ecoki.common.module_object_creator import create_object_by_module
import pandas as pd


class EcoKIDataReader(BuildingBlock):
    """
    A building block for reading data in the EcoKI architecture.

    This class provides functionality to register and execute various data readers.

    Attributes:
        architecture (str): The name of the architecture.
        description (str): A brief description of the data reader set.
        version (str): The version of the data reader.
        category (str): The category of the building block.
        data_reader_dict (dict): A dictionary to store registered data readers.

    """

    def __init__(self, **kwargs):
        """
        Initialize the EcoKIDataReader.

        Args:
            **kwargs: Additional keyword arguments to be passed to the parent BuildingBlock class.
        """
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "ecoKI data reader set"
        self.version = "1"
        self.category = ""

        self.add_outlet_port('output_data', pd.DataFrame)

        self.data_reader_dict = {}
        self.register_data_readers(**kwargs)

    def register_data_readers(self, **kwargs):
        """
        Register data readers from the DataReaderRegister.

        Args:
            **kwargs: Additional keyword arguments to be passed to create_object_by_module.
        """
        for data_reader in DataReaderRegister:
            self.data_reader_dict[data_reader.name] = create_object_by_module(data_reader.value, data_reader.name, **kwargs)

    def execute(self, **kwargs):
        """
        Execute the selected data reader.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            The result of executing the selected data reader.
        """
        bb = self.data_reader_dict[self.settings["data_reader"]]
        bb.set_settings(self.settings)

        bb.interactive_settings = self.interactive_settings
        #if self.interactive_settings:
        #    bb.interactive_settings = True
        #else:
        #    bb.interactive_settings = False
        res = bb.execute()

        return res
