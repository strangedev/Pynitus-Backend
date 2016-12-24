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
```
pip install -r requirements.txt

```
4. Edit pynitus.conf to your liking
5. Run it:
```
python3 main.py ./
```

Prerequesites:

- Python>=3.5
- PIP (the python package manager)
- mplayer
- mpv
