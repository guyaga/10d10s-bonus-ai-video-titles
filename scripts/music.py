"""Instrumental music bed via the ElevenLabs Music API, cached -> <root>/shared/sfx/<AD>_music.mp3

python music.py <AD> <seconds> "<prompt>" [--root DIR] [--force]

Write the prompt like a cue sheet: genre + instruments + mood, then the hits you need AT TIMESTAMPS that match your
title beats ("a big snap hit at 9 seconds, bass drop at 12.5 seconds"). A clean-mix clause is appended automatically.
The API returns 429 system_busy under load: requests are sequential and retried.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

CLEAN = "Clean, polished, uncluttered mix with space for a voiceover. No vocals, no harsh noise, no distortion."


def main():
    argv = paths.take_root_arg(sys.argv)
    ad, secs, prompt = argv[1], float(argv[2]), argv[3]
    out = paths.sfx_cache() / f"{ad}_music.mp3"
    if out.exists() and "--force" not in argv:
        print(out, "(cached)")
        return
    body = json.dumps({"prompt": prompt + " " + CLEAN, "music_length_ms": int(secs * 1000 + 500),
                       "force_instrumental": True}).encode()
    for attempt in range(6):
        req = urllib.request.Request("https://api.elevenlabs.io/v1/music", data=body, method="POST",
                                     headers={"xi-api-key": os.environ["ELEVEN_API_KEY"], "Content-Type": "application/json"})
        try:
            out.write_bytes(urllib.request.urlopen(req, timeout=300).read())
            print(out)
            return
        except urllib.error.HTTPError as e:
            print("retry", e.code, file=sys.stderr)
            time.sleep(20)
    raise SystemExit("music generation failed after 6 attempts")


if __name__ == "__main__":
    main()
