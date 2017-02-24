from Pynitus.upload import TrackRecord

name = "File"

description = "A file on your device."

arguments = {
    "mrl": {
        'type': "file",
        'display_name': "File",
        'description': "A file on your device."
    }
}

def handle(mrl: str=""):

    record = TrackRecord()
    record.mrl = mrl
    record.title = "Dummy File"
    record.artist = "Dummy Artist"
    record.album = "Dummy Album"
    record.backend = "vlc_backend"

    return record
