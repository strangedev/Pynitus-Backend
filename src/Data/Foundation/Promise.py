class Promise(object):

    def __init__(self, supplier):
        self.__supplier = supplier
        self.__fulfilled = False
        self.__value = None

    def get(self, *args, **kwargs):
        if not self.__fulfilled:
            self.__value = self.__supplier(*args, **kwargs)
            self.__fulfilled = True
        return self.__value
