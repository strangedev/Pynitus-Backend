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

import json
import os
from typing import NewType

from src.Data.Foundation import DictContainer

ConfigLoaderType = NewType('ConfigLoader', object)


class ConfigLoader(DictContainer.DictContainer):

    def __init__(self, workingDirectoy):

        super(ConfigLoader, self).__init__()
        self.configPath = os.path.join(workingDirectoy, "pynitus.conf")

        self.__restore()

    def __restore(self):

        try:
            f = open(self.configPath)
            self.items = json.load(f)

        except Exception as e:
            raise

        finally:
            f.close()
