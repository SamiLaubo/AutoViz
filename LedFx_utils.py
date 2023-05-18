from effects import effects_lists
import numpy as np
import json
import requests
import time

class Effects_Handler:
    def __init__(self, _sock, party_factor, use_loudness, effects_list_index):
        self.effect_index = 0
        self.party_factor = party_factor
        self.local_efefct = False
        self._sock = _sock
        self.local_thread = None
        self.last_change = time.time()
        self.use_loudness = use_loudness
        self.eli = effects_list_index

    def change_effect(self, msg='', level=-1, effect=''):
        if time.time() - self.last_change > 1: # No more than 1 change per 2 seconds
            # self.effect_index = np.random.randint(0, len(effects_list[self.party_factor]))
            # print('Change' + msg + f': {effects_list[self.party_factor][self.effect_index]}')

            if level == -1 or not self.use_loudness: level = self.party_factor

            if effect != '':
                print('Change' + msg + f': {effect}')
                self.send_LedFx(effect=effect)
            else:
                self.effect_index = np.random.randint(0, len(effects_lists[self.eli][level]))
                print('Change' + msg + f': {level} - {effects_lists[self.eli][level][self.effect_index]}')
                self.send_LedFx(level=level)

            self.last_change = time.time()

    def send_LedFx(self, no_scene=False, level=5, effect=''):
        url = "http://127.0.0.1:8888/api/scenes"

        if no_scene:
            payload = json.dumps({
                "id": 'No scene',
                "action": "activate"
            })
        elif effect != '': # SONG_BANK
            # print(f'hard change send bank - {effect}')
            payload = json.dumps({
                "id": effect,
                "action": "activate"
            })
        else:
            # print(f'no effect change - {effects_lists[self.eli][level][self.effect_index]}')
            payload = json.dumps({
                "id": effects_lists[self.eli][level][self.effect_index],
                "action": "activate"
            })

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request("PUT", url, headers=headers, data=payload)
            # print(response.text)
            return response.status_code
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import socket
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    effects_handler = Effects_Handler(_sock, 0, 0)
    effects_handler.send_LedFx(level=14)



    # pass
    # changeScene('green')
    # send_package_test()
    # main()