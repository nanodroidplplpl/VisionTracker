# Modol servera, ktory streamoje film do polaczonego klienta
# Odbierajac przy tym informacje o tym gdzie zwiekszyc rozdzielczosc
import socket
import cv2
import pickle
import struct
import imutils

HOST = '127.0.0.1'
PORT = 5001

def create_socket(server_address, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    socket_address = ((HOST, PORT))
    server_socket.bind(socket_address)
    return server_socket

def accepting_connection(server_socket):
    while True:
        server_socket.listen()
        client, addr = server_socket.accept()
        if client:
            vid = cv2.VideoCapture(0)
            while(vid.isOpened()):
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a))+a
                client.sendall(message)
                cv2.imshow('Sending...', frame)
                key = cv2.waitKey(10)


def testServer():
    server_socket = create_socket(socket.gethostbyname(socket.gethostname()), PORT)
    accepting_connection(server_socket)

if __name__ == "__main__":
    testServer()
    #print(str(socket.gethostbyname(socket.gethostname())))
