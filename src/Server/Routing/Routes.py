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
