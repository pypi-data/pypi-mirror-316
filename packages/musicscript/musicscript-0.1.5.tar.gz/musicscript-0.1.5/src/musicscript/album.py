from typing import List


class Album:
    """Class that describes an Album"""

    _songs: List[str] = []
    _download_path: str = ""

    def __init__(
        self,
        title: str = "",
        artist: str = "",
        album_artist: str = "",
        album: str = "",
        grouping: str = "",
        composer: str = "",
        year: str = "",
        track: str = "",
        comment: str = "",
        genre: str = "",
        copyright: str = "",
        performer: str = "",
        description: str = "",
        synopsis: str = "",
        lyrics: str = "",
        cover: str = "",
        path: str = "",
        url: str = "",
    ):
        self.title = title
        self.artist = artist
        self.album_artist = album_artist
        self.album = album
        self.grouping = grouping
        self.composer = composer
        self.year = year
        self.track = track
        self.comment = comment
        self.genre = genre
        self.copyright = copyright
        self.description = description
        self.synopsis = synopsis
        self.performer = performer
        self.lyrics = lyrics
        self.cover = cover
        self.path = path
        self.url = url

    def songs(self) -> List[str]:
        return self._songs
