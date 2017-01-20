from typing import List, Type


class ApiRoute(object):

    def __init__(self, crumbs: List[str], view: object.__class__):
        """
        Creates a new API Route.
        Crumbs is a list of strings, specifying where the associated view
        should be routed to. A view is just a class with


        If you want to route a view to /artists
        crumbs will look like this: ["artists"]

        If you want to route a view to /admin/login
        crumbs will look like this: ["artists", "login"]

        When a user tries to access /artists or /admin/login,
        the index() function of the view will be called.


        If you expect parameters to be passed within the url, like /artist/$some_artist,
        crumbs will look like this: ["artist", "$some_artist"].

        Parameters always start with a $ sign and will be passed as named arguments to
        your index() method. To handle this sort of request, your index() method should
        look something like this:

        @cherrypy.expose
        def index(self, some_artist):
            # some_artist will now be whatever the user entered in the url
            return "Requested artist: {}".format(some_artist)


        For more complex routing, you can intersperse parameters and fixed routing
        paths:
        If you want to route request to /artist/$some_artist/track/$some_track
        to your view, you can use ["artist", "$some_artist", "track", "$some_track"]
        as crumbs. The given parameters will be passed to:

        def index(self, some_artist, some_track):
            return "Requested artist: {} and Track: {}".format(some_artist, some_track)

        Keep in mind that you cannot have /track/$some_track and /track/all at the same
        time, as the dispatcher won't know which one to chose.

        :param crumbs: The path the route uses as described above.
        :param view: A cherrypy handler to which requests should be routed.
        """

        self.__crumbs = crumbs
        self.__view = view

    def matchesVpath(self, vpath) -> bool:
        if not len(vpath) == len(self.__crumbs):
            return False

        matches = True

        for i in range(len(self.__crumbs)):
            crumb_matches = True if self.__crumbs[i].startswith("$") else self.__crumbs[i] == vpath[i]
            matches = matches and crumb_matches

        return matches

    def swallowParameters(self, vpath, params):
        for i in range(len(self.__crumbs)):
            crumb = self.__crumbs[i]
            if crumb.startswith("$"):
                params[crumb.replace("$", "")] = vpath[i]

    @property
    def view(self):
        return self.__view

