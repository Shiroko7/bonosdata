import dash_core_components as dcc
import dash_html_components as html
from plots import percentage_series, interest_series
from api import query_by_daterange
from datetime import date, timedelta, datetime, time
import pandas as pd
import time

start_date = date(2020, 4, 1)
end_date = date(2020, 6, 11)

# dataframes
usdclp = query_by_daterange("usdclp", start_date, end_date)
df_iif = query_by_daterange("iif", start_date, end_date)

percent_series = percentage_series(df_iif, usdclp, start_date, end_date)
int_series = interest_series(df_iif, start_date, end_date)


header = html.Div(
    [
        html.Div(
            [
                html.H2('IIF Data',),
                html.H6('Versión Alpha 1.0.0', className='no-print'),
            ], className='twelve columns', style={'text-align': 'center'}
        )
    ], className='row',
)


layout_datos_iif = html.Div([
    header,
    html.Div(
        [
            dcc.Dropdown(
                id="dropdown_ma_rescate",
                options=[
                    {'label': 'CLP', 'value': 'CLP'},
                    {'label': 'UF', 'value': 'UF'},
                    {'label': 'USD', 'value': 'USD'},
                ],
                value='CLP',
                className="dcc_control no-print"
            ),
            dcc.Loading(id="loading-icon_ma_rescate",
                        children=[dcc.Graph(id='ma_rescate')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading-icon_p_series",
                        children=[dcc.Graph(id='p_series', figure=percent_series)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading-icon_f-bonos",
                        children=[dcc.Graph(id='i_series', figure=int_series)], type="circle"),
        ], className='pretty_container'
    ),

])
