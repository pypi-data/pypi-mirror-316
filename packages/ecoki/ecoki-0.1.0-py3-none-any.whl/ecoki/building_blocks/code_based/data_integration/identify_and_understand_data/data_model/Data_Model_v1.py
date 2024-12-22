# System libraries
import datetime, time, os, pprint
# Libs import + packages
from pymongo import MongoClient
import csv
import itertools
import pandas as pd
# Other libraries optional
import json

""" 
    Get the data from the opcua server and store into data-model of local MongoDB! 
"""
def create_schema_collection():
# ---------------------------------------Database----------------------------------------------
    # IP address can be : local / VM DB / other PC
    mongo_url = "mongodb://141.76.56.139:27017/"
    # mongo_url = "mongodb://localhost:27017/"
    mongo_db = MongoClient(mongo_url)
    # declare database instance
    db = mongo_db["OPCUA_Model"]
# ---------------------------------------Schema and Data-Model---------------------------------
# Create the Schema and Data-Model
    plantschema = {"$jsonSchema": {
        'bsonType': "object",
        'required': ["plantID", "timestamp", "components"],
        'properties': {
            'plantID': {
                'bsonType': "string",
                'description': "must be a string and is required"
            },
            'timestamp': {
                'bsonType': "string",
                'description': "must be a string and is required"
            },
            'components': {
                'bsonType': ["array"],
                'minItems': 1,
                'uniqueItems': False,
                'additionalProperties': False,
                'items': {
                    'bsonType': "object",
                    'description': "must contain the stated fields.",
                    'required': ["property"],
                    'properties': {
                        'name': {
                            'bsonType': "string",
                            'description': "property of component"
                        },
                        'property': {
                            'bsonType': "object",
                            'description': "property of component",
                            'required': ["name"],
                            'properties': {
                                'name': {
                                    'bsonType': "string",
                                    'description': "name of component"
                                },
                                'numericValue': {
                                    'bsonType': "number",
                                    'description': "The value of the property component"
                                }
                            }
                        },
                        'subcomponents': {
                            'bsonType': ["array"],
                            'minItems': 1,
                            'uniqueItems': False,
                            'additionalProperties': False,
                            'items': {
                                'bsonType': "object",
                                'description': "must contain the stated fields.",
                                'required': ["property"],
                                'properties': {
                                    'name': {
                                        'bsonType': "string",
                                        'description': "sensor name"
                                    },
                                    'property': {
                                        'bsonType': "object",
                                        'description': "property of sub-component",
                                        'required': ["name"],
                                        'properties': {
                                            'name': {
                                                'bsonType': "string",
                                                'description': "name of sub-component"
                                            },
                                            'numericValue': {
                                                'bsonType': "number",
                                                'description': "The value of the property sub-component"
                                            }
                                        }
                                    },
                                }  # eNd of subComponents properties
                            }  # eNd of subComponents items
                        }
                    }  # eNd of Components properties
                }  # eNd of Components items
            }  # eNd of Components
        }
    }}

    # Create collection with the Schema and Data-Model
    try:
        db.create_collection("data")
    except Exception as e:
        print(e)
    db.command("collMod", "data", validator=plantschema)