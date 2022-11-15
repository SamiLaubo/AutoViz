import config
from  utils_local import *

import numpy as np


def whole_color(_sock):
    data = np.zeros((config.NUM_LEDS, 3))

    data[:,  0] = np.random.randint(0, 255)
    data[:,  1] = np.random.randint(0, 255)
    data[:,  2] = np.random.randint(0, 255)

    send_package(_sock, data)