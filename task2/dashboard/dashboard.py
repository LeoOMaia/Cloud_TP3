import dash
from dash import Dash, html, dcc
import redis
import json
import plotly.graph_objs as go
import multiprocessing

def Date_from_redis():
    # Redis esta no IP 192.168.121.66 e na porta 6379
    connection_redis = redis.Redis(host="192.168.121.66", port=6379, db=0)
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
app = Dash(__name__)

# Layout do Dashboard
app.layout = html.Div([
    html.H1("Uso de recursos do sistema", 
            style={'text-align': 'center', 'color': 'teal', 'font-family': 'Arial', 'padding': '20px'}
    ),
    html.Div([
        html.Label(''),
        dcc.Graph(id='mem-graph'),
        html.Label(''),
        dcc.Graph(id='net-graph'),
    ], style={'background-color': 'lightgray'}),
    dcc.Interval(
        id='interval-component-resources',
        interval=1*1000,  # 1 segundo
        n_intervals=0
    ),
    html.H1("Média Móvel de CPUs",
            style={'text-align': 'center', 'color': 'red', 'font-family': 'Arial', 'padding': '20px'}
    ),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component-graph',
        interval=1*1000,  # Atualização a cada 1 segundo
        n_intervals=0
    )
], style={'font-family': 'Arial', 'padding': '20px'})

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
            'gauge': {
                'axis': {'range': [0, 100]},
                'bar': {'color': 'darkgreen'},
            }
        }],
        'layout': {'title': 'Porcentagem de conteúdo de cache de memória', 'height': 300, 'color':'red'}
    }
    net_figure = {
        'data': [{
            'type': 'indicator',
            'mode': 'gauge+number',
            'value': net_percent,
            'gauge': {
                'axis': {'range': [0, 100]},
                'bar': {'color': 'darkred'},
            }
        }],
        'layout': {'title': 'Porcentagem de bytes de tráfego de saída', 'height': 300, 'color':'red'}
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
    marker=dict(color='rgba(50, 168, 82, 0.6)'),  # Define a cor das barras
    )   
    
    layout = go.Layout(
    title='Média Móvel de CPUs',
    yaxis=dict(range=[0, 100]),
    plot_bgcolor='rgba(240, 240, 240, 0.8)',  # Define a cor de fundo do gráfico
    paper_bgcolor='rgba(240, 240, 240, 0.8)'  # Define a cor de fundo do papel onde o gráfico é plotado
    )
    return {'data': [trace], 'layout': layout}


# Executando o servico
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=32196)