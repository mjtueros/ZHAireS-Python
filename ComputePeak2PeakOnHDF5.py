import os
import sys
import logging

#root_dir = os.path.realpath(os.path.join(os.path.split(__file__)[0], "../radio-simus")) # = $PROJECT
root_dir="/home/mjtueros/GRAND/GP300/azillesnana/radio-simus"
sys.path.append(os.path.join(root_dir, "lib", "python"))
from radio_simus.in_out import _table_voltage
from radio_simus.computevoltage import compute_antennaresponse
from radio_simus.signal_processing import filters
import hdf5fileinout as hdf5io

logging.basicConfig(level=logging.DEBUG)

#if no outfilename is given, it will store the output in table AntennaInfo,  in the same HDF5 file, as a new column. (TODO: handle what happens if this already exists)

#this computes the peak to peak amplitudes of all the traces (and if voltage is available in the voltages, etc)

#TODO: Split this in 3 functions: GetP2PFromTrace(Trace) to get p2px,p2py,p2pz and p2ptotal
#      used in GetP2P(InputFilename, CurrentEventName,AntennaID,tracetype) to get the proper trace
#      used in GetEventP2P(InputFilename, CurrentEventName) to get them for all the antennas in the event

def get_p2p_hdf5(InputFilename,antennamax='All',antennamin=0,usetrace='efield'):
    '''
    read in all traces from antennamax to antennamin and output the peak to peak electric field and amplitude

    Parameters:
    InputFilename: str
        HDF5File
    antennamin: int
       starting antenna (starts from 0)
    antennamax: int
       final antenna ('All uses all the antennas)
    usetrace: str
       efield, voltage, filteredvoltage
    Output:
    p2pE: numpy array
        [p2p_Ex, p2p_Ey, p2p_Ez, p2p_total]: peak-to-peak electric fields along x, y, z, and norm

    '''
    CurrentRunInfo=hdf5io.GetRunInfo(InputFilename)
    CurrentEventName=hdf5io.GetEventName(CurrentRunInfo,0) #using the first event of each file (there is only one for now)
    CurrentAntennaInfo=hdf5io.GetAntennaInfo(InputFilename,CurrentEventName)

    if(antennamax=='All'):
     antennamax=len(CurrentAntennaInfo)-1

    # create an array

    p2p_Ex = np.zeros(1+antennamax-antennamin)
    p2p_Ey = np.zeros(1+antennamax-antennamin)
    p2p_Ez = np.zeros(1+antennamax-antennamin)
    p2p_total = np.zeros(1+antennamax-antennamin)
    p2pE=np.zeros(1+antennamax-antennamin)

    for i in range(antennamin,antennamax+1):
      AntennaID=hdf5io.GetAntennaID(CurrentAntennaInfo,i)
      if(usetrace=='efield'):
        trace=hdf5io.GetAntennaEfield(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      elif(usetrace=='voltage'):
        trace=hdf5io.GetAntennaVoltage(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      elif(usetrace=='filteredvoltage'):
        trace=hdf5io.GetAntennaFilteredVoltage(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      else:
        print('You must specify either efield, voltage or filteredvoltage, bailing out')

      #transposing takes a lot of time
      p2p= np.amax(trace,axis=0)-np.amin(trace,axis=0)
      p2p_Ex[i]= p2p[1]
      p2p_Ey[i]= p2p[2]
      p2p_Ez[i]= p2p[3]

      #amplitude = np.sqrt(trace.T[1]**2. + trace.T[2]**2. + trace.T[3]**2.) # combined components
      amplitude = np.sqrt(trace[:,1]**2. + trace[:,2]**2. + trace[:,3]**2.) # combined components

      p2p_total[i] = max(amplitude)-min(amplitude)

    p2pE = np.stack((p2p_Ex, p2p_Ey, p2p_Ez, p2p_total), axis=0)
    return p2pE

def ComputePeak2PeakOnHDF5(inputfilename,outfilename="N/A"):
#EventNumber=all could trigger a loop on all events in the file.

  if os.path.isfile(inputfilename):
    if(outfilename=="N/A"):
      outfilename=inputfilename

    RunInfo=hdf5io.GetRunInfo(inputfilename)

    NumberOfEvents=hdf5io.GetNumberOfEvents(RunInfo)

    logging.info("Opening "+inputfilename+", found "+str(NumberOfEvents)+" events")

    EventName=hdf5io.GetEventName(RunInfo,0)
    Zenith=hdf5io.GetEventZenith(RunInfo,0)
    Azimuth=hdf5io.GetEventAzimuth(RunInfo,0)

    AntennaInfo=hdf5io.GetAntennaInfo(inputfilename,EventName)
    nantennas=hdf5io.GetNumberOfAntennas(AntennaInfo)
    logging.info("Found "+str(nantennas)+" antennas")

    #about this loop: note that astropy table could use their oun iterator, like: "for row in table:" andthen access row['columnname'].
    #The porblem with this, is that it hardwires the file structure into the code, and i dont want that. All those details must remain hidden in hdf5io, so that we dont have
    #all the scripts if we decide to change something on the file format/structure.

    for i in range(0,nantennas):

      antennaID=hdf5io.GetAntennaID(AntennaInfo,i)

      logging.info("computing for antenna "+antennaID+" ("+str(i+1)+"/"+str(nantennas)+")")

      efield=hdf5io.GetAntennaEfield(inputfilename,EventName,antennaID)


    #end for

  else:
   logging.critical("input file " + inputfilename + " does not exist or is not a directory. ComputePeak2PeakOnSHDF5 cannot continue")


if __name__ == '__main__':

  if ( len(sys.argv)<2 ):
    print("usage")

  else:
   inputfile=sys.argv[1]
   ComputePeak2PeakOnHDF5(inputfile)

