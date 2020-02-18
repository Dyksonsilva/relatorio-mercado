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

# local tests
if DATABASE_URL is None:
    with open('connection.txt', 'r') as f:
        DATABASE_URL = f.readlines()[0]

    db = create_engine(DATABASE_URL, connect_args={'sslmode': 'require'})

db = create_engine(DATABASE_URL)

# layout options
gr_styles = {'height': 400,
             'width': 500,
             'template': 'plotly_white',
             'font': {
                 'family': 'Open Sans'
             }}


def gr_ipca():
    qry = f'SELECT d2n as Indicador, '\
        'd3c as Data, '\
        'value as Valor '\
        'FROM dw_ibge '\
        'WHERE d2n LIKE %(filter)s '\
        'ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%IPCA%'})

    fig = px.line(df, x='Data', y='Valor', color='Indicador')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Variação %',
                      title='Variações do IPCA',
                      **gr_styles)
    return fig


def gr_pimpf():
    qry = f'SELECT d2n as Indicador, '\
        'd3c as Data, '\
        'value as Valor '\
        'FROM dw_ibge '\
        'WHERE d2n LIKE %(filter)s '\
        'ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%IPP%'})

    fig = px.line(df, x='Data', y='Valor', color='Indicador')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Variação %',
                      title='Variações do IPP',
                      **gr_styles)
    return fig


def gr_pmc():
    qry = f'SELECT d2n as Indicador, '\
        'd3c as Data, '\
        'value as Valor '\
        'FROM dw_ibge '\
        'WHERE d2n LIKE %(filter)s '\
        'ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%comércio%'})

    fig = px.line(df, x='Data', y='Valor', color='Indicador')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Variação %',
                      title='Variações dos índices de comércio',
                      **gr_styles)
    return fig


def gr_pms():
    qry = f'SELECT d2n as Indicador, '\
        'd3c as Data, '\
        'value as Valor '\
        'FROM dw_ibge '\
        'WHERE d2n LIKE %(filter)s '\
        'ORDER BY d3c ASC;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%serviços%'})

    fig = px.line(df, x='Data', y='Valor', color='Indicador')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Variação %',
                      title='Variações dos índices de serviços',
                      **gr_styles)
    return fig

# banco central


def gr_focus():
    qry = f'SELECT Data, Indicador, Datareferencia as Projecao, Mediana, Desviopadrao '\
        'FROM dw_focus '\
        'WHERE Indicador LIKE %(filter)s '\
        'ORDER BY Data, Datareferencia;'
    df = pd.read_sql_query(qry, con=db, params={'filter': '%PIB Total%'})

    #df = df.groupby(['Data', 'indicador']).mean().reset_index()

    fig = px.line(df, x='Data', y='Mediana', color='Projecao', error_y='Desviopadrao')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Valor esperado',
                      title='Expectativas de mercado',
                      **gr_styles)
    return fig


def gr_ptax():
    qry = f'SELECT * '\
        'FROM dw_ptax '\
        'WHERE data > %(data)s '\
        'ORDER BY data ASC;'
    df = pd.read_sql_query(qry, con=db, params={'data': '2017-01-01'})

    fig = px.line(df.reset_index(), x='data', y='valor')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='Cotação (R$/1 US$)',
                      title='Dólar PTAX Compra',
                      **gr_styles)

    return fig

# commodities


def gr_comb_intl():
    qry = f'SELECT * '\
        'FROM dw_oil '\
        'ORDER BY date ASC;'
    df = pd.read_sql_query(qry, con=db)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['oil_wti'], name='Barril WTI'))
    fig.add_trace(go.Scatter(
        x=df['date'], y=df['oil_nymex'], name='Barril NYMEX'))
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='US$/barril',
                      title='Cotações internacionais do petróleo',
                      **gr_styles)
    return fig


def gr_comb_nac():
    qry = f'SELECT data_inicial, produto, AVG(preço_médio_revenda) as media '\
        'FROM dw_anp '\
        'GROUP BY data_inicial, produto '\
        'ORDER BY data_inicial ASC;'
    df = pd.read_sql_query(qry, con=db)

    fig = px.line(df, x='data_inicial', y='media', color='produto')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='R$/l, R$/13kg (GLP)',
                      title='Preços médios de revenda',
                      **gr_styles)
    return fig

# TODO: pivot table


def gr_graos():
    qry = f'SELECT index, quandl_wheat, quandl_soybeans, quandl_cotton, quandl_corn, cepea_trigo_parana, cepea_soja '\
    'FROM dw_quandl '\
    'ORDER BY index ASC;'
    df = pd.read_sql_query(qry, con=db)

    df = pd.melt(df, id_vars='data')

    fig = px.line(df, x='data', y='value', color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

# TODO: pivot table


def gr_animais():
    qry = f'SELECT index, cepea_bezerro, cepea_porco '\
        'FROM dw_quandl '\
        'ORDER BY index ASC;'
    df = pd.read_sql_query(qry, con=db)
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='data', y='value', color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

# TODO: pivot table


def gr_metais():
    qry = f'SELECT index, quandl_steel_china, quandl_steel_us '\
        'FROM dw_quandl '\
        'ORDER BY index ASC;'
    df = pd.read_sql_query(qry, con=db)
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='data', y='value',
                  color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig


def gr_gasnat():
    qry = f'SELECT index, quandl_nat_gas_us, quandl_nat_gas_uk '\
        'FROM dw_quandl '\
        'ORDER BY index ASC;'
    df = pd.read_sql_query(qry, con=db)

    df = pd.melt(df, id_vars='data')

    fig = px.line(df, x='data', y='value',
                  color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig
