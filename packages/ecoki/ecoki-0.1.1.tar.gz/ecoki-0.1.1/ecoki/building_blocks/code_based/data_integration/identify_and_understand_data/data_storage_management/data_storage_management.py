# System imports
import pymongo
import panel as pn
# import json

# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock
from ecoki.building_blocks.code_based.data_integration.identify_and_understand_data.data_model.Data_Model_v4 import \
    plantschema


class DataStorageManagement(BuildingBlock):
    """Building block for Data Storage Management """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.architecture = "EcoKI"
        self.version = "1"
        self.description = "Data Storage Management, create database and check existing database and collections"
        self.category = "DBMS"

        self.mongodb_client = None
        self.mongodb_url = None
        self.database = None
        self.database_name = None
        self.panel_widgets_list = []

        self.add_inlet_port('input_data', dict)
        self.add_outlet_port('output_data', dict)

    def create_mongodb_connection(self):
        self.mongodb_client = pymongo.MongoClient(self.mongodb_url)

    def create_database_and_collection(self, database_config):

        self.mongodb_url = database_config["url"]
        self.database_name = database_config["name"]
        collection_name = database_config["collection"]

        self.create_mongodb_connection()

        mongodb = self.mongodb_client[self.database_name]

        try:
            mongodb.create_collection(collection_name)
            mongodb.command("collMod", collection_name, validator=plantschema)

        except Exception as e:
            print(e)

        mongoDB_collection = mongodb[collection_name]

        return mongoDB_collection

    def execute(self, input_data):


        database_config = input_data["database_config"]
        mongodb_collection = self.create_database_and_collection(database_config)
        processed_data = input_data["processed_data"]
        mongodb_collection.insert_many(processed_data)

        collection_list = self.mongodb_client[self.database_name].list_collection_names()
        results = {"collection_list": collection_list, "database_name": self.database_name}

        if self.mongodb_client:
            self.mongodb_client.close()

        return {"output_data": results}
