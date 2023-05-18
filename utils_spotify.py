import numpy as np
from time import sleep
import time

import config
from song_bank import SONG_BANK


def spotify_current(spotify_handler):
    try:
        currentPlayer = spotify_handler.currently_playing()
    except Exception as e:
        print(f'2{e=}')
        config.SONG_ID = ''
        config.SPOTIFY_ACTIVE = False
    else:
        if currentPlayer == None:
            config.SPOTIFY_ACTIVE = False
            return

        try:
            new_SONG_ID = currentPlayer.get('item').get('id')
            name = currentPlayer.get('item').get('name')

            # Local song or sth wrong
            if (new_SONG_ID == '' or new_SONG_ID is None):
                if name in SONG_BANK: # Local song in bank
                    new_SONG_ID = name
                else: # If local song not in bank, use time only       
                    config.SPOTIFY_ACTIVE = False

                    if config.SONG_ID != name: # New local song
                        config.SONG_ID = name
                        config.CHANGE_SONG = True

                        print(f'\nCurrently playing local: {name}')

                    raise Exception()

            # if new_SONG_ID == '' or new_SONG_ID is None:
            #     config.SPOTIFY_ACTIVE = False


            if config.SONG_ID != new_SONG_ID:
                config.SPOTIFY_ACTIVE = True
                # name = currentPlayer.get('item').get('name')
                artist = currentPlayer.get('item').get('artists')[0].get('name')

                config.SONG_ID = new_SONG_ID
                config.CHANGE_SONG = True
                config.SONG_NAME = name

                config.SONG_PROG_S = currentPlayer.get('progress_ms') / 1000
                config.SONG_PROG_GET = time.time()
                config.SONG_DUR_S = currentPlayer.get('item').get('duration_ms') / 1000


                print(f'\nCurrently playing: {artist} - {name} ({config.SONG_PROG_S:.2f}s of {config.SONG_DUR_S:.2f}s)')


            else: # Same song check progress
                cur_prog = currentPlayer.get('progress_ms') / 1000
                # print('CUR Prog: ', cur_prog // 60, cur_prog % 60)
                # config.diff_list.append(abs(cur_prog - config.SONG_PROG_S))
                # print('Diff: ', cur_prog, (config.SONG_PROG_S + (time.time() - config.SONG_PROG_GET)), cur_prog - (config.SONG_PROG_S + time.time() - config.SONG_PROG_GET))

                # Less than 100ms off -> update
                if np.abs(config.SONG_PROG_S - cur_prog) > .5:
                    # print(f'Updated progress - {config.SONG_PROG_S} - {cur_prog}')
                    config.SONG_PROG_S = cur_prog
                # else:
                    # print('Updated not needed')
            
            if currentPlayer.get('is_playing') == False:
                config.SPOTIFY_ACTIVE = False
            else:
                config.SPOTIFY_ACTIVE = True

        except TypeError:
            print('Spotify Unavailable')
        except Exception as e:
            # print(f'1{e=}')
            pass

def spotify_timestamps(spotify_handler, blocks='sections'):
    try:
        current_data = spotify_handler.audio_analysis(config.SONG_ID)

        block_times = np.array([cdv.get('start') for cdv in current_data.get(blocks)])

    except TypeError:
        print('Spotify Unavailable')
        config.SPOTIFY_ACTIVE = False
        return np.array([0])
    except Exception as e:
        print(e)
        config.SPOTIFY_ACTIVE = False
        return np.array([0])

    else:
        return block_times
    
    return np.array([0])

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
        block_times = np.exp(block_times)
        block_times /= max(block_times)
        block_times = np.ceil(block_times * 10).astype(np.int8)
        return block_times

def spotify_thread(spotify_handler, delay_time):
    while True:
        spotify_current(spotify_handler)
        sleep(delay_time)