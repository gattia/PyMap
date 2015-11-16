# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:23:17 2015

@author: gatti
"""

#Export all of the dicom images based on the name given at the start of the program
#and the slice number. Also use the slice number and the header data collected at the start
#The header data will ensure that the oringal file information is used. 

#This is still exporting as a 2D dataset. I would like a 3D one. Not sure on how to do that as of yet. 
import pydicom 

def writeDicom (originalFile, dataSet, name, header):
    
    for i in (range(0, dataSet.shape[2])):
        image = i*8
        exportedFile = header.image
        pixel_array = dataSet[:,:,i]
        exportedFile.pixel_array = pixel_array
        exportedFile.PixelData = pixel_array.tostring()
        exportedFile.save_as(name + '_' + str(i) +'.dcm')
#    exportedFile.pixel_array = dataSet
#    pydicom.write_file(name, exportedFile)