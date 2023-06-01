from dependency_injector import containers, providers

# from dramatiq.middleware import default_middleware, Callbacks, TimeLimit
# from dramatiq.brokers.redis import RedisBroker
# from dramatiq.results.backends.redis import RedisBackend
# from dramatiq.results import Results
# from dramatiq.encoder import PickleEncoder, JSONEncoder

from . import services, converter as _converter


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    # config = providers.Configuration(yaml_files=["config.yml"])
    # encoder = providers.Singleton(PickleEncoder)
    # result_backend = providers.Singleton(RedisBackend, encoder=encoder)
    # result_middleware = providers.Singleton(Results, backend=result_backend)

    # broker = providers.Singleton(RedisBroker)

    converter = providers.Singleton(
        _converter.Converter,
        #     broker=broker,
        #     encoder=encoder,
        #     result_middleware=result_middleware,
    )

    converter_service = providers.Singleton(
        services.ConverterService, converter=converter
    )
