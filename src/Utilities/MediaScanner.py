import glob
import os
import mimetypes

SUPPORTED_TYPES = {
    ".mp3",
    ".ogg",
    ".spx",
    ".mpc",
    ".ape",
    ".flac",
    ".wv",
    ".tta",
    ".wma",
    ".m4a",
    ".m4b",
    ".m4p",
    ".mp4",
    ".3g2",
    ".wav",
    ".aif",
    ".aiff",
    ".opus",
}


def findAudioFiles(base_directory):
    mimetypes.init()

    ret = []

    for filepath in glob.iglob(os.path.join(base_directory, "/**/*.*"), recursive=True):

        guessed_type = mimetypes.guess_type(filepath)

        if not guessed_type:  # TODO: maybe allow other types to be handled elsewhere?
            continue

        if guessed_type[0].startswith("audio") and os.path.splitext(filepath)[1] in SUPPORTED_TYPES:
            ret.append(filepath)

    return ret
