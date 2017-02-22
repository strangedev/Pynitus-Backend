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

from typing import Any

from flask import g
import memcache


def get_memcache():
    """
    :return: A memcached client which is persistent throughout a request
    """
    mc = getattr(g, '_memcache_client', None)
    if mc is None:
        mc = g._memcache_client = memcache.Client(['127.0.0.1'], debug=0)
    return mc


def get(key: str) -> Any:
    """
    Gets a value from memcached
    :param key: The key of the value to retrieve
    :return: The value
    """
    return get_memcache().get(key)


def set(key: str, value: Any) -> int:
    """
    Sets a value in memcached
    :param key: The key of the value to set
    :param value: The value
    :return: Whether the action was successful
    """
    return get_memcache().set(key, value)


def incr(key: str) -> Any:
    """
    Increases a value in memcached
    :param key: The key of the value to increase
    :return: Whether the action was successful
    """
    return get_memcache().incr(key)


def decr(key: str) -> Any:
    """
    Decreases a value in memcached
    :param key: The key of the value to decrease
    :return: Whether the action was successful
    """
    return get_memcache().decr(key)
