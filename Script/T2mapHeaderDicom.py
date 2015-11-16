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

#DicomRead will read in all of the Dicom images in the folder specified by 
#the exam and series inputed. It will output a 3D array with all of the input 
#images. Though, this won't fully make sense becuase there are 8 echos for each 
#slice. This array is input into fourD to create a fourD array, where the fourth
# dimension is the echotime. Also output will be a list of the echotimes used in 
#the iamge as well as the number of pixels in each of the 3 dimensions, as well 
#as RefDs which is the inputed data from the first slice as reference and header
#which includes all of the header information for each inputed image. The first 
#image will be place @ header.1 and the second @ header.2 etc. 

ArrayDicom, echoTimes, ConstPixelDims, RefDs,header = DicomRead (exam, series, noEchos) 
fourD = fourD(ArrayDicom, ConstPixelDims) #turn 3D into 4D matrix accounting for echo times

numsl = ConstPixelDims[2]

print '''****************************************************************
An image will appear. First, click in the center of the image to bring
is to the front of your screen and to initiate; second click the top left 
hand corer of the ROI; third, clock the bottom right hand corner of the 
ROI. If done correctly, the figure should disappear & a new figure
with a red box around your ROI should appear, close this figure to cont.'''

#The next portion of code will show an image from the medial side of the knee
#where the patella is fully in view. Click where the top left corner of your 
#region of interest (ROI) is and then the bottom right corner. The image should 
#re-appear with this selected ROI. If this is wrong for some reason, re-run and
#re-select the ROI'''

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

#The region selected in the above image is extracted to zoom. 
#Only zoom will be analyzed.

zoom = numpy.zeros(shape=(y2-y1, x2-x1, numsl, noEchos))
zoom[:,:,:,:] = fourD[y1:y2, x1:x2,:,:]

#the dimensions of the image (pixels) and the zoom numpy.array are input
#into the func t2Relax and the T2, PD, and Rsq maps are supposed to be output.
#At the moment only T2 is output. 

T2, PD, Rsq = t2Relax(ConstPixelDims, zoom)


#Create arrays filled with zeros the size of the original images. 
T2map = numpy.zeros(ConstPixelDims[0:3], ArrayDicom.dtype)
PDmap = numpy.zeros(ConstPixelDims[0:3], ArrayDicom.dtype)
Rsqmap = numpy.zeros(ConstPixelDims[0:3], ArrayDicom.dtype)

#place the T2map inside of the zero-filled arrays. 
T2map[y1:y2, x1:x2, :] = T2[:,:,:]

#plot each image - this can be commented out if you don't wish to see the created T2maps. 
for y in (range (0, (numsl))):   
    plt.imshow(T2map[:,:,y])  #, cmap=pylab.cm.bone   (this code can be put back in the brackets to change th color of the image to black and white. )
    plt.show()        

#this moves to the directory that I have chosen to write my images to. This should be changed for each user. 
os.chdir('/Volumes/Gatti_Files/Users/Gatti/Desktop/T2_related_Playing/T2_map_testing')
os.mkdir(name)
os.chdir(name)

#write dicom files for each slice of the T2map. 
writeDicom(RefDs, T2map, name, header)