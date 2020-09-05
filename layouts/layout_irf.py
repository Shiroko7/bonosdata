import dash_core_components as dcc
import dash_html_components as html
import plots
from api import query_by_daterange
from datetime import date, timedelta, datetime, time
from plots import fx_dv01_participacion_reajuste

import time


end_date = date.today()
start_date = end_date - timedelta(days=3*25)

#t0 = time.time()
df_irf = query_by_daterange('irf', start_date, end_date)
#t1 = time.time()
#print('elapsed time:', t1-t0)

usdclp = query_by_daterange("usdclp", start_date, end_date)

# dataframes

header = html.Div(
    [
        html.Div(
            [
                html.H2('IRF Data',),
                html.H6('Versión 2.0.1', className='no-print'),
            ], className='twelve columns', style={'text-align': 'center'}
        )
    ], className='row',
)


layout_datos_irf = html.Div([
    header,
    html.Div(
        [
            dcc.Dropdown(
                id="dropdown_bar",
                options=[
                    {'label': 'CLP', 'value': 'CLP'},
                    {'label': 'UF', 'value': 'UF'},
                ],
                value='CLP',
                className="dcc_control no-print"
            ),
            html.Label('Seleccionar rango de data',
                       className="control_label"),
            dcc.DatePickerRange(
                id='daterange_bar',
                first_day_of_week=1,
                min_date_allowed=datetime(2020, 1, 1),
                max_date_allowed=end_date+timedelta(days=1),
                initial_visible_month=end_date,
                start_date=start_date,
                end_date=end_date,
                display_format='M-D-Y',
            ),
            dcc.Checklist(id='check_bar', options=[
                {'label': ' Mostrar acumulado', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id="loading-icon_bar",
                        children=[dcc.Graph(id='bar')], type="circle"),
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
            html.Label('Seleccionar rango de data',
                       className="control_label"),
            dcc.DatePickerRange(
                id='daterange_bonos',
                first_day_of_week=1,
                min_date_allowed=datetime(2020, 1, 1),
                max_date_allowed=end_date+timedelta(days=1),
                initial_visible_month=end_date,
                start_date=start_date,
                end_date=end_date,
                display_format='M-D-Y',
            ),
            dcc.Checklist(id='check_f-bonos', options=[
                          {'label': ' Mostrar en porcentaje', 'value': 'True'}], className="dcc_control no-print"),
            dcc.Loading(id="loading-icon_f-bonos",
                        children=[dcc.Graph(id='f-bonos')], type="circle"),
        ], className='pretty_container'
    ),
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
            html.Label('Seleccionar rango de data',
                       className="control_label"),
            dcc.DatePickerRange(
                id='daterange_montos',
                first_day_of_week=1,
                min_date_allowed=datetime(2020, 1, 1),
                max_date_allowed=end_date+timedelta(days=1),
                initial_visible_month=end_date,
                start_date=start_date,
                end_date=end_date,
                display_format='M-D-Y',
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
            html.Label('Seleccionar rango de data',
                       className="control_label"),
            dcc.DatePickerRange(
                id='daterange_dv01',
                first_day_of_week=1,
                min_date_allowed=datetime(2020, 1, 1),
                max_date_allowed=end_date+timedelta(days=1),
                initial_visible_month=end_date,
                start_date=start_date,
                end_date=end_date,
                display_format='M-D-Y',
            ),
            dcc.Loading(id="loading-icon_f-dv01",
                        children=[dcc.Graph(id='f-dv01')], type="circle"),
        ], className='pretty_container'
    ),

    html.Div(
        [
            html.Label('Seleccionar rango de data',
                       className="control_label"),
            dcc.DatePickerRange(
                id='daterange_reaj',
                first_day_of_week=1,
                min_date_allowed=datetime(2020, 1, 1),
                max_date_allowed=end_date+timedelta(days=1),
                initial_visible_month=end_date,
                start_date=start_date,
                end_date=end_date,
                display_format='M-D-Y',
            ),
            dcc.Loading(id="loading-icon_f-reaj",
                        children=[dcc.Graph(id='f-reaj')], type="circle"),
        ], className='pretty_container'
    ),
])
