# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:48:19 2015

@author: gatti
"""
import time 
import numpy 
from scipy.optimize import curve_fit

def func(TE, PD, T2):
    return PD*numpy.exp(-TE/T2)
    
def t2Relax(ConstPixelDims, zoom):
    numsl = ConstPixelDims[2]   
    echoTimes = ConstPixelDims[3]
    
    T2 = numpy.zeros(shape=(zoom.shape[0], zoom.shape[1], zoom.shape[2]))
    PD = numpy.zeros(shape=(zoom.shape[0], zoom.shape[1], zoom.shape[2]))
    Rsq = numpy.zeros(shape=(zoom.shape[0], zoom.shape[1], zoom.shape[2]))
    
    for z in range(0, numsl):
        t = time.time()
        for y in range (0, zoom.shape[0]):
            for x in range (0, zoom.shape[1]):
                S = numpy.squeeze(zoom[y,x,z,:])
            
                if S[0] < 300:
                    T2[y,x,z] = 0
                    PD[y,x,z] = 0
                    Rsq[y,x,z] = 0
                elif S[0] > 3500:
                    T2[y,x,z] = 0
                    PD[y,x,z] = 0
                    Rsq[y,x,z] = 0
                else:
                    popt, pcov = curve_fit(func, echoTimes, S)
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
