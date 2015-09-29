# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 17:44:48 2015

@author: Gatti
"""


import pydicom 
import os 
import glob

def SeriesRead (exam, series):
        directory = 'exam_' + str(exam) + '/Ser' + str(series)
        os.chdir(director) 
        images = glob.glob('E*S*I*.MR.dcm')
        noImages = len(images)
        ImageLoop = range(0, noImages)

exam = 3657
series = 3    

os.chdir('/Volumes/Anthony.Gatti_MacintoshHD/Users/Gatti/Desktop/T2_map_testing/')

directory = 'exam_' + str(exam) + '/Ser' + str(series)
os.chdir(directory) 
images = glob.glob('E*S*I*.MR.dcm')
noImages = len(images)
ImageLoop = range(0, noImages)

for x in ImageLoop:
    slice = pydicom.read_file(images[x]) 
    sliceData = dataset.pixel_array
    dataset = sliceData[:,:,x]

    
    
    
    







