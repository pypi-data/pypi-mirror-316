# System imports
# System imports
import pandas as pd
import pymongo
import threading
import pandas
# Project imports
from ecoki.building_block_framework.building_block import BuildingBlock


class MongoDBClient:
    def __init__(self):
        self.database_host_url = None
        self.database_name = None
        self.collection_name = None
        self.mongodb_client = None

        self.database = None

    def connect_to_mongodb_sever(self, db_url):
        self.database_host_url = db_url
        self.mongodb_client = pymongo.MongoClient(self.database_host_url)

    def get_database_list(self):
        database_name_list = self.mongodb_client.list_database_names()
        return database_name_list

    def get_database(self, database_name):
        self.database_name = database_name
        self.database = self.mongodb_client[self.database_name]

    def get_collection_list(self):
        collection_name_list = self.database.list_collection_names()
        return collection_name_list


class MongoDBDataReader(BuildingBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.version = "1"
        self.description = "Given the mongoDB server url, database and collection name, " \
                           "retrieve data from mongoDB and return the documents. "
        self.category = "DBMS"
        self.add_outlet_port('output_data', pd.DataFrame)

        self.mongodb_url = None
        self.mongodb_database_name = None
        self.mongodb_collections_config = None

        self.mongodb_client = MongoDBClient()
        self.mongoDB_documents = []
        self.mongoDB_collection_list = []

        self.df = None

    def create_mongodb_connection(self, db_url):
        self.mongodb_client.connect_to_mongodb_sever(db_url)

    def handle_database_configuration(self):
        """
        :param input_data: database configuration in dict
        --> {"database":{"url": ,"database_name": ,"collection": ["name": ,"query": ]}
        """
        database_config = self.settings['database']
        self.mongodb_url = database_config["url"]
        self.mongodb_database_name = database_config["database_name"]
        self.mongodb_collections_config = database_config["collection"]

    def convert_mongodb_docs_to_df(self, mongo_documents):
        mongoDB_documents = mongo_documents

        def apply_component(df_series):
            nested_dict = {}
            for i in range(len(df_series)):

                if "subcomponents" in df_series[i].keys():
                    subcomponent_dict = {}
                    sub_nested_dict = apply_subcomponent(df_series[i]["subcomponents"], subcomponent_dict)
                    df_series[i]["subcomponents"] = sub_nested_dict
                try:
                    nested_dict[df_series[i]["property"].pop("name")] = df_series[i]
                except KeyError:
                    nested_dict[i] = df_series[i]
            return {"components": nested_dict}

        def apply_subcomponent(subcomponent, sub_dict):
            for i in range(len(subcomponent)):
                if "subcomponents" in subcomponent[i].keys():
                    if subcomponent[i]["subcomponents"]:
                        subcomponent_dict = {}
                        sub_nested_dict = apply_subcomponent(subcomponent[i]["subcomponents"], subcomponent_dict)
                        subcomponent[i]["subcomponents"] = sub_nested_dict
                    else:
                        subcomponent[i].pop("subcomponents")

                try:
                    sub_dict[subcomponent[i]["property"].pop("name")] = subcomponent[i]
                except KeyError:
                    sub_dict[i] = subcomponent[i]
            return sub_dict

        normalized_df = pd.json_normalize(mongoDB_documents)
        normalized_df["components"] = normalized_df["components"].apply(apply_component)
        components_df = pd.json_normalize(normalized_df["components"].tolist())

        df = pd.concat([normalized_df, components_df], axis=1)
        df.drop(["_id", "components"], axis=1, inplace=True)

        if self.settings["index_name"]:
            df.set_index(self.settings["index_name"], inplace=True)

        self.df = df

    def execute(self):
        try:
            if not self.interactive_settings:
                self.create_mongodb_connection(self.settings["database_url"])
                self.mongodb_client.get_database(self.settings["database_name"])

            else:
                pass

            if self.mongoDB_documents:
                self.mongoDB_documents.clear()

            collection_name = self.settings["collection"]
            num_doc = self.settings["number_documents"]

            mongoDB_database = self.mongodb_client.database
            mongoDB_collection = mongoDB_database[collection_name]

            # data_queries = self.mongodb_collections_config[i].pop("query")
            data_queries = False
            # data_projection = self.mongodb_collections_config[i].pop("projection")
            data_projection = {}

            if num_doc:
                if not data_queries:
                    documents_list = list(mongoDB_collection.find()[:num_doc])
                    self.mongoDB_documents.extend(documents_list)
                else:
                    documents_list = list(
                        mongoDB_collection.find(data_queries, data_projection)[:num_doc])
                    self.mongoDB_documents.extend(documents_list)

            else:
                if not data_queries:
                    documents_list = list(mongoDB_collection.find())
                    self.mongoDB_documents.extend(documents_list)
                else:
                    documents_list = list(mongoDB_collection.find(data_queries, data_projection))
                    self.mongoDB_documents.extend(documents_list)

            self.convert_mongodb_docs_to_df(self.mongoDB_documents)

            if self.mongodb_client.mongodb_client:
                self.mongodb_client.mongodb_client.close()

            return {"output_data": self.df}

        except Exception as exc:
            self.logger.logger.error(f'Cannot execute building block {self.name}')
            self.logger.logger.error(exc, exc_info=True)
