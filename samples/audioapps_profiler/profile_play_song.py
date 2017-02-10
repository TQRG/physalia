"""Example of using Physalia to profile F-Droid."""

from time import sleep
from physalia.energy_profiler import AndroidViewClientUseCase

# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# this is just a script -- uppercase variables would look odd

def cleanup(use_case):
    """Close the app and wait a second."""
    use_case.uninstall_app()
    sleep(1)

# Spotify
def prepare_spotify(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    use_case.wait_for_text("Log in").touch()
    use_case.wait_for_text("Log in with Facebook").touch()
    use_case.wait_for_text("Home")
    use_case.wait_for_text("Your Music").touch()
    use_case.wait_for_text("Songs").touch()

def run_spotify_play_song(use_case):
    use_case.wait_for_text("SHUFFLE PLAY").touch()
    # TODO: wait until song is actually playing
    sleep(30)

spotify_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/Spotify Music_v7.5.0.1076_apkpure.com.apk",
    "com.spotify.music",
    "7.5.0.1076",
    run_spotify_play_song,
    prepare=prepare_spotify,
    cleanup=cleanup
)

# spotify_use_case.profile_and_persist()
spotify_use_case.run()

# SongFlip - Free Music & Player
# com.hypermedia.songflip

def run_songflip(use_case):
    use_case.wait_for_id("com.hypermedia.songflip:id/song_artist").touch()
    sleep(30)

def prepare_songflip(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    # use_case.start_view_client()
    # use_case.refresh()
    use_case.wait_for_text("Start").touch()
    use_case.wait_for_id("com.hypermedia.songflip:id/song_title").touch()

songflip_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/SongFlip Free Music Player_v1.1.8_apkpure.com.apk",
    "com.hypermedia.songflip",
    "1.1.8",
    run_songflip,
    prepare=prepare_songflip,
    cleanup=cleanup
)

# songflip_use_case.profile_and_persist()
songflip_use_case.run()

# SoundCloud

def run_soundcloud(use_case):
    use_case.wait_for_id("com.soundcloud.android:id/track_list_item").touch()
    # TODO: wait until song is actually playing
    sleep(30)

def prepare_soundcloud(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    use_case.wait_for_text("Sign in").touch()
    use_case.wait_for_text("Sign in with Facebook").touch()
    use_case.wait_for_text("Continue").touch()
    use_case.wait_for_id(
        "com.soundcloud.android:id/tab_layout"
    ).children[2].touch()
    use_case.wait_for_text("Liked tracks").touch()

soundcloud_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/SoundCloud Music Audio_v2017.01.24-release_apkpure.com.apk",
    "com.soundcloud.android",
    "2017.01.24-release",
    run_soundcloud,
    prepare=prepare_soundcloud,
    cleanup=cleanup
)

# soundcloud_use_case.profile_and_persist()
soundcloud_use_case.run()

# Deezer
# deezer.android.app

def run_deezer(use_case):
    use_case.wait_for_id("deezer.android.app:id/mosaic_cover_subtitle").touch()
    # TODO: wait until song is actually playing
    sleep(30)

def prepare_deezer(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    use_case.wait_for_text("Log in").touch()
    use_case.wait_for_text("Log in with email address").touch()
    use_case.wait_for_text("Facebook").touch()
    use_case.wait_for_content_description("Not Now ").touch()

deezer_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/Deezer Music Song Streaming_v5.4.0.88_apkpure.com.apk",
    "deezer.android.app",
    "5.4.0.88",
    run_deezer,
    prepare=prepare_deezer,
    cleanup=cleanup
)

deezer_use_case.run()

# YOUZEEK
# com.youzeek.AndroidApp

# Free music for YouTube: Stream
# com.djit.apps.stream


# Panasonic Music Streaming
# com.panasonic.avc.diga.wwmusicstreaming

# Musicsense - Music Streaming
# com.tentracks.musicsense

# TubeMP3

# Apple Music
