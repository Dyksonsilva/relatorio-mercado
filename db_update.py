#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Load ETL scripts from datasets.py to Postgres database

import datasets
import os
import pandas as pd
import pymongo
from db_connect import db_connect

# establish connection
cl = db_connect()

def load_mongo(df, collection):
    '''
    Auxiliary function to load pandas DataFrames into our MongoDB cluster.
    '''
    try:
        collection.insert_many(df.to_dict('records'))
    except:
        print('Data loading error')

# load into database
# client.database.collection

df_ibge = datasets.dw_ibge()
load_mongo(df_ibge, cl.ibge.ibge)

df_quandl = datasets.dw_quandl()
load_mongo(df_quandl, cl.quandl.quandl)

df_combustiveis = datasets.dw_combustiveis()
load_mongo(df_combustiveis[0], cl.prices.anp)
load_mongo(df_combustiveis[1], cl.prices.oil)

df_bacen = datasets.dw_bacen()
load_mongo(df_bacen[0], cl.bacen.ptax)
load_mongo(df_bacen[1], cl.bacen.focus)

df_cme = datasets.dw_cme()
load_mongo(df_cme, cl.cme.settle)

df_scot = datasets.dw_scot()
load_mongo(df_scot, cl.prices.scot)

df_china = datasets.dw_china()
load_mongo(df_china, cl.prices.china)

df_noticias = datasets.dw_noticias()
load_mongo(df_noticias, cl.news.google)

print('Data upload OK!')
