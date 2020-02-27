import os
import sys
import logging

#root_dir = os.path.realpath(os.path.join(os.path.split(__file__)[0], "../radio-simus")) # = $PROJECT
root_dir="/home/mjtueros/GRAND/GP300/azillesnana/radio-simus"
sys.path.append(os.path.join(root_dir, "lib", "python"))
import hdf5fileinout as hdf5io

logging.basicConfig(level=logging.DEBUG)

#if no outfilename is given, it will store the output in a new table AntennaP2PInfo,  in the same HDF5 file (TODO: handle what happens if this already exists)

#this computes the peak to peak amplitudes of all the traces (and if voltage is available in the voltages, etc)


def ComputePeak2PeakOnHDF5(InputFilename,OutputFilename="N/A"):
#EventNumber=all could trigger a loop on all events in the file.

  if os.path.isfile(InputFilename):
    if(OutputFilename=="N/A"):
      OutputFilename=InputFilename

    RunInfo=hdf5io.GetRunInfo(InputFilename)

    NumberOfEvents=hdf5io.GetNumberOfEvents(RunInfo)

    logging.info("Computing P2P amplitudes for "+InputFilename+", found "+str(NumberOfEvents)+" events")

    EventName=hdf5io.GetEventName(RunInfo,0)
    AntennaInfo=hdf5io.GetAntennaInfo(InputFilename,EventName)
    AntennaInfoMeta=AntennaInfo.meta
    IDs=AntennaInfo['ID'].data

    p2pE=hdf5io.get_p2p_hdf5(InputFilename,usetrace='efield')
    p2pV=hdf5io.get_p2p_hdf5(InputFilename,usetrace='voltage')
    p2pFV=hdf5io.get_p2p_hdf5(InputFilename,usetrace='filteredvoltage')

    peaktimeE, peakE=hdf5io.get_peak_time_hilbert_hdf5(InputFilename,usetrace='efield')
    peaktimeV, peakV=hdf5io.get_peak_time_hilbert_hdf5(InputFilename,usetrace='voltage')
    peaktimeFV, peakFV=hdf5io.get_peak_time_hilbert_hdf5(InputFilename,usetrace='filteredvoltage')

    AntennaP2PInfo=hdf5io.CreateAntennaP2PInfo(IDs, AntennaInfoMeta, P2Pefield=p2pE,P2Pvoltage=p2pV,P2Pfiltered=p2pFV,HilbertPeakE=peakE,HilbertPeakV=peakV,HilbertPeakFV=peakFV,HilbertPeakTimeE=peaktimeE,HilbertPeakTimeV=peaktimeV,HilbertPeakTimeFV=peaktimeFV)
    hdf5io.SaveAntennaP2PInfo(OutputFilename,AntennaP2PInfo,EventName)

  else:
   logging.critical("input file " + InputFilename + " does not exist or is not a directory. ComputePeak2PeakOnSHDF5 cannot continue")


if __name__ == '__main__':

  if ( len(sys.argv)<2 ):
    print("usage")

  else:
   inputfile=sys.argv[1]
   ComputePeak2PeakOnHDF5(inputfile)

