import os
from musicscript.album import Album
from musicscript.program_runner import ProgramRunner
from musicscript.runner import Runner


def download(album: Album, log=False):
    """Download songs using yt-dlp"""

    os.makedirs(album._download_path, exist_ok=True)

    args = [
        "yt-dlp",
        "-x",
        "--audio-format",
        "mp3",
        "-P",
        album._download_path,
        "-vU",
        "-R",
        "inf",
        "--file-access-retries",
        "inf",
        "--fragment-retries",
        "inf",
        "-o",
        "%(playlist_index)02d %(title)s.%(ext)s",
        album.url,
    ]

    p = ProgramRunner(program=args)
    res = p.run()
    if log:
        print("📦 Finished Running download", res[1])
        if res[0].stdout:
            print("🪵 Log: ", res[0].stdout)

    print("🗂️ Download Results: ", res[1])


def rename_songs(album: Album, log=False):
    """Rename songs by removing yt-dlpd download tags"""

    files = os.listdir(album._download_path)

    for file in files:
        new_name = file.replace(" (Official Video)", "")
        new_name = new_name.replace(" (Official Music Video)", "")
        new_name = new_name.replace(" (Official Visualizer)", "")
        new_name = new_name.replace(" (Audio)", "")
        new_name = new_name.replace(" (Official Audio)", "")
        new_name = new_name.replace(" [Official Audio]", "")
        new_name = new_name.replace(" (Lyric Video)", "")
        new_name = new_name.replace(" (Lyric Video)", "")
        new_name = new_name.replace(" (Visualizer)", "")
        new_name = new_name.replace(" (OFFICIAL VIDEO)", "")

        split_name = new_name.split(" - ")
        if len(split_name) > 1:
            album.artist = split_name[0][3:]
            new_name = split_name[0][:3] + "".join(split_name[1:])

        # TODO: santize song titles
        new_path = album._download_path + "/" + new_name
        old_path = album._download_path + "/" + file
        os.rename(old_path, new_path)
    if log:
        print("📦 Renamed Songs Complete")


def add_metadata(album: Album, log=False):
    """Add song metadata, ex. Artist Name, Album Name"""

    files = os.listdir(album._download_path)

    for file in files:
        # new paths
        file_path = album._download_path + "/" + file
        song_title = file[3:-4]
        track_number = file[:2]
        if track_number == "NA":
            track_number = ""
        try:
            track_number = eval(track_number.lstrip("0"))
        except:
            track_number = ""
        new_path = album.path + "/" + file[3:]

        # Create and merge cover stream
        album_name = "album=" + f"{album.album}"
        title = "title=" + f"{song_title}"
        artist = "artist=" + f"{album.artist}"
        album_artist = "album_artist=" + f"{album.album_artist}"
        year = "year=" + f"{album.year}"
        track = "track=" + f"{track_number}"
        comment = "comment=" + f"{album.comment}"
        genre = "genre=" + f"{album.genre}"
        copyright = "copyright=" + f"{album.copyright}"
        description = "description=" + f"{album.description}"
        grouping = "grouping=" + f"{album.grouping}"
        lyrics_file = input(f"Enter Song Lyrics file ({new_path}): ")
        song_lyrics = ""
        if os.path.isfile(lyrics_file):
            with open(lyrics_file, "r") as f:
                song_lyrics = "".join(f.readlines())
        lyrics = "lyrics=" + f"{song_lyrics}"

        metadata_args = [
            "ffmpeg",
            "-i",
            file_path,
            "-i",
            album.cover,
            "-map",
            "0",
            "-map",
            "1",
            "-c",
            "copy",
            "-disposition:1",
            "attached_pic",
            "-y",
            "-metadata",
            album_name,
            "-metadata",
            artist,
            "-metadata",
            album_artist,
            "-metadata",
            title,
            "-metadata",
            year,
            "-metadata",
            track,
            "-metadata",
            comment,
            "-metadata",
            genre,
            "-metadata",
            copyright,
            "-metadata",
            description,
            "-metadata",
            grouping,
            "-metadata",
            lyrics,
            new_path,
        ]

        # Run ffmpeg with cover args
        p = ProgramRunner(program=metadata_args)
        res = p.run()

        if log:
            print("📦 Adding Song metadata:", res[1], file)
            if res[0].stderr:
                print("🪵 Log:", res[0].stderr)
            if res[1] == Runner().PASS:
                args = ["rm", f"{file_path}"]
                p = ProgramRunner(program=args)
                p.run()

    album._songs = os.listdir(album.path)

    # Clean download directory
    if len(os.listdir(album._download_path)) == 0:
        args = ["rm", "-rf", f"{album._download_path}"]
        p = ProgramRunner(program=args)
        p.run()
        print("🧹 Cleaned download directory")
    else:
        print("⚠️ Error: Download directory has aritfacts, something went wrong")
