import dramatiq
import mimetypes

from dramatiq import PickleEncoder
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.middleware import CurrentMessage
from dramatiq.results import Results

# from .results_middleware import CustomResults


__all__ = ["ConverterWorker", "redis_backend"]

mimetypes.init()

broker = RedisBroker()
encoder = PickleEncoder()
redis_backend = RedisBackend(encoder=encoder)
broker.add_middleware(
    Results(backend=redis_backend, store_results=True, result_ttl=10000)
)
broker.add_middleware(CurrentMessage())
dramatiq.set_broker(broker)
dramatiq.set_encoder(encoder)

if __name__ != "src.worker":
    from .tasks import ConverterWorker

    ConverterWorker()
