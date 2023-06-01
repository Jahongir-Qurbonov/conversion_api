import dramatiq

from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.results import Results
from io import BytesIO
result_backend = RedisBackend()
broker = RedisBroker(
    middleware=[m() for m in dramatiq.middleware.default_middleware[1:]])
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

worker = dramatiq.Worker(broker=broker)
worker.start()


@dramatiq.actor(store_results=True)
def add(x, y):
    return y


if __name__ == "__main__":
    message = add.send(1, BytesIO(b"kssks"))
    print(message.get_result(block=True))
    print(broker.middleware)
