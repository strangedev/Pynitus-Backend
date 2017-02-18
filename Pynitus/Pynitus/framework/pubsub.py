from typing import Callable

__topics = dict({})


def sub(topic: str, subscriber: Callable) -> None:
    if __topics.get(topic) is not None:
        __topics[topic].append(subscriber)
    else:
        __topics[topic] = [subscriber]


def pub(topic: str, *args, **kwargs) -> None:
    subscribers = __topics.get(topic)

    if subscribers is not None:
        for s in subscribers:
            s(*args, **kwargs)
