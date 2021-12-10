""" uses dash 2.x and pandas 1.3.x also flask 2.x """

from dash import Dash, dcc, html
import pandas as pd

data = pd.read_csv('avocado.bz2')
data = data.query("type == 'conventional' and region == 'Albany'")
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.sort_values('Date', inplace=True)

ext_styles = [{ 'href': 'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap',
                'rel': 'stylesheet'
}]
app = Dash(__name__, external_stylesheets=ext_styles)

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
        html.Div([
            dcc.Graph(
                id="price-chart",
                config={"displayModeBar": False},
                className='card',
                figure={
                    'data': [{
                        'x': data['Date'],
                        'y': data['AveragePrice'],
                        'type': 'lines',
                        'hovertemplate':'$%{y:.2f}<extra></extra>',
                    }],
                    'layout': {
                        'title': {
                            'text': 'Avg price of avocados',
                            'x': 0.05,
                            'xanchor': 'left'
                        },
                        'xaxis': {'fixedrange': True },
                        'yaxis': {'tickprefix': "$", 'fixedrange': True},
                        'colorway': ['#17b897'],
                    }
                }
            ),
            dcc.Graph(
                id='volume-chart',
                config={"displayModeBar": True},
                className='card',
                figure={
                    'data': [{
                        'x': data['Date'],
                        'y': data['Total Volume'],
                        'type': 'lines'
                    }],
                    'layout': {
                        'title': {
                            'text': 'Avocados sold',
                            'x': 0.05,
                            'xanchor': 'left',
                        },
                        'xaxis': {'fixedrange': False },
                        'yaxis': {'fixedrange': True },
                        'colorway': ['#e12d39'],
                    }
                }
            )
        ], className='wrapper')
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
    app.title = 'Nikado Avoado analytix'
