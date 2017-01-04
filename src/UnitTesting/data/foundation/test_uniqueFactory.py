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
