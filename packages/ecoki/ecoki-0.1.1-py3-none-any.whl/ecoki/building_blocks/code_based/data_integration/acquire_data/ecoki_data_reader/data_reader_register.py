from enum import Enum
import importlib


class DataReaderGUIRegister(Enum):
    DataReaderLocal = "ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_local.interactive_gui"
    DataReaderDataverse = "ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_dataverse.interactive_gui"
    MongoDBDataReader = "ecoki.building_blocks.code_based.data_integration.acquire_data.mongoDB_data_reader.interactive_gui"


class DataReaderRegister(Enum):
    DataReaderLocal = "ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_local.data_reader_local"
    DataReaderDataverse = "ecoki.building_blocks.code_based.data_integration.acquire_data.data_reader_dataverse.data_reader_dataverse"
    MongoDBDataReader = "ecoki.building_blocks.code_based.data_integration.acquire_data.mongoDB_data_reader.mongoDB_data_reader"

