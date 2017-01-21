from src.Server.ApiRoute import ApiRoute

ROUTES = set({})  # type: Set[ApiRoute]


def addRoute(route: ApiRoute):
    ROUTES.add(route)

import src.Views.Library.ArtistsView
import src.Views.Admin.UnimportedView


