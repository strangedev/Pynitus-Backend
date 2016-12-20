import json
import os

from src.data.foundation import DictContainer


class ConfigLoader(DictContainer.DictContainer):

    def __init__(self, workingDirectoy):

        super(ConfigLoader, self).__init__()
        self.configPath = os.path.join(workingDirectoy, "pynitus.conf")

        self.__restore()

    def __restore(self):

        try:
            f = open(self.configPath)
            self.items = json.load(f)

        except Exception as e:
            raise

        finally:
            f.close()
