import cherrypy


class TestViews(object):

    def __init__(self, management):
        self.__management = management

    @cherrypy.expose
    def index(self, arg=None):
        return arg

    @cherrypy.expose
    def foo(self, arg=None):
        return arg + "foo"
