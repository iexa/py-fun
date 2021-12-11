""" uses dash 2.x and pandas 1.3.x also flask 2.x """
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np


data = pd.read_csv('avocado.bz2')
# data = data.query("type == 'conventional' and region == 'Albany'")
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.sort_values('Date', inplace=True)

ext_styles = [{ 'href': 'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap',
                'rel': 'stylesheet'
}]
app = Dash(__name__, external_stylesheets=ext_styles)
# server = app.server

app.layout = html.Div(
    children=[
        html.Div([
            html.P(children="🥑", className='header-emoji'),
            html.H1(children='Nikado Avocado', className='header-title'),
            html.P(
                className='header-description',
                children='analyze the behaviour of avocado prices and nr sold in the US between 2015-2018'
            )], className='header',
        ),
        html.Div(className='menu',           
            children=[
                html.Div(children=[
                    html.Div(children='Region', className='menu-title'),
                    dcc.Dropdown(
                        id='region-filter',
                        options=[{'label': region, 'value': region}
                            for region in np.sort(data.region.unique())],
                        value='Albany', #default
                        clearable=False,
                        className='dropdown',
                    ),
                ]),
                html.Div(children=[
                    html.Div(children='Type', className='menu-title'),
                    dcc.Dropdown(
                        id='type-filter',
                        options=[{'label': avocado_type, 'value': avocado_type}
                            for avocado_type in data.type.unique()],
                        value='organic', #default
                        clearable=False,
                        searchable=False,
                        className='dropdown',
                    ),
                ]),
                html.Div(children=[
                    html.Div(children='Date Range', className='menu-title'),
                    dcc.DatePickerRange(
                        id='date-range',
                        min_date_allowed=data.Date.min().date(),
                        max_date_allowed=data.Date.max().date(),
                        start_date=data.Date.min().date(),
                        end_date=data.Date.max().date()
                    ),
                ]),
            ]
        ),

        html.Div(className='wrapper', children=[
            html.Div(className='card', children=
            dcc.Graph(
                id="price-chart",
                config={"displayModeBar": False},
            )),
            html.Div(className='card', children=
            dcc.Graph(
                id='volume-chart',
                config={"displayModeBar": True},
            )),
        ])
    ]
)


@app.callback(
    [Output('price-chart', 'figure'), Output('volume-chart', 'figure')],
    [Input('region-filter', 'value'), Input('type-filter', 'value'),
    Input('date-range', 'start_date'), Input('date-range', 'end_date')])
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        (data.region == region)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_fig = {
        'data': [{
            'x': filtered_data['Date'],
            'y': filtered_data['AveragePrice'],
            'type': 'lines',
            'hovertemplate': '$%{y:.2f}<extra></extra>',
        }, ],
        'layout': {
            'title': {
                'text': 'Avg. price of avocados',
                'x': 0.05,
                'xanchor': 'left',
            }, 
            'xaxis': {'fixedrange': True},
            'yaxis': {'fixedrange': True, 'tickprefix': '💲'},
            'colorway': ['#2ba']            
        },
    }
    
    volume_chart_fig = {
        'data': [{
            'x': filtered_data['Date'],
            'y': filtered_data['Total Volume'],
            'type': 'lines',
            # 'hovertemplate': '$%{y:.2f}<extra></extra>',
        }, ],
        'layout': {
            'title': {
                'text': 'Avocados sold',
                'x': 0.05,
                'xanchor': 'left', 
            },
            'xaxis': {'fixedrange': True},
            'yaxis': {'fixedrange': True},
            'colorway': ['#e34']
        },
    }
    return price_chart_fig, volume_chart_fig


if __name__ == '__main__':
    app.run_server(debug=True)
    app.title = 'Nikado Avoado analytix'
