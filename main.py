import cv2
from pygame import event

from GazeTracking.gaze_tracking import GazeTracking
import pygame

def round_int(x):
    if x in [float("-inf"),float("inf")]: return float("nan")
    return int(round(x))

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

pygame.init()
sample_surface = pygame.display.set_mode((1200,1000))
color = (255,255,0)

def main():
    al, bl, sl, fl, el = 0, 0, 0, 0, 0
    ap, bp, sp, fp, ep = 0, 0, 0, 0, 0

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
                    print("al: "+str(bl))
                    po_konfl = True
                if event.key == pygame.K_RIGHT:
                    _, frame = webcam.read()
                    gaze.refresh(frame)
                    frame = gaze.annotated_frame()
                    left_pupil = gaze.pupil_left_coords()
                    right_pupil = gaze.pupil_right_coords()
                    al = int(left_pupil[0])
                    print("bl: " + str(al))
                    po_konfp = True
                if event.key == pygame.K_UP:
                    _, frame = webcam.read()
                    gaze.refresh(frame)
                    frame = gaze.annotated_frame()
                    left_pupil = gaze.pupil_left_coords()
                    right_pupil = gaze.pupil_right_coords()
                    ap = int(left_pupil[1])
                    print("ap: " + str(ap))
                    po_konfg = True
                if event.key == pygame.K_DOWN:
                    _, frame = webcam.read()
                    gaze.refresh(frame)
                    frame = gaze.annotated_frame()
                    left_pupil = gaze.pupil_left_coords()
                    right_pupil = gaze.pupil_right_coords()
                    bp = int(left_pupil[1])
                    print("bp: " + str(bp))
                    po_konfd = True

        if po_konfl and po_konfp and po_konfg and po_konfd:
            po_konf = True
            print("juz")

        #print("Czekam")

        if po_konf:
            while True:
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

                print(str(right_pupil))
                el, ep = int(left_pupil[0]), int(left_pupil[1])
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
                print("roznica = " + str(sl) + " max: " + str(bl) + " min: " + str(al))
                fl = (bl - el) * 1000
                if fl == 0:
                    fl = 1
                print("Obliczone f: " + str(fl))
                if sl == 0:
                    sl = 1
                fl = fl / sl
                print("Obliczone: " + str(fl))

                sp = bp - ap
                print("roznica = " + str(sp) + " max: " + str(bp) + " min: " + str(ap))
                fp = (bp - ep) * 1000
                if fp == 0:
                    fp = 1
                print("Obliczone f: " + str(fp))
                if sp == 0:
                    sp = 1
                fp = fp / sp
                print("Obliczone: " + str(fp))

                sample_surface.fill("BLACK")
                pygame.draw.circle(sample_surface, color, (round_int(fl), 1000 - round_int(fp)), 20)

                pygame.display.flip()

        if cv2.waitKey(1) == 27:
            break


main()

webcam.release()
cv2.destroyAllWindows()

