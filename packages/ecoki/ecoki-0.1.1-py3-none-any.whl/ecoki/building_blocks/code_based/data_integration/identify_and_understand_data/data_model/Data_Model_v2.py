# System libraries imports
import datetime
import json
from pymongo import MongoClient

def create_schema_collection():
    # url of Virtual Machine + MongoDB
    mongo_url = "mongodb://141.76.56.139:27017/"
    #mongo_url = "mongodb://localhost:27017/"
    mongo_db = MongoClient(mongo_url)
    # declare database instance
    # create db
    db = mongo_db["ecoKI_Database"]
    # ---------------------------------------Schema and Data-Model---------------------------------
    # Create the Schema and Data-Model
    plantschema = {"$jsonSchema": {
        'description': "ecoKI Database Schema implementation.",
        'bsonType': "object",
        'required': ["components"],
        'properties': {
            'plantID': {
                'bsonType': "string",
                'description': "It is a plant identifier."
            },
            'timestamp': {
                'bsonType': "string",
                'description': "It is a timeseries."
            },
            'components': {
                'bsonType': ["array"],
                'minItems': 1,
                'uniqueItems': False,
                'additionalProperties': False,
                'items': {
                    'bsonType': "object",
                    'description': "It is an array of sensors/objects",
                    'required': ["property"],
                    'properties': {
                        'property': {
                            'bsonType': "object",
                            'description': "It is an attribute of a component.",
                            'required': ["id"],
                            'properties': {
                                'id': {
                                    'bsonType': "string",
                                    'description': "It is an identifier of component."
                                },
                                'type': {
                                    'bsonType': "string",
                                    'description': "It is a name of component."
                                },
                                'value': {
                                    'bsonType': "double",
                                    'description': "It is a numericValue of component."
                                },
                                'unit': {
                                    'bsonType': "string",
                                    'description': "It is unitSymbol of the property component."
                                },
                                'annotations': {"type": "object"}
                            }#in properties
                        }#property
                    }#out properties
                }# eNd of Components items
            }# eNd of Components
        }# eNd of json properties
    }}
    # Create collection with the Schema and Data-Model
    try:
        db.create_collection("data")
    except Exception as e:
        print(e)
    db.command("collMod" ,"data", validator=plantschema)

def write_metadata():
    """Writes data to the DB entry Specified by key"""

    # url of Virtual Machine + MongoDB
    mongo_url = "mongodb://141.76.56.139:27017/"
    #mongo_url = "mongodb://localhost:27017/"
    client = MongoClient(mongo_url)

    # Database Name
    db = client["ecoKI_Database"]
    # Collection Name
    col = db["metadata"]

    t = str(datetime.datetime.now())
    doc = dict()
    doc = {
           "components": [
               {
                   "property": {"id": "HeatSensor","type": "Temperature", "unit": "Celsius"}}
           ]  # eNd of components
           }
    col.insert_one(doc)

def write_data():
    """Writes data to the DB entry Specified by key"""

    # url of Virtual Machine + MongoDB
    mongo_url = "mongodb://141.76.56.139:27017/"
    # mongo_url = "mongodb://localhost:27017/"
    client = MongoClient(mongo_url)

    # Database Name
    db = client["ecoKI_Database"]
    # Collection Name
    col = db["data"]

    # Opening JSON file
    # location \hackathonDB\db.json
    # f = open('\hackathonDB\db.json')
    f = open(r'C:\Users\Fatima\PycharmProjects\adapter\hackathonDB\db.json')

    data = json.load(f)

    # Iterating through the json
    # list
   # for i in data['app130/solar']:

    # Closing file
    f.close()

def write_subdata(self, **kwargs):
    """Writes data to the DB entry Specified by key"""

    # url of Virtual Machine + MongoDB
    mongo_url = "mongodb://141.76.56.139:27017/"
    # mongo_url = "mongodb://localhost:27017/"
    client = MongoClient(mongo_url)

    # Database Name
    db = client["ecoKI_Database"]
    # Collection Name
    col = db["data"]

    t = str(datetime.datetime.now())
    doc = dict()
    doc = {
           "components": [
               {
                   "property": {"id": "HeatSensor","type": "Temperature", "unit": "Celsius"}}
           ]  # eNd of components
           }
    col.insert_one(doc)

if __name__ == '__main__':
    create_schema_collection()
    #write_metadata()
    write_data()