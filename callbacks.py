from dash.dependencies import Input, Output
import plots
from app import app
from layouts.layout_irf import df_irf, usdclp


@app.callback(
    Output('f-montos', 'figure'),
    [Input('dropdown_f-montos', 'value'),
     Input('daterange_montos', 'start_date'),
     Input('daterange_montos', 'end_date')]
)
def update_output(value, start_date, end_date):
    fig = plots.montos_time_series(df_irf, start_date, end_date, value)
    return fig


@app.callback(
    Output('f-dv01', 'figure'),
    [Input('dropdown_f-dv01', 'value'),
     Input('daterange_montos', 'start_date'),
     Input('daterange_montos', 'end_date')]
)
def update_output(value, start_date, end_date):
    fig = plots.fx_dv01_series(df_irf, usdclp, start_date, end_date, value)
    return fig


@app.callback(
    Output('f-bonos', 'figure'),
    [Input('dropdown_f-bonos', 'value'),
     Input('check_f-bonos', 'value'),
     Input('daterange_bonos', 'start_date'),
     Input('daterange_bonos', 'end_date')]
)
def update_output(drop, value, start_date, end_date):
    flag = False
    if value is not None:
        if len(value) != 0:
            flag = True
    fig = plots.fx_dv01_series_bonos(
        df_irf, usdclp, start_date, end_date, drop, [], flag)
    return fig


@app.callback(
    Output('bar', 'figure'),
    [Input('dropdown_bar', 'value'),
     Input('check_bar', 'value'),
     Input('daterange_bar', 'start_date'),
     Input('daterange_bar', 'end_date')]
)
def update_output(drop, value, start_date, end_date):
    flag = False
    if value is not None:
        if len(value) != 0:
            flag = True
    fig = plots.bar_bonos(df_irf, usdclp, start_date, end_date, drop, [], flag)
    return fig

@app.callback(
    Output('f-reaj', 'figure'),
    [Input('daterange_reaj', 'start_date'),
     Input('daterange_reaj', 'end_date')]
)
def update_output(start_date, end_date):            
    fig = plots.fx_dv01_participacion_reajuste(df_irf, usdclp, start_date, end_date)
    return fig