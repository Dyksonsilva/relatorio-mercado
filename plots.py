#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Plotly interactive charts

# inflação

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash_app import app
from dash.dependencies import Input, Output
from db_interface import db_connect, read_mongo

# establish connection
cl = db_connect()

# layout options
gr_styles = {'height': 400,
             'width': 500,
             'template': 'plotly_white',
             'font': {
                 'family': 'Open Sans'
             }}


@app.callback(
    Output('plots-ipca','figure'),
    Input('dropdown-ipca','value'))
def gr_ipca(filt):
    df = read_mongo(cl.ibge.ibge, {'d2n': filt})

    fig = px.line(df, x='d3c', y='value', color='d2n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações do IPCA',
                      **gr_styles)
    return fig


def gr_pimpf():
    df = read_mongo(cl.ibge.ibge, {'d2n': {'$regex': 'IPP'}})

    fig = px.line(df, x='d3c', y='value', color='d2n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações do IPP',
                      **gr_styles)
    return fig


def gr_pmc():
    df = read_mongo(cl.ibge.ibge, {'d2n': {'$regex': 'comércio'}})

    fig = px.line(df, x='d3c', y='value', color='d2n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações dos índices de comércio',
                      **gr_styles)
    return fig


def gr_pms():
    df = read_mongo(cl.ibge.ibge, {'d2n': {'$regex': 'serviços'}})

    fig = px.line(df, x='d3c', y='value', color='d2n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações dos índices de serviços',
                      **gr_styles)
    return fig

# banco central


def gr_focus():
    df = read_mongo(cl.bacen.focus, {'indicador': {'$regex': 'PIB Total'}})

    fig = px.line(df, x='data', y='mediana', color='projecao', error_y='desviopadrao')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='valor esperado',
                      title='Expectativas de mercado',
                      **gr_styles)
    return fig


def gr_ptax():
    df = read_mongo(cl.bacen.ptax)

    fig = px.line(df[df.data>'2010-01-01'].reset_index(), x='data', y='valor')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
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
                      xaxis_title='data',
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
                      xaxis_title='data',
                      yaxis_title='R$/l, R$/13kg (GLP)',
                      title='Preços médios de revenda',
                      **gr_styles)
    return fig

# TODO: pivot table


def gr_graos():
    qry = f'SELECT index as data, quandl_wheat, quandl_soybeans, quandl_cotton, quandl_corn, cepea_trigo_parana, cepea_soja '\
    'FROM dw_quandl '\
    'ORDER BY data ASC;'
    df = pd.read_sql_query(qry, con=db)

    df = pd.melt(df, id_vars='data')

    fig = px.line(df, x='data', y='value', color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

# TODO: pivot table


def gr_animais():
    qry = f'SELECT index as data, cepea_bezerro, cepea_porco '\
        'FROM dw_quandl '\
        'ORDER BY data ASC;'
    df = pd.read_sql_query(qry, con=db)
    df = pd.melt(df, id_vars='data')

    fig = px.line(df, x='data', y='value', color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

# TODO: pivot table


def gr_metais():
    qry = f'SELECT index as data, quandl_steel_china, quandl_steel_us '\
        'FROM dw_quandl '\
        'ORDER BY data ASC;'
    df = pd.read_sql_query(qry, con=db)
    df = pd.melt(df, id_vars='data')

    fig = px.line(df, x='data', y='value',
                  color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig


def gr_gasnat():
    qry = f'SELECT index as data, quandl_nat_gas_us, quandl_nat_gas_uk '\
        'FROM dw_quandl '\
        'ORDER BY data ASC;'
    df = pd.read_sql_query(qry, con=db)

    df = pd.melt(df, id_vars='data')

    fig = px.line(df, x='data', y='value',
                  color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

print('Plots loaded!')
