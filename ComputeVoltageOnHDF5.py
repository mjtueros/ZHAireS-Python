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

#if no outfilename is given, it will store the table in the same HDF5 dile, in a separate table (handle what happens if it already exists)

#this computes the voltage on all the antennas, but if this gets too CPU intense in some application we might want to apply some filter,
#that could go in the funnction call like...such as only compute if the peak to peak amplitude is higher than something, or the distance to the core is less than something.

def ComputeVoltageOnHDF5(inputfilename,EventNumber=0,FreqMin=50.e6,FreqMax=200.e6,outfilename="N/A"):
#EventNumber=all could trigger a loop on all events in the file.

  if os.path.isfile(inputfilename):
    if(outfilename=="N/A"):
      outfilename=inputfilename

      RunInfo=hdf5io.GetRunInfo(inputfilename)

      NumberOfEvents=len(RunInfo) #Should this be hdf5io.GetNumberOfEvents(filename (o RunInfo)?)? Probably
      print("Opening "+inputfilename+", found "+str(NumberOfEvents)+" events")

      EventName=RunInfo["EventName"][0] #This gets the Column EventName of the table. Should this be hdf5io.GetEventName(RunInfo?, eventnumber) Yes!
      Zenith=RunInfo["Zenith"][0]
      Azimuth=RunInfo["Azimuth"][0]
      print(EventName,Zenith,Azimuth)
      print(EventName,type(Zenith),type(Azimuth))

      AntennaInfo=hdf5io.GetAntennaInfo(inputfilename,EventName)
      nantennas=len(AntennaInfo)  #Should this be hdf5io.GetNumberOfAntennas(AntennaInfo)? Possibly
      print("Found "+str(nantennas)+" antennas")

      #about this loop: note that astropy table could use their oun iterator, like: "for row in table:" andthen access row['columnname'].
      #The porblem with this, is that it hardwires the file structure into the code, and i dont want that. All those details must remain hidden in hdf5io, so that we dont have
      #all the scripts if we decide to change something on the file format/structure.

      for i in range(0,nantennas):

        antennaID=AntennaInfo["ID"][i] #Should this be hdf5io.GetAntennaID(AntennaInfo, AntennaNumber)? yes, it should.

        logging.info("computing voltage for antenna "+antennaID+" ("+str(i+1)+"/"+str(nantennas)+")")

        position=(AntennaInfo["X"][i],AntennaInfo["Y"][i],AntennaInfo["Z"][i]) #yes, this should be a call to hdf5io.GetAntennaPosition(AntennaInfo,AntennaNumber)
        logging.debug("at position"+str(position))

        #in the current implementation, the electric field trace is stored in an astropy table
        #trace=hdf5io.GetElectricFieldTrace(inputfilename,antennaID)
        #slopes=hdf5io.GetSlopesFromTrace(trace)
        slopes=(AntennaInfo["SlopeA"][i] ,AntennaInfo["SlopeB"][i]) #and this a call to hdf5io.GetAntennaSlope(AntennaInfo,AntennaNumber)

        #A NICE call to the radio-simus library. Configuration and details of the voltage computation unavailable for now!.
        #Configuration should be a little more "present" in the function call,
        #also maybe the library to handle .ini files would be more profesional and robust than current implementation

        #other detail, we are storing things in astropy arrays, but then switching to numpy, that needs Transposition. This is not very efficient.
        #I hide this detail to hf5io, so that the names of the field dont remain hardcoded in the script
        #efield=hdf5io.ElectricFieldTraceToNumpy(trace)
        efield=hdf5io.GetAntennaEfield(inputfilename,EventName,antennaID)

        voltage = compute_antennaresponse(efield, Zenith, Azimuth, alpha=slopes[0], beta=slopes[1] )

        #now i need to put a numpy array into an astropy table, but before y change the data type to float32 so that it takes less space (its still good to 7 decimals)
        voltage32= voltage.astype('f4')
        TableVoltage = hdf5io.CreateVoltageTable(voltage32,EventName,0,antennaID,i,"computevoltage.compute_antennaresponse")

        #and this is saved to the hdf5 file
        hdf5io.SaveVoltageTable(outfilename,EventName,antennaID,TableVoltage)

        if(FreqMin!=FreqMax):
          filteredvoltage=filters(voltage, FreqMin, FreqMax)
          filteredvoltage32=voltage.astype('f4')
          TableFilteredVoltage = hdf5io.CreateVoltageTable(filteredvoltage32,EventName,0,antennaID,i,"signal_processing.filters",info={"FreqMin":FreqMin,"FreqMax":FreqMax})
          hdf5io.SaveFilteredVoltageTable(outfilename,EventName,antennaID,TableFilteredVoltage)


        #end for

  else:
   logging.critical("input file " + inputfilename + " does not exist or is not a directory. ComputeVoltageOnSHDF5 cannot continue")


if __name__ == '__main__':

  if ( len(sys.argv)<2 ):
    print("usage")

  else:
   inputfile=sys.argv[1]
   ComputeVoltageOnHDF5(inputfile)

