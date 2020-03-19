#!/usr/bin/env python
import os
import sys
import subprocess
import datetime
import time
import glob

ZHAIRESPYTHON=os.environ["ZHAIRESPYTHON"]
PYTHONINTERPRETER=os.environ["PYTHONINTERPRETER"]


python=PYTHONINTERPRETER
ZHAireSReader=ZHAIRESPYTHON+"/ZHAireSReader.py"
ComputeVoltage=ZHAIRESPYTHON+"/ComputeVoltageOnHDF5.py"
ComputePeak2Peak=ZHAIRESPYTHON+"/ComputePeak2PeakOnHDF5.py"
RemoveTables=ZHAIRESPYTHON+"/RemoveTableFromHDF5.py"

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


