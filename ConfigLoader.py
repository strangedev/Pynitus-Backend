import os


class ConfigLoader(object):

    def __init__(self, workingDirectoy):

        selfy.configPath = os.path.join(workingDirectoy, "pynitus.conf")
        self.cherrypyConf = dict({})
