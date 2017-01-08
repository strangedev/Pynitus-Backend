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


class UniqueFactory(object):

    def __init__(self, constructor, *key_names):

        self.__instances = dict({})
        self.__key_names = []
        self.__constructor = constructor

        for key_name in key_names:
            self.__key_names.append(key_name)

    def new(self, **kwargs):
        for key in kwargs:
            if key not in self.__key_names:
                raise Exception("Wrong argument: ", key)

        cargs = []

        for key in self.__key_names:
            if key not in kwargs:
                raise Exception("Missing argument: ", key)

            cargs.append(kwargs[key])

        cargs = tuple(cargs)

        if cargs not in self.__instances:
            new_instance = self.__constructor(**kwargs)
            self.__instances[cargs] = new_instance

        return self.__instances[cargs]

    def setConstructor(self, constructor):
        self.__constructor = constructor
