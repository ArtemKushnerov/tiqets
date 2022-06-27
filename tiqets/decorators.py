import logging
import pickle

import redis

from tiqets import config

REDIS = redis.Redis(host=config.REDIS_HOST)

logger = logging.getLogger(__name__)


def cache(key, ttl=60):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            if not config.USE_CACHE:
                return f(*args, **kwargs)

            value = REDIS.get(key)
            if value is None:
                value = f(*args, **kwargs)
                serialized_value = pickle.dumps(value)
                logger.info(f"Caching value of {key} for {ttl} seconds")
                REDIS.set(key, serialized_value, ttl)
            else:
                value = pickle.loads(value)
                logger.info(f"Using cached value of {key}")
            return value

        return wrapped

    return inner_decorator
