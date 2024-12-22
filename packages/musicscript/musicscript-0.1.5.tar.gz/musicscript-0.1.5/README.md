# Music Script

Add metadata to downloaded songs from Youtube Playlist or Soundcloud.

<img width="685" alt="Screenshot 2024-12-20 at 3 08 02 PM" src="https://github.com/user-attachments/assets/52fa0b53-490c-4f9f-964f-63f96ae008fe" />

- [x] 💿 Artist (+ muliple artists)
- [x] 💿 Album Artist
- [x] 💿 Album name
- [x] 💿 Album art
- [x] 💿 Song Title
- [x] 💿 Comment
- [x] 💿 Copyright
- [x] 💿 Track #No
- [x] 💿 Genre
- [x] 💿 Composser
- [x] 💿 Description
- [x] 💿 Year
- [x] 💿 Lyrics

## Dependencies

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - used to download songs from youtube / soundcloud / spotify
- [ffmpeg](https://ffmpeg.org/download.html) - using for adding metadata to music files

## How to Install

Install from pypi:

```sh
pip install musicscript
```

Run `musicscript` in terminal:

```sh
# run in terminal
musicscript

# 👾 Hello, Music Script
# Enter Artist Name:
# Enter Album Name:
# Enter Yotube Playlist / Soundcloud Album:
```

<img width="722" alt="Screenshot 2024-12-18 at 9 51 21 AM" src="https://github.com/user-attachments/assets/3022e351-de04-4c17-9261-ac8ab02145f3" />

## Local Setup

> [!NOTE]
>
> ### Installing UV
>
> Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) python package manager written in rust
>
> ```sh
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
>
> After install uv you can clone this project with:
>
> ```sh
> git clone https://github.com/mmsaki/music-script.git
> ```

Run inside project

```sh
cd music-script;

uv sync;

uv run musicscript;

# Answer input prompts
#
# 👾 Hello, Music Script
# Enter Artist Name:
# Enter Album Name:
# Enter Yotube Playlist / Soundcloud Album:
```

## Test

TODO!

Enjoy offline streaming!
