#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Market report dashboard for supply chain at SLC Agrícola S. A.

import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import texts
from db_interface import db_connect, read_mongo

# app declaration
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server

# establish database connection
cl = db_connect()

# static graphs ===============================================================


def gr_ptax():
    df = read_mongo(cl.bacen.ptax, {})

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
    df = read_mongo(cl.prices.oil, {})

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
    df = read_mongo(cl.quandl.quandl, {
                    'index': 1, 'quandl_corn': 1,  'quandl_cotton': 1,  'quandl_soybeans': 1})
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='data', y='value', color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

# TODO: pivot table


def gr_animais():
    df = read_mongo(cl.quandl.quandl, {
                    'index': 1, 'cepea_bezerro': 1,  'cepea_porco': 1})
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='data', y='value', color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

# TODO: pivot table


def gr_metais():
    df = read_mongo(cl.quandl.quandl, {
                    'index': 1, 'quandl_steel_china': 1,  'quandl_steel_us': 1})
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='data', y='value',
                  color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig


def gr_gasnat():
    df = read_mongo(cl.quandl.quandl, {
                    'index': 1, 'quandl_nat_gas_us': 1,  'quandl_nat_gas_uk': 1})
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='data', y='value',
                  color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig


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
                    id='drop-ipca-filt',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find(
                        {'d2n': {'$regex': 'IPCA'}}).distinct('d2n')],
                    value='IPCA15 - Variação acumulada em 12 meses',
                    clearable=False
                ),
                dcc.Dropdown(
                    id='drop-ipca-grupo',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find(
                        {'d2n': {'$regex': 'IPCA'}}).distinct('d4n')],
                    value=['Índice geral'],
                    multi=True,
                    clearable=False
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
            dcc.Graph(id='gr-pmc')
        ]),
    ]),
    # Dados de serviços
    html.H2('Serviços'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.pms),
        ]),
        dbc.Col([
            dcc.Graph(id='gr-pms')
        ]),
    ]),
    # Preços ao produtor
    html.H2('Produção'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.pimpf),
        ]),
        dbc.Col([
            dcc.Graph(id='gr-pimpf')
        ])
    ]),
    # Construção civil
    html.H2('Construção civil'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.constr),
        ]),
        dbc.Col([
            # dcc.Graph(id='gr-sinapi')
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
                dcc.Dropdown(
                    id='drop-focus-filt',
                    options=[{'label': i, 'value': i}
                             for i in cl.bacen.focus.distinct('indicador')],
                    value='PIB Total',
                    clearable=False
                ),
                dcc.Graph(id='gr-focus')
            ])
            ]),
    # Dólar PTAX
    html.H2('Dólar'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.ptax),
        ]),
        dbc.Col([
            # dcc.Graph(figure=gr_ptax())
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
    className='mt-4'
)

app.layout = html.Div([navbar, body])

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
    [Input('drop-ipca-filt', 'value'),
     Input('drop-ipca-grupo', 'value')])
def gr_ipca(filt, grupo):
    df = read_mongo(
        cl.ibge.ibge, {'d2n': {'$regex': str(filt)}})
    df = df[df['d4n'].isin(list(grupo))]

    # format database for plotting
    df = df[['d3c', 'd4n', 'd1n', 'v']].groupby(
        ['d3c', 'd4n']).mean().reset_index()

    fig = px.line(df, x='d3c', y='v', color='d4n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações do IPCA',
                      **gr_styles)
    return fig


@app.callback(
    Output('gr-pimpf', 'figure'),
    [Input('drop-pimpf-filt', 'value'),
     Input('drop-pimpf-grupo', 'value')])
def gr_pimpf(filt, grupo):
    df = read_mongo(
        cl.ibge.ibge, {'d2n': {'$regex': str(filt)}})
    df = df[df['d4n'].isin(list(grupo))]

    # format database for plotting
    df = df[['d3c', 'd4n', 'd1n', 'v']].groupby(
        ['d3c', 'd4n']).mean().reset_index()

    fig = px.line(df, x='d3c', y='v', color='d4n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações do IPCA',
                      **gr_styles)
    return fig


@app.callback(
    Output('gr-pmc', 'figure'),
    [Input('drop-pmc-filt', 'value'),
     Input('drop-pmc-grupo', 'value')])
def gr_pmc(filt, grupo):
    df = read_mongo(
        cl.ibge.ibge, {'d2n': {'$regex': str(filt)}})
    df = df[df['d4n'].isin(list(grupo))]

    # format database for plotting
    df = df[['d3c', 'd4n', 'd1n', 'v']].groupby(
        ['d3c', 'd4n']).mean().reset_index()

    fig = px.line(df, x='d3c', y='v', color='d4n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações do IPCA',
                      **gr_styles)
    return fig


@app.callback(
    Output('gr-pms', 'figure'),
    [Input('drop-pms-filt', 'value'),
     Input('drop-pms-grupo', 'value')])
def gr_pms(filt, grupo):
    df = read_mongo(
        cl.ibge.ibge, {'d2n': {'$regex': str(filt)}})
    df = df[df['d4n'].isin(list(grupo))]

    # format database for plotting
    df = df[['d3c', 'd4n', 'd1n', 'v']].groupby(
        ['d3c', 'd4n']).mean().reset_index()

    fig = px.line(df, x='d3c', y='v', color='d4n')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Variação %',
                      title='Variações do IPCA',
                      **gr_styles)
    return fig


# banco central

@app.callback(
    Output('gr-focus', 'figure'),
    [Input('drop-focus-filt', 'value')])
def gr_focus(filt):
    df = read_mongo(cl.bacen.focus, {'indicador': {'$regex': str(filt)}})

    fig = px.line(df, x='data', y='mediana',
                  color='datareferencia', error_y='desviopadrao')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='valor esperado',
                      title='Expectativas de mercado',
                      **gr_styles)
    return fig


print('Loading OK!')

if __name__ == "__main__":
    app.run_server(debug=True)
