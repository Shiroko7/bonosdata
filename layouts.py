import dash_core_components as dcc
import dash_html_components as html
import plots
from api import query_by_daterange
from datetime import date, timedelta, datetime, time
from plots import usdclp_fx, montos_time_series, fx_dv01_series, fx_dv01_series_bonos, fx_dv01_participacion_reajuste
start_date = date(2018, 1, 1)

# cambiar por today eventualmente
end_date = date(2020, 6, 11)

df_irf = query_by_daterange('irf', start_date, end_date)
usdclp = usdclp_fx()

fig_montos = montos_time_series(df_irf, start_date, end_date, 'CLP')
#fig_montos_uf = montos_time_series(df_irf, start_date, end_date, 'UF')

fig_dv01 = fx_dv01_series(df_irf, usdclp, start_date, end_date, 'CLP')
#fig_dv01_uf = fx_dv01_series(df_irf,usdclp,start_date,end_date, 'UF')

fig_bonos = fx_dv01_series_bonos(
    df_irf, usdclp, start_date, end_date, 'CLP', [], porcentaje=False)
#fig_bonos_clp_p = fx_dv01_series_bonos(df_irf,usdclp,start_date,end_date, 'CLP', [], porcentaje=True)

#fig_bonos_uf = fx_dv01_series_bonos(df_irf,usdclp,start_date,end_date, 'UF', [], porcentaje=False)
#fig_bonos_uf_p = fx_dv01_series_bonos(df_irf,usdclp,start_date,end_date, 'UF', [], porcentaje=True)

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


layout_datos = html.Div([
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
                        children=[dcc.Graph(id='f-montos', figure=fig_montos)], type="circle"),
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
                        children=[dcc.Graph(id='f-dv01', figure=fig_dv01)], type="circle"),
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
                        children=[dcc.Graph(id='f-bonos', figure=fig_bonos)], type="circle"),
        ], className='pretty_container'
    ),
    html.Div(
        [
            dcc.Loading(id="loading-icon_f-reaj",
                        children=[dcc.Graph(id='f-reaj', figure=fig_reaj)], type="circle"),
        ], className='pretty_container'
    ),
])
