#if you are having encoding errors, specially in lyon, be sure to force the environment to utf8
#setenv  LANGUAGE en_US.UTF-8 ;setenv  LC_ALL en_US.UTF-8 ;setenv  LANG en_US.UTF-8setenv LC_TYPE en_US.UTF-8
#

#this functions will accept GRAND and AIRES outmode, to give the results in each convention
#it will output the primary zen,azim,energy,primarytype, taken from the .inp file present at input_file_path) (assumed only one .inp file per dir)

#aditional output parameters could be:
#  task name,
#  injection depth,
#  ground level,
#  xmax grams (from the sry)
#  xmax position (from the new version sry)
#  AIRES and ZHAireS version
# any other?

#TO DO: treat correctly the different possible primary types, including RASPASS Multi primary
#TO DO: treat correctly the case where a distribution of primary types or energies or angles is put in the input
#TO DO: Check consistency of the output (energy within a range, angles within a range, etc)
#TO DO: have the .sry reader regenerate the summary using AiresSry, if the file is not foun


#6/2019 Matias Tueros, first attempt at python based on original script by Anne Zilles.
#10/2019 Migrated them to make it the official library
#12/2019 Set up on git

import sys
from sys import argv
import os

import glob
import logging

#this function reads he Aires .sry file and tries to extract information from the simulation parameters
#using the .sry file is preferred to using the .inp files because:
#Output is standarized: you dont know what you can find in an .inp file (leading spaces, commented lines, repeated keywords, etc)
#Output is what really happened, not what the user whished it would happen when he did his crappy .inp file.

#lets break the ReadAiresSry into smaller modules. It has the disadventage of opening, scanning and closing the file each time
#but it adds modularity, and closes the files when it does not use it any more.
#If at some point we need speed, then we could input datafile, and make a wraper for opening the file

AiresPath="/sps/hep/trend/software/Aires-19-04-00-ZHAireS-1.0.27/aires/bin/"

def GetZenithAngleFromSry(sry_file,outmode="GRAND"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Primary zenith angle:' in line:
          line = line.lstrip()
          stripedline=line.split(' ',-1)
          zen=float(stripedline[len(stripedline)-2])
          if outmode == 'GRAND':
            zen = 180-zen  #conversion to GRAND convention i.e. pointing towards antenna/propagtion direction
          #logging.debug('Found Zenith ' + str(zen))
          return zen
      try:
        zen
      except NameError:
        zen = 0 #If no zenith angle was included in the input file, AIRES defaults to 0
        if outmode == 'GRAND':
          zen = 180-0 #that translates to 180 in GRAND
        logging.info("Zenith Angle not found in sry file, defaulting to:" + str(zen))
        return zen
  except:
    logging.error("GetZenithAngleFromSry:file not found? or invalid:"+sry_file)
    raise
    return -1

def GetAzimuthAngleFromSry(sry_file,outmode="GRAND"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Primary azimuth angle:' in line:
          line = line.lstrip()
          stripedline=line.split(' ',-1)
          azim = float(stripedline[len(stripedline)-2])
          if outmode == 'GRAND':
            azim=azim+180 #conversion to GRAND convention i.e. pointing towards antenna/propagtion direction
            if azim>=360:
              azim= azim-360
          #logging.debug('Found Azimuth ' + str(azim))
          return azim
      try:
        azim
      except NameError:
        azim = 0 #If no azimuth angle was included in the input file, AIRES defaults to 0
        if outmode == 'GRAND':
          azim = 0+180 # that translates to 18
        logging.info("Azimuth Angle not found in sry file, defaulting to:" + str(azim))
        return azim

  except:
    logging.error("GetAzimuthAngleFromSry:file not found or invalid:"+sry_file)
    raise
    return -1


def GetEnergyFromSry(sry_file,outmode="GRAND"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Primary energy:' in line:
          line = line.lstrip()
          stripedline=line.split(' ',-1)
          try: #this is to detect if it is the first time we find the string, so that we ignore the following
            energy
          except NameError:
            energy = float(stripedline[len(stripedline)-2])
            unit= str(stripedline[len(stripedline)-1])
            if unit == "eV\n":
             energy = energy *1e-9
            if unit == "KeV\n":
             energy = energy *1e-6
            if unit == "MeV\n":
              energy = energy *1e-3
            if unit == "GeV\n":
              energy = energy
            if unit == "TeV\n":
              energy = energy *1e3
            if unit == "PeV\n":
              energy = energy *1e6
            if unit == "EeV\n":
              energy = energy *1e9

            if outmode == 'GRAND': #AIRES mode outputs in GeV, GRAND in EeV
              energy = energy * 1e-9
            #logging.debug('Found Energy ' + str(energy)) #debug level 1
            return energy
      try:
        energy
      except NameError:
        logging.error('warning energy not found, Aires has no default value,  cannot continue')
        exit()
  except:
    logging.error("GetEnergyFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetThinningRelativeEnergyFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Thinning energy:' in line:
          line = line.lstrip()
          stripedline=line.split('Thinning energy:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          Thinning=stripedline[0]
          Relative=stripedline[1]
          if(Relative!="Relative\n"):
             logging.error('warning , we only support Relative thinning for now, sorry!. This is easy to implement if you need it!')
             return -1
          return Thinning
      try:
        Thinning
      except NameError:
        logging.error('warning Thinning energy not found, Aires has no default value, cannot continue')
        exit()
  except:
    logging.error("GetThinningRelativeEnergyFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetGammaEnergyCutFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Cut energy for gammas:' in line:
          line = line.lstrip()
          stripedline=line.split('Cut energy for gammas:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          energy=stripedline[0]
          unit=stripedline[1]
          if unit == "eV\n":
            energy = energy *1e-6
          if unit == "KeV\n":
            energy = energy *1e-3
          if unit == "MeV\n":
            energy = energy
          if unit == "GeV\n":
            energy = energy *1e3
          if unit == "TeV\n":
            energy = energy *1e6
          if unit == "PeV\n":
            energy = energy *1e9
          if unit == "EeV\n":
            energy = energy *1e12
          return energy
      try:
        energy
      except NameError:
        logging.error('warning GammaCutEnergy not found, defaulting to 80keV')
        return 80+1e-3
  except:
    logging.error("GetGammaEnergyCutFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetElectronEnergyCutFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Cut energy for e+ e-:' in line:
          line = line.lstrip()
          stripedline=line.split('Cut energy for e+ e-:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          energy=stripedline[0]
          unit=stripedline[1]
          if unit == "eV\n":
            energy = energy *1e-6
          if unit == "KeV\n":
            energy = energy *1e-3
          if unit == "MeV\n":
            energy = energy
          if unit == "GeV\n":
            energy = energy *1e3
          if unit == "TeV\n":
            energy = energy *1e6
          if unit == "PeV\n":
            energy = energy *1e9
          if unit == "EeV\n":
            energy = energy *1e12
          return energy
      try:
        energy
      except NameError:
        logging.error('warning ElectronCutEnergy not found, defaulting to 80keV')
        return 80+1e-3
  except:
    logging.error("GetElectronEnergyCutFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetMuonEnergyCutFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Cut energy for mu+ mu-:' in line:
          line = line.lstrip()
          stripedline=line.split('Cut energy for mu+ mu-:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          energy=stripedline[0]
          unit=stripedline[1]
          if unit == "eV\n":
            energy = energy *1e-6
          if unit == "KeV\n":
            energy = energy *1e-3
          if unit == "MeV\n":
            energy = energy
          if unit == "GeV\n":
            energy = energy *1e3
          if unit == "TeV\n":
            energy = energy *1e6
          if unit == "PeV\n":
            energy = energy *1e9
          if unit == "EeV\n":
            energy = energy *1e12
          return energy
      try:
        energy
      except NameError:
        logging.error('warning MuonCutEnergy not found, defaulting to 10MeV')
        return 10
  except:
    logging.error("GetMuonEnergyCutFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetMesonEnergyCutFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Cut energy for mesons:' in line:
          line = line.lstrip()
          stripedline=line.split('Cut energy for mesons:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          energy=stripedline[0]
          unit=stripedline[1]
          if unit == "eV\n":
            energy = energy *1e-6
          if unit == "KeV\n":
            energy = energy *1e-3
          if unit == "MeV\n":
            energy = energy
          if unit == "GeV\n":
            energy = energy *1e3
          if unit == "TeV\n":
            energy = energy *1e6
          if unit == "PeV\n":
            energy = energy *1e9
          if unit == "EeV\n":
            energy = energy *1e12
          return energy
      try:
        energy
      except NameError:
        logging.error('warning MesonCutEnergy not found, defaulting to 60MeV')
        return 60
  except:
    logging.error("GetMesonEnergyCutFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetNucleonEnergyCutFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Cut energy for nucleons:' in line:
          line = line.lstrip()
          stripedline=line.split('Cut energy for nucleons:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          energy=stripedline[0]
          unit=stripedline[1]
          if unit == "eV\n":
            energy = energy *1e-6
          if unit == "KeV\n":
            energy = energy *1e-3
          if unit == "MeV\n":
            energy = energy
          if unit == "GeV\n":
            energy = energy *1e3
          if unit == "TeV\n":
            energy = energy *1e6
          if unit == "PeV\n":
            energy = energy *1e9
          if unit == "EeV\n":
            energy = energy *1e12
          return energy
      try:
        energy
      except NameError:
        logging.error('warning NucleonCutEnergy not found, defaulting to 60MeV')
        return 60
  except:
    logging.error("GetNucleonEnergyCutFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetPrimaryFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Primary particle:' in line:
          line = line.lstrip()
          stripedline=line.split(' ',-1)
          if(len(stripedline)==3):
            primarytype = str(stripedline[len(stripedline)-1])
          elif(len(stripedline)==5):
            primarytype = str(stripedline[len(stripedline)-3])
          elif(len(stripedline)==6):
            primarytype = str(stripedline[len(stripedline)-4])
          elif(len(stripedline)==7):
            primarytype = str(stripedline[len(stripedline)-5])
          else:
            primarytype = "unknown"
          primarytype=primarytype.replace('\n','')
          #logging.debug('Found Primary ' + primarytype) #debug level 1
          return primarytype
      try:
        primarytype
      except NameError:
        logging.error('warning primary not found, Aires has no default value, cannot continue')
        exit()
  except:
    logging.error("GetPrimaryFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetSlantXmaxFromSry(sry_file,outmode="N/A"): #To do. Handle when Xmax is not found, becouse the fit didnt converge
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Sl. depth of max. (g/cm2)' in line:
          line = line.lstrip()
          stripedline=line.split(' ',-1)
          xmax = float(stripedline[len(stripedline)-1])
          #logging.debug('Found Xmax ' + str(xmax)) #debug level 1
          return xmax
      try:
        xmax
      except NameError:
        logging.info('warning xmax not found')
        xmax=-1
        return xmax
  except:
    logging.error("GetSlantXmaxFromSry:file not found or invalid:"+sry_file)
    raise
    return -1


#                              Altitude  Distance     x        y        z
#      Location of max.(Km):     3.612     3.66     0.00     0.57     3.61
def GetKmXmaxFromSry(sry_file,outmode="N/A"): #To do. Handle when Xmax is not found, becouse the fit didnt converge, or becouse this is not ZHAireS, or its latest version
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Location of max.(Km)' in line:
          line = line.lstrip()
          stripedline=line.split()
          kmxmax = float(stripedline[len(stripedline)-5])
          distance = float(stripedline[len(stripedline)-4])
          x = float(stripedline[len(stripedline)-3])
          y = float(stripedline[len(stripedline)-2])
          z = float(stripedline[len(stripedline)-1])
          logging.debug("Found Xmax altitude " + str(kmxmax) + " distance " + str(distance) + " x:" + str(x) + " y:"+ str(y) + " z:" + str(z) ) #debug level 1
          return kmxmax,distance,x,y,z
      try:
        kmxmax
      except NameError:
        logging.info('warning distance to xmax not found')
        return -1,-1,-1,-1,-1
  except:
    logging.error("GetKmXmaxFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetTaskNameFromSry(sry_file,outmode="N/A"):
  datafile=open(sry_file,'r')
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Task Name:' in line:
          line = line.lstrip()
          stripedline=line.split(' ',-1)
          taskname=stripedline[len(stripedline)-1]
          taskname=taskname.replace('\n','')
          logging.debug("Found taskname " + taskname)
          if '...' in taskname:
            base=os.path.basename(sry_file)
            taskname=os.path.splitext(base)[0]
            logging.debug("taskname contained ... (too long), using filename instead")
            print("taskname:"+taskname)

          return taskname
      try:
        taskname
      except NameError:
        logging.error('warning taskname not found, Aires has no default value, cannot continue')
        exit()
  except:
    logging.error("GetTaskNameFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetRandomSeedFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Seed of random generator:' in line:
          line = line.lstrip()
          stripedline=line.split(' ',-1)
          randomseed=stripedline[len(stripedline)-1]
          randomseed=randomseed.replace('\n','')
          return randomseed
      try:
        randomseed
      except NameError:
        logging.error('warning randomseed not found, Aires has no default value, cannot continue')
        exit()
  except:
    logging.error("GetRandomSeedFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

#output is in meters
def GetGroundAltitudeFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Ground altitude:' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.split(' ',-1)
          groundalt=float(stripedline[1])
          unit=stripedline[2]
          if unit == "km":
           groundalt=groundalt*1000.0
          if unit == "cm":
           groundalt=groundalt/100.0
          return groundalt
      try:
        groundalt
      except NameError:
        logging.error('warning groundalt not found, defaulting to sea level')
        return 0
  except:
    logging.error("GetGroundAltitudeFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetTimeBinFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Time Domain Bin Size:' in line:
          line = line.lstrip()
          stripedline=line.split('Time Domain Bin Size:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          timebin=float(stripedline[0])
          unit=stripedline[1]
          if unit != "sec\n":
              logging.error('warning, time bin must be in seconds on the summary file, other units not supported yet')
              return -1
          return timebin*1e9

      try:
        timebin
      except NameError:
        logging.error('warning timebin not found')
        return 0
  except:
    logging.error("GetTimeBinFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetTimeWindowMinFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Antenna Time Window Min:' in line:
          line = line.lstrip()
          stripedline=line.split('Antenna Time Window Min:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          timemin=float(stripedline[0])
          unit=stripedline[1]
          if unit != "sec\n":
              logging.error('warning, time window must be in seconds on the summary file, other units not supported yet')
              return -1
          return timemin*1e9

      try:
        timemin
      except NameError:
        logging.error('warning timewindow min not found')
        return 0
  except:
    logging.error("GetTimeWindowMinFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetTimeWindowMaxFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Antenna Time Window Max:' in line:
          line = line.lstrip()
          stripedline=line.split('Antenna Time Window Max:',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          timemax=float(stripedline[0])
          unit=stripedline[1]
          if unit != "sec\n":
              logging.error('warning, time window must be in seconds on the summary file, other units not supported yet')
              return -1
          return timemax*1e9

      try:
        timemax
      except NameError:
        logging.error('warning timewindow max not found')
        return 0
  except:
    logging.error("GetTimeWindowMaxFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetWeightFactorFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Max. stat. weight factor:' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1)
          stripedline=stripedline[1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          wf=float(stripedline[0])
          return wf
      try:
        wf
      except NameError:
        logging.error('warning weight factor not found, default is 12')
        return 12
  except:
    logging.error("GetWeightFactorFromSry:file not found or invalid:"+sry_file)
    raise
    return -1



def GetMagneticFieldFromSry(sry_file,outmode="N/A"):
  fieldintensity=float(0.0)
  fieldinclination=float(0.0)
  fielddeclination=float(0.0)
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Geomagnetic field:' in line:
          line = line.lstrip()
          stripedline=line.split('Intensity:',-1)
          intensityline=stripedline[1]
          intensityline=intensityline.lstrip()
          stripedline=intensityline.split(' ',-1)
          fieldintensity=float(stripedline[0])
        if 'I:' in line:
          line = line.lstrip()
          stripedline=line.split('I:',-1)
          inclinationline=stripedline[1]
          inclinationline=inclinationline.lstrip()
          stripedline=inclinationline.split(' ',-1)
          fieldinclination=float(stripedline[0])
          stripedline=line.split('D:',-1)
          declinationline=stripedline[1]
          declinationline=declinationline.lstrip()
          stripedline=declinationline.split(' ',-1)
          fielddeclination=float(stripedline[0])

      try:
        fieldintensity
        return fieldintensity,fieldinclination,fielddeclination
      except NameError:
        logging.error('warning MagneticField not found, defaulting to sea level')
        return 0,0,0
  except:
    logging.error("GetMagneticFieldFromSry:file not found or invalid:"+sry_file)
    raise
    return -1,-1,-1


def GetTotalCPUTimeFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Total CPU time' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1)
          CPUtime=stripedline[len(stripedline)-1]
          #logging.debug("Found taskname " + taskname)
          return CPUtime
      try:
        CPUtime
      except NameError:
        logging.error('warning Total CPU time not found')
        return -1
  except:
    logging.error("GetTotalCPUTimeFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetHadronicModelFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Hadronic Mean Free Paths' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1)
          HadronicModel=stripedline[len(stripedline)-1]
          #logging.debug("Found taskname " + taskname)
          return HadronicModel
      try:
        HadronicModel
      except NameError:
        logging.error('warning Hadronic Model not found')
        return -1
  except:
    logging.error("GetHadronicModelFromSry:file not found or invalid:"+sry_file)
    raise
    return -1


def GetRandomSeedFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Seed of random generator:' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1)
          RandomSeed=stripedline[len(stripedline)-1]
          #logging.debug("Found taskname " + taskname)
          return RandomSeed
      try:
        RandomSeedl
      except NameError:
        logging.error('warning RandomSeed not found')
        return -1
  except:
    logging.error("GetRandomSeedFromSry:file not found or invalid:"+sry_file)
    raise
    return -1


def GetAiresVersionFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'This is AIRES version' in line:
          line = line.lstrip()
          stripedline=line.split('This is AIRES version',-1)
          stripedline=stripedline[-1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          AiresVersion=stripedline[0]
          #ogging.debug("Found Version " + AiresVersion)
          return AiresVersion
      try:
        AiresVersion
      except NameError:
        logging.error('warning Aires Version not found')
        return -1
  except:
    logging.error("GetAiresVersionFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetZHAireSVersionFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'With ZHAireS version' in line:
          line = line.lstrip()
          stripedline=line.split('With ZHAireS version',-1)
          stripedline=stripedline[-1]
          stripedline=stripedline.lstrip()
          stripedline=stripedline.split(' ',-1)
          ZHAiresVersion=stripedline[0]
          #ogging.debug("Found Version " + AiresVersion)
          return ZHAiresVersion
      try:
        ZHAiresVersion
      except NameError:
        logging.error('warning ZHAireS Version not found')
        return -1
  except:
    logging.error("GetZHAireSVersionFromSry:file not found or invalid:"+sry_file)
    raise
    return -1


def GetAtmosphericModelFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Atmospheric model' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1)
          AtmosphericModel=stripedline[len(stripedline)-1]
          #logging.debug("Found taskname " + taskname)
          return AtmosphericModel
      try:
        AtmosphericModel
      except NameError:
        logging.error('warning Atmospheric Model not found')
        return -1
  except:
    logging.error("GetAtmosphericModelFromSry:file not found or invalid:"+sry_file)
    raise
    return -1


def GetSiteFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Site:' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1)
          Site=stripedline[len(stripedline)-1]
          #logging.debug("Found taskname " + taskname)
          return Site
      try:
        Site
      except NameError:
        logging.error('warning Site not found')
        return -1
  except:
    logging.error("GetSiteFromSry:file not found or invalid:"+sry_file)
    raise
    return -1

def GetDateFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Date:' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1)
          Date=stripedline[len(stripedline)-1]
          #logging.debug("Found taskname " + taskname)
          return Date
      try:
        Date
      except NameError:
        logging.error('warning Date not found')
        return -1
  except:
    logging.error("GetDateFromSry:file not found or invalid:"+sry_file)
    raise
    return -1


def GetInjectionAltitudeFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      for line in datafile:
        if 'Injection altitude' in line:
          line = line.lstrip()
          stripedline=line.split(':',-1) #since somtimes we can have the (D) of default and sometimes not i make sure this is whatever is after the :
          stripedline=stripedline[1]
          stripedline=stripedline.split(' ',-1)
          injalt=float(stripedline[1])
          unit=stripedline[2]
          if unit == "km":
           injalt=injalt*1000.0
          if unit == "cm":
           injalt=injalt/100.0
          return injalt
      try:
        injalt
      except NameError:
        logging.error('warning Injection Altitude not found')
        return -1
  except:
    logging.error("GetInjectionAltitudeFromSry:file not found or invalid:"+sry_file)
    raise
    return -1



def GetEnergyFractionInNeutrinosFromSry(sry_file,outmode="N/A"):
  try:
    datafile=open(sry_file,'r')
    with open(sry_file, "r") as datafile:
      founditonce=0
      for line in datafile:
        if 'Neutrinos:' in line:
          if(founditonce==1):
            line = line.lstrip()
            stripedline=line.split('Neutrinos:',-1)
            stripedline=stripedline[1]
            stripedline=stripedline.lstrip()
            stripedline=stripedline.split(' ',-1)
            energyf=float(stripedline[0])
            return energyf
          founditonce=founditonce+1
      try:
        energyf
      except NameError:
        logging.error('warning NeutrinoEnergyFraction not found')
        return -1
  except:
    logging.error("GetEnergyFractionInNeutrinosFromSry:file not found or invalid:"+sry_file)
    raise
    return -1



def GetLongitudinalTable(Path,TableNumber,Slant=True,Precision="Double"):
    #todo: check against a list of valid tables
    deletefile=False
    sryfile=glob.glob(Path+"/*.sry")
    idffile=glob.glob(Path+"/*.idf")
    inpfile=glob.glob(Path+"/*.inp")
    tablefile=glob.glob(Path+"/*.t"+str(TableNumber))

    if(len(tablefile)==0 and len(idffile)==0):
      logging.error("The requested table was not found, and the idf file is not present. Cannot get the table")
      return -1

    if(len(idffile)==1 and len(tablefile)==0):
      logging.info("could not find the table, trying to guess it from the idf")
      base=os.path.basename(idffile[0])
      taskname=os.path.splitext(base)[0]

      if(Slant==True):
        cmd=AiresPath+"/AiresExport -O a "+Path+"/"+taskname+" "+str(TableNumber)
      elif(Slant==False):
        cmd=AiresPath+"/AiresExport "+Path+"/"+taskname+" "+str(TableNumber)
      else:
        logging.error("unrecognized Slant value, please state either True/False")
        return -1

      os.system(cmd)
      tablefile=glob.glob(Path+"/*.t"+str(TableNumber))

      if(len(tablefile)==1):
        logging.debug("Table exported successfully")
        deletefile=True

    if(len(tablefile)==1):
      logging.debug("reading file")

      from numpy import loadtxt

      if(Precision=="Double"):
        numpyarray=loadtxt(tablefile[0],usecols=(1,2),dtype='f8')
      elif(Precision=="Simple"):
        numpyarray=loadtxt(tablefile[0],usecols=(1,2),dtype='f4')
      else:
        logging.error("unrecognized precison, please state either Double or Simple")
        return -1

      if(deletefile==True):
        cmd="rm "+tablefile[0]
        os.system(cmd)
        logging.debug("Table deleted successfully")

      return numpyarray
    else:
      logging.error("The requested table was not found and could not be regenerated. Sorry")
      return -1


def GetLateralTable(Path,TableNumber,Density=True,Precision="Double"):
    #todo: check against a list of valid tables
    deletefile=False
    sryfile=glob.glob(Path+"/*.sry")
    idffile=glob.glob(Path+"/*.idf")
    inpfile=glob.glob(Path+"/*.inp")
    tablefile=glob.glob(Path+"/*.t"+str(TableNumber))

    if(len(tablefile)==0 and len(idffile)==0):
      logging.error("The requested table was not found, and the idf file is not present. Cannot get the table")
      return -1

    if(len(idffile)==1 and len(tablefile)==0):
      logging.info("could not find the table, trying to guess it from the idf")
      base=os.path.basename(idffile[0])
      taskname=os.path.splitext(base)[0]

      if(Density==True):
        cmd=AiresPath+"/AiresExport -O dX "+Path+"/"+taskname+" "+str(TableNumber)
      elif(Density==False):
        cmd=AiresPath+"/AiresExport -O X "+Path+"/"+taskname+" "+str(TableNumber)
      else:
        logging.error("unrecognized Density value, please state either True/False")
        return -1

      os.system(cmd)
      tablefile=glob.glob(Path+"/*.t"+str(TableNumber))

      if(len(tablefile)==1):
        logging.debug("Table exported successfully")
        deletefile=True

    if(len(tablefile)==1):
      logging.debug("reading file")

      from numpy import loadtxt

      if(Precision=="Double"):
        numpyarray=loadtxt(tablefile[0],usecols=(1,2),dtype='f8')
      elif(Precision=="Simple"):
        numpyarray=loadtxt(tablefile[0],usecols=(1,2),dtype='f4')
      else:
        logging.error("unrecognized precison, please state either Double or Simple")
        return -1

      if(deletefile==True):
        cmd="rm "+tablefile[0]
        os.system(cmd)
        logging.debug("Table deleted successfully")

      return numpyarray
    else:
      logging.error("The requested table was not found and could not be regenerated. Sorry")
      return -1






def ReadAiresSry(sry_file,outmode="N/A"):

  zen=GetZenithAngleFromSry(sry_file,outmode)
  azim=GetAzimuthAngleFromSry(sry_file,outmode)
  energy=GetEnergyFromSry(sry_file,outmode)
  primary=GetPrimaryFromSry(sry_file,outmode)
  xmax=GetSlantXmaxFromSry(sry_file,outmode)
  kmxmax,distance,x,y,z=GetKmXmaxFromSry(sry_file,outmode)
  taskname=GetTaskNameFromSry(sry_file,outmode)
  return zen,azim,energy,primary,xmax,distance,taskname

def ReadAiresLgf(lgf_file,outmode="N/A"):

  zen=GetZenithAngleFromSry(lgf_file,outmode)
  azim=GetAzimuthAngleFromSry(lgf_file,outmode)
  energy=GetEnergyFromSry(lgf_file,outmode)
  primary=GetPrimaryFromSry(lgf_file,outmode)
  taskname=GetTaskNameFromSry(lgf_file,outmode)
  return zen,azim,energy,primary,-1,-1,taskname


def GetStatusFromStatus(status_file):
  try:
    datafile=open(status_file,'r')
    with open(status_file, "r") as datafile:
      for line in datafile:
        if 'Aires_Msg' in line:
          line = line.lstrip()
          stripedline=line.split('=',-1)
          status=stripedline[len(stripedline)-1]
          status=status.replace('\'','')
          status=status.replace('\n','')
          #logging.debug("Found status " + status)
          return status
      try:
        status
      except NameError:
        logging.error('warning status not found in status file')
        return 'not found'
  except:
    logging.error("GetStatusFromStatus:file not found or invalid:"+status_file)
    return -1

def GetTmpFromDirs(dirs_file):
  try:
    datafile=open(dirs_file,'r')
    with open(dirs_file, "r") as datafile:
      for line in datafile:
        if 'Aires_DRandomfn' in line:
          line = line.lstrip()
          stripedline=line.split('=',-1)
          tmp=stripedline[len(stripedline)-1]
          tmp=tmp.replace('\'','')
          tmp=tmp.replace('\n','')
          #logging.debug("Found Tmp " + tmp)
          return tmp
      try:
        tmp
      except NameError:
        logging.error('warning Aires_DRandomfn not found in dirs file')
        return 'not found'
  except:
    logging.error("GetTmpFromSDirs:file not found or invalid:"+dirs_file)
    return -1

def DeprecatedReadAiresSry(sry_file,outmode="GRAND"):

    try:
     datafile=open(sry_file,'r')

    except:
      logging.error("ReasAiresSry:file not found or invalid:"+sry_file)
      raise
      return -1, -1, -1, -1, -1

    for line in datafile:
        ## print(line) #debug level 2

        if 'Primary zenith angle:' in line:
            line = line.lstrip()
            stripedline=line.split(' ',-1)
            zen=float(stripedline[len(stripedline)-2])
            if outmode == 'GRAND':
                zen = 180-zen  #conversion to GRAND convention i.e. pointing towards antenna/propagtion direction
            logging.debug('Found Zenith ' + str(zen))

        if 'Primary azimuth angle:' in line:
            line = line.lstrip()
            stripedline=line.split(' ',-1)
            azim = float(stripedline[len(stripedline)-2])

            if outmode == 'GRAND':
                azim=azim+180 #conversion to GRAND convention i.e. pointing towards antenna/propagtion direction
                if azim>=360:
                    azim= azim-360
            logging.debug('Found Azimuth ' + str(azim))

        if 'Primary energy:' in line:
            line = line.lstrip()
            stripedline=line.split(' ',-1)
            try:
              energy
            except NameError:
              energy = float(stripedline[len(stripedline)-2])
              unit= str(stripedline[len(stripedline)-1])

              if outmode == 'GRAND':
                if unit == "eV\n":
                    energy = energy *1e-18
                if unit == "KeV\n":
                    energy = energy *1e-15
                if unit == "MeV\n":
                    energy = energy *1e-12
                if unit == "GeV\n":
                    energy = energy *1e-9
                if unit == "TeV\n":
                    energy = energy *1e-6
                if unit == "PeV\n":
                    energy = energy *1e-3
                if unit == "EeV\n":
                    energy = energy

              if outmode == 'AIRES':
                if unit == "eV\n":
                    energy = energy *1e-9
                if unit == "KeV\n":
                    energy = energy *1e-6
                if unit == "MeV\n":
                    energy = energy *1e-3
                if unit == "GeV\n":
                    energy = energy
                if unit == "TeV\n":
                    energy = energy *1e3
                if unit == "PeV\n":
                    energy = energy *1e6
                if unit == "EeV\n":
                    energy = energy *1e9

              logging.debug('Found Energy ' + str(energy)) #debug level 1

        if 'Primary particle:' in line:
            line = line.lstrip()
            stripedline=line.split(' ',-1)
            if(len(stripedline)==3):
              primarytype = str(stripedline[len(stripedline)-1])
            elif(len(stripedline)==5):
              primarytype = str(stripedline[len(stripedline)-3])
            elif(len(stripedline)==6):
              primarytype = str(stripedline[len(stripedline)-4])
            elif(len(stripedline)==7):
              primarytype = str(stripedline[len(stripedline)-5])
            else:
              primarytype = "unknown"

            logging.debug('Found Primary ' + primarytype) #debug level 1


        if 'Sl. depth of max. (g/cm2)' in line:
            line = line.lstrip()
            stripedline=line.split(' ',-1)
            xmax = float(stripedline[len(stripedline)-1])
            logging.debug('Found Xmax ' + str(xmax)) #debug level 1


    try:
        zen
    except NameError:
        zen = 0 #If no zenith angle was included in the input file, AIRES defaults to 0
        if outmode == 'GRAND':
          zen = 180-0 #that translates to 180 in GRAND
    try:
        azim
    except NameError:
        azim = 0 #If no azimuth angle was included in the input file, AIRES defaults to 0
        if outmode == 'GRAND':
          azim = 0+180 # that translates to 180
    try:
        energy
    except NameError:
        logging.error('warning energy not found, Aires has no default value,  cannot continue')
        exit()
    try:
        primarytype
    except NameError:
        logging.error('warning primary not found, Aires has no default value, cannot continue')
        exit()

    try:
        xmax
    except NameError:
        logging.info('warning xmax not found')
        xmax=-1

    return zen,azim,energy,primarytype,xmax



if __name__ == '__main__':
    #main ReadAiresInput
    path = sys.argv[1]
    outmode = 'AIRES'
    #print(ReadAiresInput(path,outmode))
    print(ReadAiresSry(path,outmode))
