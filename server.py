# Modol servera, ktory streamoje film do polaczonego klienta
# Odbierajac przy tym informacje o tym gdzie zwiekszyc rozdzielczosc
import socket
from time import sleep

import cv2
import pickle
import struct
import imutils
import os

HOST = '127.0.0.1'
PORT = 5001


class Server():
    client_socket = None
    server_socket = None
    client_server_socket = None
    PORT_CLIENT_SERVER = 5002
    mind_pointx = 0
    mind_pointy = 0
    # 0 - nie ma pauzy, 1-jest pauza
    pause = 0
    prep_to_send = True

    def __init__(self, host, port):
        self.clinet_server_socket = None
        self.HOST = host
        self.PORT = port

    def create_socket(self, server_address, server_port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        socket_address = ((HOST, PORT))
        # self.server_socket = server_socket
        server_socket.bind(socket_address)
        return server_socket

    def accepting_connection(self, server_socket):
        while True:
            server_socket.listen()
            client, addr = server_socket.accept()
            if client:
                # vid = cv2.VideoCapture(0)
                vid = cv2.VideoCapture("taniec_na_lodzie.mp4")
                while (vid.isOpened()):
                    img, frame = vid.read()
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    client.sendall(message)
                    print("Wielkość wysyłanego pliku: " + str(len(a)))
                    cv2.imshow('Sending...', frame)
                    key = cv2.waitKey(10)

    def get_titles(self):
        files = os.listdir()
        titles = []
        for file in files:
            if file.endswith('.mp4'):
                titles.append(str(file))
                print(file)
        print(titles)
        return titles

    # Step one of comunication
    def send_titles(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        socket_address = ((self.HOST, self.PORT))
        self.server_socket.bind(socket_address)
        while True:
            self.server_socket.listen()
            self.client_socket, addr = self.server_socket.accept()
            if self.client_socket:
                titles = self.get_titles()
                print(titles)
                self.client_socket.sendall(str(titles).encode())
                # do wywalenia
                # self.server_socket.close()
                return

    def get_chosen_title(self):
        sleep(0.5)
        self.client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client_server_socket.settimeout(2)
        while True:
            try:
                self.client_server_socket.connect((self.HOST, self.PORT_CLIENT_SERVER))
                break
            except socket.error as err:
                sleep(0.5)
                print("Wyjatek: " + str(err))
        data = self.client_server_socket.recv(4096).decode()
        print(data)
        return data

    def mind_point_and_pause_update(self):
        while True:
            data = self.client_server_socket.recv(1024).decode()
            d = data.split()
            self.pause = int(d[0])
            self.mind_pointx = int(d[1])
            self.mind_pointy = int(d[2])
            print("Pauza: " + str(self.pause) + " mind_pointx: " +
                  str(self.mind_pointx) + " mind_pointy: " + str(self.mind_pointy))

    def testServer(self):
        server_socket = self.create_socket(socket.gethostbyname(socket.gethostname()), PORT)
        self.accepting_connection(server_socket)

    def reset_all(self):
        try:
            self.server_socket.close()
        except socket.error:
            pass
        try:
            self.client_socket.close()
        except socket.error:
            pass
        try:
            self.client_server_socket.close()
        except socket.error:
            pass


if __name__ == "__main__":
    server = Server(HOST, PORT)

    server.send_titles()
    server.get_chosen_title()
    server.mind_point_and_pause_update()
