#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Plotly interactive charts

# inflação

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# Heroku
DATABASE_URL = os.getenv('DATABASE_URL')
db = create_engine(DATABASE_URL)

# local tests
if DATABASE_URL is None:
    with open('connection.txt', 'r') as f:
        DATABASE_URL = f.readlines()[0]

    db = create_engine(DATABASE_URL, connect_args={'sslmode': 'require'})


def gr_ipca():
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter':'%IPCA%'})

    fig = px.line(df, x='d3c', y='value', color='d2n')
    fig.update_layout(template='plotly_white')
    return fig


def gr_pimpf(df):
    df = df.loc[df.D2N ==
                'IPP - Variação mês/mesmo mês do ano anterior (M/M-12)']
    df = df.loc[df.D4N.str.contains(r'Indústria Geral', regex=False)]
    df = df.groupby(['D3C', 'D4N']).mean().reset_index().copy()

    fig = px.line(df, x='D3C', y='V', color='D4N')
    fig.update_layout(template='plotly_white')
    return fig


def gr_pmc(df):
    df = df.loc[df.D2N ==
                'Índice de volume de vendas no comércio varejista ampliado']
    df = df.groupby(['D3C', 'D5N']).mean().reset_index().copy()

    fig = px.line(df, x='D3C', y='V', color='D5N')
    fig.update_layout(template='plotly_white')
    return fig


def gr_pms(df):
    df = df.loc[df.D2N == 'Índice de volume de serviços']
    df = df.groupby(['D3C', 'D1N']).mean().reset_index().copy()

    fig = px.line(df, x='D3C', y='V', color='D1N')
    fig.update_layout(template='plotly_white')
    return fig

# banco central


def gr_focus(df):
    df = df.groupby(['Data', 'Indicador']).mean().reset_index()

    fig = px.line(df, x='Data', y='Mediana', color='Indicador')
    fig.update_layout(template='plotly_white')
    return fig


def gr_ptax(df):
    df = df[df.data > '2017-01-01']

    fig = px.line(df.sort_values(by='data'), x='data', y='valor')
    fig.update_layout(template='plotly_white')
    return fig

# commodities


def gr_comb_intl(df):
    df = df[1].sort_index()
    fig = go.Figure()
    fig.update_layout(template='plotly_white')
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Oil WTI'], name='Oil WTI'))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Oil NYMEX'], name='Oil NYMEX'))
    return fig


def gr_graos(df):
    df = df[['Quandl Wheat', 'Quandl Soybeans',
             'Quandl Cotton', 'Quandl Corn', 'CEPEA Trigo Parana', 'CEPEA Soja']]
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable')
    fig.update_layout(template='plotly_white', title='.')
    return fig


def gr_animais(df):
    df = df[['CEPEA Bezerro', 'CEPEA Porco']]
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable')
    fig.update_layout(template='plotly_white', title='.')
    return fig


def gr_metais(df):
    df = df[['Quandl Steel China',
             'Quandl Steel US', 'Quandl Zinc China']]
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df.dropna(), x='index', y='value', color='variable')
    fig.update_layout(template='plotly_white')
    return fig


def gr_gasnat(df):
    df = df[['Quandl Nat Gas US', 'Quandl Nat Gas UK']]
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable')
    fig.update_layout(template='plotly_white')
    return fig
