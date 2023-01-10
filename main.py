import eyeTrack
import client
import threading
import eyeTrack
import cv2
from GazeTracking.gaze_tracking import GazeTracking
import eyeTrack
import pygame
import eyeTrackLinear
import PySimpleGUI as sg
import guiEye

MASTER = False
SLAVE = True

layout = [
    [sg.Text("Wybierz akcje:")],
    [sg.Button('      Zakoncz dzialanie       ', key='-GCS0-')],
    [sg.Button('           Zagluszanie           ', key='-GCS1-')],
    [sg.Button('Podsluchiwanie i Detekcja', key='-GCS2-')],
    [sg.Button('            Lokalizacja           ', key='-GCS3-')],
    [sg.Button('       Wylacz BSP        ', key='-END-')],
    [sg.Text(' -> ', key="-output-")],
]

def main_dump():
    if MASTER:
        pass
    elif SLAVE:
        al, bl, sl, fl, el = 0, 0, 0, 0, 0
        ap, bp, sp, fp, ep = 0, 0, 0, 0, 0
        gaze = GazeTracking()
        webcam = cv2.VideoCapture(0)

        g = eyeTrackLinear.GazeFinder()

        pygame.init()
        sample_surface = pygame.display.set_mode((1200, 1000))
        color = (255, 255, 0)
        al, bl, sl, fl, el, ap, bp, sp, fp, ep, po_konf \
            = eyeTrack.configCum(webcam, gaze, sample_surface,al, bl, sl, fl, el, ap, bp, sp, fp, ep)
        slave = client.Client(client.HOST, client.PORT, client.PORT_CLIENT, g)
        data = slave.get_titles()
        slave.send_chosen_title(data)

        thread1 = threading.Thread(target=slave.send_mindpoint_and_pause_thread1,
                                   args=(webcam, gaze, sample_surface, al, bl, sl, fl, el, ap, bp, sp, fp, ep))

        thread1.start()

        slave.get_streamed_vid_thread2(sample_surface)

        thread1.join()

def main():
    if MASTER:
        pass
    elif SLAVE:
        al, bl, sl, fl, el = 0, 0, 0, 0, 0
        ap, bp, sp, fp, ep = 0, 0, 0, 0, 0
        gaze = GazeTracking()
        webcam = cv2.VideoCapture(0)

        pygame.init()
        sample_surface = pygame.display.set_mode((1200, 1000))
        color = (255, 255, 0)

        g = eyeTrackLinear.GazeFinder()
        start = g.calibration(sample_surface, webcam, gaze)

        slave = client.Client(client.HOST, client.PORT, client.PORT_CLIENT, g)
        data = slave.get_titles()
        #guiEye.dump_gui(data)
        slave.send_chosen_title(data)

        thread1 = threading.Thread(target=slave.send_mindpoint_and_pause_thread1,
                                   args=(webcam, gaze, sample_surface, al, bl, sl, fl, el, ap, bp, sp, fp, ep))

        thread1.start()

        slave.get_streamed_vid_thread2(sample_surface)

        thread1.join()

if __name__ == "__main__":
    main()

'''
0000000000
0000000000
0000000000
0000000000
0000000000
'''