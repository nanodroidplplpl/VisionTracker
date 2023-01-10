# Modol klienta odbierajacy stream od serwera, ktory
# jednoczesnie wysyla informacje o tym gdzie zwiekszyc rozdzielczosc
import socket
from time import sleep
import threading
import eyeTrack
import guiEye

import cv2
import pickle
import struct
import imutils
import eyeTrackLinear

HOST = '127.0.0.1'
PORT = 5001
PORT_CLIENT = 5002


class Client():
    client_socket = None
    server_socket = None
    client_server_socket = None #adres kliena jako serweru
    server_client_socket = None # adres serweru jako klienta
    mind_pointx = 0
    mind_pointy = 0
    g = None
    one = False
    pause = 0
    choice = 0

    lock = threading.Lock()

    def __init__(self, host, port, port_client, g):
        self.HOST = host
        self.PORT = port
        self.PORT_CLIENT = port_client
        self.g = g

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

    def send_chosen_title(self, data):
        self.client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        client_server_address = ((self.HOST, self.PORT_CLIENT))
        self.client_server_socket.bind(client_server_address)
        while True:
            self.client_server_socket.listen()
            self.server_client_socket, addr = self.client_server_socket.accept()
            if self.server_client_socket:
                self.server_client_socket.sendall(data[self.choice].encode())
                # do wywalenia
                #self.server_socket.close()
                return

    def send_mindpoint_and_pause_thread1(self, webcam, gaze, sample_surface, al, bl, sl, fl, el, ap, bp, sp, fp, ep):
        print("Start1")
        if self.one:
            while True:
                a = self.pause
                b, c = eyeTrack.get_eye_mindpoint(webcam, gaze, sample_surface, al, bl, sl, fl, el, ap, bp, sp, fp, ep)
                d = str(a) + ' ' + str(b) + ' ' + str(c)
                self.server_client_socket.sendall(d.encode())
        else:
            while True:
                a = self.pause
                b, c = self.g.get_mind_point(webcam, gaze)
                b, c = int(b), int(c)
                #print(b)
                if b > 900:
                    b = 899
                if b < 300:
                    b = 301
                if c > 700:
                    c = 699
                if c < 300:
                    c = 301
                d = str(a) + ' ' + str(b) + ' ' + str(c)
                self.server_client_socket.sendall(d.encode())

            #print("Sending...")

    '''Oryginal
    def get_streamed_vid_thread2(self, sample_surface):
        print("Start2")
        data = b""
        buf = None
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload_size = struct.calcsize("Q")
        big_payload_size = struct.calcsize("QQ")
        while True:
            while len(data) < payload_size:
                packet = self.client_socket.recv(1096)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(1096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame_max = pickle.loads(frame_data)
            #cv2.imshow("Receiving...", frame_max)
            key = cv2.waitKey(10)
            while len(data) < payload_size:
                packet = self.client_socket.recv(1096)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(1096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame_min = pickle.loads(frame_data)
            #cv2.imshow("Rec", frame_min)
            guiEye.put_vid_on_screen(sample_surface, frame_max, frame_min, self.mind_pointx, self.mind_pointy)
            ke = cv2.waitKey(10)
            if ke == 13:
                break
        self.client_socket.close()
        #self.client_socket.close()
        '''

    def get_streamed_vid_thread2(self, sample_surface):
        print("Start2")
        data = b""
        buf = None
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload_size = struct.calcsize("Q")
        big_payload_size = struct.calcsize("QQ")
        while True:
            while len(data) < big_payload_size:
                packet = self.client_socket.recv(8096)
                if not packet: break
                data += packet
            packed_msg_size = data[:big_payload_size]
            data = data[big_payload_size:]
            msg = struct.unpack("Q I I", packed_msg_size)
            msg_size = msg[0]
            self.mind_pointx = msg[1] - 300
            self.mind_pointy = msg[2] - 300
            while len(data) < msg_size:
                data += self.client_socket.recv(8096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame_max = pickle.loads(frame_data)
            #cv2.imshow("Receiving...", frame_max)
            key = cv2.waitKey(10)
            while len(data) < payload_size:
                packet = self.client_socket.recv(8096)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(8096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame_min = pickle.loads(frame_data)
            #cv2.imshow("Rec", frame_min)
            frame_max = cv2.resize(frame_max,(1200, 1000))
            guiEye.put_vid_on_screen(sample_surface, frame_max, frame_min, self.mind_pointx, self.mind_pointy)
            ke = cv2.waitKey(10)
            if ke == 13:
                break
        self.client_socket.close()
        #self.client_socket.close()

    def testClient(self):
        client_socket = self.create_socket()
        self.getting_server_connect(client_socket, HOST, PORT)


if __name__ == "__main__":
    client = Client(HOST, PORT, PORT_CLIENT)
    data = client.get_titles()
    #data = ['taniec_na_lodzie.mp4', 'taniec_na_sniegu.mp4']
    client.send_chosen_title(0, data)
    #client.send_mindpoint_and_pause()
    #client.get_streamed_vid_thread2()

    thread1 = threading.Thread(target=client.send_mindpoint_and_pause_thread1)
    #thread2 = threading.Thread(target=client.get_streamed_vid_thread2)

    thread1.start()
    #thread2.start()

    client.get_streamed_vid_thread2()

    thread1.join()
    #thread2.join()
    #client.testClient()
