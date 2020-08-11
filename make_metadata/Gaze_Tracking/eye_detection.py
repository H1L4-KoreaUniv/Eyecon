# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 23:16:11 2020

@author: 이다혜
"""

import cv2
import Gaze_Tracking
from Gaze_Tracking.gaze_tracking import GazeTracking

gaze = GazeTracking()
# webcam = cv2.VideoCapture(0)

# load image and get coordinates of eyes
def detect_eye(frame):
    frame = frame
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)
    
    frame = gaze.annotated_frame()
    text = ""
    
    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"
    
    # cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
   
    # cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    # cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    
    return [left_pupil, right_pupil]
    # cv2.imshow("Demo", frame)
    # print(left_pupil, right_pupil)
    # if cv2.waitKey(1) == 27:
        # cv2.destroyAllWindow()
