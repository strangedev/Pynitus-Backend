import os


class Attribute(object):

    def __init__(
        self,
        display_name=None,
        attribute_type=None,
        required=None,
        target=None
    ):
        self.display_name = display_name
        self.attributeType = attribute_type
        self.required = True if required == "required" else False
        self.target = target

    def __lt__(self, other):
        return self.display_name < other.display_name


class UploadHandler(object):

    def __init__(self, working_dir):
        self.working_dir = working_dir
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
        #  TODO: Implement
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

        artist_path = os.path.join(self.working_dir, track.artistName)
        album_path = os.path.join(artist_path, track.albumTitle)
        record_path = os.path.join(album_path, track.title) + ".rec"

        if not os.path.exists(artist_path):
            os.makedirs(artist_path)
        if not os.path.exists(album_path):
            os.makedirs(album_path)
        if not os.path.exists(record_path):
            os.makedirs(record_path)

        track.storeToFilePath(record_path)
