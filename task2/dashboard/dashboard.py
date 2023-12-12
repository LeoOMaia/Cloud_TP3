from dash import Dash, html, dcc
import redis


def Dates_from_redis():
    redis_data = getDataFromRedis()
    cpu_percent = redis_data['percent-cpu-use']
    mem_percent = redis_data['percent-memory-use']
    net_percent = redis_data['percent-network-egress']
    moving_average = {}
    for i in range(16):
        moving_average[i] = redis_data[f'moving-average-{i}']
    return cpu_percent, mem_percent, net_percent, moving_average

# Pegando dados ja processados do Redis
cpu_percent, mem_percent, net_percent, moving_average = Dates_from_redis()

# Criando o Dashboard
app = Dash(__name__)

# Layout do Dashboard


# Executando o servico
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=32196)