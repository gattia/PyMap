# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:23:17 2015

@author: gatti
"""


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