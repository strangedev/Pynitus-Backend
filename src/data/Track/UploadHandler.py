import os


class Attribute(object):

    def __init__(
        self,
        displayName=None,
        attributeType=None,
        required=None,
        target=None
    ):
        self.displayName = displayName
        self.attributeType = attributeType
        self.required = True if required == "required" else False
        self.target = target

    def __lt__(self, other):
        return self.displayName < other.displayName


class UploadHandler(object):

    def __init__(self, workingDir):
        self.workingDir = workingDir
        self.attributes = {
            "Artist": ["string", "required", "artistName"],
            "Album": ["string", "required", "albumTitle"],
            "Title": ["string", "required", "title"],
            "Genre": ["string", "optional", "genre"],
            "Label": ["string", "optional", "label"],
            "Release Date": ["string", "optional", "releaseDate"],
            "Featuring": ["string", "optional", "features"]
        }

    def getUploadAttributes(self):
        return [Attribute(
            attribute,
            self.attributes[attribute][0],
            self.attributes[attribute][1],
            self.attributes[attribute][2]
        ) for attribute in self.attributes
        ]

    def trackFromUploadedAttributes(self, attributes):
        return NotImplemented

    def autoImportAttributes(self, obj, attributes):

        attributes["Artist"] = attributes["Artist"].title()
        attributes["Album"] = attributes["Album"].title()
        attributes["Track"] = attributes["Track"].title()

        for attribute in attributes:

            if attribute in self.attributes:

                target = self.attributes[attribute][2]
                setattr(obj, target, attributes[attribute])

    def writeTrackRecord(self, track):

        artistPath = os.path.join(self.workingDir, track.artistName)
        albumPath = os.path.join(artistPath, track.albumTitle)
        recordPath = os.path.join(albumPath, track.title) + ".rec"

        if not os.path.exists(artistPath):
            os.makedirs(artistPath)
        if not os.path.exists(albumPath):
            os.makedirs(albumPath)
        if not os.path.exists(recordPath):
            os.makedirs(recordPath)

        track.storeToFilePath(recordPath)
