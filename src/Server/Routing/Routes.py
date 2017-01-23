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

from typing import List

from src.Data.Foundation.Promise import Promise
from src.Server.Routing.ApiRoute import ApiRoute
from src.Views.Admin.AdminViews import AdminViews
from src.Views.Admin.UnimportedViews import UnimportedViews
from src.Views.Library.DetailViews import DetailViews
from src.Views.Library.LibraryViews import LibraryViews
from src.Views.Queue.QueueViews import QueueViews
from src.Views.Upload.UploadViews import NewUploadView, UploadHandlerViews


class Routes(object):

    __routes = []  # type: List[ApiRoute]
    __default_route = None  # type: Promise(object.__class__)

    @classmethod
    def register(cls, path: str, view: object.__class__):
        cls.__routes.append(ApiRoute(path, view))

    @classmethod
    def setDefaultRoute(cls, view: object.__class__):
        cls.__default_route = Promise(view)

    @staticmethod
    def getRoute(vpath: List[str], management, params):
        """
        TODO
        :param vpath:
        :param management:
        :param params:
        :return:
        """
        for route in Routes.__routes:
            if route.matchesVpath(vpath):
                route.swallowParameters(vpath, params)
                return route.view.get(management)

    @staticmethod
    def getDefaultRoute(management):
        return Routes.__default_route.get(management)

Routes.setDefaultRoute(LibraryViews)
Routes.register("/admin/panel", AdminViews)
Routes.register("/admin/unimported", UnimportedViews)
Routes.register("/library", LibraryViews)
Routes.register("/details", DetailViews)
Routes.register("/queue", QueueViews)
Routes.register("/upload/new", NewUploadView)
Routes.register("/upload/handler/$track_type", UploadHandlerViews)
