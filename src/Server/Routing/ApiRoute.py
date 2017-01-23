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