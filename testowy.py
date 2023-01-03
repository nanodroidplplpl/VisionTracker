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

al = 1200
bl = 0
sl = 0
fl = 0
ap = 1000
bp = 0
sp = 0
fp = 0

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    print(str(left_pupil))
    if al >= int(left_pupil[0]):
        al = int(left_pupil[0])

    if bl <= int(left_pupil[0]):
        bl = int(left_pupil[0])

    sl = bl-al
    print("roznica = " + str(sl) + " max: " + str(bl) + " min: " + str(al))
    fl = (bl-left_pupil[0])*1000
    if fl == 0:
        fl = 1
    print("Obliczone f: "+str(fl))
    if sl == 0:
        sl = 1
    fl = fl/sl
    print("Obliczone: "+str(fl))

    if ap >= int(left_pupil[1]):
        ap = int(left_pupil[1])

    if bp <= int(left_pupil[1]):
        bp = int(left_pupil[1])

    sp = bp-ap
    print("roznica = " + str(sp) + " max: " + str(bp) + " min: " + str(ap))
    fp = (bp-left_pupil[1])*1000
    if fp == 0:
        fp = 1
    print("Obliczone f: "+str(fp))
    if sp == 0:
        sp = 1
    fp = fp/sp
    print("Obliczone: "+str(fp))

    sample_surface.fill("BLACK")
    pygame.draw.circle(sample_surface, color, (round_int(fl), 1000 - round_int(fp)), 20)

    pygame.display.flip()

    if cv2.waitKey(1) == 27:
        break



webcam.release()
cv2.destroyAllWindows()

