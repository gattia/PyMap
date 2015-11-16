# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:45:04 2015

@author: gatti
"""

import pydicom
import os
import numpy
import glob
from natsort import natsorted
import scipy 

exam = 3657
series = 3
noEchos = 8 


os.chdir('/Volumes/Gatti_Files/Users/Gatti/Desktop/T2_related_Playing/T2_map_testing')

def DicomRead (exam, series, noEchos):
    #Call in the images within the exam and series of interest
    directory = 'exam_' + str(exam) + '/Ser' + str(series)
    os.chdir(directory)
    listFilesDCM = natsorted(glob.glob('E*S*I*.MR.dcm'))
    #Get the reference information from the very first image of that list of images    
    RefDs = pydicom.read_file(listFilesDCM[0])  #Stored ref file 
    #Import array dims are the dimensions of the imported 3D array. ConstPixelDims are the dimensions of the 4D matrix (row, column, slice, echo)
    #spacing is the size of each voxel in 3D space along the three axes.    
    ImportArrayPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(listFilesDCM)) #Dimensions of rows, columns, slicers
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), int(len(listFilesDCM)/noEchos), noEchos)
    ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))  #spacing values (mm)
    
    #these are a list of the dimensions. Not used at the moment. 
    x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
    y = numpy.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
    z = numpy.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])  
    
    #Below seciont of cose will import each dcm in the folder of interest. The array data is all saved to ArrayDicom. 
    #The header data is all saved to header.X where X is the image of interest
    #The first Y echoes are saved so echos, where Y is the number of echos for each slice.     
    ArrayDicom = numpy.zeros(ImportArrayPixelDims, dtype=RefDs.pixel_array.dtype)    
    echoTimes =[]
    class container:
        pass
    header = container()
    for filenameDCM in listFilesDCM:
        ds = pydicom.read_file(filenameDCM)
        ArrayDicom[:,:,listFilesDCM.index(filenameDCM)] = ds.pixel_array
        echoTimes = numpy.hstack((echoTimes, ds.EchoTime))
        echos = echoTimes[0:noEchos]
    for image in range (0, len(listFilesDCM)):
        ds = pydicom.read_file(listFilesDCM[image])
        header.image = ds 
    return(ArrayDicom, echos, ConstPixelDims, RefDs, header)

#fourD was created to turn the 3D matrix that was imported from the folder into a 4D matrix
#The fourth dimenions is echotime. This allways easy accessing of data based on spacial location 
#as well as based on the acquisition echotime. 
def fourD (ArrayDicom, ConstPixelDims):
    numsl = ConstPixelDims[2]
    echos = ConstPixelDims[3]
    fourD = numpy.zeros(shape=(ConstPixelDims[0],ConstPixelDims[1],ConstPixelDims[2],ConstPixelDims[3]))
    for sl in (range(1, numsl+1)):
        for te in (range(1, echos+1)):
            image = ((echos*(sl-1))+(te-1))
            fourD [:,:, sl-1, te-1] = ArrayDicom [:,:,image]  
    return (fourD)

