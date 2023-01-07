import cv2
import numpy


# przyjmuje to co wypluje cap = cv2.VideoCapture("film.mp4")
def get_part_of_img(img, x, y, size_x, size_y) -> (numpy.ndarray, int, int, int, int):
    #ret, img = cap.read()
    part = None
    x = int(x)
    y = int(y)
    size_x = int(size_x)
    size_y = int(size_y)
    rowsy, colsx, channels = img.shape
    if y - (size_y / 2) < 0:
        part = img[0:size_y, 0:colsx]
    elif y + (size_y / 2) > rowsy:
        prat = img[int(rowsy - size_y):rowsy, 0:colsx]
    else:
        prat = img[int(y - size_y / 2):int(y + size_y / 2), 0:colsx]

    if x - (size_x / 2) < 0:
        part = img[0:size_y, 0:size_x]
    elif x + (size_x / 2) > colsx:
        part = img[0:size_y, int(colsx - size_x):colsx]
    else:
        part = img[0:size_y, int(x - size_x / 2):int(y + size_x / 2)]
    #cv2.imshow("Obraz...", part)
    return part


if __name__ == '__main__':
    cap = cv2.VideoCapture("taniec_na_lodzie.mp4")
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video file")

    # Read until video is completed
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # Display the resulting frame
            frame = frame[200-150:200+150, 200-150:200+150]
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

