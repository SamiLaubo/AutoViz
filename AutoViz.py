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
from song_bank import SONG_BANK

# Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from _secrets import Client_ID, Client_Secret #stored in secrets.py - this file is ignored by GIT

import matplotlib.pyplot as plt

def main(effects_list_index, party_factor=0, use_loudness=True, USE_SPOTIFY=True, do_tests=False):
    print('\n-- Start AutoViz ---')
    print(f'Effects list  {effects_list_index}')
    print(f'Partyfactor   {party_factor}')
    print(f'Loudness      {use_loudness}')
    print(f'Spotify       {USE_SPOTIFY}')
    print(f'Do tests      {do_tests}')


    # TODO: Put all of spotify into class

    
    # Set up socket
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if USE_SPOTIFY:
        # Setup Spotify API
        scope = "user-read-playback-state"
        spotify_handler = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=Client_ID, client_secret=Client_Secret, redirect_uri='https://www.google.com'))

    # Effects Handler
    effects_handler = Effects_Handler(_sock, party_factor, use_loudness, effects_list_index)

    # Test setup
    if do_tests: 
        test_setup(
            _sock,
            spotify_handler
            )

    if USE_SPOTIFY:
        # Set up spotify get
        delay_time = 2
        t = threading.Thread(target=spotify_thread, args=(spotify_handler, delay_time), daemon=True)
        t.start()

    # Keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    # listener.join()   # remove if main thread is polling self.keys

    # Vars
    last_change_s = time.time()

    # Spotify
    current_section = 0
    spotify_active = False
    # start_s = 0.0
    # time_in_song = 0.0
    last_time_check = time.time()
    cur_section_idx = 0
    cur_time = time.time()

    section_times = []  # In s!
    section_loudness = []
    beat_times = []     # In s!

    song_end_changed = False
    use_song_bank = False

    effects_handler.change_effect()

    config.SONG_ID = ''
    config.SPOTIFY_ACTIVE = False

    # Lets go
    while(True):
        if config.KEY_OVERRIDE:
            if config.KEY_OVERRIDE_NOW:
                config.KEY_OVERRIDE_NOW = False
                last_change_s = time.time()
                effects_handler.change_effect(' - Key override changed', level=config.KEY_NUMBER)

            if time.time() - last_change_s > 10:
                last_change_s = time.time()
                effects_handler.change_effect(' - Key override time', level=config.KEY_NUMBER)

            continue # Skip rest of loop
    
        if not USE_SPOTIFY or not config.SPOTIFY_ACTIVE:
            if time.time() - last_change_s > 10:
                last_change_s = time.time()
                effects_handler.change_effect(f' - No spotify change: {USE_SPOTIFY=}, {config.SPOTIFY_ACTIVE=}')

            continue # Skip rest of loop

        
        # USE SPOTIFY below
        # -----------------

        # Change song
        if config.CHANGE_SONG and config.SONG_ID != '':
            config.CHANGE_SONG = False

            # Get analysis
            if config.SONG_NAME in SONG_BANK:
                print('Using song bank!')
                section_times = SONG_BANK.get(config.SONG_NAME).get('times')
                section_loudness = SONG_BANK.get(config.SONG_NAME).get('effects')
                use_song_bank = True
            else:
                section_times = spotify_timestamps(spotify_handler, blocks='sections')
                section_loudness = spotify_loudness(spotify_handler)
                use_song_bank = False

            cur_section_idx = -1
            last_time_check = time.time()

            song_end_changed = False

        # Update song time
        config.SONG_PROG_S += time.time() - last_time_check
        last_time_check = time.time()

        # Check and change effect
        if config.SONG_PROG_S < config.SONG_DUR_S:
            new_section_idx = np.argmax(config.SONG_PROG_S < section_times) - 1
            if config.SONG_PROG_S > section_times[-1]:
                new_section_idx = len(section_times) - 1

            if new_section_idx != cur_section_idx:
                cur_section_idx = new_section_idx

                if use_song_bank:
                    # section_loudness is now the effect
                    effects_handler.change_effect(' - New bank section ', effect=section_loudness[cur_section_idx])
                else:
                    effects_handler.change_effect(' - New section      ', level=section_loudness[cur_section_idx])
                last_change_s = time.time()

            elif time.time() - last_change_s > 12 and not use_song_bank:
                last_change_s = time.time()
                effects_handler.change_effect(' - Time             ', level=section_loudness[cur_section_idx])

            continue # Skip song ended

        # Song ended
        if song_end_changed == False: # Stop 1000 changes if duration is off
            effects_handler.change_effect(' - Song ended       ', level=5)
            last_change_s = time.time()
            song_end_changed = True    


def print_info():
    print("""
    -- Automode for LedFx --
    conda activate autoparty ->
    cmd: AutoViz effects_set([0-1]) const_partyfactor(=0, [0-10]) USE_SPOTIFY(=True) do_tests(=False)

        0-10 - Loudness
        11   - start
        12   - Rave
        13   - Extreme

        const_partyfactor sets use_loudness to False
        use_SPOTIFY = False: only use const partyfactor

        EX: AutoViz 0
    """)

if __name__ == "__main__":
    # main(do_tests=True)
    main(0)

    if len(sys.argv) == 1 or sys.argv[1] == 'info':
        print_info()
    elif len(sys.argv) == 2:
        main(int(sys.argv[1]))
    elif len(sys.argv) == 3:
        main(int(sys.argv[1]), int(sys.argv[2]), False)
    elif len(sys.argv) == 4:
        main(int(sys.argv[1]), int(sys.argv[2]), False, int(sys.argv[3]))
    elif len(sys.argv) == 5:
        main(int(sys.argv[1]), int(sys.argv[2]), False, int(sys.argv[3]), int(sys.argv[4]))
    else:
        print('To many arguments')
        print_info()



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