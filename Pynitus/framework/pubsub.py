"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel
    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Callable

from Pynitus.framework import memcache


def init_pubsub():
    """
    Should be called once on server startup.
    Initializes the persistent cache.
    :return: None
    """
    memcache.set("pubsub.topics", dict({}))


def sub(topic: str, subscriber: Callable) -> None:
    """
    Subscribes a listener method to a certain topic.
    :param topic: The topic ti subscribe to
    :param subscriber: The subscriber method
    :return: None
    """

    topics = memcache.get("pubsub.topics")

    if topics.get(topic) is not None:
        topics[topic].append(subscriber)
    else:
        topics[topic] = [subscriber]

    memcache.set("pubsub.topics", topics)


def pub(topic: str, *args, **kwargs) -> None:
    """
    Publishes data to a certain topic.
    When data is published, all subscribed methods will be called and the
    published data is handed over. Make sure that all subscribers can handle
    the published data in their method definition.
    Use keyword args when published data is heterogeneous.
    :param topic: The topic to publish to
    :param args: All non positional args
    :param kwargs: All keyword args
    :return: None
    """

    subscribers = memcache.get("pubsub.topics").get(topic)

    if subscribers is not None:
        for s in subscribers:
            try:
                s(*args, **kwargs)
            except Exception as e:
                # TODO: log error
                print("Pubsub: Data on {} could not be published to {}, because {}".format(topic, s, e))
