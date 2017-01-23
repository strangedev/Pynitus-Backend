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

import os


def htmlRelPath(config, path):
    return os.path.join(config.get("html_dir"), path)


def getConfig(config):
    return {

            "/css/bootstrap.min.css": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "css/bootstrap.min.css")
            },

            "/fonts/glyphicons-halflings-regular.eot": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.eot")
            },

            "/fonts/glyphicons-halflings-regular.svg": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.svg")
            },

            "/fonts/glyphicons-halflings-regular.ttf": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.ttf")
            },

            "/fonts/glyphicons-halflings-regular.woff": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.woff")
            },

            "/fonts/glyphicons-halflings-regular.woff2": {
                "tools.staticfile.on": True,
                "tools.staticfile.filename": htmlRelPath(config, "fonts/glyphicons-halflings-regular.woff2")
            },

            '/favicon.ico':
                {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(config, "img/pynitus_32x32.ico")
            },

            '/favicon.png':
                {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(config, "img/pynitus_32x32.png")
            },

            '/img/artist.jpeg':
            {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(config, "img/artist.jpeg")
            },

            '/img/album.jpeg':
            {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(config, "img/album.jpeg")
            },

            '/img/cd.jpg':
            {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(config, "img/cd.jpg")
            },

            '/img/search.jpg':
            {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': htmlRelPath(config, "img/search.jpg")
            }

        }