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


class DictContainer(object):

    def __init__(self):
        self.items = dict({})

    def update(self, attribute, o):

        if not self.exists(attribute):
            raise Exception("Item does not exist, can't update!")

        self.items[attribute] = o

    def insert(self, attribute, o):

        if self.exists(attribute):
            raise Exception("Item already exists:", attribute)

        self.items[attribute] = o

    def exists(self, attribute):

        return attribute in self.items.keys()

    def get(self, attribute):

        if not self.exists(attribute):
            raise Exception("Item does not exist:", attribute)

        return self.items[attribute]

    def set(self, attr, val):
        if self.exists(attr):
            self.update(attr, val)
        else:
            self.insert(attr, val)

    def getAll(self):
        return [(key, self.items[key]) for key in self.items.keys()]

    def getCount(self):
        return len(self.items)

    def remove(self, attribute):

        if self.exists(attribute):
            del self.items[attribute]
