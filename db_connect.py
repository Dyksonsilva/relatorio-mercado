#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Establish connection to MongoDB database

import os
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