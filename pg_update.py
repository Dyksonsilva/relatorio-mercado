#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Load ETL scripts from datasets.py to Postgres database

import datasets
import os
import pandas as pd
from sqlalchemy import create_engine

# Heroku
DATABASE_URL = os.getenv('DATABASE_URL')
db = create_engine(DATABASE_URL)

# local tests
if DATABASE_URL is None:
    with open('connection.txt', 'r') as f:
        DATABASE_URL = f.readlines()[0]

    db = create_engine(DATABASE_URL, connect_args={'sslmode': 'require'})


# load into database
df_ibge = datasets.dw_ibge()
df_ibge.to_sql('dw_ibge', con=db, if_exists='replace', index=False)

df_quandl = datasets.dw_quandl()
df_quandl.to_sql('dw_quandl', con=db, if_exists='replace', index=False)

df_combustiveis = datasets.dw_combustiveis()
df_combustiveis[0].to_sql('dw_anp', con=db, if_exists='replace', index=False)
df_combustiveis[1].to_sql('dw_oil', con=db, if_exists='replace', index=False)

df_bacen = datasets.dw_bacen()
df_bacen[0].to_sql('dw_ptax', con=db, if_exists='replace', index=False)
df_bacen[1].to_sql('dw_focus', con=db, if_exists='replace', index=False)

df_cme = datasets.dw_cme()
df_cme.to_sql('dw_cme', con=db, if_exists='replace', index=False)

df_scot = datasets.dw_scot()
df_scot.to_sql('dw_scot', con=db, if_exists='replace', index=False)

df_china = datasets.dw_china()
df_china.to_sql('dw_china', con=db, if_exists='replace', index=False)

df_noticias = datasets.dw_noticias()
df_noticias.to_sql('dw_noticias', con=db, if_exists='replace', index=False)

print('Data upload OK!')
