import psutil

def handler(input: dict, context: object) -> dict:
    # pega a quantidade de CPUs
    cpus = psutil.cpu_count()

    # porcentagem de uso de cada CPU
    cpu_percent = {}
    for i in range(cpus):
        percent = input[f'cpu_percent-{i}']
        cpu_percent[i] = percent
    
    # porcentagem de uso de memória
    mem_cashed = input['virtual_memory-cached']
    mem_buffer = input['virtual_memory-buffers']
    mem_total = input['virtual_memory-total']
    mem_percent = ((mem_cashed + mem_buffer)) * 100 / mem_total

    # porcentagem de trafego de rede
    bytes_sent = input['net_io_counters_eth0-packets_sent']
    bytes_recv = input['net_io_counters_eth0-packets_recv']
    if bytes_sent + bytes_recv > 0:
        net_percent = (bytes_sent * 100) / (bytes_sent + bytes_recv)
    else:
        net_percent = 0

    # média móvel de utilização de cada CPU no ultimo minuto
    moving_average = {}
    for i in range(cpus):
        use = context.env.get(f'cpu-{i}')
        use.append(cpu_percent[i])
        if len(use) > 60:
            use.pop(0)
        moving_average[i] = sum(use) / len(use)
        context.env[f'cpu-{i}'] = use
    
    # retorna o dicionário com os dados
    return_dict = {
        'percent-cpu-use': cpu_percent,
        'percent-memory-use': mem_percent,
        'percent-network-egress': net_percent,
    }
    for i in range(cpus):
        return_dict[f'moving-average-{i}'] = moving_average[i]
    return return_dict