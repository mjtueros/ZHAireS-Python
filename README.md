# ZHAireS-Python testrelease
Python scripts to get data from ZHAireS files, and to create ZHAireS inputs

# I will document this eventually
But for now, know that

AiresInfoFunctions.py has functions that get information from the .sry and .lgf file


AitesInpFunctions.py has functions that generate .inp files:

All input files can be divided in:
1)An "Input Header" with the most important, and frequently changing input parameters (Energy, Zenith, Azimuth, etc)
2)A "Skelton", that usually do not change between simulations (but you must check is what you need!)
3) The antenna positions you want to simulate

#HDF5 File format
hdf5fileinout.py has the routines to read and write ZHAireS events in HDF5 Format

ZHAiresReader.py creates the file from the standar ZHAIRES output (no tables should be present on the directory, the script will export the required tables if needed)

ComputeVoltageOnHDF5.py can then be aplied to compute the antenna response, and the filtered antenna response.

ComputePeak2PealOnHDF5 can then be plied to compute the P2Pamplitude of each channel, and the hilbertpeak and peak time.

and some more

testing
