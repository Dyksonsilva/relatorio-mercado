#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Market report dashboard for supply chain at SLC Agrícola S. A.

import datetime
import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import texts
from db_interface import *

# app declaration
app=dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])
server=app.server

# establish database connection
cl = db_connect()

# layout ======================================================================
# navbar
navbar = dbc.NavbarSimple(
    children=[
        html.Img('assets/slc_white.png', height='30px'),
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand="Relatório de Mercado - Suprimentos",
    brand_href="#",
    sticky="top",
    color='green',
    dark=True
)

# structure
body = dbc.Container([
    # Card inicial --------------------------------------------------
    dcc.Markdown('[Angelo Salton - Suprimentos SLC Agrícola S.A.](mailto:angelo.salton@slcagricola.com.br?subject=Relatório%20de%20Mercado%20Suprimentos) - Atualizado em {0}'.format(
        datetime.datetime.now().strftime('%d/%m/%Y, %H:%M'))),
    # Notícias ------------------------------------------------------
    html.H1('Notícias'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('noticias noticias noticias')
        ])
    ]),
    # Dados de inflação do IBGE -------------------------------------
    html.H1('Inflação'),
    html.H2('IPCA'),
    dbc.Row([
            dbc.Col([
                dcc.Markdown(texts.ipca)
            ]),
            dbc.Col([
                dcc.Dropdown(
                    id='drop-ipca',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find({'d2n': {'$regex': 'IPCA'}}).distinct('d2n')],
                    value='Selecione'
                ),
                dcc.Graph(id='gr-ipca')
            ])
            ]),
    # Dados de comércio
    html.H2('Comércio'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.pmc),
        ]),
        dbc.Col([
            # dcc.Graph(figure=gr_pmc())
        ]),
    ]),
    # Dados de serviços
    html.H2('Serviços'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.pms),
        ]),
        dbc.Col([
            # dcc.Graph(figure=gr_pms())
        ]),
    ]),
    # Preços ao produtor
    html.H2('Produção'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.pimpf),
        ]),
        dbc.Col([
            # dcc.Graph(figure=gr_pimpf())
        ])
    ]),
    # Construção civil
    html.H2('Construção civil'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.constr),
        ]),
        dbc.Col([
            # # dcc.Graph(figure=gr_pimpf())
        ])
    ]),

    # Dados do Banco Central - expectativas de mercado --------------
    html.H1('Expectativas de mercado'),
    html.H2('Relatório Focus'),
    dbc.Row([
            dbc.Col([
                dcc.Markdown(texts.focus)
            ]),
            dbc.Col([
                # # dcc.Graph(figure=gr_focus())
            ])
            ]),
    # Dólar PTAX
    html.H2('Dólar'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.ptax),
        ]),
        dbc.Col([
            # # dcc.Graph(figure=gr_ptax())
        ]),
    ]),
    # Dados de commodities ------------------------------------------
    html.H1('Commodities'),
    # Combustíveis
    html.H2('Combustíveis'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.comb_intl),
        ]),
        dbc.Col([
            # # dcc.Graph(figure=gr_comb_intl())
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.comb_nac),
        ]),
        dbc.Col([
            # # dcc.Graph(figure=gr_comb_nac())
        ]),
    ]),
    # Grãos
    html.H2('Grãos'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.graos),
        ]),
        dbc.Col([
            # # dcc.Graph(figure=gr_graos())
        ]),
    ]),
    # Animais
    html.H2('Animais'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.animais),
        ]),
        dbc.Col([
            # # dcc.Graph(figure=gr_animais())
        ]),
    ]),
    # Metais
    html.H2('Metais'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.metais),
        ]),
        dbc.Col([
            # # dcc.Graph(figure=gr_metais())
        ]),
    ]),
    # Gás natural
    html.H2('Gás natural'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.gasnat),
        ]),
        dbc.Col([
            # # dcc.Graph(figure=gr_gasnat())
        ])
    ]),
    html.Footer([
        'aaa'
    ], style={
        'color': 'white',
        'background-color': 'green'
    })
],
    className = 'mt-4'
)

app.layout=html.Div([navbar, body])

# plots =======================================================================
# layout options
gr_styles = {'height': 400,
             'width': 500,
             'template': 'plotly_white',
             'font': {
                 'family': 'Open Sans'
             }}

@app.callback(
    Output('gr-ipca', 'figure'),
    [Input('drop-ipca','value')])
def gr_ipca(filt):
    df = read_mongo(cl.ibge.ibge, {'d2n': {'$regex': str(filt)}})

    fig = px.line(df, x='d3c', y='v', color='d2n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações do IPCA',
                      **gr_styles)
    return fig


def gr_pimpf():
    df = read_mongo(cl.ibge.ibge, {'d2n': {'$regex': 'IPP'}})

    fig = px.line(df, x='d3c', y='v', color='d2n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações do IPP',
                      **gr_styles)
    return fig


def gr_pmc():
    df = read_mongo(cl.ibge.ibge, {'d2n': {'$regex': 'comércio'}})

    fig = px.line(df, x='d3c', y='v', color='d2n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações dos índices de comércio',
                      **gr_styles)
    return fig


def gr_pms():
    df = read_mongo(cl.ibge.ibge, {'d2n': {'$regex': 'serviços'}})

    fig = px.line(df, x='d3c', y='v', color='d2n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações dos índices de serviços',
                      **gr_styles)
    return fig

# banco central


def gr_focus():
    df = read_mongo(cl.bacen.focus, {'indicador': {'$regex': 'PIB Total'}})

    fig = px.line(df, x='data', y='mediana',
                  color='projecao', error_y='desviopadrao')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='valor esperado',
                      title='Expectativas de mercado',
                      **gr_styles)
    return fig


def gr_ptax():
    df = read_mongo(cl.bacen.ptax)

    fig = px.line(df[df.data > '2010-01-01'].reset_index(),
                  x='data', y='valor')
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


print('Loading OK!')

if __name__ == "__main__":
    app.run_server(debug = True)
