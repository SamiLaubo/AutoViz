import time

NUM_LEDS = 300

UDP_PORT = 21324         # WLED Sync Settings
UDP_IP = '192.168.1.145'  # WLED Wifi Setting

SONG_ID = ''
SONG_NAME = ''
CHANGE_SONG = False
SONG_PROG_S = 0.0
SONG_PROG_GET = time.time()
SONG_DUR_S = 0.0
SPOTIFY_ACTIVE = False

# Keyboard input
KEY_OVERRIDE = False
KEY_OVERRIDE_NOW = False
KEY_NUMBER = 0