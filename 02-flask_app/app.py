from flask import Flask
import redis
import time

app = Flask(__name__)
cache = redis.Redis(host = 'redis', port = 6379)

def get_hit_count():
    conns = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if conns == 0:
                raise exc
            conns -= 1
            time.sleep(0.5)

@app.route('/')
def home():
    count = get_hit_count()
    return 'Number of requests: {}\n'.format(count)