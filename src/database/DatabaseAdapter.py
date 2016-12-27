from typing import Dict, List


class DatabaseAdapter(object):
    def addTrack(
            self,
            title: str,
            artist: str,
            album: str,
            type: str,
            location: str,
            **kwargs
    ) -> None:
        return NotImplemented

    def getTracksByArtist(self, artist: str) -> List[Dict[str, str]]:
        return NotImplemented

    def getTracksByAlbum(self,
                         artist: str,
                         album: str) -> List[Dict[str, str]]:
        return NotImplemented

    def getTrack(self,
                 title: str,
                 artist: str,
                 album: str) -> Dict[str, str]:
        return NotImplemented

    def getUnavailable(self) -> List[Dict[str, str]]:
        return NotImplemented

    def getUnimported(self) -> List[Dict[str, str]]:
        return NotImplemented

    def getMetainformation(
            self,
            title: str,
            artist: str,
            album: str) -> Dict[str, str]:
        return NotImplemented