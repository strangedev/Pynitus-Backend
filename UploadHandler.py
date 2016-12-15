import os

import Track


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


class FileUploadHandler(UploadHandler):

    def __init__(self, workingDir):
        super().__init__(workingDir)

        self.attributes.update({
            "File": ["file", "required", None]
        })

    def trackFromUploadedAttributes(self, attributes):

        track = Track.FileTrack(
            attributes["Artist"],
            attributes["Album"],
            attributes["Title"]
        )

        file = attributes["File"]
        fileData = None

        # TODO
        # if not file.content_type.startswith("audio"):
        #    return None

        size = 0
        while True:
            dataChunk = file.file.read(8192)
            if not dataChunk:
                break
            size += len(dataChunk)
            if not fileData:
                fileData = dataChunk
            else:
                fileData += dataChunk

        #fileData = file.read()
        fileName = file.filename

        del attributes["Artist"]
        del attributes["Album"]
        del attributes["Title"]
        del attributes["File"]

        super().autoImportAttributes(track, attributes)
        super().writeTrackRecord(track)

        artistPath = os.path.join(self.workingDir, track.artistName)
        albumPath = os.path.join(artistPath, track.albumTitle)
        recordPath = os.path.join(albumPath, track.title) + ".rec"
        localFilePath = os.path.join(recordPath, fileName)

        fileToWrite = open(localFilePath, 'wb+')
        fileToWrite.write(fileData)
        fileToWrite.close()

        print("File length: ", size)
        track.filepath = localFilePath

        return track


class YoutubeUploadHandler(UploadHandler):

    def __init__(self, workingDir):
        super().__init__(workingDir)

        self.attributes.update({
            "URL": ["string", "required", "url"]
        })

    def trackFromUploadedAttributes(self, attributes):

        track = Track.YoutubeTrack(
            attributes["Artist"],
            attributes["Album"],
            attributes["Title"]
        )

        del attributes["Artist"]
        del attributes["Album"]
        del attributes["Title"]

        super().autoImportAttributes(track, attributes)
        super().writeTrackRecord(track)

        artistPath = os.path.join(self.workingDir, track.artistName)
        albumPath = os.path.join(artistPath, track.albumTitle)
        recordPath = os.path.join(albumPath, track.title) + ".rec"
        localFilePath = os.path.join(recordPath, "muzak.yturl")

        fileToWrite = open(localFilePath, 'w+')
        fileToWrite.write(track.url)
        fileToWrite.close()

        return track


class SoundcloudUploadHandler(UploadHandler):

    def __init__(self, workingDir):
        super().__init__(workingDir)

        self.attributes.update({
            "URL": ["string", "required", "url"]
        })

    def trackFromUploadedAttributes(self, attributes):

        track = Track.YoutubeTrack(
            attributes["Artist"],
            attributes["Album"],
            attributes["Title"]
        )

        del attributes["Artist"]
        del attributes["Album"]
        del attributes["Title"]

        super().autoImportAttributes(track, attributes)
        super().writeTrackRecord(track)

        artistPath = os.path.join(self.workingDir, track.artistName)
        albumPath = os.path.join(artistPath, track.albumTitle)
        recordPath = os.path.join(albumPath, track.title) + ".rec"
        localFilePath = os.path.join(recordPath, "muzak.sndcldurl")

        fileToWrite = open(localFilePath, 'w+')
        fileToWrite.write(track.url)
        fileToWrite.close()

        return track
