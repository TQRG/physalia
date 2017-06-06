"""Example of using Physalia to profile F-Droid."""

from time import sleep
import subprocess
from samples.utils import AndroidViewClientUseCase

# pylint: disable=invalid-name
# this is just a script -- uppercase variables would look odd

def get_running_pkg():
    """Get Running App's package."""
    return subprocess.check_output(
        "adb shell dumpsys window windows |"
        " grep mCurrentFocus | cut -d'/' -f1 |"
        " rev | cut -d' ' -f1 | rev",
        shell=True
    ).strip()

def run_open_app(use_case):
    """Simply open app and wait 10 seconds."""
    use_case.open_app()
    sleep(10)

def cleanup(use_case):
    """Close the app and wait a second."""
    use_case.kill_app()
    sleep(1)

# Youtube Music

youtube_open_app_use_case = AndroidViewClientUseCase(
    "OpenApp",
    "./apks/YouTube Music_v1.62.7_apkpure.com.apk",
    "com.google.android.apps.youtube.music",
    "1.62.7",
    run_open_app,
    prepare=None,
    cleanup=cleanup
)

youtube_open_app_use_case.prepare_apk()
youtube_open_app_use_case.run()
youtube_open_app_use_case.profile_and_persist()

# Spotify

spotify_open_app_use_case = AndroidViewClientUseCase(
    "OpenApp",
    "./apks/Spotify Music_v7.5.0.1076_apkpure.com.apk",
    "com.spotify.music",
    "7.5.0.1076",
    run_open_app,
    prepare=None,
    cleanup=cleanup
)

spotify_open_app_use_case.prepare_apk()
spotify_open_app_use_case.run()
spotify_open_app_use_case.profile_and_persist()

# Google Play

google_play_open_app_use_case = AndroidViewClientUseCase(
    "OpenApp",
    "./apks/Google Play Music_v7.3.4313-1.M.3679657_apkpure.com.apk",
    "com.google.android.music",
    "7.3.4313.M.3679657",
    run_open_app,
    prepare=None,
    cleanup=cleanup
)

google_play_open_app_use_case.prepare_apk()
google_play_open_app_use_case.run()
google_play_open_app_use_case.profile_and_persist()

# SoundCloud

soundcloud_open_app_use_case = AndroidViewClientUseCase(
    "OpenApp",
    "./apks/SoundCloud Music Audio_v2017.01.24-release_apkpure.com.apk",
    "com.soundcloud.android",
    "2017.01.24-release",
    run_open_app,
    prepare=None,
    cleanup=cleanup
)

soundcloud_open_app_use_case.prepare_apk()
soundcloud_open_app_use_case.run()
soundcloud_open_app_use_case.profile_and_persist()

# Deezer

deezer_open_app_use_case = AndroidViewClientUseCase(
    "OpenApp",
    "./apks/Deezer Music Song Streaming_v5.4.0.88_apkpure.com.apk",
    "deezer.android.app",
    "5.4.0.88",
    run_open_app,
    prepare=None,
    cleanup=cleanup
)

deezer_open_app_use_case.prepare_apk()
deezer_open_app_use_case.run()
deezer_open_app_use_case.profile_and_persist()

# Apple Music

apple_music_open_app_use_case = AndroidViewClientUseCase(
    "OpenApp",
    "./apks/Apple Music_v1.2.0_apkpure.com.apk",
    "com.apple.android.music",
    "1.2.0",
    run_open_app,
    prepare=None,
    cleanup=cleanup
)

apple_music_open_app_use_case.prepare_apk()
apple_music_open_app_use_case.run()
apple_music_open_app_use_case.profile_and_persist()
