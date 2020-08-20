import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server

import callbacks


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/irf':
        from layouts.layout_irf import layout_datos_irf
        return layout_datos_irf
    elif pathname == '/iif':
        from layouts.layout_iif import layout_datos_iif
        return layout_datos_iif
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
