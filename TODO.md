# Switch Database to SQLite

## Think of structure for sql db

Tables:
- Tracks
- Dirty tracks (tracks found during refresh but couldn't automatically imported into the db)

Tracks contain:
- Artist [KEY]
- Album [KEY]
- Title [KEY]
- Type
- All tag attributes
- Initialized <-(- Sanity check on startup was performed)
- Resource unavailable <-(- when the local file doesn't exist)
- Location (filename, url for streaming, etc..)
- JSON/BSON of instance (for non-user viewable information)

Dirty Tracks contain:
- Artist
- Album
- Title
- All tag attributes
- Location (filename, url for streaming, etc..) [KEY]
- CanBeImported

## SQL-Database related classes

### Database Interface

- Add new track entry (needed attributes: artist, album, title, location, type)

- List all Tracks/Albums/Artists

Views:
- Tracks from Artist
- Tracks on Album (given an Artist)
- Albums of Artist

- Get Track entry

### Implement concrete Database class

- Implements Database Interface
- Database is constructed by DatabaseFactory
- DatabaseFactory returns concrete implementation
- This makes database implementations interchangeable (DB-agnostic backend)

### TrackFactory

- Get Track instance from db (TrackFactory) <-(- TrackFactory gets track entry / track type from db and instanciates the corresponding Track subclass)

### Track superclass (Persistent Track Instances)

- Tracks are constructed from database entries
- Database entry of track specifies track type (class name)
- All Tracks share a common superclass
- Track superclass automagically loads attributes from db and stores attributes to db (in JSON/BSON attribute of track table)

## DB refresh
- DB refresh happens on startup
- DB refresh can be triggered by the admin

What DB refresh does:
- recursively find all audio files (by mime type) in music directory
    - if track is known to db mark resourceUnavailable as false
    - if track is not known to db put into dirty tracks to process later
    - set initialized to true
- For all uninitialized tracks in db
    - perform sanity check
    - flag as initialized

How dirty tracks (not imported yet) are handled:
- try to read the tag information into db
- if tagged data is sufficient, set canBeImported to true
- A hint is displayed in the frontend to the admin showing all dirty tracks with canBeImported == False
- The admin has to approve all tracks before they are actually imported into the tracks table
- The admin has the option to tag all incomplete audio files to make them importable

## Track Sanity Check (instance.resourceAvailable(self) -> bool)

- Every instance provides a function to check whether the resource can be played
- Sanity check is performed when a track is added to playbackQueue
- If sanity check fails, set resourceUnavailable to true
- Unavailable tracks are not shown to the user
- Unavailable tracks are shown to the admin, admin has the option to fix the track or delete the track entry