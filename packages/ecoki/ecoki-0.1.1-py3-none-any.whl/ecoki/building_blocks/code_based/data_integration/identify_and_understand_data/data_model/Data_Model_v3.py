# Libs import + packages
import csv
import itertools
import pandas as pd
import time
import json
from pymongo import MongoClient
import bson

# ---------------------------------------Schema and Data-Model----------------------------------------------
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
                    },  # property
                    'subcomponents_ID': {
                        'bsonType': ["array"],
                        'minItems': 0,
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
                                            'bsonType': "objectId",
                                            'description': "It is an identifier of component."
                                        }}}}
                        }
                    }
                }  # out properties
            }  # eNd of Components items
        }  # eNd of Components
    }  # eNd of json properties
}}  # data model
# ---------------------------------------Create Data----------------------------------------------

def import_data():
    ds = pd.read_csv(r'D:\ViewMeasurements1000Sample.csv', encoding='unicode_escape')
    # print the shape of the dataframe
    print("print rows:", ds.shape)
    print(ds.head())
    # print(list(ds['date_time']))

    # col_1 = list(ds['Unnamed:0'])
    col_2 = list(ds['Zeitstempel'])
    col_3 = list(ds['OrderID'])
    col_4 = list(ds['Eigenschaft_ID'])
    col_5 = list(ds['Eigenschaft_Name'])
    col_6 = list(ds['Eigenschaft_Typ'])
    col_7 = list(ds['Kategorie_ID'])
    col_8 = list(ds['Kategorie_Name'])
    col_9 = list(ds['TextValue'])
    col_10 = list(ds['DateTimeValue'])
    col_11 = list(ds['BooleanValue'])
    col_12 = list(ds['NumericValue'])
    col_13 = list(ds['EntityValue'])

    for (b, c, d, e, f, g, h, i, j, k, l, m) in itertools.zip_longest(col_2, col_3, col_4,
                                                                      col_5, col_6, col_7, col_8,
                                                                      col_9, col_10, col_11, col_12,
                                                                      col_13):
        value = float(l)
        if value is not None:
            doc = {"timestamp": str(b),
                   "components": [
                       {"property": {"id": str(g), "type": str(h), "value": float(l)},
                        'subcomponents_ID': [
                            {"property": {"id": str(d)}}]  # eNd of subcomponents
                        }]  # eNd of components
                   }

            collection.insert_one(doc)
        else:
            doc = {"timestamp": str(b),
                   "components": [
                       {"property": {"id": str(g), "type": str(h), "value": float(k)},
                        'subcomponents_ID': [
                            {"property": {"id": str(d)}}]  # eNd of subcomponents
                        }]  # eNd of components
                   }
            collection.insert_one(doc)

        doc2 = {
            "components": [
                {"property": {"id": str(d), "name": str(e), "type": str(f), "annotation": str(c)}}
            ]  # eNd of subcomponents
        }
        collection.insert_one(doc2)


if __name__ == "__main__":

    # ---------------------------------------Database----------------------------------------------
    # mongo client
    # other IP if db is on other PC
    mongo_url = "mongodb://141.76.56.139:27017/"
    # Compound_Feed_Production.viewMeasurements_Sample
    database_name = 'Compound_Feed_Production_1000'
    collection_name = 'viewMeasurements_Sample_1000'
    # build a client instance of MongoClient
    mongo_db = MongoClient(mongo_url)
    # declare database instance
    # create db
    database = mongo_db[database_name]
    try:
        database.create_collection("viewMeasurements_Sample_1000")
    except Exception as e:
        print(e)

    collection = database[collection_name]
    database.command("collMod", "viewMeasurements_Sample_1000", validator=plantschema)  # add json validation

    import_data()
