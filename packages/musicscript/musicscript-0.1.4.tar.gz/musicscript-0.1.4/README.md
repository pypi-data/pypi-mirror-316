# Music Script

Downloads songs from Youtube Playlist or Soundcloud and turns them into an Album with Artist metadata.

Add album to your Apple Music App or Android to listen offline.

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
