#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Establish connection to MongoDB database

import os
import pandas as pd
import pymongo
from retry import retry

def db_connect():
    '''
    Set connection to database. The credentials are stored in the server's environmental variables.
    '''
    # Heroku
    MONGODB_URL = os.getenv('MONGODB_URL')
    cl = pymongo.MongoClient(MONGODB_URL)
    return cl

    # local tests
    if MONGODB_URL is None:
        with open('connection.txt', 'r') as f:
            MONGODB_URL = f.readlines()[0]

        cl = pymongo.MongoClient(MONGODB_URL)
        return cl

def read_mongo(coll, query=None):
    '''
    Function to read a MongoDB collection as a pandas DataFrame.
    :param coll: a collection.
    :param query: a dict
    '''
    if query is None:
        df = pd.DataFrame(list(coll.find())).reset_index()
    else:
        df = pd.DataFrame(list(coll.find(query))).reset_index()

    return df

def write_mongo(df, collection):
    '''
    Auxiliary function to load pandas DataFrames into our MongoDB cluster.
    '''
    try:
        collection.delete_many({}) # clear previous data
        collection.insert_many(df.to_dict('records')) # add data
    except:
        print('Data loading error')