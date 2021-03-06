#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Market report dashboard for supply chain at SLC Agrícola S. A.

import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import texts
import external
from db_interface import db_connect, read_mongo

# application declaration
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
application = app.server

# establish database connection
cl = db_connect()

# static graphs ===============================================================
# layout options
gr_styles = {'height': 400,
             'width': 500,
             'template': 'plotly_white',
             'font': {
                 'family': 'Open Sans'
             }}


def gr_ptax():
    df = read_mongo(cl.bacen.ptax)
    #df['data'] = pd.to_datetime(df['data'])

    fig = px.line(df,
                  x='data', y='valor', labels={'data': 'Data', 'valor': 'Valor'})
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='Cotação (R$/1 US$)',
                      title='Dólar PTAX Compra',
                      **gr_styles)

    return fig

# commodities


def gr_comb_intl():
    df = read_mongo(cl.prices.oil)

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

# TODO: pivot table


def gr_graos():
    df = read_mongo(cl.quandl.quandl, projection={
                    '_id': 0, 'index': 1, 'quandl_corn': 1,  'quandl_cotton': 1,  'quandl_soybeans': 1})
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

# TODO: pivot table


def gr_animais():
    df = read_mongo(cl.quandl.quandl, projection={
                    '_id': 0, 'index': 1, 'cepea_bezerro': 1,  'cepea_porco': 1})
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='index', y='value', color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig

# TODO: pivot table


def gr_metais():
    df = read_mongo(cl.quandl.quandl, projection={
                    '_id': 0, 'index': 1, 'quandl_steel_china': 1,  'quandl_steel_us': 1})
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='index', y='value',
                  color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig


def gr_gasnat():
    df = read_mongo(cl.quandl.quandl, projection={
                    '_id': 0, 'index': 1, 'quandl_nat_gas_us': 1,  'quandl_nat_gas_uk': 1})
    df = pd.melt(df, id_vars='index')

    fig = px.line(df, x='index', y='value',
                  color='variable')
    fig.update_layout(showlegend=False, **gr_styles)
    return fig


# layout ======================================================================
# navbar
navbar = dbc.NavbarSimple(
    children=[
        html.Img('assets/slc_white.png', height='40px'),
        dbc.NavItem(dbc.NavLink(
            "Contato", href="mailto:angelo.salton@slcagricola.com.br?subject=Relatório%20de%20Mercado%20Suprimentos")),
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
    # Ticker TradingView
    html.Iframe(srcDoc=external.ticker_tv,
                width='100%', style={'border': '0'}),
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
                dcc.Dropdown(
                    id='drop-pmc-filt',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find(
                        {'d2n': {'$regex': 'comércio'}}).distinct('d2n')],
                    value='Índice de volume de vendas no comércio varejista ampliado',
                    clearable=False
                ),
                dcc.Dropdown(
                    id='drop-pmc-grupo',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find(
                        {'d2n': {'$regex': 'comércio'}}).distinct('d4n')],
                    value=[
                        'Variação mensal (base: igual mês do ano anterior)'],
                    multi=True,
                    clearable=False
                ),
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
                dcc.Dropdown(
                    id='drop-pms-filt',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find(
                        {'d2n': {'$regex': 'serviço'}}).distinct('d2n')],
                    value='Índice de receita nominal de serviços',
                    clearable=False
                ),
                dcc.Dropdown(
                    id='drop-pms-grupo',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find(
                        {'d2n': {'$regex': 'serviço'}}).distinct('d4n')],
                    value=[
                        'Variação mensal (base: igual mês do ano anterior)'],
                    multi=True,
                    clearable=False
                ),
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
                dcc.Dropdown(
                    id='drop-pimpf-filt',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find(
                        {'d2n': {'$regex': 'IPP'}}).distinct('d2n')],
                    value='IPP - Variação mês/mesmo mês do ano anterior (M/M-12)',
                    clearable=False
                ),
                dcc.Dropdown(
                    id='drop-pimpf-grupo',
                    options=[{'label': i, 'value': i} for i in cl.ibge.ibge.find(
                        {'d2n': {'$regex': 'IPP'}}).distinct('d4n')],
                    value=['Indústria Geral'],
                    multi=True,
                    clearable=False
                ),
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
                             for i in cl.bacen.focus.find({'indicadordetalhe': np.nan}).distinct('indicador')],
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
            dcc.Graph(figure=gr_ptax())
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
            dcc.Graph(figure=gr_comb_intl())
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.comb_nac),
        ]),
        dbc.Col([
            html.P('Unidade da federação:'),
            dcc.Dropdown(
                id='drop-anp-uf',
                options=[{'label': i, 'value': i}
                         for i in cl.prices.anp.distinct('estado')],
                value='SAO PAULO',
                clearable=False
            ),
            html.P('Município:'),
            dcc.Dropdown(id='drop-anp-cidade'),
            dcc.Graph(id='gr-anp'),
            dcc.Graph(id='gr-anp-margem')
        ]),
    ]),
    # Grãos
    html.H2('Grãos'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.graos),
        ]),
        dbc.Col([
            dcc.Graph(figure=gr_graos())
        ]),
    ]),
    # Animais
    html.H2('Animais'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.animais),
        ]),
        dbc.Col([
            dcc.Graph(figure=gr_animais())
        ]),
    ]),
    # Metais
    html.H2('Metais'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.metais)
        ]),
        dbc.Col([
            dcc.Graph(figure=gr_metais()),
            html.Img(src='assets/analises/infomet1.png', width='100%')
        ]),
    ]),
    # Gás natural
    html.H2('Gás natural'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(texts.gasnat),
        ]),
        dbc.Col([
            dcc.Graph(figure=gr_gasnat())
        ])
    ]),
    html.H1('Calendário Econômico'),
    html.Iframe(srcDoc=external.calendar_tv, width='100%',
                height='600px', style={'border': '0'}),
    html.Footer([
        dcc.Markdown('Elaboração: [Angelo Salton - Suprimentos SLC Agrícola S.A.](mailto:angelo.salton@slcagricola.com.br?subject=Relatório%20de%20Mercado%20Suprimentos) - Atualizado em {0}'.format(
            datetime.datetime.now().strftime('%d/%m/%Y, %H:%M'))),
    ], style={
        'color': 'white',
        'background-color': 'green'
    })
],
    className='mt-4'
)

app.layout = html.Div([navbar, body])

# plots =======================================================================


@app.callback(
    Output('gr-ipca', 'figure'),
    [Input('drop-ipca-filt', 'value'),
     Input('drop-ipca-grupo', 'value')])
def gr_ipca(filt, grupo):
    df = read_mongo(
        cl.ibge.ibge, query={'d2n': {'$regex': str(filt)}})
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
        cl.ibge.ibge, query={'d2n': {'$regex': str(filt)}})
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
        cl.ibge.ibge, query={'d2n': {'$regex': str(filt)}})
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
    df = read_mongo(cl.bacen.focus, query={'indicador': {
                    '$regex': str(filt)}, 'indicadordetalhe': np.nan})

    fig = px.line(df, x='data', y='mediana',
                  color='datareferencia')
    fig.update_layout(showlegend=False,
                      xaxis_title='data',
                      yaxis_title='valor esperado',
                      title='Expectativas de mercado',
                      **gr_styles)
    return fig

# gráfico combustíveis nacional


@app.callback(
    Output('drop-anp-cidade', 'options'),
    [Input('drop-anp-uf', 'value')])
def drop_anp_cidade(options):
    return [{'label': i, 'value': i} for i in cl.prices.anp.find({'estado': str(options)}).distinct('município')]


@app.callback(
    Output('gr-anp', 'figure'),
    [Input('drop-anp-uf', 'value'),
     Input('drop-anp-cidade', 'value')])
def gr_comb_nac(uf, cidade):

    # match all if no selection
    cidade_sel = cidade if cidade != None else '.'

    df = read_mongo(cl.prices.anp,
                    query={'estado': {'$regex': str(uf)}, 'município': {
                        '$regex': str(cidade_sel)}, 'produto': {'$nin': ['GLP']}},
                    projection={
                        'data_inicial': 1, 'produto': 1, 'estado': 1, 'município': 1, 'preço_médio_revenda': 1})
    df = df.groupby(['data_inicial', 'produto']).mean().reset_index()

    fig = px.line(df, x='data_inicial',
                  y='preço_médio_revenda', color='produto')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='R$/l',
                      title='Preços médios de revenda',
                      **gr_styles)
    return fig


@app.callback(
    Output('gr-anp-margem', 'figure'),
    [Input('drop-anp-uf', 'value'),
     Input('drop-anp-cidade', 'value')])
def gr_comb_nac_margem(uf, cidade):

    # match all if no selection
    cidade_sel = cidade if cidade != None else '.'

    df = read_mongo(cl.prices.anp,
                    query={'estado': {'$regex': str(uf)}, 'município': {
                        '$regex': str(cidade_sel)}, 'produto': {'$nin': ['GLP']}},
                    projection={
                        'data_inicial': 1, 'produto': 1, 'estado': 1, 'município': 1, 'margem_média_revenda': 1})
    df = df.groupby(['data_inicial', 'produto']).mean().reset_index()

    fig = px.line(df, x='data_inicial',
                  y='margem_média_revenda', color='produto')
    fig.update_layout(showlegend=False,
                      xaxis_title='Data',
                      yaxis_title='R$/l',
                      title='Margens médias de revenda',
                      **gr_styles)
    return fig


print('Loading OK!')

if __name__ == "__main__":
    application.run()
