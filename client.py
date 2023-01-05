# Modol klienta odbierajacy stream od serwera, ktory
# jednoczesnie wysyla informacje o tym gdzie zwiekszyc rozdzielczosc
import socket
import cv2
import pickle
import struct
import imutils

HOST = '127.0.0.1'
PORT = 5001

def create_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client_socket

def getting_server_connect(client_socket, server_address, server_port):
    data = b""
    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Receiving...", frame)
        key = cv2.waitKey(10)
        if key == 13:
            break
    client_socket.close()


def testClient():
    client_socket = create_socket()
    getting_server_connect(client_socket, HOST, PORT)

if __name__ == "__main__":
    testClient()