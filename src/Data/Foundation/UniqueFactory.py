class UniqueFactory(object):

    def __init__(self, constructor, *key_names):

        self.__instances = dict({})
        self.__key_names = []
        self.__constructor = constructor

        for key_name in key_names:
            self.__key_names.append(key_name)

    def new(self, **kwargs):
        for key in kwargs:
            if key not in self.__key_names:
                raise Exception("Wrong argument: ", key)

        cargs = []

        for key in self.__key_names:
            if key not in kwargs:
                raise Exception("Missing argument: ", key)

            cargs.append(kwargs[key])

        cargs = tuple(cargs)

        if cargs not in self.__instances:
            new_instance = self.__constructor(**kwargs)
            self.__instances[cargs] = new_instance

        return self.__instances[cargs]

    def setConstructor(self, constructor):
        self.__constructor = constructor
