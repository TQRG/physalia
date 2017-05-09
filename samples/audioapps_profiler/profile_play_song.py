"""Example of using Physalia to profile F-Droid.

In this script free top apps for music streaming were profiled
in terms of energy consumption in common use cases.
"""

from time import sleep
from samples.utils import AndroidViewClientUseCase

# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# this is just a script -- uppercase variables would look odd

PLAY_DURATION = 30 # seconds

def cleanup(use_case):
    """Close the app and wait a second."""
    use_case.uninstall_app()
    sleep(1)

def run(_):
    sleep(PLAY_DURATION)

# Spotify
def prepare_spotify(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    use_case.wait_for_text("Log in").touch()
    use_case.wait_for_text("Log in with Facebook").touch()
    use_case.wait_for_text("Home")
    use_case.wait_for_text("Your Music").touch()
    use_case.wait_for_text("Songs").touch()
    use_case.wait_for_text("SHUFFLE PLAY").touch()

spotify_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/Spotify Music_v7.5.0.1076_apkpure.com.apk",
    "com.spotify.music",
    "7.5.0.1076",
    run,
    prepare=prepare_spotify,
    cleanup=cleanup
)

# spotify_use_case.profile_and_persist()

# SongFlip - Free Music & Player
# com.hypermedia.songflip

def prepare_songflip(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    use_case.wait_for_text("Start").touch()
    use_case.wait_for_id("com.hypermedia.songflip:id/song_title").touch()
    use_case.wait_for_id("com.hypermedia.songflip:id/song_artist").touch()

songflip_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/SongFlip Free Music Player_v1.1.8_apkpure.com.apk",
    "com.hypermedia.songflip",
    "1.1.8",
    run,
    prepare=prepare_songflip,
    cleanup=cleanup
)

songflip_use_case.profile_and_persist()

# SoundCloud

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
    use_case.wait_for_id("com.soundcloud.android:id/track_list_item").touch()

soundcloud_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/SoundCloud Music Audio_v2017.01.24-release_apkpure.com.apk",
    "com.soundcloud.android",
    "2017.01.24-release",
    run,
    prepare=prepare_soundcloud,
    cleanup=cleanup
)

soundcloud_use_case.profile_and_persist()

# Deezer
# deezer.android.app

def prepare_deezer(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    use_case.wait_for_text("Log in").touch()
    use_case.wait_for_text("Log in with email address").touch()
    use_case.wait_for_text("Facebook").touch()
    use_case.wait_for_content_description("Not Now ").touch()
    use_case.wait_for_id("deezer.android.app:id/mosaic_cover_subtitle").touch()

deezer_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/Deezer Music Song Streaming_v5.4.0.88_apkpure.com.apk",
    "deezer.android.app",
    "5.4.0.88",
    run,
    prepare=prepare_deezer,
    cleanup=cleanup
)

deezer_use_case.profile_and_persist()

# YOUZEEK
# com.youzeek.AndroidApp

def prepare_youzeek(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    use_case.wait_for_id("com.youzeek.AndroidApp:id/login_facebook").touch()
    use_case.wait_for_content_description("Interstitial close button").touch()
    use_case.wait_for_text("Next").touch()
    use_case.wait_for_text("Next").touch()
    use_case.wait_for_text("Next").touch()
    use_case.wait_for_text("Maybe later").touch()
    use_case.wait_for_id("com.youzeek.AndroidApp:id/songTitle").touch()

youzeek_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/YOUZEEK Free Music Streaming_v4.4.6_apkpure.com.apk",
    "com.youzeek.AndroidApp",
    "4.4.6",
    run,
    prepare=prepare_youzeek,
    cleanup=cleanup
)

youzeek_use_case.profile_and_persist()

# Free music for YouTube: Stream
# com.djit.apps.stream
# FIXME this is an app that reproduces youtube videos - SKIP IT

# Panasonic Music Streaming
# com.panasonic.avc.diga.wwmusicstreaming
# Skipped because the purpose of this app is to stream music to devices
# in the network


# Musicsense - Music Streaming
# com.tentracks.musicsense

def prepare_musicsense(use_case):
    use_case.prepare_apk()
    use_case.open_app()
    use_case.wait_for_text("Allow").touch()
    use_case.wait_for_text("Allow").touch()
    use_case.wait_for_text("LOG IN").touch()
    use_case.wait_for_text("START LISTENING").touch()

musicsense_use_case = AndroidViewClientUseCase(
    "PlaySong",
    "./apks/Musicsense Music Streaming_v1.1.15_apkpure.com.apk",
    "com.tentracks.musicsense",
    "1.1.15",
    run,
    prepare=prepare_musicsense,
    cleanup=cleanup
)

musicsense_use_case.profile_and_persist()

# Napster
# com.rhapsody.napster
# Could not find a freemium version

# TIDAL
# com.aspiro.tidal
# Does not provide a free version (only tria)

# Apple Music
# com.apple.android.music
# Does not have a free streaming service
