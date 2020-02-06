# ZHAireS-Python
Python scripts to get data from ZHAireS files, and to create ZHAireS inputs

# I will document this eventually
But for now, know that

AiresInfoFunctions.py has functions that get information from the .sry and .lgf file


AitesInpFunctions.py has functions that generate .inp files:

All input files can be divided in:
1)An "Input Header" with the most important, and frequently changing input parameters (Energy, Zenith, Azimuth, etc)
2)A "Skelton", that usually do not change between simulations (but you must check is what you need!)
3) The antenna positions you want to simulate


hdf5fileinout.py has the routines to read and write ZHAireS events in HDF5 Format
