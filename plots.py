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
             'width': 500,
             'template': 'plotly_white'}


def gr_ipca():
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%IPCA%'})

    fig = px.line(df, x='d3c', y='value', color='d2n', **gr_styles)
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Variação %',
                      title='Variações do IPCA')
    return fig


def gr_pimpf():
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%IPP%'})

    fig = px.line(df, x='d3c', y='value', color='d2n', **gr_styles)
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Variação %',
                      title='Variações do IPP')
    return fig


def gr_pmc():
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%comércio%'})

    fig = px.line(df, x='d3c', y='value', color='d2n', **gr_styles)
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Variação %',
                      title='Variações dos índices de comércio')
    return fig


def gr_pms():
    qry = f'SELECT * FROM dw_ibge WHERE d2n LIKE %(filter)s ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%serviços%'})

    fig = px.line(df, x='d3c', y='value', color='d2n', **gr_styles)
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Variação %',
                      title='Variações dos índices de serviços')
    return fig

# banco central


def gr_focus():
    qry = f'SELECT * FROM dw_focus;'
    df = pd.read_sql_query(qry, con=db)

    df = df.groupby(['data', 'indicador']).mean().reset_index()

    fig = px.line(df, x='data', y='mediana', color='indicador', **gr_styles)
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Valor esperado',
                      title='Expectativas de mercado')
    return fig


def gr_ptax():
    qry = f'SELECT * FROM dw_ptax WHERE data > %(data)s;'
    df = pd.read_sql_query(qry, con=db, params={'data': '2017-01-01'})

    fig = px.line(df, x='data', y='valor', **gr_styles)
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Cotação (R$/1 US$)',
                      title='Dólar PTAX Compra')

    return fig

# commodities


def gr_comb_intl():
    qry = f'SELECT * FROM dw_oil;'
    df = pd.read_sql_query(qry, con=db)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['oil_wti'], name='Barril WTI'))
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['oil_nymex'], name='Barril NYMEX'))
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='US$/barril',
                      title='Cotações internacionais do petróleo')
    return fig

def gr_comb_nac():
    qry = f'SELECT data_inicial, produto, AVG(preço_médio_revenda) as media FROM dw_anp GROUP BY data_inicial, produto ORDER BY data_inicial ASC;'
    df = pd.read_sql_query(qry, con=db)

    fig = px.line(df, x='data_inicial', y='media', color='produto', **gr_styles)
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='R$/l, R$/13kg (GLP)',
                      title='Preços médios de revenda')
    return fig


def gr_graos():
    qry = f'SELECT index, quandl_wheat, quandl_soybeans,quandl_cotton, quandl_corn, cepea_trigo_parana, cepea_soja FROM dw_quandl;'
    df = pd.read_sql_query(qry, con=db)

    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable', **gr_styles)
    fig.update_layout(title='.', showlegend=False)
    return fig


def gr_animais():
    qry = f'SELECT index, cepea_bezerro, cepea_porco FROM dw_quandl;'
    df = pd.read_sql_query(qry, con=db)
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable', **gr_styles)
    fig.update_layout(title='.', showlegend=False)
    return fig


def gr_metais():
    qry = f'SELECT index, quandl_steel_china, quandl_steel_us, quandl_zinc_china FROM dw_quandl;'
    df = pd.read_sql_query(qry, con=db)
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df.dropna(), x='index', y='value',
                  color='variable', **gr_styles)
    fig.update_layout(showlegend=False)
    return fig


def gr_gasnat():
    df = f'SELECT index, quandl_nat_gas_us, quandl_nat_gas_uk FROM dw_quandl;'
    df = pd.melt(df.reset_index(), id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable', **gr_styles)
    fig.update_layout(showlegend=False)
    return fig
