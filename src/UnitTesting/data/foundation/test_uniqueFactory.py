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

from unittest import TestCase
from unittest.mock import MagicMock

from src.Data.Foundation.UniqueFactory import UniqueFactory


class TestUniqueFactory(TestCase):
    def test_new(self):

        constructor = MagicMock(return_value=42)

        factory = UniqueFactory(constructor, "foo", "bar", "baz")

        new_instance = factory.new(foo=1, bar=2, baz=3)
        snd_instance = factory.new(foo=1, bar=2, baz=3)

        self.assertEquals(new_instance, 42, "New didn't call constructor")
        constructor.assert_called_once_with(foo=1, bar=2, baz=3)
        self.assertEquals(id(new_instance), id(snd_instance), "UniqueFactory created separate instances")

    def test_setConstructor(self):
        fst_constructor = MagicMock(return_value=42)
        snd_constructor = MagicMock(return_value=1337)

        factory = UniqueFactory(fst_constructor, "foo", "bar", "baz")
        fst_instance = factory.new(foo=1, bar=2, baz=3)

        factory.setConstructor(snd_constructor)
        snd_instance = factory.new(foo=1, bar=2, baz=1)

        fst_constructor.assert_called_once_with(foo=1, bar=2, baz=3)
        snd_constructor.assert_called_once_with(foo=1, bar=2, baz=1)
