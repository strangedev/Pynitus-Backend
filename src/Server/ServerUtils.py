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

import cherrypy


def getCurrentSession(management):
    return management.session_handler.get(getClientIp())


def setForCurrentSession(management, attr, val):
    management.session_handler.setAttribute(getClientIp(), attr, val)


def getForCurrentSession(management, attr):
    return getCurrentSession(management).get(attr)


def existsForCurrentSession(management, attr):
    return getCurrentSession(management).exists(attr)


def removeForCurrentSession(management, attr):
    getCurrentSession(management).remove(attr)


def returnToLastPage(view, management):
    if getCurrentSession(management).exists('lastpage'):

        if getCurrentSession(management).get('lastpageArgs'):
            return getCurrentSession(management).get("lastpage")(
                    view,
                    **getCurrentSession(management).get('lastpageArgs')
                )
        else:
            return getCurrentSession(management).get("lastpage")(view)

    return view.index()


def getClientIp():
    return cherrypy.request.headers['Remote-Addr']


def refreshSession(management):
    management.session_handler.activity(getClientIp())


def setLastPage(management, page, args):
    management.session_handler.setAttribute(getClientIp(), "lastpage", page)
    management.session_handler.setAttribute(getClientIp(), "lastpageArgs", args)
