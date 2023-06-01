import dramatiq
import mimetypes

from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends.redis import RedisBackend
from dramatiq.encoder import PickleEncoder
from dramatiq.middleware import CurrentMessage

from .tasks import ConverterWorker


__all__ = ["ConverterWorker"]

mimetypes.init()

broker = RedisBroker()
encoder = PickleEncoder()
redis_backend = RedisBackend(encoder=encoder)
broker.add_middleware(Results(backend=redis_backend, store_results=True))
broker.add_middleware(CurrentMessage())

dramatiq.set_broker(broker)
dramatiq.set_encoder(encoder)

if __name__ != "src.worker":

    class ConfigureActors(ConverterWorker):
        def __init__(self) -> None:
            super().__init__()

    ConfigureActors()
