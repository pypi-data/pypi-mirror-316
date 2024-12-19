from typing import List

class Album:
    """Class that describes an Album"""

    _songs: List[str] = []
    _download_path: str = ""
    
    def __init__(
            self, 
            title: str = "", 
            artist: str = "", 
            url: str = "",
            path: str = ""
            ):
        self.title = title
        self.artist = artist
        self.url = url
        self.path = path

    def songs(self) -> List[str]:
        return self._songs