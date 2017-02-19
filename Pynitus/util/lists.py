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

    You should have received a copy of twhe GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Callable, List, Iterable

from Pynitus.util.extended_typing import Either, One, Another, Maybe


def apply(method: Callable[[One], Maybe(Another)], one_or_many: Either(One, List[One])):
    """
    Applies a method to single value or a list of values and returns the result.
    Think of it as method(one_or_many) combined with map(method, one_or_many).

    :param method: The method to apply
    :param one_or_many: The value(s) to apple the method to
    :return: The result of the method application
    """

    if type(one_or_many) is list:
        return list(map(method, one_or_many))
    else:
        return method(one_or_many)


def iJustList(xs: List[Maybe(One)]) -> Iterable[One]:
    """
    Removes None values from a list. Returns a generator.
    :param xs: The input list
    :return: The input list without None values
    """
    return (x for x in xs if x is not None)


def justList(xs: List[Maybe(One)]) -> List[One]:
    """
    Removes None values from a list.
    :param xs: The input list
    :return: The input list without None values
    """
    return list(iJustList(xs))
