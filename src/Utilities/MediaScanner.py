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


def iterateAudioFiles(base_directory):
    mimetypes.init()
    p = base_directory + "**/*.*" if base_directory.endswith("/") else base_directory + "/**/*.*"

    for filepath in glob.iglob(p, recursive=True):
        guessed_type = mimetypes.guess_type(filepath)

        if not guessed_type or not guessed_type[0]:  # TODO: maybe allow other types to be handled elsewhere?
            continue

        if guessed_type[0].startswith("audio") and os.path.splitext(filepath)[1] in SUPPORTED_TYPES:
            yield filepath
