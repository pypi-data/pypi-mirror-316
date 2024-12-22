# System libraries
# import datetime, time, os, pprint
# Libs import + packages
# from pymongo import MongoClient
import csv
import itertools
import pandas as pd
# Other libraries optional
import json

# ---------------------------------------Schema and Data-Model---------------------------------
# Create the Schema and Data-Model
plantschema = {"$jsonSchema": {
    'bsonType': "object",
    'required': ["timestamp", "components"],
    'properties': {
        'plantID': {
            'bsonType': "string",
            'description': "must be a string"
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
                        'description': "It is an attribute of a component.",
                        'properties': {
                            'id': {
                                'bsonType': "string",
                                'description': "It is an identifier of component."
                            },
                            'name': {
                                'bsonType': "string",
                                'description': "It is a name of the component."
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
                            'annotation': {"bsonType": "string"}
                        }  # in properties
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
                                    'description': "It is an attribute of a component.",
                                    # 'required': ["id"],
                                    'properties': {
                                        'id': {
                                            'bsonType': "string",
                                            'description': "It is an identifier of component."
                                        },
                                        'name': {
                                            'bsonType': "string",
                                            'description': "It is a name of the component."
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
                                        'annotation': {"bsonType": "string"}
                                    }  # in properties
                                },
                            }  # eNd of subComponents properties
                        }  # eNd of subComponents items
                    }
                }  # eNd of Components properties
            }  # eNd of Components items
        }  # eNd of Components
    }
}}
