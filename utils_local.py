import numpy as np
import socket
from pynput import keyboard

import config


def send_package(_sock, data):
    # _sock = socket to send to
    # data = np.array((NUM_PIXELS, 3), dtype=int32)
    #      [[r, g, b]  for pixel 1
    #       [r, g, b]  for pixel 2
    #       [r, g, b]] for pixel 3

    # https://kno.wled.ge/interfaces/udp-realtime/
    # Max 490 pixler per pakke

    send_data = [4] + [2] + [0, 0] + data.astype(int).ravel().tolist()

    _sock.sendto(bytes(send_data), (config.UDP_IP, config.UDP_PORT))


# Add manual override
def on_press(key):
    # print(f'{key = }')
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    # if key == keyboard.Key.esc:
    if k == '§':
        print('! --- Stopping keyboard listener --- !')
        config.KEY_OVERRIDE = False
        return False  # stop listener
    
    # elif key == keyboard.Key.space:
    elif k == '`':
        print('Pressed space - Back to normal mode')
        config.KEY_OVERRIDE = False

    else:

        # print(f'{k = }')
        # print(f'{config.KEY_CTRL = }')
        # nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        shifts = np.array(['=', '!', '"', '#', '¤', '%', '&', '/', '(', ')'])

        if k in shifts:  # keys of interest
            # print(f'{int(np.where(shifts==k)[0]) = }')
            # print('Key pressed: ' + k)
            try:
                config.KEY_OVERRIDE = True
                config.KEY_OVERRIDE_NOW = True
                config.KEY_NUMBER = int(np.where(shifts==k)[0])
            except:
                print('! --- Failed key override --- !')


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread