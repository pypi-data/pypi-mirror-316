# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock
from ecoki.building_blocks.code_based.data_integration.identify_and_understand_data.data_model.Data_Model_v4 import \
    plantschema

# External library imports
from opcua import Client
import pandas as pd
import time
import datetime
import pymongo
from enum import Enum
import json


def get_data_by_number(func, param=1, interval=0):
    for i in range(param):
        func()
        time.sleep(interval)


def get_data_by_timeout(func, param=10, interval=0):
    start_time = datetime.datetime.now()
    timeout = datetime.timedelta(seconds=param)

    while True:
        current = datetime.datetime.now()
        if current - start_time >= timeout:
            break
        func()
        time.sleep(interval)


class OPCUAExecutionMode(Enum):
    num = get_data_by_number
    timeout = get_data_by_timeout


class DataReaderOPCUA(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Read data from OPC UA server and store data into MongoDB"
        self.version = "1"
        self.category = "Data integration/acquire data"
        self.reset_attributes()
        # self.add_outlet_port('output_data', pd.DataFrame)
        self.add_outlet_port('output_data', list)

    def reset_attributes(self):
        self.opcua_client = None
        self.mongodb_client = None
        self.mongodb_collection = None
        self.store_data = False

        self.opcua_database_config = None
        self.plantID = None

        self.nodes_list = []
        self.node_dict = {}

        self.opcua_data_list = []

        self.mode = None
        self.param = None
        self.interval = None

        self.node_timestamp = None

        self.execution_func = None

    def handle_configuration(self):
        config_path = self.settings["opcua_config"]
        opcua_config_file = open(config_path)
        self.opcua_database_config = json.load(opcua_config_file)
        self.plantID = self.opcua_database_config["opcua"]["plantID"]
        self.mode = self.opcua_database_config["opcua"]["parameters"]["mode"]
        self.param = self.opcua_database_config["opcua"]["parameters"]["param"]
        self.interval = self.opcua_database_config["opcua"]["parameters"]["interval"]
        self.execution_func = eval(f"OPCUAExecutionMode.{self.mode}")

    def connect_to_opcua_server(self):
        opcua_server_url = self.opcua_database_config["opcua"]["server_url"]
        self.opcua_client = Client(opcua_server_url)

        time_out = 5

        while True:
            try:
                self.opcua_client.connect()
                print("connected")
                break

            except Exception as e:
                self.logger.logger.error(
                    f"Trying to re-establish connection with server {opcua_server_url} in {time_out} seconds ..................."
                )
                print(e)
                time.sleep(time_out)

    def create_nodes_list(self):
        for node_id, node_info in self.opcua_database_config["opcua"]["nodes"].items():
            namespace = node_info["name_space"]
            index = node_info["index"]
            if type(index) is int:
                self.nodes_list.append(f"ns={namespace};i={index}")
            else:
                self.nodes_list.append(f"ns={namespace};s={index}")

    def connect_to_database(self):

        database_server_url = self.opcua_database_config["opcua"]["database"]["database_server_url"]
        database_name = self.opcua_database_config["opcua"]["database"]["database_name"]
        collection_name = self.opcua_database_config["opcua"]["database"]["collection_name"]

        self.mongodb_client = pymongo.MongoClient(database_server_url)

        mongodb = self.mongodb_client[database_name]

        try:
            mongodb.create_collection(collection_name)
            mongodb.command("collMod", collection_name, validator=plantschema)

        except Exception as e:
            self.logger.logger.error(e)

        mongoDB_collection = mongodb[collection_name]

        self.mongodb_collection = mongoDB_collection

    def get_nodes(self, nodeID):
        """
        convert nodeID (string) to opcua node object
        :param node_list: a list containing nodeIDs (string)
        :return: opc ua node object
        """
        # for nodeID in node_list:
        node = self.opcua_client.get_node(nodeID)  # node object of opc ua
        return node

    def request_nodes_value(self, node):
        name = node.get_display_name().Text
        nodeID = str(node)

        node_data_value = None
        try:
            node_data_value = node.get_data_value()
        except Exception:
            pass

        if not node_data_value:
            return {}

        node_value = node_data_value.Value.Value
        node_timestamp = node_data_value.SourceTimestamp

        node_dict = {"timestamp": node_timestamp, f"{name}_ID": nodeID, f"{name}_value": node_value}

        return node_dict

    def get_node_dict(self, node):
        self.node_dict.update(self.request_nodes_value(node))
        if node.get_children():
            for sub_node in node.get_children():
                self.get_node_dict(sub_node)

    def get_node_value(self, node, main_component_dict):
        opcua_node = self.get_nodes(node)
        name = opcua_node.get_display_name().Text + node
        nodeID = str(opcua_node)
        node_data_value = None
        try:
            node_data_value = opcua_node.get_data_value()
        except Exception:
            pass
        if not node_data_value:
            component_dict = {"property": {"id": str(nodeID), "name": str(name)}}
        else:
            node_value = node_data_value.Value.Value
            self.node_timestamp = node_data_value.SourceTimestamp
            component_dict = {"property": {"id": str(nodeID), "name": str(name), "value": float(node_value)}}

        if main_component_dict:
            main_property_name = main_component_dict["property"]["name"]
            component_name = component_dict["property"]["name"]
            component_dict["property"]["name"] = f"{main_property_name} {component_name}"
            main_component_dict["subcomponents"].append(component_dict)

        if opcua_node.get_children():
            for sub_node in opcua_node.get_children():
                component_dict["subcomponents"] = []
                self.get_node_value(sub_node, component_dict)
        return component_dict

    def get_and_save_data(self):
        components_list = []
        for node in self.nodes_list:
            components_dict = self.get_node_value(node, None)
            components_list.append(components_dict)

        if self.plantID:
            opcua_data = {"plantID": self.plantID, "timestamp": self.node_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                          "components": components_list}
        else:
            opcua_data = {"timestamp": self.node_timestamp.strftime('%Y-%m-%d %H:%M:%S'), "components": components_list}

        self.opcua_data_list.append(opcua_data)

        if self.store_data:
            print(opcua_data)
            self.mongodb_collection.insert_one(opcua_data)

    def execute(self):
        try:
            if not self.opcua_client:
                self.handle_configuration()
                self.connect_to_opcua_server()
                self.create_nodes_list()

                if self.opcua_database_config["opcua"]["database"]:
                    self.connect_to_database()
                    self.store_data = True

            if self.opcua_data_list:
                self.opcua_data_list = []

            self.execution_func(self.get_and_save_data, self.param, self.interval)

            return {"output_data": self.opcua_data_list}

        except Exception as exc:
            self.logger.logger.error(f'Cannot execute building block {self.name}')
            self.logger.logger.error(exc, exc_info=True)

    def close_connection(self):
        self.opcua_client.disconnect()