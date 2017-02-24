from Pynitus.upload import TrackRecord

name = "URL dummy upload plugin"

description = "For testing purposes"

arguments = {
    "url": {
        'type': "url",
        'display_name': "URL",
        'description': "An url."
    }
}

def handle(url: str=""):

    record = TrackRecord()
    record.mrl = url
    record.title = url
    record.artist = "Dummy Artist"
    record.album = "Dummy Album"
    record.backend = "vlc_backend"

    return  record
