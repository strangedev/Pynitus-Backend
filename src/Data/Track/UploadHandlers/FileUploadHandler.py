from src.Data import Track
from src.Data.Track import UploadHandler


class FileUploadHandler(UploadHandler):

    def __init__(self, working_dir):
        super().__init__(working_dir)

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

        # fileData = file.read()
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
