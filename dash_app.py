#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - SLC Agrícola <angelo.salton@slcagricola.com.br>
# Market report dashboard for supply chain at SLC Agrícola S. A.

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import datetime
import plots
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    dcc.Markdown('[Angelo Salton - Suprimentos SLC Agrícola S.A.](mailto:angelo.salton@slcagricola.com.br?subject=Relatório%20de%20Mercado%20Suprimentos) - Atualizado em {0}'.format(datetime.datetime.now().strftime('%d/%m/%Y, %H:%M'))),
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
                dcc.Markdown('Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?')
            ]),
            dbc.Col([
                dcc.Graph(figure=plots.gr_ipca())
            ])
            ]),
    # Dados de comércio
    html.H2('Comércio'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui'),
        ]),
        dbc.Col([
            dcc.Graph(figure=plots.gr_pmc())
        ]),
    ]),
    # Dados de serviços
    html.H2('Serviços'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui'),
        ]),
        dbc.Col([
            dcc.Graph(figure=plots.gr_pms())
        ]),
    ]),
    # Preços ao produtor
    html.H2('Produção'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui'),
        ]),
        dbc.Col([
            dcc.Graph(figure=plots.gr_pimpf())
        ])
    ]),

    # Dados do Banco Central - expectativas de mercado --------------
    html.H1('Expectativas de mercado'),
    html.H2('Relatório Focus'),
    dbc.Row([
            dbc.Col([
                dcc.Markdown('Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?')
            ]),
            dbc.Col([
                dcc.Graph(figure=plots.gr_focus())
            ])
            ]),
    # Dólar PTAX
    html.H2('Dólar'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui'),
        ]),
        dbc.Col([
            dcc.Graph(figure=plots.gr_ptax())
        ]),
    ]),
    # Dados de commodities ------------------------------------------
    html.H1('Commodities'),
    # Combustíveis
    html.H2('Combustíveis'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui'),
        ]),
        dbc.Col([
            dcc.Graph(figure=plots.gr_comb_intl())
        ]),
    ]),
    # Grãos
    html.H2('Grãos'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui'),
        ]),
        dbc.Col([
            # dcc.Graph(figure=plots.gr_graos())
        ]),
    ]),
    # Animais
    html.H2('Animais'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui'),
        ]),
        dbc.Col([
            # dcc.Graph(figure=plots.gr_animais())
        ]),
    ]),
    # Metais
    html.H2('Metais'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui'),
        ]),
        dbc.Col([
            # dcc.Graph(figure=plots.gr_metais())
        ]),
    ]),
    # Gás natural
    html.H2('Gás natural'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui texto aqui'),
        ]),
        dbc.Col([
            dcc.Graph(figure=plots.gr_gasnat())
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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server

app.layout = html.Div([navbar, body])

if __name__ == "__main__":
    app.run_server(debug=True)
