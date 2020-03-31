#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Load ETL scripts from datasets.py to Postgres database

import datasets
from db_interface import db_connect, write_mongo

# establish connection
cl = db_connect()

# load into database
# client.database.collection

df_ibge = datasets.dw_ibge()
df_quandl = datasets.dw_quandl()
df_combustiveis = datasets.dw_anp()
df_bacen = datasets.dw_bacen()
df_cme = datasets.dw_cme()
df_scot = datasets.dw_scot()
df_china = datasets.dw_china()
df_noticias = datasets.dw_noticias()

print('Data upload init')
try:
    write_mongo(df_noticias, cl.news.google)
    write_mongo(df_ibge, cl.ibge.ibge)
    write_mongo(df_quandl, cl.quandl.quandl)
    write_mongo(df_bacen[0], cl.bacen.ptax)
    write_mongo(df_bacen[1], cl.bacen.focus)
    write_mongo(df_cme, cl.cme.settle)
    write_mongo(df_scot, cl.prices.scot)
    write_mongo(df_china, cl.prices.china)
    write_mongo(df_combustiveis[0], cl.prices.anp)
    write_mongo(df_combustiveis[1], cl.prices.oil)
except:
    print('Data upload error')
    pass
finally:
    print('Data upload end')
