import dash
from dash import Dash, html, dcc
import redis
import json
import os
import plotly.graph_objs as go
import multiprocessing

HOST = os.environ.get('REDIS_HOST')
PORT = int(os.environ.get('REDIS_PORT'))

def Date_from_redis():
    # Redis esta no IP 192.168.121.66 e na porta 6379
    connection_redis = redis.Redis(host=HOST, port=PORT, db=0)
    request_data = connection_redis.get("leonardooliveira-proj3-output").decode('utf-8')
    
    # Pegando os dados do Redis em formato JSON e retornando os dados computados
    redis_data = json.loads(request_data)
    mem_percent = redis_data['percent-memory-use']
    net_percent = redis_data['percent-network-egress']
    moving_average = {}
    for i in range(multiprocessing.cpu_count()):
        moving_average[i] = redis_data[f'moving-average-{i}']
    return mem_percent, net_percent, moving_average

# Pegando dados ja processados do Redis
mem_percent, net_percent, moving_average = Date_from_redis()

# Criando o Dashboard
app = Dash(__name__, external_stylesheets=['styles.css'])

# Layout do Dashboard
app.layout = html.Div([
    html.H1("Uso de recursos do sistema", className='label-class'),
    html.Div([
        html.Label('Memória', className='label-class'),
        dcc.Graph(id='mem-graph', className='graph-style'),
        html.Label('Tráfego de Rede', className='label-class'),
        dcc.Graph(id='net-graph', className='graph-style'),
    ]),
    dcc.Interval(
        id='interval-component-resources',
        interval=1*1000,  # 1 segundo
        n_intervals=0
    ),
    html.H1("Média Móvel de CPUs", className='label-class'),
    dcc.Graph(id='live-update-graph', className='graph-style'),
    dcc.Interval(
        id='interval-component-graph',
        interval=1*1000,  # Atualização a cada 1 segundo
        n_intervals=0
    )
])

# Callback para atualizar Recursos do sistema
@app.callback(
    [
        dash.dependencies.Output('mem-graph', 'figure'),
        dash.dependencies.Output('net-graph', 'figure')
    ],
    [dash.dependencies.Input('interval-component-resources', 'n_intervals')]
)
def update_resources(n):
    mem_percent, net_percent, moving_average = Date_from_redis()
    
    # Criando gráficos de indicadores para memória e rede
    mem_figure = {
        'data': [{
            'type': 'indicator',
            'mode': 'gauge+number',
            'value': mem_percent,
            'title': {'text': 'Porcentagem de uso de Memória'},
            'gauge': {
                'axis': {'range': [0, 100]},
                'bar': {'color': 'darkgreen'},
            }
        }],
        'layout': {'title': 'Porcentagem de uso de Memória'}
    }
    net_figure = {
        'data': [{
            'type': 'indicator',
            'mode': 'gauge+number',
            'value': net_percent,
            'title': {'text': 'Porcentagem de tráfego de Rede'},
            'gauge': {
                'axis': {'range': [0, 100]},
                'bar': {'color': 'darkred'},
            }
        }],
        'layout': {'title': 'Porcentagem de tráfego de Rede'}
    }
    return mem_figure, net_figure

# Callback para atualizar o gráfico de média móvel
@app.callback(
    dash.dependencies.Output('live-update-graph', 'figure'),
    [dash.dependencies.Input('interval-component-graph', 'n_intervals')]
)
def update_graph(n):
    mem_percent, net_percent, moving_average = Date_from_redis()
    x = list(range(1,17))  # Eixo x para cada CPU ordenada
    y = list(moving_average.values()) # Eixo y com a média móvel de cada CPU
    
    # Criando o gráfico de barras
    trace = go.Bar(
        x=x,
        y=y,
        name='Media Movel de CPUs',
    )
    
    layout = go.Layout(title='Média Móvel de CPUs', yaxis=dict(range=[0, 100]))
    return {'data': [trace], 'layout': layout}


# Executando o servico
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=32196)