import os
from musicscript.album import Album
from musicscript.utils import download
from musicscript.utils import rename_songs
from musicscript.utils import add_metadata


def main() -> None:
    print("👾 Hello, Music Script")

    # [0]: USER prompt
    artist = input("Enter Artist Name: ")
    album_name = input("Enter Album Name: ")
    url = input("Enter Soundcloud / Youtube Playlist: ")
    cover = input("Enter Image: ")
    year = input("Enter Year: ")
    copyright = input("Enter Copyright: ")
    genre = input("Enter Genre: ")
    comment = input("Enter Comment: ")
    description = input("Enter Description: ")
    grouping = input("Enter grouping: ")

    # [0]: DEFAULT values
    if not artist:
        artist = "LUCKI"
        print("💿 Using default artist:", artist)

    if not album_name:
        album_name = "GEMINI!"
        print("💿 Using default album:", album_name)

    if not url:
        url = "https://www.youtube.com/watch?v=-_CXWQQIOnQ&list=OLAK5uy_nOYJu0d8SCcr6K9n_0cJFEwG9WwjtyJQk"
        print("💿 Using default url:", url)

    # [0]: Populate Album
    album = Album()
    album.artist = artist
    album.album_artist = artist
    album.album = album_name
    album.url = url
    album.cover = cover
    album.path = "music/" + album.artist + " - " + album.album
    album._download_path = album.path + "/download"
    album.year = year
    album.copyright = copyright
    album.genre = genre
    album.comment = comment
    album.description = description
    # album.grouping = grouping

    print("📦 Album Directory: ", album.path)

    # [1]: Download songs
    download(album, log=True)

    # [2]: Rename songs
    rename_songs(album, log=True)

    # [3]: Add Artist metadata
    add_metadata(album, log=True)

    # [4]: Print Results
    print("🗂️ Job Completed: Open", os.getcwd() + "/" + album.path)
    print("🔗 Url:", album.url)
    print("💿 Album:", album.album)
    print("💿 Artist:", album.artist)
    print("💿 Cover:", album.cover)
    print("💿 Year:", album.year)
    print("💿 Genre:", album.genre)
    print("💿 Copyright:", album.copyright)


if __name__ == "__main__":
    main()
