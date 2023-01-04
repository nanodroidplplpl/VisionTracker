# Modol servera, ktory streamoje film do polaczonego klienta
# Odbierajac przy tym informacje o tym gdzie zwiekszyc rozdzielczosc
import socket
import cv2
import pickle
import struct
import imutils

HOST = "127.0.0.1"
PORT = 5000

def create_socket(server_address, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    socket_address = (server_address, server_port)
    server_socket.bind(socket_address)
    return server_socket

def accepting_connection():
    pass

def testServer():
    pass

if __name__ == "__main__":
    testServer()
