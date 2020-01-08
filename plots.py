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

# layout options
gr_styles = {'height': 400,
             'width': 500}


def gr_ipca():
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%IPCA%'})

    fig = px.line(df, x='d3c', y='value', color='d2n', **gr_styles)
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig


def gr_pimpf(df):
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%IPP%'})

    fig = px.line(df, x='d3c', y='value', color='d2n', **gr_styles)
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig


def gr_pmc(df):
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%comércio%'})

    fig = px.line(df, x='d3c', y='value', color='d2n', **gr_styles)
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig


def gr_pms(df):
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%serviços%'})

    fig = px.line(df, x='d3c', y='value', color='d2n', **gr_styles)
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig

# banco central


def gr_focus(df):
    qry = f'SELECT * FROM dw_focus;'
    df = pd.read_sql_query(qry, con=db)

    df = df.groupby(['data', 'indicador']).mean().reset_index()

    fig = px.line(df, x='data', y='mediana', color='indicador', **gr_styles)
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig


def gr_ptax(df):
    qry = f'SELECT * FROM dw_focus WHERE data > %(data)s;'
    df = pd.read_sql_query(qry, con=db, params={'data': '2017-01-01'})

    fig = px.line(df.sort_values(by='data'), x='data', y='valor', **gr_styles)
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig

# commodities


def gr_comb_intl(df):
    qry = f'SELECT * FROM dw_combustiveis;'
    df = pd.read_sql_query(qry, con=db)

    fig = go.Figure()
    fig.update_layout(template='plotly_white', showlegend=False)
    fig.add_trace(go.Scatter(
        x=df['index'], y=df['oil_wti'], name='Barril WTI'))
    fig.add_trace(go.Scatter(
        x=df['index'], y=df['oil_nymex'], name='Barril NYMEX'))
    return fig


def gr_graos(df):
    qry = f'SELECT index, quandl_wheat, quandl_soybeans,quandl_cotton, quandl_corn, cepea_trigo_parana, cepea_soja FROM dw_quandl;'
    df = pd.read_sql_query(qry, con=db)

    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable', **gr_styles)
    fig.update_layout(template='plotly_white', title='.', showlegend=False)
    return fig


def gr_animais(df):
    qry = f'SELECT index, cepea_bezerro, cepea_porco FROM dw_quandl;'
    df = pd.read_sql_query(qry, con=db)
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable', **gr_styles)
    fig.update_layout(template='plotly_white', title='.', showlegend=False)
    return fig


def gr_metais(df):
    qry = f'SELECT index, quandl_steel_china, quandl_steel_us, quandl_zinc_china FROM dw_quandl;'
    df = pd.read_sql_query(qry, con=db)
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df.dropna(), x='index', y='value', color='variable', **gr_styles)
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig


def gr_gasnat(df):
    df = f'SELECT index, quandl_nat_gas_us, quandl_nat_gas_uk FROM dw_quandl;'
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable', **gr_styles)
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig
