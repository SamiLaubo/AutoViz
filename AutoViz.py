import sys
import socket
import threading
import time

import config
# from utils import *

from utils_local import *
from testing import *
from local_effects import *
from LedFx_utils import *

# Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from _secrets import Client_ID, Client_Secret #stored in secrets.py - this file is ignored by GIT


def main(party_factor=0, do_tests=False, use_dancefactor=False):
    print(party_factor)
    # Set up socket
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Setup Spotify API
    scope = "user-read-playback-state"
    spotify_handler = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=Client_ID, client_secret=Client_Secret, redirect_uri='https://www.google.com'))

    # Effects Handler
    effects_handler = Effects_Handler(_sock, party_factor)

    # Test setup
    if do_tests: 
        test_setup(
            _sock,
            spotify_handler
            )

    # Set up spotify get
    delay_time = 2
    t = threading.Thread(target=spotify_thread, args=(spotify_handler, delay_time), daemon=True)
    t.start()

    # Vars
    last_change_s = time.time()

    # Spotify
    current_section = 0
    spotify_active = False
    start_s = 0.0
    time_in_song = 0.0
    cur_section_idx = 0

    section_times = []  # In s!
    section_loudness = []
    beat_times = []     # In s!

    effects_handler.change_effect()

    # Lets go
    while(True):
        config.SONG_ID = ''
        config.SPOTIFY_ACTIVE = False
        if config.CHANGE_SONG and config.SONG_ID != '':
            config.CHANGE_SONG = False
            spotify_active = True

            start_s = time.time()
            time_in_song_s = config.SONG_PROG_S + time.time() - start_s

            # Get analysis
            section_times = spotify_timestamps(spotify_handler, blocks='sections')
            beats_times = spotify_timestamps(spotify_handler, blocks='beats')
            # section_loudness = spotify_loudness(spotify_handler)
            # print(section_loudness)
            cur_section_idx = -1

            # print(f'len section times: {len(section_times)}')
            # print(f'len beats times: {len(beats_times)}')

        if config.SPOTIFY_ACTIVE:
            # Update song time
            time_in_song_s = config.SONG_PROG_S + time.time() - start_s

            if time_in_song_s < config.SONG_DUR_S:
                new_section_idx = np.argmax(time_in_song_s < section_times)
                # new_section_idx = np.argmax(time_in_song_s < beats_times)
                # print(f'{time_in_song_s:.2f} - {section_times[cur_section_idx]}')

                if new_section_idx > cur_section_idx:
                    # print(f'Boom! {new_section_idx}')
                    cur_section_idx = new_section_idx

                    # whole_color(_sock)
                    effects_handler.change_effect()
                    # print(f'Change - {section_loudness[cur_section_idx]}')
                    # print(f'Change')
            else: # Song ended
                effects_handler.change_effect()
        
        else: # No spotify
            if time.time() - last_change_s > 20:
                last_change_s = time.time()
                effects_handler.change_effect()
            


    # try:

    #     currentPlayer = spotify.currently_playing()
        
    #     duration_s = currentPlayer.get('item').get('duration_ms') / 1000
    #     prog_ms = currentPlayer.get('progress_ms')
    
    #     start_s = time.time()

    #     currentSongID = currentPlayer.get('item').get('id')
    #     current_data = spotify.audio_analysis(currentSongID)


    #     beat_times = np.array([cdv.get('start') for cdv in current_data.get('beats')])
    #     # print(beat_times)
    #     cur_idx = 0

    #     cur_time = prog_ms / 1000 + time.time() - start_s
    #     while(cur_time < duration_s):
    #         cur_time = prog_ms / 1000 + time.time() - start_s
            
    #         new_idx = np.argmax(cur_time < beat_times)
    #         # print(new_idx)

    #         if new_idx > cur_idx:
    #             print(f'Boom! {new_idx}')
    #             send_package_test(_sock)

    #             cur_idx = new_idx

    # except Exception as e:
    #     print('Could not get info')
    #     print(e)

def print_info():
    print("""
    -- Automode for LedFx --
    conda activate autoparty ->
    cmd: AutoViz partyfactor(=0, [0-10]) do_tests(=False)
    """)

if __name__ == "__main__":
    # main(do_tests=True)
    # main(0)

    # print(len(effects_list[0]))

    if len(sys.argv) == 1 or sys.argv[1] == 'info':
        print_info()
    elif len(sys.argv) == 2:
        main(int(sys.argv[1]))
    elif len(sys.argv) == 3:
        main(int(sys.argv[1]), int(sys.argv[2]))
    elif len(sys.argv) == 4:
        main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    else:
        print('To many arguments')
        print_info()