

class DictContainer(object):

    def __init__(self):
        self.items = dict({})

    def update(self, attribute, o):

        if not self.exists(attribute):
            raise Exception("Item does not exist, can't update!")

        self.items[attribute] = o

    def insert(self, attribute, o):

        if self.exists(attribute):
            raise Exception("Item already exists:", attribute)

        self.items[attribute] = o

    def exists(self, attribute):

        return attribute in self.items.keys()

    def get(self, attribute):

        if not self.exists(attribute):
            raise Exception("Item does not exist:", attribute)

        return self.items[attribute]

    def set(self, attr, val):
        if self.exists(attr):
            self.update(attr, val)
        else:
            self.insert(attr, val)

    def getAll(self):
        return [(key, self.items[key]) for key in self.items.keys()]

    def getCount(self):
        return len(self.items)

    def remove(self, attribute):

        if self.exists(attribute):
            del self.items[attribute]
