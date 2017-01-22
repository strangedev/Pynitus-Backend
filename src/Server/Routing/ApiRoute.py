from typing import List, Type

from src.Data.Foundation.Promise import Promise


class ApiRoute(object):

    def __init__(self, crumbs: str, view: object.__class__):
        """
        :deprecated
        Creates a new API Route.
        Crumbs is a list of strings, specifying where the associated view
        should be routed to. A view is just a class with


        If you want to route a view to /artists
        crumbs will look like this: /artists

        If you want to route a view to /admin/login
        crumbs will look like this: /admin/login

        When a user tries to access /artists or /admin/login,
        the index() function of the view will be called.

        If a route to /admin exists and the corresponding view has a login() method
        and it's exposed, /admin/login will be routed to this method.

        :param crumbs: The path the route uses as described above.
        :param view: A cherrypy handler to which requests should be routed.
        """

        self.__crumbs = [x for x in crumbs.split("/") if len(x) > 0]
        self.__crumbs_count = len(self.__crumbs)
        self.__view = Promise(view)

    def matchesVpath(self, vpath) -> bool:
        if len(vpath) < self.__crumbs_count:
            return False

        matches = True

        for i in range(self.__crumbs_count):
            crumb = self.__crumbs[i]
            crumb_matches = crumb.startswith("$") or (crumb == vpath[i])
            matches = matches and crumb_matches

        return matches

    def swallowParameters(self, vpath, params):
        for i in range(self.__crumbs_count):
            crumb = self.__crumbs[i]
            vcomponent = vpath.pop(0)

            if crumb.startswith("$"):
                params[crumb.replace("$", "")] = vcomponent

    @property
    def view(self):
        return self.__view