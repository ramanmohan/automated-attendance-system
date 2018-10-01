#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:23:24 2018

@author: rajesh

"""
from __future__ import _raman print_function
from imutils.video import WebcamVideoStream
from communication import serialCommunication
from mtcnn_detect import MTCNNDetect
from database import database
import cv2
import json
import numpy as np
import time
import datetime
import sys
import glob
global dictionary_list
global data_file

#serial = serialCommunication()
database = database()


def intialize_dict():
    '''
        Initialize function:
            takes care of intializing variables
            1)Loads the names of all the people in the dataset
            2)Creates a list of Dictionary with keys as Name and Count 
    '''
    f = open('./database.txt','r')
    global data_file 
    data_file = open('./data.txt','w')
    global data_set 
    data_set = json.loads(f.read())
    List = []
    for i in data_set.keys():
        name = {'Name' : i , 'count' : 0}
        List.append(name)
        #Add all the names in the list to the database
    List.append({'Name': "Unknown" , 'count' : 0})
    return List

dictionary_list= intialize_dict()
names = []

class face_Recognition:
    def __init__(self,FRGraph,aligner,extract_feature):
        self.FRGraph = FRGraph
        self.aligner = aligner
        self.extract_feature = extract_feature
        self.face_detect = MTCNNDetect(FRGraph, scale_factor=2)
        

    def add_faces(self):
        '''
            Calculates the embeddings of the face and stores it in the .txt file
            This file is later used to recognize faces
            To improve recognition rate we consider 5 different positions of the face i.e 
            1)Left 2)Right 3)Top 4)Bottom 5) Center
        '''
        count=1
        frame = cv2.imread('26.jpg')
        #cam = cv2.VideoCapture('shankar.mp4')
        print("Please input new user ID:")
        new_name = input()
        person_imgs = {"Left" : [], "Right": [], "Center": [] , "Top" :[] , "Bottom" :[]}
        person_features = {"Left" : [], "Right": [], "Center": [] , "Top" :[] , "Bottom" :[]}
        print("Please start turning slowly. Press 'q' to save and add this new user to the dataset")
        while True:
            #ret,frame = cam.read()
            if True:
                rects, landmarks = self.face_detect.detect_face(frame,20)
                if len(rects) > 0 :
                    for (i, rect) in enumerate(rects):
                        aligned_frame, pos = self.aligner.align(160,frame,landmarks[i])
                        person_imgs[pos].append(aligned_frame)
                    cv2.imshow("Captured face", aligned_frame)
                    count=count+1                   
                cv2.waitKey(1)
            else:
                break
        
        cv2.destroyAllWindows()
        '''
            Writing the embeddings to the file 
        '''
        for pos in person_imgs:
            person_features[pos] = [np.mean(self.extract_feature.get_features(person_imgs[pos]),axis=0).tolist()]
        data_set[new_name] = person_features;
        f = open('./database.txt', 'w');
        f.write(json.dumps(data_set))
    
    def recognize_Face(self):
        '''
            Recognition of the new input image
            Input is from web camera 
        '''
        #frame = cv2.imread('bhog.jpg')
        #frame = cv2.resize(frame,(640,480))
        cam =  WebcamVideoStream(src=1).start()
        prevTime = 0
        while True:
            curTime = time.time()
            frame = cam.read()
            rects, landmarks = self.face_detect.detect_face(frame,20)
            aligns = []
            positions = []
            if len(rects) > 0 :
                for (i, rect) in enumerate(rects):
                    aligned_face, face_pos = self.aligner.align(160,frame,landmarks[i])
                    aligns.append(aligned_face)
                    positions.append(face_pos)
                features_arr = self.extract_feature.get_features(aligns)
                recog_data = findPeople(features_arr,positions)
                for (i,rect) in enumerate(rects):
                    cv2.rectangle(frame,(rect[0],rect[1]),(rect[0] + rect[2],rect[1]+rect[3]),(255,0,0),3) #draw bounding box for the face
                    cv2.putText(frame,recog_data[i][0]+ "-" +str(recog_data[i][1])+"%",(rect[0],rect[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                    communicate(recog_data[i][0],dictionary_list)
                      
            sec = curTime - prevTime
            prevTime = curTime
            fps = 1 / (sec)
            string = 'FPS: %2.3f' % fps
            text_fps_x = len(frame[0]) - 150
            text_fps_y = 20
            #frame = cv2.resize(frame,(640,480))
            cv2.putText(frame, string,(text_fps_x, text_fps_y),cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), thickness=1, lineType=2)
            #cv2.imwrite('group.jpg',frame)
            cv2.imshow("Frame",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
                #cv2.destroyAllWindows()
            #database.close_connection()
        cv2.destroyAllWindows()
        cam.stop()
        data_file.close()
        
    def create_embeddings(self):
        '''
            For visualisation of the generated embeddings
        '''
        image_features_list=[]
        for img in glob.glob("/home/rajesh/Documents/my_code/Code/pics/pranav/*.jpg"):
            image = cv2.imread(img)
            frame = np.array(image)
            image_features = self.extract_feature.get_features(frame)    
            image_features_list.append(image_features)
        image_features_arr = np.asarray(image_features_list)
        image_features_arr = np.rollaxis(image_features_arr,1,0)
        image_features_arr = image_features_arr[0,:,:]

        np.savetxt('embed.txt',image_features_arr)


def findPeople(features_arr, positions, thres = 0.7, percent_thres = 70):
    
    '''
    :param features_arr: a list of 128d Features of all faces on screen
    :param positions: a list of face position types of all faces on screen
    :param thres: distance threshold
    :return: person name and percentage
    '''
    returnRes = []
    for (i,features_128D) in enumerate(features_arr):
        result = "Unknown"
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person][positions[i]]
            for data in person_data:
                distance = np.sqrt(np.sum(np.square(data-features_128D)))
                if(distance < smallest):
                    smallest = distance
                    result = person
        percentage =  int(min(100, 100 * thres / smallest))
        if percentage <= percent_thres :
            result = "Unknown"
        returnRes.append((result,percentage))
    return returnRes


def communicate(name,dict_list):
    
        #Serial Communication to the relay indicating which light to turn ON
        #para: Recognized name and the list of names in the dataset
    
    for elem in dict_list:
        if name == elem['Name']:
            elem['count'] += 1

        if elem['count'] >= 10 and elem['Name'] is not 'Unknown':
            elem['count'] = 0
            print(elem['Name'] + ' detected')
            #Thread(target=func1).start()
            #func1()
            ts=time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            database.updateTable(timestamp,name)
            data_file.write(name + '\t' + timestamp + '\n')
        elif dict_list[-1]['count'] > 10:
            dict_list[-1]['count'] = 0
            #Thread(target=func2).start()
            #func2()

def func1():    
        #To serially communicate when face detected is in the dataset    
    serial.detected()    
    
    
def func2():    
        #To serially communicate when face detetced is not in the dateset    
    serial.unknown()

    
        
    
    
    
