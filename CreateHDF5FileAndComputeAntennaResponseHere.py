#!/usr/bin/env python
import os
import sys
import subprocess
import datetime
import time
import glob
python="/home/mjtueros/GRAND/GP300/GRANDMOTHER/GRANDpython"
ZHAireSReader="/home/mjtueros/AiresRepository/Dropbox/GitAiresPython/ZHAireS-Python/ZHAireSReader.py"
ComputeVoltage="/home/mjtueros/AiresRepository/Dropbox/GitAiresPython/ZHAireS-Python/ComputeVoltageOnHDF5.py"
ComputePeak2Peak="/home/mjtueros/AiresRepository/Dropbox/GitAiresPython/ZHAireS-Python/ComputePeak2PeakOnHDF5.py"
RemoveTables="/home/mjtueros/AiresRepository/Dropbox/GitAiresPython/ZHAireS-Python/RemoveTableFromHDF5.py"

Filename=glob.glob("*.idf")
Filename=os.path.splitext(Filename[0])[0]

Filename2=Filename+".NoTraces.hdf5"
Filename=Filename+".hdf5"
print(Filename)


cmd=python + ' ' + ZHAireSReader + ' ./'
wd = os.getcwd()
p = subprocess.Popen(cmd,cwd=wd,shell=True)
stdout,stderr=p.communicate()

cmd=python + ' ' + ComputeVoltage + ' '+ Filename
wd = os.getcwd()
p = subprocess.Popen(cmd,cwd=wd,shell=True)
stdout,stderr=p.communicate()

cmd=python + ' ' + ComputePeak2Peak + ' '+ Filename
wd = os.getcwd()
p = subprocess.Popen(cmd,cwd=wd,shell=True)
stdout,stderr=p.communicate()

cmd=python + ' ' + RemoveTables + ' ' + Filename + ' ' + Filename2 +' AntennaTraces'
wd = os.getcwd()
p = subprocess.Popen(cmd,cwd=wd,shell=True)
stdout,stderr=p.communicate()


