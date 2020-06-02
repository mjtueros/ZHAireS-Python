import os
import sys
import logging

#root_dir = os.path.realpath(os.path.join(os.path.split(__file__)[0], "../radio-simus")) # = $PROJECT
root_dir=os.environ["RADIOSIMUS"]
sys.path.append(os.path.join(root_dir, "lib", "python"))
from radio_simus.in_out import _table_voltage
from radio_simus.computevoltage import compute_antennaresponse
from radio_simus.signal_processing import filters
import hdf5fileinout as hdf5io

logging.basicConfig(level=logging.DEBUG)

#if no outfilename is given, it will store the table in the same HDF5 dile, in a separate table (TODO: handle what happens if it already exists)

#this computes the voltage on all the antennas, but if this gets too CPU intense in some application we might want to apply some filter,
#that could go in the funnction call like...such as only compute if the peak to peak amplitude is higher than something, or the distance to the core is less than something,etc.

def ComputeVoltageOnHDF5(inputfilename,EventNumber=0,FreqMin=100.e6,FreqMax=180.e6,outfilename="N/A"):
#EventNumber=all could trigger a loop on all events in the file.

  if os.path.isfile(inputfilename):
    if(outfilename=="N/A"):
      outfilename=inputfilename

    RunInfo=hdf5io.GetRunInfo(inputfilename)

    NumberOfEvents=hdf5io.GetNumberOfEvents(RunInfo)

    logging.info("Computing Voltages for "+inputfilename+", found "+str(NumberOfEvents)+" events")

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

      logging.info("computing voltage for antenna "+antennaID+" ("+str(i+1)+"/"+str(nantennas)+")")

      position=hdf5io.GetAntennaPosition(AntennaInfo,i)
      logging.debug("at position"+str(position))

      slopes=hdf5io.GetAntennaSlope(AntennaInfo,i)

      #A NICE call to the radio-simus library. Configuration and details of the voltage computation unavailable for now!.
      #Configuration should be a little more "present" in the function call,
      #also maybe the library to handle .ini files would be more profesional and robust than current implementation

      #other detail, we are storing things in astropy arrays, but then switching to numpy, that needs Transposition. This is not very efficient.
      #I hide this detail to hf5io, so that the names of the field dont remain hardcoded in the script
      efield=hdf5io.GetAntennaEfield(inputfilename,EventName,antennaID)

      #i compute the antenna response using the compute_antennaresponse function
      voltage = compute_antennaresponse(efield, Zenith, Azimuth, alpha=slopes[0], beta=slopes[1] )

      #now i need to put a numpy array into an astropy table, but before y change the data type to float32 so that it takes less space (its still good to 7 decimals)
      voltage32= voltage.astype('f4')
      TableVoltage = hdf5io.CreateVoltageTable(voltage32,EventName,0,antennaID,i,"computevoltage.compute_antennaresponse")

      #and this is saved to the hdf5 file
      hdf5io.SaveVoltageTable(outfilename,EventName,antennaID,TableVoltage)

      if(FreqMin!=FreqMax):
        #filtering the trace using the filters function in signal_processing
        filteredvoltage=filters(voltage, FreqMin, FreqMax)
        #now i need to put a numpy array into an astropy table, but before y change the data type to float32 so that it takes less space (its still good to 7 decimals)
        filteredvoltage32=filteredvoltage.astype('f4')
        TableFilteredVoltage = hdf5io.CreateVoltageTable(filteredvoltage32,EventName,0,antennaID,i,"signal_processing.filters",info={"FreqMin":FreqMin,"FreqMax":FreqMax})
        hdf5io.SaveFilteredVoltageTable(outfilename,EventName,antennaID,TableFilteredVoltage)
      #endif

    #end for

    if inputfilename!=outfilename:
      import RemoveTableFromHDF5 as rt
      #this should copy allt the contents from the input file, inthe outputfile, exept the traces
      logging.debug("Copying tables from field file")
      rt.RemoveTableFromHDF5(inputfilename,outfilename,"AntennaTraces")

  else:
   logging.critical("input file " + inputfilename + " does not exist or is not a directory. ComputeVoltageOnSHDF5 cannot continue")


if __name__ == '__main__':

  if ( len(sys.argv)<2 ):
    print("usage ComputVoltagaOnHDF5 inputfile (outputfile)")
    print("if outputfile is not specified, voltage is writen on the same file")

  if ( len(sys.argv)==2 ):
   inputfile=sys.argv[1]
   ComputeVoltageOnHDF5(inputfile)

  if ( len(sys.argv)==3 ):
   inputfile=sys.argv[1]
   outputfile=sys.argv[2]
   ComputeVoltageOnHDF5(inputfile,outfilename=outputfile)




