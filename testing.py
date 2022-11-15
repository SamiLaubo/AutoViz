import numpy as np
from time import sleep

import config
from utils_local import *
from utils_spotify import *

def test_strip_connection(_sock):
    for _ in range(2):
        for rgb_idx in range(3):
            data = np.zeros((config.NUM_LEDS, 3))

            data[0,  rgb_idx] = 255
            data[1,  rgb_idx] = 255
            data[2,  rgb_idx] = 255
            data[-1, rgb_idx] = 255
            data[-2, rgb_idx] = 255
            data[-3, rgb_idx] = 255

            send_package(_sock, data)

            sleep(.5)


def test_spotify(spotify_handler):
    spotify_current(spotify_handler)
    spotify_timestamps(spotify_handler)

def test_setup(_sock, spotify_handler):
    try:
        test_strip_connection(_sock)
    except Exception as e:
        print('Failed Strip Connection')
        print(e)
    else:
        print('Strip connection successful')

    try:
        test_spotify(spotify_handler)
    except Exception as e:
        print('Failed Spotify Handler')
        print(e)
    else:
        print('Spotify Handler successful')