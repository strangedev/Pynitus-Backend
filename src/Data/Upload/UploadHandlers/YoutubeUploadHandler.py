from src.Data.Upload.Upload import Upload
from src.Data.Upload.UploadBroker import UploadBroker
from src.Data.Upload.UploadHandlers.AUrlUploadHandler import AUrlUploadHandler


class YoutubeUploadHandler(AUrlUploadHandler):

    def handle(self, upload_argument: Upload.UploadArgument):
        pass

UploadBroker.registerUploadHandler(YoutubeUploadHandler)
