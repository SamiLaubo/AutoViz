from effects import effects_list
import numpy as np
import json
import requests

class Effects_Handler:
    def __init__(self, _sock, party_factor):
        self.effect_index = 0
        self.party_factor = party_factor
        self.local_efefct = False
        self._sock = _sock
        self.local_thread = None

    def change_effect(self):
        self.effect_index = np.random.randint(0, len(effects_list[self.party_factor]))
        print(f'Change {effects_list[self.party_factor][self.effect_index]}')
        self.send_LedFx()

    def send_LedFx(self, no_scene=False):
        url = "http://127.0.0.1:8888/api/scenes"

        if no_scene:
            payload = json.dumps({
                "id": 'No scene',
                "action": "activate"
            })
        else:
            payload = json.dumps({
                "id": effects_list[self.party_factor][self.effect_index],
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
    pass
    # changeScene('green')
    # send_package_test()
    # main()