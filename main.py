from pathlib import Path

import subprocess

if __name__ == "__main__":
    ICECAST_URL = "icecast://source:password@localhost:8000/mystream"
    SONG_FILE = "songs/t.mp3"

    path = Path(SONG_FILE)
    if not path.exists():
        raise FileNotFoundError(f"{SONG_FILE} does not exist")

    ffmpeg_cmd = [
        "ffmpeg",
        "-re",  # read input at real-time speed
        "-i", str(path),  # input file
        "-map", "0:a",
        "-content_type", "audio/mpeg",
        "-f", "mp3",
        ICECAST_URL
    ]

    print(f"Streaming {SONG_FILE} to {ICECAST_URL}...")
    subprocess.run(ffmpeg_cmd)
