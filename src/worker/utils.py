from dramatiq import get_broker
from dramatiq.actor import Actor, _queue_name_re


class ActorMixin:
    def actor(
        self,
        fn=None,
        *,
        actor_name=None,
        queue_name="default",
        priority=0,
        broker=None,
        **options,
    ):
        actor_name = actor_name or fn.__name__
        if not _queue_name_re.fullmatch(queue_name):
            raise ValueError(
                "Queue names must start with a letter or an underscore followed "
                "by any number of letters, digits, dashes or underscores."
            )

        broker = broker or get_broker()
        invalid_options = set(options) - broker.actor_options
        if invalid_options:
            raise ValueError(
                f"The following actor options are undefined: {', '.join(invalid_options)}. "
                "Did you forget to add a middleware to your Broker?"
            )

        _fn = fn
        if not (hasattr(_fn, "__self__") and _fn.__self__):
            raise ValueError("It is not a classmethod")

        def _fn(*a, **kw):
            return fn(*a, **kw)

        _fn.__name__ = fn.__name__

        a = Actor(
            _fn,
            actor_name=actor_name,
            queue_name=queue_name,
            priority=priority,
            broker=broker,
            options=options,
        )

        setattr(fn.__self__, fn.__name__, a)
