# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:40:57 2015

@author: gatti
"""

import pydicom 

def writeDicom (originalFile, dataSet, name, position, center, width, instance, acquisition, ID):
    
    for i in (range(0, dataSet.shape[2])):
        exportedFile = originalFile
        exportedFile.ImagePositionPatient = list(tuple(position[i]))
        exportedFile.WindowCenter = center[i]
        exportedFile.WindoWidth = width[i]
        exportedFile.AcquisitionNumber = acquisition[i]
        exportedFile.InstanceNumber = instance[i]
        exportedFile.StackID = ID[i]
        pixel_array = dataSet[:,:,i]
        exportedFile.pixel_array = pixel_array
        exportedFile.PixelData = pixel_array.tostring()
        exportedFile.save_as(name + '_' + str(i) +'.dcm')
#    exportedFile.pixel_array = dataSet
#    pydicom.write_file(name, exportedFile)