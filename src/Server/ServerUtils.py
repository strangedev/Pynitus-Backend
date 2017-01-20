import cherrypy


def getCurrentSession(management):
    return management.session_handler.get(getClientIp())


def setForCurrentSession(management, attr, val):
    management.session_handler.setAttribute(getClientIp(), attr, val)


def getForCurrentSession(management, attr):
    return getCurrentSession(management).get(attr)


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
