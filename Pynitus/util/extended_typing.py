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

import typing

# This allows someone to get the "str" part from List[str]
# For example:
#   >>> d = Dict[str, int]
#   >>> d.containedTypes()
#   (<class 'str'>, <class 'int'>)
#
# You can then test for things like:
#   >>> d.containedTypes()[0] is str
#   True

typing.GenericMeta.containedTypes = lambda self: self.__args__


def Either(*ts):
    """
    A type that can be any of the given types.
    :param ts: Any number of types
    :return: A type that can be any of the given types
    """
    name = "".join((str(t) for t in ts))
    return typing.TypeVar(name, *ts)


def Maybe(t: type):
    """
    A type that can either be t or None.
    :param t: A type
    :return: A type that can either be t or None
    """
    return Either(t, None)

One = typing.TypeVar("One")

Another = typing.TypeVar("Another")
