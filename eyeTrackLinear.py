from time import sleep

import pygame
import cv2

import numpy as np

from GazeTracking.gaze_tracking import GazeTracking


class GazeFinder:
    gaze = None
    data_x = None
    data_y = None
    count = 0
    b0x, b1x, b2x, b3x = 0, 0, 0, 0
    b0y, b1y, b2y, b3y = 0, 0, 0, 0
    array_len = None
    gaze_right = None

    hipodata = 0


    def __init__(self):
        self.data_x = np.zeros(shape=(0, 4))
        self.data_y = np.zeros(shape=(0, 4))
        self.count = 0
        self.array_len = 0
        self.gaze_right = np.zeros(shape=(0,2))

    def modol(self, x, y):
        if x - y > 0:
            return x - y
        else:
            return y - x

    def calc_avg(self):
        return (np.mean(self.data_x[:,1], axis=0), np.mean(self.data_x[:,1], axis=0),)

    def calc_avg_right(self):
        return (np.mean(self.gaze_right[:, 0], axis=0), np.mean(self.gaze_right[:, 1], axis=0),)
    def get_gaze_position(self, webcam, gaze):
        _, frame = webcam.read()
        gaze.refresh(frame)
        frame = gaze.annotated_frame()
        left_pupil = gaze.pupil_left_coords()
        if not left_pupil:
            left_pupil = self.calc_avg()
        return left_pupil[0], left_pupil[1]

    def get_face_distance(self, webcam, gaze):
        _, frame = webcam.read()
        gaze.refresh(frame)
        frame = gaze.annotated_frame()
        left_pupil = gaze.pupil_left_coords()
        if not left_pupil:
            left_pupil = self.calc_avg()
        right_pupil = gaze.pupil_right_coords()
        if right_pupil:
            self.gaze_right = np.vstack([self.gaze_right, [right_pupil[0], right_pupil[1]]])
        else:
            right_pupil = self.calc_avg_right()
        return self.modol(left_pupil[0], right_pupil[0])

    def get_nose_pos(self, webcam):
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
        return xd, yd

    def add_data(self, choice_x_or_y, x_or_y, mind_point_x_or_y, distance, nose_x_or_y):
        if choice_x_or_y:
            self.data_x = np.vstack([self.data_x, [x_or_y, mind_point_x_or_y, distance, nose_x_or_y]])
        else:
            self.data_y = np.vstack([self.data_y, [x_or_y, mind_point_x_or_y, distance, nose_x_or_y]])

    def linear_regression(self):
        X = np.zeros(shape=(self.array_len, 3))
        for i in range(self.array_len):
            X[i][0] = self.data_x[i][1]
            X[i][1] = self.data_x[i][2]
            X[i][2] = self.data_x[i][3]
        yx = np.zeros(shape=(self.array_len, 1))
        for i in range(self.array_len):
            yx[i][0] = self.data_x[i][0]

        X = np.hstack([np.ones((X.shape[0], 1)), X])
        wx = np.linalg.inv(X.T @ X) @ X.T @ yx

        Y = np.zeros(shape=(self.array_len, 3))
        for i in range(self.array_len):
            Y[i][0] = self.data_y[i][1]
            Y[i][1] = self.data_y[i][2]
            Y[i][2] = self.data_y[i][3]
        yy = np.zeros(shape=(self.array_len, 1))
        for i in range(self.array_len):
            yy[i][0] = self.data_y[i][0]

        Y = np.hstack([np.ones((X.shape[0], 1)), Y])
        wy = np.linalg.inv(Y.T @ Y) @ Y.T @ yy

        self.b0x = wx[0][0]
        self.b1x = wx[1][0]
        self.b2x = wx[2][0]
        self.b3x = wx[3][0]

        self.b0y = wy[0][0]
        self.b1y = wy[1][0]
        self.b2y = wy[2][0]
        self.b3y = wy[3][0]

        print("Inna metoda: ")
        print(wx)
        print(wy)

    # gaze_x, distance, nose_x

    def get_mind_point(self, webcam, gaze):
        x, y = self.get_gaze_position(webcam, gaze)
        distance = self.get_face_distance(webcam, gaze)
        nose_x, nose_y = self.get_nose_pos(webcam)
        return self.b0x + self.b1x * x + self.b2x * distance + self.b3x * nose_x, \
               self.b0y + self.b1y * y + self.b2y * distance + self.b3y * nose_y


    def calibration(self, sample_surface, webcam, gaze):
        contine = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mind_point_x, mind_point_y = pygame.mouse.get_pos()
                    x, y = self.get_gaze_position(webcam, gaze)
                    distance = self.get_face_distance(webcam, gaze)
                    nose_x, nose_y = self.get_nose_pos(webcam)
                    self.add_data(True, mind_point_x, x, distance, nose_x)
                    self.add_data(False, mind_point_y, y, distance, nose_y)
                    # print("mind point = "+str(mind_point_x)+" x = "+str(x)+" distance = "
                    #     +str(distance)+" nose = "+str(nose_x))
                    print(str(mind_point_x) + " " + str(x) + " " + str(distance) + " " + str(nose_x))
                    self.array_len += 1
                    sample_surface.fill("RED")
                    pygame.display.flip()
                    sleep(0.5)
                    sample_surface.fill("BLACK")
                    pygame.display.flip()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.linear_regression()
                    print(
                        " b0 = " + str(self.b0x) + " b1 = " + str(self.b1x) + " b2 = " + str(self.b2x) + " b3 = " + str(
                            self.b3x))
                    print("KONIEC")

                    for i in range(self.array_len):
                        print(str(self.data_x[i][0]))
                    print("kolejne")
                    for i in range(self.array_len):
                        print(str(self.data_x[i][1]))
                    print("kolejne")
                    for i in range(self.array_len):
                        print(str(self.data_x[i][2]))
                    print("kolejne")
                    for i in range(self.array_len):
                        print(str(self.data_x[i][3]))

                    contine = True

            if contine:
                return True

    def test_tracking(self):
        gaze = GazeTracking()
        webcam = cv2.VideoCapture(0)

        pygame.init()
        sample_surface = pygame.display.set_mode((1200, 1000))
        color = (255, 255, 0)
        start = False
        while True:
            start = self.calibration(sample_surface, webcam, gaze)
            if start:
                while True:
                    fl, fp = self.get_mind_point(webcam, gaze)
                    print("x = " + str(fl) + " y = " + str(fp))

                    sample_surface.fill("BLACK")
                    pygame.draw.circle(sample_surface, color, (int(fl), int(fp)), 20)

                    pygame.display.flip()
                    # sleep(0.5)

            webcam.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    g = GazeFinder()
    g.test_tracking()
