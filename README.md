### Pynitus is in alpha and might not be working as expected.

## Listen to the people.

Pynitus is a music playlist by and for the people. Users may upload their own music from a plethora of online or local sources. Users decide on what's being played and what's being skipped.

### Features

- An Html & CSS only (no JavaScript needed!) web interface any device can access
- A playback queue which can be filled by any user
- A voting system to skip unpopular songs
- A flood protection system to prohibit spamming
- A persistent library of music which can be added to by anyone

Pynitus supports the following sources:

- Local files (MP3, MP4/AAC, OGG, WMA)
- YouTube
- SoundCloud

And because it's easy to extend, more sources will follow.

### Getting started

Getting Pynitus up and running is easy. Just follow these steps:

1. Download Pynitus as .tar.gz or .zip compressed archive
2. Unpack Pynitus
3. Install missing python dependencies by using:


    pip install -r requirements.txt

4. Edit pynitus.conf to your liking
5. Run it:


    python3 main.py ./

Prerequesites:

- Python>=3.5
- PIP (the python package manager)
- mplayer
- mpv

## Contributing

Contributions to Pynitus are welcome. However, it is still in alpha and there's not much of a codebase to build upon.
If you'd still like to help out, see TODO.md in our Github repository for notes on planned features, fixes etc.
Feel free to contact [strangedev](https://github.com/strangedev) if you've got any questions concerning contributing.

If you are contributing to this project, make sure to include the license boilerplate in all files created by you:

    
    Pynitus - A free and democratic music playlist
    Copyright (C) 2017  <Author(s)>

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

Also make sure to credit all authors who contributed meaningful contributions to files created by you, by mentioning
them as authors.