""" This module handles getting camera inputs and stuff """
import cv2 as cv


def webcam_window():
    # connecting to webcam
    capture = cv.VideoCapture(0)

    if not capture.isOpened():
        print('Cannot Open Camera')
        exit()

    while True:
        isTrue, frame = capture.read()

        if not isTrue:
            print('Failed to grab frame')
            break

        cv.imshow('Webcam Feed', frame)

        # breaks loop with 'q' key press
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Done execution and clean up
    capture.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    webcam_window()
    