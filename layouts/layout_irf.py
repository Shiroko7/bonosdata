import dash_core_components as dcc
import dash_html_components as html
import plots
from api import query_by_daterange
from datetime import date, timedelta, datetime, time
from plots import fx_dv01_participacion_reajuste

import time


start_date = date(2020, 3, 1)
end_date = date(2020, 6, 11)

#t0 = time.time()
df_irf = query_by_daterange('irf', start_date, end_date)
#t1 = time.time()
#print('elapsed time:', t1-t0)

usdclp = query_by_daterange("usdclp", start_date, end_date)


fig_reaj = fx_dv01_participacion_reajuste(df_irf, usdclp, start_date, end_date)


# dataframes

header = html.Div(
    [
        html.Div(
            [
                html.H2('IRF Data',),
                html.H6('Versión Alpha 1.0.0', className='no-print'),
            ], className='twelve columns', style={'text-align': 'center'}
        )
    ], className='row',
)


layout_datos_irf = html.Div([
    header,
    html.Div(
        [
            dcc.Dropdown(
                id="dropdown_f-montos",
                options=[
                    {'label': 'CLP', 'value': 'CLP'},
                    {'label': 'UF', 'value': 'UF'},
                ],
                value='CLP',
                className="dcc_control no-print"
            ),
            dcc.Loading(id="loading-icon_f-montos",
                        children=[dcc.Graph(id='f-montos')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Dropdown(
                id="dropdown_f-dv01",
                options=[
                    {'label': 'CLP', 'value': 'CLP'},
                    {'label': 'UF', 'value': 'UF'},
                ],
                value='CLP',
                className="dcc_control no-print"
            ),
            dcc.Loading(id="loading-icon_f-dv01",
                        children=[dcc.Graph(id='f-dv01')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Dropdown(
                id="dropdown_f-bonos",
                options=[
                    {'label': 'CLP', 'value': 'CLP'},
                    {'label': 'UF', 'value': 'UF'},
                ],
                value='CLP',
                className="dcc_control no-print"
            ),
            dcc.Checklist(id='check_f-bonos', options=[
                          {'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id="loading-icon_f-bonos",
                        children=[dcc.Graph(id='f-bonos')], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading-icon_f-reaj",
                        children=[dcc.Graph(id='f-reaj', figure=fig_reaj)], type="circle"),
        ], className='pretty_container'
    ),
])
