# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 17:44:48 2015

@author: Gatti
"""


import pydicom 
import os 
import glob
import numpy 
import pylab 


def SeriesRead (exam, series):
        directory = 'exam_' + str(exam) + '/Ser' + str(series)
        os.chdir(directory) 
        images = glob.glob('E*S*I*.MR.dcm')
        noImages = len(images)
        ImageLoop = range(0, noImages)
        slices = noImages/8
        #dataset = np.matrix(np.zeros([256, 256, noImages]))
        
        for x in ImageLoop:
            if x == 0:
               slice = pydicom.read_file(images[x])        
               sliceData = slice.pixel_array  
               dataset = sliceData
            else:
                slice = pydicom.read_file(images[x]) 
                sliceData = slice.pixel_array
                dataset = numpy.dstack((dataset, sliceData))
        return dataset

exam = raw_input("Enter exam number, for practice (3657): ")
series = raw_input ("Enter seris numner, for this person (3): ")    

os.chdir('/Volumes/Anthony.Gatti_MacintoshHD/Users/Gatti/Desktop/T2_map_testing/')

T2data = SeriesRead (exam, series)
plt.bone()
for y in (range (1, slices)):
    slice = ((8*y)-7)    
    pylab.imshow(T2data[:,:,slice], cmap=pylab.cm.bone)
    pylab.figure(y+1)
    







