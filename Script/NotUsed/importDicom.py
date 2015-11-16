# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:36:44 2015

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


os.chdir('/home/gatti/Documents/T2_Play_Images/T2_map_testing')

def DicomRead (exam, series, noEchos):
    #Call in the images within the exam and series of interest
    directory = 'exam_' + str(exam) + '/Ser' + str(series)
    os.chdir(directory)
    listFilesDCM = natsorted(glob.glob('E*S*I*.MR.dcm'))
    #Get the reference information from the very first image of that list of images    
    RefDs = pydicom.read_file(listFilesDCM[0])  #Stored ref file 
    ImportArrayPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(listFilesDCM)) #Dimensions of rows, columns, slicers
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), int(len(listFilesDCM)/noEchos), noEchos)
    ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))  #spacing values (mm)
    
    x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
    y = numpy.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
    z = numpy.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])  
    #
    ArrayDicom = numpy.zeros(ImportArrayPixelDims, dtype=RefDs.pixel_array.dtype)
    
    echoTimes =[]
    imagePosition = numpy.zeros(shape=(3))
    windowCenter = []
    windowWidth = []
    stackID = []
    acqNumber = []
    instanceNumber = []
    for filenameDCM in listFilesDCM:
        ds = pydicom.read_file(filenameDCM)
        ArrayDicom[:,:,listFilesDCM.index(filenameDCM)] = ds.pixel_array
        echoTimes = numpy.hstack((echoTimes, ds.EchoTime))
        echos = echoTimes[0:noEchos]
        imagePosition = numpy.vstack((imagePosition,map(float,ds.ImagePositionPatient)))
        windowCenter = numpy.hstack((windowCenter, ds.WindowCenter))
        windowWidth = numpy.hstack((windowWidth, ds.WindowWidth))
        stackID=numpy.hstack((stackID, ds.StackID))
        acqNumber = numpy.hstack((acqNumber, ds.AcquisitionNumber))
        intanceNumber =numpy.hstack((instanceNumber, ds.InstanceNumber))
    imagePosition = scipy.delete(imagePosition, 0,0)
    position, center, width, instance, acquisition, ID  = dicomData(ConstPixelDims, imagePosition, windowCenter, windowWidth, instanceNumber, acqNumber, stackID)
    return(ArrayDicom, echos, ConstPixelDims, RefDs, position, center, width, instance, acquisition, ID)

def fourD (ArrayDicom, ConstPixelDims):
    numsl = ConstPixelDims[2]
    echos = ConstPixelDims[3]
    fourD = numpy.zeros(shape=(ConstPixelDims[0],ConstPixelDims[1],ConstPixelDims[2],ConstPixelDims[3]))
    for sl in (range(1, numsl+1)):
        for te in (range(1, echos+1)):
            image = ((echos*(sl-1))+(te-1))
            fourD [:,:, sl-1, te-1] = ArrayDicom [:,:,image]  
    return (fourD)

def dicomData (ConstPixelDims, imagePosition, windowCenter, windowWidth, instanceNumber, acqNumber, stackID):
    numsl = ConstPixelDims[2]
    position = numpy.zeros(shape=(ConstPixelDims[2],3))
    center = numpy.zeros(ConstPixelDims[2])
    width = numpy.zeros(ConstPixelDims[2])
    instance = numpy.zeros(ConstPixelDims[2])
    acquisition = numpy.zeros(ConstPixelDims[2])
    ID = numpy.zeros(ConstPixelDims[2])
    
    for sl in (range(0,numsl)):
        image = (sl*8)
        position [sl,0:3] = imagePosition[image]
        center [sl] = windowCenter[image]
        width [sl] = windowWidth[image]
        instance[sl] = instanceNumber[image]
        acquisition[sl] = acqNumber[image]
        ID [sl] = stackID[image]
    return(position, center, width, instance, acquisition, ID)
    
    
    
#ArrayDicom, echoTimes, ConstPixelDims, RefDs, update = DicomRead(exam, series, noEchos)
#fourD = fourD (ConstPixelDims, ArrayDicom)