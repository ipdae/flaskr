import os

import redis
from flaskr import app
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        with app.test_request_context("/"):
            worker = Worker(map(Queue, listen))
            worker.work()
