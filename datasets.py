#!/usr/bin/env python
# encoding: utf-8
# Angelo Salton - Suprimentos <angelo.salton@slcagricola.com.br>
# Load market data from the web to pandas DataFrames

import re
import os
from ftplib import FTP
import pandas as pd
import requests
from retry import retry
import json
import xmltodict

# load API keys
api_quandl = os.getenv('api_quandl')

# fix column names


def fixnames(col_names):
    out = [item.lower() for item in col_names]
    out = [item.replace(' ', '_') for item in out]
    out = [re.sub('[$\/]', '', item) for item in out]
    return out


@retry(ConnectionError, tries=5, delay=1)
def dw_bacen():
    '''
    Load BACEN data.
    :return: A :class:`pandas.DataFrame`.
    '''
    # Load dict w/ links
    with open('links_dados.json', 'r') as f:
        links = f.read()
        links_f = json.loads(str(links))

    # load PTAX dollar data
    try:
        df_ptax = pd.read_csv(
            links_f['BACEN PTAX'], sep=';', decimal=',', parse_dates=['data'])
    except:
        return None

    df_ptax.columns = fixnames(df_ptax.columns)

    # load FOCUS report data (end of year expectations)
    try:
        df_focus = pd.read_csv(links_f['BACEN FOCUS'], index_col=[
                               'Data'], decimal=',')
    except:
        return None

    # use date as column
    df_focus.reset_index(inplace=True)
    df_focus['Data'] = pd.to_datetime(df_focus['Data'], format='%Y-%m-%d')

    df_focus.columns = fixnames(df_focus.columns)

    # timestamp
    df_ptax['updated'] = pd.to_datetime('now')
    df_focus['updated'] = pd.to_datetime('now')

    return df_ptax, df_focus


@retry(ConnectionError, tries=5, delay=1)
def dw_cme():
    '''
    Load daily CME data.
    :return: A :class:`pandas.DataFrame`.
    '''
    cme_ftp = FTP('ftp.cmegroup.com')
    cme_ftp.login()
    cme_ftp.cwd('/settle')

    # list files
    arq = cme_ftp.nlst()

    # the last 7 days
    padrao = re.compile(r'cbt.settle.2\d*\.s.csv.zip')
    tmp_arq = [i for i in arq if padrao.match(i)]

    # full path
    arq = ['ftp://ftp.cmegroup.com/settle/'+i for i in tmp_arq]

    # load files in DataFrames
    cbot = pd.concat(
        [pd.read_csv(i, parse_dates=['BizDt', 'MatDt', 'LastTrdDt']) for i in arq])

    # commodities and fertilizers curve
    comm = ['ZC', 'ZC2', 'ZC3', 'ZC5', 'ZS', 'ZS1', 'ZS2', 'ZS3', 'ZS5']
    ferts = ['UFV', 'UFU', 'UME', 'UFN', 'DFN', 'UFE', 'UFB', 'DFL', 'MFC']

    lista = comm+ferts
    df_cme = cbot[cbot['Sym'].isin(lista)]

    # return summarized table
    # df_cme = df_cme.groupby(['BizDt', 'Sym', 'MatDt', 'PutCall'])[
    # 'SettlePrice'].max().reset_index()

    # timestamp
    df_cme['updated'] = pd.to_datetime('now')

    df_cme.columns = fixnames(df_cme.columns)

    return df_cme


@retry(ConnectionError, tries=5, delay=1)
def dw_anp():
    '''
    Load fossil fuels data
    :return: A :class:`pandas.DataFrame`.
    '''
    # load dict w/ links
    with open('links_dados.json', 'r') as f:
        links = f.read()
        links_f = json.loads(str(links))

    try:
        df_anp = pd.read_excel(
            links_f['ANP Semanal'], skiprows=12, na_values='-', parse_dates=['DATA INICIAL', 'DATA FINAL'])
    except:
        return None

    # filter regions
    df_anp = df_anp[df_anp.REGIÃO.isin(
        ['NORDESTE', 'CENTRO OESTE', 'SUDESTE'])]

    # return summarized table
    # df_anp = df_anp.groupby(['DATA INICIAL', 'PRODUTO', 'REGIÃO']).agg({
    #     'PREÇO MÉDIO REVENDA': 'mean',
    #     'DESVIO PADRÃO REVENDA': 'mean',
    #     'PREÇO MÍNIMO REVENDA': 'min',
    #     'PREÇO MÁXIMO REVENDA': 'max',
    #     'PREÇO MÉDIO DISTRIBUIÇÃO': 'mean',
    #     'DESVIO PADRÃO DISTRIBUIÇÃO': 'mean',
    #     'PREÇO MÍNIMO DISTRIBUIÇÃO': 'min',
    #     'PREÇO MÁXIMO DISTRIBUIÇÃO': 'max',
    #     'MARGEM MÉDIA REVENDA': 'mean',
    # }
    # ).reset_index()

    df_anp.columns = fixnames(df_anp.columns)

    # Load oil quotes data
    try:
        df_wti = pd.read_csv(links_f['Oil WTI'].format(
            api_quandl), index_col=['Date'])
        df_nym = pd.read_csv(links_f['Oil NYMEX'].format(
            api_quandl), index_col=['Date'])
    except:
        return None

    df_wti.rename(columns={'Settle': 'Oil WTI'}, inplace=True)
    df_nym.rename(columns={'Settle': 'Oil NYMEX'}, inplace=True)

    df_oil = pd.merge(df_wti, df_nym, left_index=True, right_index=True)
    df_oil.reset_index(inplace=True)

    df_oil.columns = fixnames(df_oil.columns)
    df_oil['date'] = pd.to_datetime(df_oil['date'], format='%Y-%m-%d')

    # timestamp
    df_anp['updated'] = pd.to_datetime('now')
    df_oil['updated'] = pd.to_datetime('now')

    return df_anp, df_oil


@retry(ConnectionError, tries=5, delay=1)
def dw_anp_import():

    # load dict w/ links
    with open('links_dados.json', 'r') as f:
        links = f.read()
        links_f = json.loads(str(links))

    url = links_f['ANP PPI']
    xls = pd.ExcelFile(url)

    # sheet 0: Gasolina
    # sheet 1: QAV
    # sheet 2: Diesel
    try:
        df1 = pd.read_excel(xls, sheet_name=0, skiprows=2, usecols='B:R')
        df2 = pd.read_excel(xls, sheet_name=1, skiprows=2, usecols='B:R')
        df3 = pd.read_excel(xls, sheet_name=2, skiprows=2, usecols='B:R')
    except:
        return None

    def prep_data(df, label):
        # data preparation helper function
        df['Data'] = df['Data'].str.slice(stop=10)
        df['Data'] = pd.to_datetime(df['Data'])
        df = df.dropna(subset=['Data'], axis=0)

        df = pd.melt(df, id_vars='Data')
        df['Combustivel'] = label
        return df

    df1 = prep_data(df1, 'Gasolina')
    df2 = prep_data(df2, 'QAV')
    df3 = prep_data(df3, 'Diesel')

    df = pd.concat([df1, df2, df3])
    df.columns = ['Data', 'Local', 'Valor', 'Combustivel']

    df_anp_import = pd.pivot_table(
        df, index=['Data', 'Local'], columns=['Combustivel'])

    # timestamp
    df_anp_import['updated'] = pd.to_datetime('now')

    return df_anp_import


@retry(ConnectionError, tries=5, delay=1)
def dw_comexstat():
    '''
    Load COMEX STAT data (WIP).
    :return: A :class:`pandas.DataFrame`.
    '''
    # Data download
    anos = ['2017', '2018', '2019']
    #caminho = 'G:\\Produção\\Suprimentos\\_Comum\\23 - Gestão de Performance\\3 - Análise de Mercado\\Dados\\COMEX\\'

    # imports
    imp = pd.concat([pd.read_csv(
        'http://www.mdic.gov.br/balanca/bd/comexstat-bd/mun/IMP_'+ano+'_MUN.csv', sep=';') for ano in anos])
    imp.to_csv(caminho+'IMP.csv')

    # exports
    exp = pd.concat([pd.read_csv(
        'http://www.mdic.gov.br/balanca/bd/comexstat-bd/mun/EXP_'+ano+'_MUN.csv', sep=';') for ano in anos])
    exp.to_csv(caminho+'EXP.csv')

    # auxiliary tables
    # tab_aux = urllib.request.urlretrieve(
    #    'http://www.mdic.gov.br/balanca/bd/tabelas/TABELAS_AUXILIARES.xlsx', filename=caminho+'TABELAS_AUXILIARES.xlsx')

    # exporta para csv
    #tabs = pd.read_excel(caminho+'TABELAS_AUXILIARES.xlsx', sheet_name=0)
    #lista_nomes = tabs['Arquivo Referência'].to_list()

    # salva na pasta
    # for indice, tabela in enumerate(lista_nomes, start=1):
    #    pd.read_excel(caminho+'TABELAS_AUXILIARES.xlsx',
    #                  sheet_name=indice).to_csv(caminho+tabela)


@retry(ConnectionError, tries=5, delay=1)
def dw_ibge():
    '''
    Load IBGE data.
    :return: A :class:`pandas.DataFrame`.
    '''
    # load dict w/ links
    with open('links_dados.json', 'r') as f:
        links = f.read()
        links_f = json.loads(str(links))

    # find Quandl data in links dict
    keys_quandl = [key for key, val in links_f.items() if 'IBGE' in key]

    for base in keys_quandl:
        # faz o download dos dados (vem como JSON da API)
        try:
            dt = requests.get(links_f[base])
        except:
            return None

        # carrega de string para json
        tmp = json.loads(dt.content)
        tmp = tmp[1:]

        # agrega à base
        try:
            df_ibge = df_ibge.append(pd.DataFrame(tmp), ignore_index=True)
        except NameError:
            # se não estiver inicializada (primeira iteração)
            df_ibge = pd.DataFrame(tmp)

    # tratamento dos dados
    # formata datas
    df_ibge['V'] = pd.to_numeric(df_ibge['V'], errors='coerce')
    df_ibge['D3C'] = df_ibge['D3C'].apply(
        lambda row: row[:4]+'-'+row[4:6]+'-01')
    df_ibge['D3C'] = pd.to_datetime(df_ibge['D3C'])

    # remove code variables
    df_ibge = df_ibge[['D1N', 'D2N', 'D3C', 'D4N', 'D5N', 'MN', 'NN', 'V']]

    # average observations by location
    # to reduce data size
    # temp = df_ibge.melt(id_vars=['D3C', 'D2N', 'D1N'], value_vars=['V'])
    # df_ibge = temp.groupby(['D3C', 'D2N']).mean().reset_index()

    # timestamp
    df_ibge['updated'] = pd.to_datetime('now')

    df_ibge.columns = fixnames(df_ibge.columns)

    return df_ibge


@retry(ConnectionError, tries=5, delay=1)
def dw_noticias():
    '''
    Load headlines from Google News.
    :return: A :class:`pandas.DataFrame`.
    '''
    # load dict w/ links
    with open('links_dados.json', 'r') as f:
        links = f.read()
        links_f = json.loads(str(links))

    # Google News
    try:
        goog_req = requests.get(links_f['RSS']['Noticias Google Brasil'])
    except:
        return None

    goog_dic = xmltodict.parse(goog_req.content)

    # navigate XML from Google RSS to the items (list of dicts)
    goog_its = goog_dic['rss']['channel']['item']

    # a DataFrame with news
    df_goog = pd.DataFrame(goog_its)

    # extract links from sites
    df_goog['source'] = df_goog['source'].apply(lambda x: x['@url'])

    # adjust dates
    df_goog['pubDate'] = pd.to_datetime(df_goog['pubDate'])
    df_goog['pubDate'] = df_goog.pubDate.dt.tz_convert('America/Sao_Paulo')

    df_goog.columns = fixnames(df_goog.columns)

    # select columns
    df_goog = df_goog[['title', 'link', 'pubdate', 'source']]

    # timestamp
    df_goog['updated'] = pd.to_datetime('now')

    return df_goog


@retry(ConnectionError, tries=5, delay=1)
def dw_quandl():
    '''
    Load Quandl Data.
    :return: A :class:`pandas.DataFrame`.
    '''
    # load dict w/ links
    with open('links_dados.json', 'r') as f:
        links = f.read()
        links_f = json.loads(str(links))

    # find Quandl data in links dict
    keys_quandl = [key for key, val in links_f.items() if 'Quandl' in key]

    # Add CEPEA data
    [keys_quandl.append(key) for key, val in links_f.items() if 'CEPEA' in key]

    # load data in dict of dataframes
    dicc = {}

    for base in keys_quandl:
        # load commodity data
        try:
            tmpdf = pd.read_csv(links_f[base].format(api_quandl))
        except:
            return None

        tmpdf.set_index(['Date'], inplace=True)
        tmpdf.rename(columns={'Settle': str(base),
                              'Price US$': str(base)}, inplace=True)

        dicc_tmp = {str(base): tmpdf}
        dicc.update(dicc_tmp)

    # appends to base
    df_quandl = pd.concat(
        (value for key, value in dicc.items()), axis=1, sort=True)

    # drop unnecessary variables
    cols = df_quandl.columns.str.startswith(('Quandl', 'CEPEA'))
    df_quandl = df_quandl.iloc[:, cols]
    df_quandl.reset_index(inplace=True)

    # timestamp
    df_quandl['updated'] = pd.to_datetime('now')

    df_quandl.columns = fixnames(df_quandl.columns)
    df_quandl['index'] = pd.to_datetime(df_quandl['index'])

    return df_quandl


@retry(ConnectionError, tries=5, delay=1)
def dw_scot():
    """
    Scrape feeder cattle quotes from Scot Consultoria data.
    """
    url = 'https://www.scotconsultoria.com.br/cotacoes/boi-gordo/'

    # load data
    df_scot = pd.read_html(url, skiprows=2, decimal=',',
                           thousands='.', na_values='-')[0]

    # data formatting
    df_scot['Data Obs'] = pd.datetime.now().strftime('%Y-%m-%d')

    # drop footer rows
    df_scot = df_scot.iloc[:32, :]

    df_scot.columns = ['Praça', 'à vista RS/@-Kg', '.', '30 dias R$/@-Kg',
                       '.', 'base', 'à vista com Funrural', '.', '30 dias com Funrural', '.', 'Data Obs']
    df_scot.drop('.', axis=1, inplace=True)

    # set data types
    df_scot_dtypes = {'Praça': 'object',
                      'à vista RS/@-Kg': 'float64',
                      '30 dias R$/@-Kg': 'float64',
                      'base': 'object',
                      'à vista com Funrural': 'float64',
                      '30 dias com Funrural': 'float64',
                      'Data Obs': 'datetime64[ns]'}

    df_scot = df_scot.astype(df_scot_dtypes)

    # timestamp
    df_scot['updated'] = pd.to_datetime('now')

    df_scot.columns = fixnames(df_scot.columns)

    return df_scot


@retry(ConnectionError, tries=5, delay=1)
def dw_china():
    """
    Get China weekly commodity prices.
    """

    # URLs
    urls = {'energy': 'http://www.sunsirs.com/uk/sectors-11.html',
            'chemicals': 'http://www.sunsirs.com/uk/sectors-14.html',
            'rubber': 'http://www.sunsirs.com/uk/sectors-15.html',
            'textile': 'http://www.sunsirs.com/uk/sectors-16.html',
            'metals': 'http://www.sunsirs.com/uk/sectors-12.html',
            'steel': 'http://www.sunsirs.com/uk/sectors-13.html'}

    # read and join datasets
    df_china = pd.concat([pd.read_html(i, header=0)[1]
                          for i in list(urls.values())])
    df_china['Data Obs'] = pd.datetime.now().strftime('%Y-%m-%d')
    df_china.columns = ['Commodity', 'Sectors',
                        'Last week', 'This week', 'Change', 'Data Obs']

    df_china.columns = fixnames(df_china.columns)

    # timestamp
    df_china['updated'] = pd.to_datetime('now')

    return df_china


@retry(ConnectionError, tries=5, delay=1)
def dw_fretes():
    """
    Get inland freights data.
    """

    # ESALQ-Log data
    url_cepea = "https://sifreca.esalq.usp.br/mercado/fertilizantes"
    df_fretes = pd.read_html(url_cepea, decimal=',', thousands='.')[1]

    # join columns
    df_fretes['Origem'] = df_fretes['Origem']+'/'+df_fretes['UF']
    df_fretes['Destino'] = df_fretes['Destino']+'/'+df_fretes['UF.1']

    df_fretes.drop(['UF', 'UF.1'], axis=1, inplace=True)

    # timestamp
    df_fretes['updated'] = pd.to_datetime('now')

    df_fretes.columns = fixnames(df_fretes.columns)

    return df_fretes


@retry(ConnectionError, tries=5, delay=1)
def dw_acobrasil(y='2020', m='02'):
    '''
    Get information from Brazilian steel production data.
    '''

    url = 'https://institutoacobrasil.net.br/site/wp-content/uploads/{0}/{1}/PERFORMANCE-MENSAL_MERCADO.xls'.format(
        y, m)

    try:
        df_aco = pd.read_excel(url, skiprows=6)
    except:
        return None

    # data cleaning
    df_aco.iloc[1, 0] = 'Mês'

    # drop null lines
    inds = df_aco.iloc[:, 0].dropna().index
    df_aco = df_aco.loc[inds]

    # transpose
    df_aco = df_aco.T
    df_aco.columns = df_aco.iloc[0, :]
    df_aco = df_aco.iloc[1:, :]
    df_aco['ESPECIFICAÇÃO'] = df_aco['ESPECIFICAÇÃO'].ffill()
    df_aco['Data'] = df_aco['Mês'].str.lower()+"/"+df_aco['ESPECIFICAÇÃO']

    # select columns
    df_aco = df_aco.iloc[:, 2:]

    # remove remaining nulls
    df_aco.dropna(axis=0, subset=['Data'], inplace=True)
    df_aco.dropna(axis=1, how='all', inplace=True)
    df_aco.reset_index(drop=True, inplace=True)

    # timestamp
    df_aco['updated'] = pd.to_datetime('now')

    return df_aco
