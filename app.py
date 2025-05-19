
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

app = Dash(__name__)
server = app.server

# Descargar datos del NASDAQ-100 (por ejemplo, usando el ETF QQQ)
def get_data(period='1y'):
    ticker = yf.Ticker("QQQ")
    df = ticker.history(period=period)
    df.reset_index(inplace=True)
    return df

# Diseño inicial
app.layout = html.Div([
    html.H1("NASDAQ-100 Performance"),
    dcc.Dropdown(
        id='time-range',
        options=[
            {'label': '1 Day', 'value': '1d'},
            {'label': '6 Months', 'value': '6mo'},
            {'label': '1 Year', 'value': '1y'},
            {'label': '5 Years', 'value': '5y'},
            {'label': '10 Years', 'value': '10y'},
            {'label': 'Max', 'value': 'max'}
        ],
        value='1y'
    ),
    dcc.Graph(id='price-graph')
])

@app.callback(
    Output('price-graph', 'figure'),
    Input('time-range', 'value')
)
def update_graph(selected_period):
    df = get_data(period=selected_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))
    fig.update_layout(title=f'QQQ (NASDAQ-100) - {selected_period}',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      hovermode='x unified')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
