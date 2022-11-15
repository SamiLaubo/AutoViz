import numpy as np
from time import sleep

import config


def spotify_current(spotify_handler):
    try:
        currentPlayer = spotify_handler.currently_playing()
    except Exception as e:
        print(e)
        config.SONG_ID = ''
        config.SPOTIFY_ACTIVE = False
    else:
        try:
            new_SONG_ID = currentPlayer.get('item').get('id')

            if new_SONG_ID == '':
                config.SPOTIFY_ACTIVE = False

                raise Exception()

            if config.SONG_ID != new_SONG_ID:
                config.SONG_ID = new_SONG_ID
                config.CHANGE_SONG = True

                config.SONG_PROG_S = currentPlayer.get('progress_ms') / 1000
                config.SONG_DUR_S = currentPlayer.get('item').get('duration_ms') / 1000

                name = currentPlayer.get('item').get('name')
                artist = currentPlayer.get('item').get('artists')[0].get('name')

                print(f'Currently playing: {artist} - {name} ({config.SONG_PROG_S:.2f}s of {config.SONG_DUR_S:.2f}s)')

                config.SPOTIFY_ACTIVE = True
            
            if currentPlayer.get('is_playing') == False:
                config.SPOTIFY_ACTIVE = False
            else:
                config.SPOTIFY_ACTIVE = True



        except TypeError:
            print('Spotify Unavailable')
        except Exception as e:
            print(e)

def spotify_timestamps(spotify_handler, blocks='sections'):
    try:
        current_data = spotify_handler.audio_analysis(config.SONG_ID)

        block_times = np.array([cdv.get('start') for cdv in current_data.get(blocks)])

    except TypeError:
        print('Spotify Unavailable')
        config.SPOTIFY_ACTIVE = False
    except Exception as e:
        print(e)
        config.SPOTIFY_ACTIVE = False

    else:
        return block_times

def spotify_loudness(spotify_handler):
    try:
        current_data = spotify_handler.audio_analysis(config.SONG_ID)

        block_times = np.array([cdv.get('loudness') for cdv in current_data.get('sections')])

    except TypeError:
        print('Spotify Unavailable')
        config.SPOTIFY_ACTIVE = False
    except Exception as e:
        print(e)
        config.SPOTIFY_ACTIVE = False

    else:
        return block_times


def spotify_thread(spotify_handler, delay_time):
    while True:
        spotify_current(spotify_handler)
        sleep(delay_time)