#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Load ETL scripts from datasets.py to Postgres database

import datasets
import os
import pandas as pd
import pymongo

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
# df_ibge.to_sql('dw_ibge', con=db, if_exists='replace', index=False)
load_mongo(df_ibge, cl.ibge.ibge)

df_quandl = datasets.dw_quandl()
# df_quandl.to_sql('dw_quandl', con=db, if_exists='replace', index=False)
load_mongo(df_quandl, cl.quandl.quandl)

# df_combustiveis = datasets.dw_combustiveis()
# df_combustiveis[0].to_sql('dw_anp', con=db, if_exists='replace', index=False)
# df_combustiveis[1].to_sql('dw_oil', con=db, if_exists='replace', index=False)

df_bacen = datasets.dw_bacen()
# df_bacen[0].to_sql('dw_ptax', con=db, if_exists='replace', index=False)
# df_bacen[1].to_sql('dw_focus', con=db, if_exists='replace', index=False)
load_mongo(df_bacen[0], cl.bacen.ptax)
load_mongo(df_bacen[1], cl.bacen.focus)

# df_cme = datasets.dw_cme()
# df_cme.to_sql('dw_cme', con=db, if_exists='replace', index=False)

# df_scot = datasets.dw_scot()
# df_scot.to_sql('dw_scot', con=db, if_exists='replace', index=False)

# df_china = datasets.dw_china()
# df_china.to_sql('dw_china', con=db, if_exists='replace', index=False)

df_noticias = datasets.dw_noticias()
# df_noticias.to_sql('dw_noticias', con=db, if_exists='replace', index=False)
load_mongo(df_noticias, cl.news.google)

print('Data upload OK!')
