# PyMap
T2 mapping software written in python


To run this program you will need to have a number of python modules installed on your computer. Some of these are included in anaconda which you can install and others you will need in addition. 


The ones included within anaconda are: (https://www.continuum.io/downloads):
pylab
matplotlib
numpy
scipy 

The additional ones you will need are:
pydicom (http://pydicom.readthedocs.org/en/latest/getting_started.html#installing)
natsort (http://pythonhosted.org/natsort/intro.html#installation)


The program is within the script File. The actual file that is run is T2mapHeaderDicom.py

You will need to alter a few things to make the program work on your specific machine. 

Line 21: you will need to change this directory to the firectory that your images are located. 
Within this director I have folders listed by exam and within each exam I have a series. The 
series and exam are input at the start of the program and are done this way so that the program 
automatically goes to where the T2 images of interest are. This can be changed to accomodate 
your personal file structure. 

- future work should make this something that is input at the start of the program or within a GUI. 

Line 96: similarly this needs to be changed to where you want to write your files. A folder with 
the name you input at the start will be created and the files placed in this folder. 

- Similarly future work should include the selection of where your images are written within the inputs or a GUI. 
