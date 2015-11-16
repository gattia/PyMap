# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 14:34:05 2015

@author: gatti
"""

import matplotlib.pyplot as plt

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