import cv2
import numpy


# przyjmuje to co wypluje cap = cv2.VideoCapture("film.mp4")
'''
def get_part_of_img(img, x, y, size_x, size_y):
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
'''
def get_part_of_img(frame, y, x, size_y, size_x):
    return frame[y - size_y:y + size_y, x - size_x:x + size_x]

def make_low_quality():
    import cv2

    # Open the video file
    cap = cv2.VideoCapture("chinczyk_na_wrotkach.mp4")

    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the codec information of the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Set the output file name and location
    output_file = "chinczyk_na_wrotkach2.mp4"

    # Set the output video dimensions
    width = 1200
    height = 1000

    # Create a VideoWriter object
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        if not ret:
            # If the video is over, break out of the loop
            break

        # Resize the frame to the desired dimensions
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)

        # Write the frame to the output file
        out.write(frame)

    # Release the resources
    cap.release()
    out.release()


if __name__ == '__main__':
    make_low_quality()
    '''
    cap = cv2.VideoCapture("chinczyk_na_wrotkach.mp4")
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video file")

    # Read until video is completed
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # Display the resulting frame
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
    '''

