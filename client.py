# Modol klienta odbierajacy stream od serwera, ktory
# jednoczesnie wysyla informacje o tym gdzie zwiekszyc rozdzielczosc
import socket
from time import sleep

import cv2
import pickle
import struct
import imutils

HOST = '127.0.0.1'
PORT = 5001
PORT_CLIENT = 5002


class Client():
    client_socket = None
    server_socket = None
    client_server_socket = None #adres kliena jako serweru
    server_client_socket = None # adres serweru jako klienta

    def __init__(self, host, port, port_client):
        self.HOST = host
        self.PORT = port
        self.PORT_CLIENT = port_client

    def create_socket(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client_socket

    def getting_server_connect(self, client_socket, server_address, server_port):
        data = b""
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
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

    def brackets_out(self, data):
        data = data[:len(data) - 1]
        data = data[1:]
        return data
    def get_titles(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        data = self.client_socket.recv(4096).decode()
        print(data)
        data = self.brackets_out(data)
        print(data)
        data = data.split(', ')
        i = 0
        for d in data:
            data[i] = self.brackets_out(d)
            i += 1
            #print(d)
        print(data)
        return data

    def send_chosen_title(self, choice, data):
        self.client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        client_server_address = ((self.HOST, self.PORT_CLIENT))
        self.client_server_socket.bind(client_server_address)
        while True:
            self.client_server_socket.listen()
            server_client_socket, addr = self.client_server_socket.accept()
            if server_client_socket:
                server_client_socket.sendall(data[choice].encode())
                # do wywalenia
                #self.server_socket.close()
                return

    def wyslanie_mindpoint(self, mindpoint):
        pass
    def testClient(self):
        client_socket = self.create_socket()
        self.getting_server_connect(client_socket, HOST, PORT)


if __name__ == "__main__":
    client = Client(HOST, PORT, PORT_CLIENT)
    data = client.get_titles()
    #data = ['taniec_na_lodzie.mp4', 'taniec_na_sniegu.mp4']
    client.send_chosen_title(0, data)
    #client.testClient()
