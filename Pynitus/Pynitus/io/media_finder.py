"""
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  Noah Hummel

    This file is part of the Pynitus program, see <https://github.com/strangedev/Pynitus>.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import glob
import os
import mimetypes

SUPPORTED_EXTENSIONS = {
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

        if guessed_type[0].startswith("audio") and os.path.splitext(filepath)[1] in SUPPORTED_EXTENSIONS:
            yield filepath
