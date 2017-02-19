from typing import Callable

from Pynitus import get_memcache


def init_pubsub():
    if get_memcache().get("pubsub.topics") is None:
        get_memcache().set("pubsub.topics", dict({}))


def sub(topic: str, subscriber: Callable) -> None:

    topics = get_memcache().get("pubsub.topics")

    if topics.get(topic) is not None:
        topics[topic].append(subscriber)
    else:
        topics[topic] = [subscriber]

    get_memcache().set("pubsub.topics", topics)


def pub(topic: str, *args, **kwargs) -> None:

    subscribers = get_memcache().get("pubsub.topics").get(topic)

    if subscribers is not None:
        for s in subscribers:
            s(*args, **kwargs)
