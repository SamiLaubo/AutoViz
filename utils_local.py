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
    if key == keyboard.Key.esc:
        print('! --- Stopping keyboard listener --- !')
        config.KEY_OVERRIDE = False
        return False  # stop listener
    
    elif key == keyboard.Key.space:
        print('Pressed space - Back to normal mode')
        config.KEY_OVERRIDE = False

    else:
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys

        if k in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:  # keys of interest
            print('Key pressed: ' + k)
            try:
                config.KEY_OVERRIDE = True
                config.KEY_OVERRIDE_NOW = True
                config.KEY_NUMBER = int(k)
            except:
                print('! --- Failed key override --- !')
                
        # if k == 'm':


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread