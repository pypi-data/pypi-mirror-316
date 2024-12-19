import os
from musicscript.album import Album
from musicscript.utils import download
from musicscript.utils import rename_songs
from musicscript.utils import add_metadata

def main() -> None:
    print("👾 Hello, Music Script")

    # [0]: USER prompt
    artist = input("Enter Artist Name: ")
    title = input("Enter Album Name: ")
    url = input("Enter Soundcloud / Youtube Playlist: ")

    # [0]: DEFAULT values
    if not artist: 
        artist = "LUCKI"
        print("💿 Using default artist:", artist)

    if not title: 
        title = "GEMINI!"
        print("💿 Using default album:", title)
        
    if not url: 
        url = "https://www.youtube.com/watch?v=-_CXWQQIOnQ&list=OLAK5uy_nOYJu0d8SCcr6K9n_0cJFEwG9WwjtyJQk"
        print("💿 Using default album:", title)

    # [0]: Populate Album
    album = Album()
    album.artist = artist
    album.title = title
    album.url = url
    album.path = "music/" + album.artist + " - " + album.title
    album._download_path = album.path + '/download'

    print("📦 Album Directory: ", album.path)
    
    # [1]: Download songs
    download(album, log=True)

    # [2]: Rename songs
    rename_songs(album, log=True)

    # [3]: Add Artist metadata
    add_metadata(album, log=True)

    # [4]: Print Results
    print("🗂️ Job Completed", os.getcwd() + "/" + album.path)
    print("🔗 Url:", album.url)
    print("💿 Album:", album.title)
    print("💿 Artist:", album.artist)
