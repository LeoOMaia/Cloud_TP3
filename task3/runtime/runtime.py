import redis
import usermodule
import os
import json
from time import sleep
from datetime import datetime

HOST = os.environ.get('REDIS_HOST')
PORT = int(os.environ.get('REDIS_PORT'))
INPUT_KEY = os.environ.get('REDIS_INPUT_KEY')
OUTPUT_KEY = os.environ.get('REDIS_OUTPUT_KEY')

class Context:
    def __init__(self, host, port, input_key, output_key):
        self.host = host 
        self.port = port 
        self.input_key = input_key 
        self.output_key = output_key
        self.function_getmtime = os.path.getmtime('usermodule.py')
        self.last_execution = None
        self.env = {}
        
context = Context(HOST, PORT, INPUT_KEY, OUTPUT_KEY)
redis_connection = redis.Redis(host=context.host, port=context.port, db=0)
old_input = redis_connection.get(INPUT_KEY)
while True:
    input_redis = redis_connection.get(INPUT_KEY)
    if input_redis != old_input:
        context.last_execution = datetime.now()
        context.function_getmtime = os.path.getmtime('usermodule.py')
        old_input = input_redis
        output = json.dumps(usermodule.handler(json.loads(input_redis.decode('utf-8')), context))
        redis_connection.set(OUTPUT_KEY, output)
    # Checagem a cada 1seg
    sleep(1)