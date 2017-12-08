import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from imutils import face_utils
import imutils
from detectSkinColor import onlyFace
import numpy as np
import dlib
import cv2
import copy

face_cascade = cv2.CascadeClassifier('../faceDetection/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('../faceDetection/haarcascade_eye.xml')
predictor = dlib.shape_predictor("../faceDetection/shape_predictor_68_face_landmarks.dat")

def face_points(gray):
    b,r = gray.shape[:2]
    rect = dlib.rectangle(left=0,top=0,right=r,bottom=b)
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    face_curve = shape[:17]
    left_eyebro = shape[17:22]
    right_eyebro = shape[22:27]
    nose = shape[27:36]
    left_eye = shape[36:42]
    right_eye = shape[42:48]
    mouth = shape[48:]
    for (x, y) in shape:
        cv2.circle(gray, (x, y), 1, (0, 0, 255), -1)
    return gray,shape

def getLEM(shape,count):
    root = Tk()
    f = Frame()
    f.master.title("Lines "+str(count))
    f.pack(fill=BOTH, expand=1)
    canvas = Canvas(f)
    for i in range(1,len(shape)):
        canvas.create_line(shape[i-1][0], shape[i-1][1], shape[i][0], shape[i][1])  
    canvas.pack(fill=BOTH, expand=1)
    root.geometry("200x200+300+300")
    root.mainloop()

for img_num in range(1,128):
    print("image",img_num)
    img = cv2.imread('../../face_images/image'+str(img_num)+'.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    file = ''
    file = open("line_edge_maps.csv",'w')

    cropped_faces = []
    for (x,y,w,h) in faces:
        roi_color = copy.copy(img[y-5:y+5+h, x-5:x+5+w])
        roi_gray = copy.copy(gray[y:y+h, x:x+w])
        eyes = []
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if(len(eyes)):
            cropped_faces.append(roi_color)
            cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)

    count = 0
    # cv2.imshow('Detected Images',gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    shape = []
    for i in cropped_faces:
        i = imutils.resize(i,width=200)
        i = onlyFace(i)
        i,shape = face_points(i)
        cv2.imshow('img'+str(count),i)
        getLEM(shape, count)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        count += 1
        y = input("Update y/n?")
        if(y=='y' or y=='Y'):
            for point in shape:
                file.write(str(point[0])+" "+str(point[1])+",")
            name = input("Give Name : ")
            file.write(name+"\n")