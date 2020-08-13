from dash.dependencies import Input, Output
import plots
from app import app
from layouts import df_irf,start_date,end_date,usdclp



@app.callback(
    Output('f-montos', 'figure'),
    [Input('dropdown_f-montos', 'value'),]
)
def update_output(value):
    fig = plots.montos_time_series(df_irf,start_date,end_date,value)
    return fig


@app.callback(
    Output('f-dv01', 'figure'),
    [Input('dropdown_f-dv01', 'value'),]
)
def update_output(value):
    fig = plots.fx_dv01_series(df_irf,usdclp,start_date,end_date,value)
    return fig

@app.callback(
    Output('f-bonos', 'figure'),
    [Input('dropdown_f-bonos', 'value'),
     Input('check_f-bonos', 'value')]
)
def update_output(drop,value):
    flag = False
    if value is not None:
        if len(value)!=0:
            flag = True
    fig = plots.fx_dv01_series_bonos(df_irf,usdclp,start_date,end_date,drop,[],flag)
    return fig


