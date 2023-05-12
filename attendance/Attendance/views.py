from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView, status
from .models import Student, Attended
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
# for the func
import cv2
import numpy as np
import face_recognition
import pickle
import os
import time
from openpyxl import Workbook

from datetime import datetime
import pandas as pd


#to show db
class AttendanceApp(generics.ListCreateAPIView):
        queryset = Student.objects.all()
        serializer_class = StudentSerializer

@api_view(['GET'])
@csrf_exempt
def face_recognize(request):
    if request.method == 'GET':

        start_time = time.time()
        # load the encoding file
        file = open('Attendance\encodefile.p', 'rb')
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
        students = []
        while True:
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)  # Flip vertically
            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                # rgb_small_frame = small_frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(small_frame)

                face_encodings = face_recognition.face_encodings(small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_incodings, face_encoding)
                    name = 'unknown'

                    faceDis = face_recognition.face_distance(known_face_incodings, face_encoding)
                    for n in faceDis:

                        if n <= 0.49:

                            # print( faceDis.argmin())
                            matchindx = np.argmin(faceDis)
                            # print(matchindx)

                            if matches [matchindx]:
                                name = known_face_names [matchindx].upper()
                                name = name.split(",")
                                # name=name[1]
                                # make the array of objects
                                names = [name [1]]
                                # dept = [name[2]]
                                # year = [name [3]]
                                sections = [name [3]]

                                for i in range(len(names)):
                                    st_data = {
                                        'name': names [i],
                                        # 'dept': dept [i],
                                        # 'year': year [i],
                                        'section': sections [i]
                                    }
                                    students.append(st_data)

                                # save_in_excel(nam)
                    face_names.append(name)

            process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # nam = name.split(",")

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
        result = []
        for i in students:
            if i not in result:
                result.append(i)

        print(result)
        cam.release()
        cv2.destroyAllWindows()
        # print(face_names)

        

            # Do a bit of cleanup
        # cam.release()
        # cv2.destroyAllWindows()

        return Response(result)
    
    

        