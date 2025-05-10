""" This module handles getting camera inputs and stuff """
import cv2 as cv
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def detect_pose():
    """ Runs the pose detection pipeline """
    # connecting to webcam
    capture = cv.VideoCapture(0)

    # if camera cannot be opend
    if not capture.isOpened():
        print('Cannot Open Camera')
        exit()

    # mediapipe instances
    # min_detection_confidence and min_tracking_confidence affects the accuracy of the pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        while True:
            isTrue, frame = capture.read()

            if not isTrue:
                print('Failed to grab frame')
                break

            # Recolor image (BGR -> RGB)
            image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            # helps save memory (idk why but followed tutorial)
            image.flags.writeable = False

            # makes detection by accessing pose model -> stores it in an array
            results = pose.process(image)

            # Recoloring image back to BGR format so CV can render it
            image.flags.writeable = True
            image = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

            # Rendering pose
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv.imshow('Webcam Feed', image)

            # breaks loop with 'q' key press
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        # Done execution and clean up
        capture.release()
        cv.destroyAllWindows()



if __name__ == "__main__":
    detect_pose()
