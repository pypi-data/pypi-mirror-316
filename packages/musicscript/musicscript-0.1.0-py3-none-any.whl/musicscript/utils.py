import os
from musicscript.album import Album
from musicscript.program_runner import ProgramRunner
from musicscript.runner import Runner


def download(album: Album, log=False):
    """Download songs using yt-dlp"""

    os.makedirs(album._download_path, exist_ok=True)

    args = [
        'yt-dlp',
        '-x',
        '--audio-format',
        'mp3',
        '-P',
        f'{album._download_path}',
        '-vU', 
        '-R', 
        'inf',
        '--file-access-retries', 
        'inf',
        '--fragment-retries',
        'inf',
        '-o',
        '%(title)s.%(ext)s',
        album.url
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
        new_name = new_name.replace(" (Official Visualizer)", "")
        new_name = new_name.replace(" (Audio)", "")
        new_name = new_name.replace(" (Lyric Video)", "")
        new_name = new_name.replace(" (Lyric Video)", "")
        new_name = new_name.replace(" (Visualizer)", "")
        new_name = new_name.replace(f"{album.artist} - ", "")
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
        new_path = album.path + "/" + file

        # song metadata
        album_name = 'album=' + f'{album.title}'
        artist_name = 'artist=' + f'{album.artist}'
        args =  [
            'ffmpeg', 
            '-i', 
            file_path, 
            '-y', 
            '-metadata', 
            album_name, 
            '-metadata', 
            artist_name, 
            f"{new_path}"
        ]

        # run ffmpeg
        p = ProgramRunner(program=args)
        res = p.run()
        if log:
            print("📦 Adding Song metadata:", res[1], file)
            if res[0].stderr:
                print("🪵 Log:", res[0].stderr)
            if res[1] == Runner().PASS:
                args = ["rm", f"{file_path}"]
                p = ProgramRunner(program=args)
                p.run()

    # Clean download directory
    if len(os.listdir(album._download_path)) == 0:
        args = ["rm", "-rf", f"{album._download_path}"]
        p = ProgramRunner(program=args)
        p.run()
        print("🧹 Cleaned download directory")
    else:
        print("⚠️ Download directory has aritfacts")
