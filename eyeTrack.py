# Modol odpowiedzialny za znajdowanie pozycji galek ocznych i umieszczanie ich na ekranie

from time import sleep, time

import cv2
from pygame import event
import numpy as np

from GazeTracking.gaze_tracking import GazeTracking
import pygame

def round_int(x):
    if x in [float("-inf"),float("inf")]: return float("nan")
    return int(round(x))

def configCum(webcam, gaze, sample_surface,al, bl, sl, fl, el, ap, bp, sp, fp, ep):
    po_konf = False
    po_konfl, po_konfp, po_konfg, po_konfd = False, False, False, False
    print("Dupa1")

    while True:
        for event in pygame.event.get():
            # Konfiguracja
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("Dupa")
                    _, frame = webcam.read()
                    gaze.refresh(frame)
                    frame = gaze.annotated_frame()
                    left_pupil = gaze.pupil_left_coords()
                    right_pupil = gaze.pupil_right_coords()
                    bl = int(left_pupil[0])
                    print("al: " + str(bl))
                    po_konfl = True
                    sample_surface.fill("RED")
                    pygame.display.flip()
                    sleep(0.5)
                    sample_surface.fill("BLACK")
                    pygame.display.flip()
                if event.key == pygame.K_RIGHT:
                    _, frame = webcam.read()
                    gaze.refresh(frame)
                    frame = gaze.annotated_frame()
                    left_pupil = gaze.pupil_left_coords()
                    right_pupil = gaze.pupil_right_coords()
                    al = int(left_pupil[0])
                    print("bl: " + str(al))
                    po_konfp = True
                    sample_surface.fill("RED")
                    pygame.display.flip()
                    sleep(0.5)
                    sample_surface.fill("BLACK")
                    pygame.display.flip()
                if event.key == pygame.K_UP:
                    _, frame = webcam.read()
                    gaze.refresh(frame)
                    frame = gaze.annotated_frame()
                    left_pupil = gaze.pupil_left_coords()
                    right_pupil = gaze.pupil_right_coords()
                    ap = int(left_pupil[1])
                    print("ap: " + str(ap))
                    po_konfg = True
                    sample_surface.fill("RED")
                    pygame.display.flip()
                    sleep(0.5)
                    sample_surface.fill("BLACK")
                    pygame.display.flip()
                if event.key == pygame.K_DOWN:
                    _, frame = webcam.read()
                    gaze.refresh(frame)
                    frame = gaze.annotated_frame()
                    left_pupil = gaze.pupil_left_coords()
                    right_pupil = gaze.pupil_right_coords()
                    bp = int(left_pupil[1])
                    print("bp: " + str(bp))
                    po_konfd = True
                    sample_surface.fill("RED")
                    pygame.display.flip()
                    sleep(0.5)
                    sample_surface.fill("BLACK")
                    pygame.display.flip()

        if po_konfl and po_konfp and po_konfg and po_konfd:
            po_konf = True
            print("juz")
            return al, bl, sl, fl, el, ap, bp, sp, fp, ep, po_konfl

def get_nose_pos(webcam):
    nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
    ds_factor = 0.5

    if nose_cascade.empty():
        raise IOError('Unable to load the nose cascade classifier xml file')

    ret, frame = webcam.read()
    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
    xd, yd = 0, 0
    for (x, y, w, h) in nose_rects:
        # print("x: "+str(x)+"y: "+str(y))
        xd = int(x)
        yd = int(y)
        break
    return xd, yd # 0 -dla poziomego a 1 dla pionowego

def get_eye_mindpoint(webcam, gaze, sample_surface, al, bl, sl, fl, el, ap, bp, sp, fp, ep):
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    left_pupi = gaze.pupil_left_coords()
    right_pupi = gaze.pupil_right_coords()
    if left_pupi is not None or right_pupi is not None:
        left_pupil = left_pupi
        right_pupil = right_pupi
        el, ep = int(left_pupil[0]), int(left_pupil[1])
    else:
        el, ep = 600, 500

    #print(str(right_pupil))
    #xlupdate, xpupdate = get_nose_pos(webcam)
    # wyznaczenie nowych skali dla oczu
    #zl = xlupdate - xl
    #zp = xpupdate - xp

    #zl = (-1) * zl
    #print("Nos x: " + str(zl) + " y: " + str(zp))

    # al = al + zl
    # ap = ap - zp
    # bl = bl + zl
    # bp = bp - zp
    # kiedy oczy wyjda po za skale to wbijamy je w standard
    if el < al:
        el = al
    elif el > bl:
        el = bl

    if ep < ap:
        ep = ap
    elif ep > bp:
        ep = bp

    sl = bl - al
    #print("roznica = " + str(sl) + " max: " + str(bl) + " min: " + str(al) + " el: " + str(el))
    fl = (bl - el) * 1000
    if fl == 0:
        fl = 1
    # print("Obliczone f: " + str(fl))
    if sl == 0:
        sl = 1
    fl = fl / sl
    #print("Obliczone: " + str(fl))

    sp = bp - ap
    # print("roznica = " + str(sp) + " max: " + str(bp) + " min: " + str(ap))
    fp = (bp - ep) * 1000
    if fp == 0:
        fp = 1
    # print("Obliczone f: " + str(fp))
    if sp == 0:
        sp = 1
    fp = fp / sp
    # print("Obliczone: " + str(fp))

    # fl = fl + zl*10
    #print("Obliczone fl: " + str(fl) + " i zl: " + str(zl))

    return round_int(fl), 1000 - round_int(fp)

def test_eye_racking(webcam, gaze, sumple_surface):
    al, bl, sl, fl, el = 0, 0, 0, 0, 0
    ap, bp, sp, fp, ep = 0, 0, 0, 0, 0
    zl, xl, xlupdate = 0, 0, 0
    zp, xp, xpupdate = 0, 0, 0

    po_konf = False
    po_konfl, po_konfp, po_konfg, po_konfd = False, False, False, False
    print("Dupa1")

    while True:
        # wstepna konfiguracja
        xlupdate, xpupdate = get_nose_pos(webcam)
        xl, xp = xlupdate, xpupdate
        print("Pozycja nosa: " + str(xl), str(xp))
        al, bl, sl, fl, el, ap, bp, sp, fp, ep, po_konf = configCum(webcam, gaze, sumple_surface, al, bl, sl, fl, el, ap, bp, sp, fp, ep)
        # xl, xp = getNosePos(webcam)
        if po_konf:
            while True:
                fl, fp = get_eye_mindpoint(webcam, gaze, sumple_surface,al, bl, sl, fl, el, ap, bp, sp, fp, ep)
                # fp = fp + zp
                sample_surface.fill("BLACK")
                pygame.draw.circle(sample_surface, color, (fl, fp), 20)

                pygame.display.flip()
                # sleep(0.5)

        if cv2.waitKey(1) == 27:
            break

if __name__ == "__main__":
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    pygame.init()
    sample_surface = pygame.display.set_mode((1200, 1000))
    color = (255, 255, 0)

    test_eye_racking(webcam, gaze, sample_surface)

    webcam.release()
    cv2.destroyAllWindows()