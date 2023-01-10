import pygame
import cv2
import PySimpleGUI as sg
import client


def put_vid_on_screen(sample_surface, frame_max, frame_min, x, y):
    if frame_max.size != 0 and frame_min.size != 0:
        frame_max = cv2.cvtColor(frame_max, cv2.COLOR_BGR2RGB)
        frame_min = cv2.cvtColor(frame_min, cv2.COLOR_BGR2RGB)

        frame_max = cv2.rotate(frame_max, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_min = cv2.rotate(frame_min, cv2.ROTATE_90_COUNTERCLOCKWISE)

        frame_max = pygame.surfarray.make_surface(frame_max)
        frame_min = pygame.surfarray.make_surface(frame_min)


        sample_surface.blit(frame_max, (0, 0))
        sample_surface.blit(frame_min, (x, y))
        pygame.display.flip()

def dump_gui(data):
    dat = ['Pobierz tytuly']
    num_buttons = 2
    layout = [*[[sg.Button(i), ] for i in dat],
              [sg.Button('Pauza'), sg.Button('Exit')]]

    location = (600, 600)
    window = sg.Window('Window Title', location=location).Layout(layout)

    num_buttons = 2
    while True:  # Event Loop
        event, values = window.Read()
        print(event, values)
        if event is None or event == 'Exit':
            break
        if event == 'Pobierz tytuly' or event == 'Delete Rows':
            num_buttons += -2 if event == 'Delete Rows' else 2

            layout = [*[[sg.Button(i), ] for i in data],
                      [sg.Button('Pauza'), sg.Button('Exit')]]
            window1 = sg.Window('Window Title', location=location).Layout(layout)
            window.Close()
            window = window1

    window.Close()

if __name__ == '__main__':
    #data =['cos1', 'cos2']
    #dump_gui(data)
    # Ścieżka do nagrania mp4
    video_path = 'taniec_na_lodzie.mp4'

    # Otwórz nagranie
    cap = cv2.VideoCapture(video_path)

    # Pętla odtwarzająca nagranie
    while True:
        # Pobierz klatkę z nagrania
        ret, frame = cap.read()

        # Jeśli nie udało się pobrać klatki (koniec nagrania), zakończ pętlę
        if not ret:
            break

        # Wyświetl klatkę
        cv2.imshow('Video', frame)

        # Jeśli naciśnięto klawisz 'q', zakończ odtwarzanie
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Zakończ odtwarzanie
    cap.release()
    cv2.destroyAllWindows()