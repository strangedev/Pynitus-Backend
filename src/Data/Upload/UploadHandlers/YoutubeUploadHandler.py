from src.Data.Upload.Upload import Upload
from src.Data.Upload.UploadHandlers.AUrlUploadHandler import AUrlUploadHandler


class YoutubeUploadHandler(AUrlUploadHandler):

    display_name = "Youtube Track"
    description = "An URL to a Track on Youtube."

    @classmethod
    def handle(cls, upload_argument: Upload.UploadArgument):
        pass
