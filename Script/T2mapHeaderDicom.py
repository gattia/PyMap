# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:54:50 2015

@author: gatti
"""

from exportDicomHeader import *
from selectROI import *
from T2calc import *
from importDicomHeader import *
import os
import pylab 
import matplotlib.pyplot as plt


exam = raw_input("Enter exam number, for practice (3657): ")
series = raw_input ("Enter seris numner, for this person (3): ")    
noEchos = int (raw_input ("How many echoes are there?"))
name = raw_input("What would you like to name the output images?")
os.chdir('/Volumes/Gatti_Files/Users/Gatti/Desktop/T2_related_Playing/T2_map_testing')


ArrayDicom, echoTimes, ConstPixelDims, RefDs,header = DicomRead (exam, series, noEchos)  #import dicom files into big 3D matrix
fourD = fourD(ArrayDicom, ConstPixelDims) #turn 3D into 4D matrix accounting for echo times

numsl = ConstPixelDims[2]

print '''****************************************************************
An image will appear. First, click in the center of the image to bring
is to the front of your screen and to initiate; second click the top left 
hand corer of the ROI; third, clock the bottom right hand corner of the 
ROI. If done correctly, the figure should disappear & a new figure
with a red box around your ROI should appear, close this figure to cont.'''

#Show an image from the medial side of the knee and select the ROI 
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.imshow(fourD[:,:, numsl/4, 1])
coords = []
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show(1)

print coords

coords = [(55.3445, 58.8333), (191.5, 207.5)] #needs to be inputted when using iPython

vecx, vecy, x1, x2, y1, y2 = roi (coords)

#display the ROI that was selected 
implot = plt.imshow(fourD[:,:, numsl/4, 1])
plt.plot(vecx, vecy, c='r', linewidth=2)
plt.show()

# extract data from the ROI selected in the previous steps. Only analyze this.

zoom = numpy.zeros(shape=(y2-y1, x2-x1, numsl, noEchos))
zoom[:,:,:,:] = fourD[y1:y2, x1:x2,:,:]

T2, PD, Rsq = t2Relax(ConstPixelDims, zoom)

#pre-allocate maps
T2map = numpy.zeros(ConstPixelDims[0:3], ArrayDicom.dtype)
PDmap = numpy.zeros(ConstPixelDims[0:3], ArrayDicom.dtype)
Rsqmap = numpy.zeros(ConstPixelDims[0:3], ArrayDicom.dtype)


T2map[y1:y2, x1:x2, :] = T2[:,:,:]

for y in (range (0, (numsl))):   
    plt.imshow(T2map[:,:,y])  #, cmap=pylab.cm.bone
    plt.show()        

os.chdir('/Volumes/Gatti_Files/Users/Gatti/Desktop/T2_related_Playing/T2_map_testing')
os.mkdir(name)

writeDicom(RefDs, T2map, name, header)