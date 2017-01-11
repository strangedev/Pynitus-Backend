class UploadHandler(object):

    def __init__(self, internal_name, display_name, description):
        self.__internal_name = internal_name
        self.__display_name = display_name
        self.__description = description

    @property
    def internal_name(self):
        return self.__internal_name

    @property
    def display_name(self):
        return self.__display_name

    @property
    def description(self):
        return self.__description
