# Modol klienta odbierajacy stream od serwera, ktory
# jednoczesnie wysyla informacje o tym gdzie zwiekszyc rozdzielczosc
import socket
import cv2
import pickle
import struct
import imutils

def create_socket(server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    return client_socket

def getting_server_connect():
    pass

def testClient():
    pass

if __name__ == "__main__":
    testClient()