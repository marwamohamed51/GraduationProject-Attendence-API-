import cv2
import numpy as np
import face_recognition
import pickle
import os
import time
from openpyxl import Workbook

from datetime import datetime
import pandas as pd
import sys
# from .find_encodings import findencode

def face_recognize():
    start_time = time.time()
    # load the encoding file
    # findencode()
    file = open('encodefile.p', 'rb')
    encodelistknownwithids = pickle.load(file)
    file.close()
    known_face_incodings, known_face_names = encodelistknownwithids

    # print(students
    # )
    face_locations = []
    face_encodings = []
    face_names = []
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    process_this_frame = True

    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)  # Flip vertically
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)

            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_incodings, face_encoding)
                name = "unknown"
                faceDis = face_recognition.face_distance(known_face_incodings, face_encoding)
                matchindx = np.argmin(faceDis)
                if matches[matchindx]:
                    name = known_face_names[matchindx].upper()

                    nam = name.split(",")
                    # save_in_excel(nam)

                    print (nam)
                   

                face_names.append(name)




        process_this_frame = not process_this_frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            nam = name.split(",")

            if name == "unknown":
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "rejected", (left + 6, bottom - 6), font, 1.0, (255, 255, 0), 1)
            else:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "accepted", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.imshow('camera', frame)
        k = cv2.waitKey(10) & 0xff  # Press 'esc' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
 
    cam.release()
    cv2.destroyAllWindows()
    return nam


# createexcel()
# face_recognize()
# save_withot_dupplicate()

