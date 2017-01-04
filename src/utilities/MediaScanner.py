import glob
import os
import mimetypes


def findAudioFiles(base_directory):
    mimetypes.init()

    ret = []

    for filepath in glob.iglob(os.path.join(base_directory, "/**/*.*"), recursive=True):

        guessed_type = mimetypes.guess_type(filepath)

        if not guessed_type:  # TODO: maybe allow other types to be handled elsewhere?
            continue

        if guessed_type[0].startswith("audio"):
            ret.append(filepath)

    return ret
