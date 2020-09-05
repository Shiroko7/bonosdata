# Operaciones con fechas
from datetime import date, timedelta, datetime, time
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from pandas.tseries.offsets import BDay
# Descargar de la web
import urllib.request
from urllib.request import urlopen, Request

# Para leer tablas: excel,csv,html
import pandas as pd
import numpy as np
#import xlrd
#import os

# graficos
import plotly
import plotly.graph_objects as go


# IRF


def usdclp_fx():
    req = Request('https://www.investing.com/currencies/usd-clp-historical-data',
                  headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()

    usdclp = pd.read_html(html)[0]

    usdclp['Date'] = pd.to_datetime(usdclp['Date'], format='%b %d, %Y')

    return usdclp


def montos_time_series(df, start_date, end_date, moneda):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    mask = (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)
    df = df.loc[mask]

    df = df[df['Familia'] != 'LH']

    if moneda == "CLP":
        df = df[df['Reaj'] == '$']
    elif moneda == "UF":
        df = df[df['Reaj'] == 'UF']

    emisores = ['BT', 'BE']  # df['Familia'].unique()

    df = df.groupby(['Familia', 'Fecha'])['Monto'].sum().reset_index()

    df_total = df.groupby(['Fecha'])['Monto'].sum().reset_index()

# .rolling(window).mean().loc[window:]
    fig = go.Figure()
    for emisor in emisores:
        df_emi = df[df['Familia'] == emisor].reset_index()
        emi_monto = df_emi['Monto'] / df_total['Monto'] * 100

        fig.add_trace(go.Scatter(
            x=df[df['Familia'] == emisor]['Fecha'], y=emi_monto, name=emisor))

    # formatear fecha
    start_date = start_date.strftime('%d %B %Y')
    end_date = end_date.strftime('%d %B %Y')

    fig.update_layout(yaxis=dict(ticksuffix="%", range=[
                      0, 100]), title='Porcentaje de Montos Operados por Moneda: '+moneda)

    return fig


def clp_to_fxdiv01(row, usdclp):

    fx = usdclp[usdclp['Fecha'] == row['Fecha']]['Precio']
    if fx is not None and len(fx) != 0:
        return 0.0001 * row['Duration'] * row['Monto'] / fx.squeeze()
    else:
        return 0.0001 * row['Duration'] * row['Monto'] / 820


def fx_dv01_series(df, usdclp, start_date, end_date, moneda):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    mask = (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)
    df = df.loc[mask]

    df = df[df['Familia'] != 'LH']

    df = df[~df['Instrumento'].str.match('BR')]

    if moneda == "CLP":
        df = df[df['Reaj'] == '$']
    elif moneda == "UF":
        df = df[df['Reaj'] == 'UF']

    df['fx dv01'] = df.apply(lambda row: clp_to_fxdiv01(row, usdclp), axis=1)

    df = df.groupby(['Fecha', 'Familia'])['fx dv01'].sum().reset_index()

    familias = df['Familia'].unique()

    fig = go.Figure()
    for familia in familias:
        df_mone = df[df['Familia'] == familia].reset_index()

        fig.add_trace(go.Scatter(
            x=df_mone['Fecha'], y=df_mone['fx dv01'], name=familia))

    # formatear fecha
    #start_date = start_date.strftime('%d %B %Y')
    #end_date = end_date.strftime('%d %B %Y')

    fig.update_layout(title='DV01 diario por familia y reajuste ' + moneda)

    return fig

# intento 1


def fx_dv01_series_bonos(df, usdclp, start_date, end_date, moneda, bonos, porcentaje=False):
    # solo para BT
    df = df[df['Familia'] == 'BT']
    # date filter
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df.loc[:, 'Fecha'] = pd.to_datetime(df['Fecha'])
    mask = (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)
    df = df.loc[mask]

    # quitar bonos que parten con BR
    df = df[~df['Instrumento'].str.match('BR')]

    # currency filter
    if moneda == "CLP":
        df = df[df['Reaj'] == '$']
        df = df[df['Instrumento'].str.match('BTP')]
    elif moneda == "UF":
        df = df[df['Reaj'] == 'UF']
        df = df[df['Instrumento'].str.match('BTU')]

    # bono filter
    ###df = df[df['Instrumento'].isin(bonos)]

    df['fx dv01'] = df.apply(lambda row: clp_to_fxdiv01(row, usdclp), axis=1)

    df = df.groupby(['Fecha', 'Instrumento'])['fx dv01'].sum().reset_index()

    bonos = df['Instrumento'].unique()

    fig = go.Figure()
    count = 0
    if porcentaje:
        df_total = df.groupby(['Fecha'])['fx dv01'].sum().reset_index()

        for bono in bonos:
            df_mone = df[df['Instrumento'] == bono].reset_index()
            dates_mask = df_mone['Fecha'].unique()
            df_total_masked = df_total[df_total['Fecha'].isin(
                dates_mask)].reset_index()
            df_mone['fx dv01'] = df_mone['fx dv01'] / \
                df_total_masked['fx dv01'] * 100
            if count > 4 or count < 1:
                fig.add_trace(go.Scatter(
                    x=df_mone['Fecha'], y=df_mone['fx dv01'], name=bono, visible='legendonly'))
            else:
                fig.add_trace(go.Scatter(
                    x=df_mone['Fecha'], y=df_mone['fx dv01'], name=bono))
            count = count + 1
    else:
        for bono in bonos:
            df_mone = df[df['Instrumento'] == bono].reset_index()
            if count > 4 or count < 1:
                fig.add_trace(go.Scatter(
                    x=df_mone['Fecha'], y=df_mone['fx dv01'], name=bono, visible='legendonly'))
            else:
                fig.add_trace(go.Scatter(
                    x=df_mone['Fecha'], y=df_mone['fx dv01'], name=bono))
            count = count + 1

    # formatear fecha
    #start_date = start_date.strftime('%d %B %Y')
    #end_date = end_date.strftime('%d %B %Y')
    if porcentaje:
        fig.update_layout(yaxis=dict(ticksuffix="%", range=[
                          0, 100], title='DV01'), title=' Porcentaje de participación DV01 diario por bono: ' + moneda)
    else:
        fig.update_layout(yaxis=dict(title='DV01'),
                          title='DV01 diario por bono: ' + moneda)

    return fig

# porcentaje de participación por reajuste


def fx_dv01_participacion_reajuste(df, usdclp, start_date, end_date):
    # solo para BT
    df = df[df['Familia'] == 'BT']
    # date filter
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df.loc[:, 'Fecha'] = pd.to_datetime(df['Fecha'])
    mask = (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)
    df = df.loc[mask]

    df = df[~df['Instrumento'].str.match('BR')]

    df['fx dv01'] = df.apply(lambda row: clp_to_fxdiv01(row, usdclp), axis=1)

    df = df.groupby(['Fecha', 'Reaj'])['fx dv01'].sum().reset_index()

    df_total = df.groupby(['Fecha'])['fx dv01'].sum().reset_index()

    fig = go.Figure()
    # CLP
    df_mone = df[df['Reaj'] == '$'].reset_index()
    if not df_mone.empty:
        dates_mask = df_mone['Fecha'].unique()
        df_total_masked = df_total[df_total['Fecha'].isin(
            dates_mask)].reset_index()
        df_mone['fx dv01'] = df_mone['fx dv01'] / \
            df_total_masked['fx dv01'] * 100

        fig.add_trace(go.Scatter(
            x=df_mone['Fecha'], y=df_mone['fx dv01'], name='CLP'))
    # UF
    df_mone = df[df['Reaj'] == 'UF'].reset_index()
    if not df_mone.empty:
        dates_mask = df_mone['Fecha'].unique()
        df_total_masked = df_total[df_total['Fecha'].isin(
            dates_mask)].reset_index()
        df_mone['fx dv01'] = df_mone['fx dv01'] / \
            df_total_masked['fx dv01'] * 100

        fig.add_trace(go.Scatter(
            x=df_mone['Fecha'], y=df_mone['fx dv01'], name='UF'))

    fig.update_layout(yaxis=dict(ticksuffix="%", range=[
                      0, 100], title='DV01'), title='Participación DV01 diario por reajuste')

    return fig


def bar_bonos(df, usdclp, start_date, end_date, moneda, bonos, acumulado):
    # solo para BT
    df = df[df['Familia'] == 'BT']
    # date filter
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df.loc['Fecha'] = pd.to_datetime(df['Fecha'])
    mask = (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)
    df = df.loc[mask]

    # quitar bonos que parten con BR
    df = df[~df['Instrumento'].str.match('BR')]

    # currency filter
    if moneda == "CLP":
        df = df[df['Reaj'] == '$']
        df = df[df['Instrumento'].str.match('BTP')]
    elif moneda == "UF":
        df = df[df['Reaj'] == 'UF']
        df = df[df['Instrumento'].str.match('BTU')]

    # bono filter
    ###df = df[df['Instrumento'].isin(bonos)]
    df['fx dv01'] = df.apply(lambda row: clp_to_fxdiv01(row, usdclp), axis=1)

    df = df[['Instrumento', 'fx dv01']].reset_index(drop=True)
    bonos = df['Instrumento'].unique()
    x_ = list()
    y_ = list()

    for bono in bonos:
        x_.append(bono)
        value = df[df['Instrumento'] == bono]['fx dv01'].sum()
        if not isinstance(value, np.float64):
            if type(value) is float:
                value = np.float64(value)
            else:
                value = value.sum()
        y_.append(value)

    if not acumulado:
        days = np.busday_count(start_date.date(), end_date.date())
        y_ = y_ / days
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_, y=y_))

    if acumulado:
        fig.update_layout(yaxis=dict(title='DV01'),
                          title=' Acumulado de DV01 diario por bono: ' + moneda)
    else:
        fig.update_layout(yaxis=dict(title='DV01'),
                          title='Promedio de DV01 por bono: ' + moneda)
    return fig
