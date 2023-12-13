from dash import Dash, html, dcc, dash
from dash.dependencies import Input, Output
import redis
import json
import plotly.graph_objs as go

def Date_from_redis():
    # Redis esta no IP 192.168.121.66 e na porta 6379
    connection_redis = redis.Redis(host='192.168.121.66', port=6379, db=0)
    request_data = connection_redis.get("leonardooliveira-proj3-output").decode('utf-8')
    
    # Pegando os dados do Redis em formato JSON e retornando os dados computados
    redis_data = json.loads(request_data)
    cpu_percent = redis_data['percent-cpu-use']
    mem_percent = redis_data['percent-memory-use']
    net_percent = redis_data['percent-network-egress']
    moving_average = {}
    for i in range(16):
        moving_average[i] = redis_data[f'moving-average-{i}']
    return cpu_percent, mem_percent, net_percent, moving_average

# Pegando dados ja processados do Redis
cpu_percent, mem_percent, net_percent, moving_average = Date_from_redis()

# Criando o Dashboard
app = Dash(__name__)

# Layout do Dashboard
app.layout = html.Div([
    html.H1("Uso de recursos do sistema"),
    html.Div([
        html.Label('Porcentagem de uso de CPU'),
        dcc.Graph(id='cpu-graph'),
        html.Label('Porcentagem de uso de Memória'),
        dcc.Graph(id='mem-graph'),
        html.Label('Porcentagem de tráfego de Rede'),
        dcc.Graph(id='net-graph'),
    ]),
    dcc.Interval(
        id='interval-component-resources',
        interval=1*1000,  # 1 segundo
        n_intervals=0
    ),
    html.H1("Média Móvel de CPUs"),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component-graph',
        interval=1*1000,  # Atualização a cada 1 segundo
        n_intervals=0
    )
])

# Callback para atualizar Recursos do sistema
@app.callback(
    [
        Output('cpu-graph', 'figure'),
        Output('mem-graph', 'figure'),
        Output('net-graph', 'figure')
    ],
    [Input('interval-component-resources', 'n_intervals')]
)
def update_resources(n):
    cpu_percent, mem_percent, net_percent, moving_average = Date_from_redis()
    
    # Criando gráficos simples de barras para exibir os valores de CPU, memória e rede
    cpu_figure = {
        'data': [{
            'type': 'indicator',
            'mode': 'gauge+number',
            'value': cpu_percent,
            'title': {'text': 'Porcentagem de uso de CPU'},
            'gauge': {
                'axis': {'range': [0, 100]},
                'bar': {'color': 'darkblue'},
            }
        }],
        'layout': {'title': 'Porcentagem de uso de CPU'}
    }
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
    return cpu_figure, mem_figure, net_figure

# Callback para atualizar o gráfico de média móvel
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component-graph', 'n_intervals')]
)
def update_graph(n):
    cpu_percent, mem_percent, net_percent, moving_average = Date_from_redis()
    x = list(range(16))  # Eixo x para numero de CPU
    y = list(moving_average.values())  # Valores para o eixo y
    # Criando o gráfico de barras
    trace = go.Bar(
        x=x,
        y=y,
        name='Media Movel de CPUs',
    )
    
    layout = go.Layout(title='Media Movel de CPUs')
    return {'data': [trace], 'layout': layout}


# Executando o servico
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=32196, debug=True)