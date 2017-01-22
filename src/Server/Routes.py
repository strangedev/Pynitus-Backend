from typing import List

from src.Server.ApiRoute import ApiRoute
from src.Views.TestViews import TestViews

from src.Views.Admin.AdminViews import AdminViews
from src.Views.Library.LibraryViews import LibraryViews


class Routes(object):

    __routes = []  # type: List[ApiRoute]

    @classmethod
    def register(cls, path: str, view: object.__class__):
        cls.__routes.append(ApiRoute(path, view))

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


Routes.register("/admin", AdminViews)
Routes.register("/library", LibraryViews)
Routes.register("/test/$arg", TestViews)
