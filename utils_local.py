import numpy as np
import socket

from config import UDP_IP, UDP_PORT


def send_package(_sock, data):
    # _sock = socket to send to
    # data = np.array((NUM_PIXELS, 3), dtype=int32)
    #      [[r, g, b]  for pixel 1
    #       [r, g, b]  for pixel 2
    #       [r, g, b]] for pixel 3

    # https://kno.wled.ge/interfaces/udp-realtime/
    # Max 490 pixler per pakke

    send_data = [4] + [2] + [0, 0] + data.astype(int).ravel().tolist()

    _sock.sendto(bytes(send_data), (UDP_IP, UDP_PORT))





# def send_package_test(_sock):
#     # _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#     # https://kno.wled.ge/interfaces/udp-realtime/
#     # Max 490 pixler per pakke
    
#     data = np.zeros((300, 3), dtype=np.int)
#     # data[:, 0] = np.arange(0, data.shape[0]) >> 8
#     # data[:, 1] = np.arange(0, data.shape[0]) & 0xff
#     data[:, 0] = np.random.randint(0, 250)
#     data[:, 1] = np.random.randint(0, 250)
#     data[:, 2] = np.random.randint(0, 250)

#     send_data = [4] + [10] + [0, 0] + data.ravel().tolist()

#     _sock.sendto(bytes(send_data), ('192.168.1.22', 21324))
#     # _sock.sendto(bytes(send_data2), ('192.168.1.22', 21324))