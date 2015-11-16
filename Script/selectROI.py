# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 14:34:05 2015

@author: gatti
"""

import matplotlib.pyplot as plt

#the below code will take the clicks of your mouse to determine the coordinates
#on the image ROI. The coordinates for each click are saved to coords where the
#first column is the x-coordinate and the second is the y-coordinate. The first 
#row is the from click #1 and the second row is from click #2. 

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

#The coordinates recorded from the clicks are changed into  their x and y 
#componenets. These components are used to draw out and to extract the ROI. 
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