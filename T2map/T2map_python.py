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
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
import time 
   
# call in all of the images from the exam of interest and the series that 
#has the T2 data. Put all of the images into a 3D matrix 
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
               first_slice = pydicom.read_file(images[x])        
               sliceData = first_slice.pixel_array
               dataset = sliceData
               Echos = first_slice.EchoTime
               EchoTime = Echos
            else:
                slice = pydicom.read_file(images[x]) 
                sliceData = slice.pixel_array
                dataset = numpy.dstack((dataset, sliceData))
                Echos = slice.EchoTime
                EchoTime = numpy.hstack((EchoTime, Echos))
        return (dataset, slices, EchoTime, first_slice)

#take the data from the 3D matrix and put them into a 4D matrix where 
#D1= y, D2 = x, D3 = slice, D4 = echo.         
def fourD (numsl, echos, T2data, TE):
    fourD = numpy.zeros(shape=(256,256,numsl,echos))
    EchoTimes = numpy.zeros(shape=(echos))
    for sl in (range(1, numsl+1)):
        for te in (range(1, echos+1)):
            image = ((echos*(sl-1))+(te-1))
            fourD [:,:, sl-1, te-1] = T2data [:,:,image]
            
            if sl == 1:
                EchoTimes [te-1] = EchoTime[image]  
    return (fourD, EchoTimes)

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata

    # assign global variable to access outside of function
    global coords
    coords.append((ix, iy))

    # Disconnect after 2 clicks
    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)
        plt.close(1)
    return coords    

def roi(coords):    
    click1 = coords[0]
    click2 = coords[1]
    xx1 = int (click1[0])
    xx2 = int (click2[0])
    yy1 = int (click1[1])
    yy2 = int (click2[1])

    vecx = [xx1, xx1, xx2, xx2, xx1]
    vecy = [yy1, yy2, yy2, yy1, yy1] 

    return(vecx, vecy, xx1, xx2, yy1, yy2)

def func(TE, PD, T2):
    return PD*numpy.exp(-TE/T2)

def t2Relax(numsl, zoom, T2, PD, Rsq):
    for z in range(0, numsl):
        t = time.time()
        for y in range (0, zoom.shape[0]):
            for x in range (0, zoom.shape[1]):
                S = numpy.squeeze(zoom[y,x,z,:])
            
                if S[1] < 400:
                    T2[y,x,z] = 0
                    PD[y,x,z] = 0
                    Rsq[y,x,z] = 0
                elif S[1] > 3000:
                    T2[y,x,z] = 0
                    PD[y,x,z] = 0
                    Rsq[y,x,z] = 0
                else:
                    popt, pcov = curve_fit(func, EchoTimes, S)
                    T2[y,x,z] = popt[1]
                    PD[y,x,z] = popt[0]
                    Rsq[y,x,z] = 0
                    if T2[y,x,z] >100: # show values much closer to the real T2
                        T2[y,x,z] = 0
                        PD[y,x,z] = 0
                        Rsq[y,x,z] = 0
                    elif T2[y,x,z] <0:
                        T2[y,x,z] = 0
                        PD[y,x,z] = 0
                        Rsq[y,x,z] = 0
                    
        elapsed = time.time() - t
        print z    
        print elapsed
    return(T2, PD, Rsq)

exam = raw_input("Enter exam number, for practice (3657): ")
series = raw_input ("Enter seris numner, for this person (3): ")    
echos = 8
os.chdir('/Volumes/Anthony.Gatti_MacintoshHD/Users/Gatti/Desktop/T2_map_testing/')

T2data, numsl, EchoTime, T2export= SeriesRead (exam, series)

fourD, EchoTimes = fourD(numsl, echos, T2data, EchoTime)
          
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

coords = [(55.3445, 58.8333), (191.5, 207.5)]

vecx, vecy, x1, x2, y1, y2 = roi (coords)

#display the ROI that was selected 
implot = plt.imshow(fourD[:,:, numsl/4, 1])
plt.plot(vecx, vecy, c='r', linewidth=2)
plt.show()

# extract data from the ROI selected in the previous steps. Only analyze this.
#zoom = fourD[(range (y1, y2)), :,:,:]
#zoom = zoom[:, (range (x1, x2)),:,:]

zoom= numpy.zeros(shape=(y2-y1, x2-x1, numsl, echos))
zoom[:,:,:,:] = fourD[y1:y2, x1:x2,:,:]

# pre-allocate arrays for the T2/PD/Rsq data
T2 = numpy.zeros(shape=(zoom.shape[0], zoom.shape[1], zoom.shape[2]))
PD = numpy.zeros(shape=(zoom.shape[0], zoom.shape[1], zoom.shape[2]))
Rsq = numpy.zeros(shape=(zoom.shape[0], zoom.shape[1], zoom.shape[2]))

T2, PD, Rsq = t2Relax(numsl, zoom, T2, PD, Rsq)

T2new = numpy.zeros(shape=(T2data.shape[0], T2data.shape[1], numsl))
PDnew = numpy.zeros(shape=(T2data.shape[0], T2data.shape[1], numsl))
Rsqnew = numpy.zeros(shape=(T2data.shape[0], T2data.shape[1], numsl))

#ydimension = range(y1,y2+1)
#xdimension = range(x1, x2+1)
T2new[y1:y2, x1:x2, :] = T2[:,:,:]

#T2export

#pydicom.filewriter.write_file(T2export, T2new)
#pydicom.filewriter.dataset.save_as

for y in (range (0, (numsl))):   
    plt.imshow(T2new[:,:,y], cmap=pylab.cm.bone)
    plt.show()
            
            
#guess = (1500, 30)           
#popt, pcov = curve_fit(func, EchoTimes, zoom[50,50,6,:], guess)

#popt, pcov = curve_fit(func, EchoTimes, zoom[50,50,6,:])