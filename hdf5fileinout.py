
from astropy.table import Table, Column
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt


################################################################################################################################
#### by M. Tueros. Shared with the Wineware licence. Support and feature requests accepted only accompanied by bottles of wine.
################################################################################################################################
#this library provides a user interface and defines HDF5 file format for the GRAND experiment
#
# FILE FORMAT (0.0)
#============================
# RunInfo (AstropyTable).
#============================
#This table holds the list of events present on the file, and some general parameters to aid event selection.
#each event is in a separate folder.
#each table has its meta in TableName._table_column_meta__
#     the meta has the units of each value in the table, and maybe something more)
#
# EVENT FORMAT (0.0)
#============================
# EventInfo (AstropyTable)
#============================
# containing general shower information (zenith, azimuth, energy, xmax, xmax position and the like) (for now the meta of EventInfo for compatibility with anne)
# the meta contains the list of suported tables in the event , and if they are present (True) or not (Fase)
#=============================
# ShowerSimInfo (AstropyTable)
#=============================
# showersimulation: simulation details: thinning paramethers, energy cut, ground altitude, injection height, atmospheric model, hadronic model. number of observing levels, number of lateral bins
#=============================
# SignalSimInfo (AstropyTable)
#=============================
# containing details on the electric field computation: index of refraction model, tmin, tmax, tbin (this would be the meta of the antenalist)
#=============================
# AntennaInfo (AstropyTable)
#=============================
# containing the names, positions, slopes and probabbly p2p amplitudes and such of each antenna
#=============================
# (SubFolder) AntenaTraces
#=============================
# This subfolder holds one sub-subfolder per antenna (named after the antenna name).
# each sub-subfolder holds one table per trace.
#=============================
# (AntennaName)   efield  (the electric field produced by the shower)
#                 voltage (the antenna response to said field)
#                 noise   (the ambien noise to be added to the voltage)
#                 filteredvoltage (the antenna response after the electronics)
#                 filterednoise (the ambient noise after the electonics - including electronics noise)
#
#=============================
# (SubFolder) ShowerTables
#==============================
# In this SubFolder we store different tables from the shower simulation
#=======================================
# EGround (AstropyTable)
#=======================================
# Contains the energy distribution of particles arriving at ground level
#=======================================
# ELongitudinalProfile (AstropyTable)
#=======================================
# Contains the longitudinal evolution of the energy content in each particle species
#=======================================
# EdepLongitudinalProfile (AstropyTable)
#=======================================
# Contains the longitudinal evolution of the energy deposit by each particle species
#=======================================
# ElowLongitudinalProfile (AstropyTable)
#=======================================
# Contains the longitudinal evolution of the energy of the discarded low energy particles
#=======================================
# NLateralProfile (AstropyTable)
#=======================================
# Contains the lateral distribution of particles at ground level (in radial bins)
#=======================================
# NLongitudinalProfile (AstropyTable)
#=======================================
# Contains the longitudinal evolution of the of the numebr of particles
#=======================================
# NlowLongitudinalProfile (AstropyTable)
#=======================================
# Contains the longitudinal evolution of the number of dicarded  low energy particles
#
################################################################################################################################################################
# Table Savers
################################################################################################################################################################

#all the error handling might be easier defined in a general routine: SaveAstropyTable(Tablepath/TableName)
def SaveRunInfo(OutFilename,RunInfo):
   #TODO: Handle error when OutFilename already contains RunInfo
   RunInfo.write(OutFilename, path="RunInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveEventInfo(OutFilename,EventInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/EventInfo
   EventInfo.write(OutFilename, path=EventName+"/EventInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveAntennaInfo(OutFilename,AntennaInfo,EventName,overwrite=False):
   #TODO: Handle error when OutFilename already contains EventName/AntennaInfo
   #if overwrite=True, it will overwrite the contennts in AntennaInfo, but not on the file (becouse append is True)
   AntennaInfo.write(OutFilename, path=EventName+"/AntennaInfo", format="hdf5", append=True,  compression=True, serialize_meta=True, overwrite=overwrite)

def SaveAntennaInfo4(OutFilename,AntennaInfo,EventName,overwrite=False):
   #TODO: Handle error when OutFilename already contains EventName/AntennaInfo
   #if overwrite=True, it will overwrite the contennts in AntennaInfo, but not on the file (becouse append is True)
   AntennaInfo.write(OutFilename, path=EventName+"/AntennaInfo4", format="hdf5", append=True,  compression=True, serialize_meta=True, overwrite=overwrite)

def SaveShowerSimInfo(OutFilename,ShowerSimInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerSimInfo
   ShowerSimInfo.write(OutFilename, path=EventName+"/ShowerSimInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveSignalSimInfo(OutFilename,SignalSimInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/SignalSimInfo
   SignalSimInfo.write(OutFilename, path=EventName+"/SignalSimInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveNLongitudinal(OutFilename,NLongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/NLongitudinalProfile
   NLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/NLongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveELongitudinal(OutFilename,ELongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/ELongitudinalProfile
   ELongitudinal.write(OutFilename, path=EventName+"/ShowerTables/ELongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveNlowLongitudinal(OutFilename,NlowLongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/NlowLongitudinalProfile
   NlowLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/NlowLongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveElowLongitudinal(OutFilename,ElowLongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/ElowLongitudinalProfile
   ElowLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/ElowLongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveEdepLongitudinal(OutFilename,EdepLongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/EdepLongitudinalProfile
   EdepLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/EdepLongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveLateralDistribution(OutFilename,NLateral,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/NLateral
   NLateral.write(OutFilename, path=EventName+"/ShowerTables/NLateralProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveEnergyDistribution(OutFilename,EGround,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/EGRound
   EGround.write(OutFilename, path=EventName+"/ShowerTables/EGround", format="hdf5", append=True,  compression=True, serialize_meta=True)


######################################################################################################################################################################
# Table Getters
######################################################################################################################################################################

def GetRunInfo(InputFilename):
   #TODO: Handle error when "RunInfo" does not exists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   RunInfo=Table.read(InputFilename, path="RunInfo")
   return RunInfo

def GetEventInfo(InputFilename,EventName):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/EventInfo" does not exists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   EventInfo=Table.read(InputFilename, path=EventName+"/EventInfo")
   return EventInfo

def GetAntennaInfo(InputFilename,EventName):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaInfo" does not exists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   AntennaInfo=Table.read(InputFilename, path=EventName+"/AntennaInfo")
   return AntennaInfo

def GetAntennaInfo4(InputFilename,EventName):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaInfo" does not exists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   AntennaInfo=Table.read(InputFilename, path=EventName+"/AntennaInfo4")
   return AntennaInfo

def GetAntennaEfield(InputFilename,EventName,AntennaName,OutputFormat="numpy"):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaTraces" does not exists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName" does not exsists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName/Efield" does not exsists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   EfieldTrace=Table.read(InputFilename, path=str(EventName)+"/AntennaTraces/"+str(AntennaName)+"/efield")
   if(OutputFormat=="numpy"):
     EfieldTrace=np.array([EfieldTrace['Time'], EfieldTrace['Ex'],EfieldTrace['Ey'],EfieldTrace['Ez']]).T
   return EfieldTrace

def GetAntennaVoltage(InputFilename,EventName,AntennaName,OutputFormat="numpy"):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaTraces" does not exists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName" does not exsists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName/Efield" does not exsists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   VoltageTrace=Table.read(InputFilename, path=str(EventName)+"/AntennaTraces/"+str(AntennaName)+"/voltage")
   if(OutputFormat=="numpy"):
     VoltageTrace=np.array([VoltageTrace['Time'], VoltageTrace['Vx'],VoltageTrace['Vy'],VoltageTrace['Vz']]).T
   return VoltageTrace

def GetAntennaFilteredVoltage(InputFilename,EventName,AntennaName,OutputFormat="numpy"):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaTraces" does not exists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName" does not exsists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName/Efield" does not exsists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   VoltageTrace=Table.read(InputFilename, path=str(EventName)+"/AntennaTraces/"+str(AntennaName)+"/filteredvoltage")
   if(OutputFormat=="numpy"):
     VoltageTrace=np.array([VoltageTrace['Time'], VoltageTrace['Vx'],VoltageTrace['Vy'],VoltageTrace['Vz']]).T
   return VoltageTrace


def GetShowerSimInfo(InputFilename,EventName):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/EventInfo" does not exists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   ShowerSimInfo=Table.read(InputFilename, path=EventName+"/ShowerSimInfo")
   return ShowerSimInfo

def GetSignalSimInfo(InputFilename,EventName):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/EventInfo" does not exists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   SignalSimInfo=Table.read(InputFilename, path=EventName+"/SignalSimInfo")
   return SignalSimInfo

#######################################################################################################################################################################
# RunInfo Getters
#######################################################################################################################################################################

def GetNumberOfEvents(RunInfo):
   #TODO: Handle errors
    return len(RunInfo)

def GetEventName(RunInfo,EventNumber):
   #TODO: Handle errors
    return RunInfo["EventName"][EventNumber]

def GetEventZenith(RunInfo,EventNumber):
   #TODO: Handle errors
    return float(RunInfo["Zenith"][EventNumber])

def GetEventAzimuth(RunInfo,EventNumber):
   #TODO: Handle errors
    return float(RunInfo["Azimuth"][EventNumber])

def GetEventPrimary(RunInfo,EventNumber):
   #TODO: Handle errors
    return str(RunInfo["Primary"][EventNumber])

def GetEventEnergy(RunInfo,EventNumber):
   #TODO: Handle errors
    return float(RunInfo["Energy"][EventNumber])

def GetEventXmaxDistance(RunInfo,EventNumber):
   #TODO: Handle errors
    return float(RunInfo["XmaxDistance"][EventNumber])

def GetEventSlantXmax(RunInfo,EventNumber):
   #TODO: Handle errors
    return float(RunInfo["SlantXmax"][EventNumber])

def GetEventEnergy(RunInfo,EventNumber):
   #TODO: Handle errors
    return float(RunInfo["Energy"][EventNumber])

def GetEventHadronicModel(RunInfo,EventNumber):
   #TODO: Handle errors
    return str(RunInfo["HadronicModel"][EventNumber])

#######################################################################################################################################################################
# EventInfo Getters
#######################################################################################################################################################################
#TODO: define magnetic field units and coordinate frame propperly. Current implementation uses ZHAireS conventions, but this needs be standarized.

def GetEventBFieldIncl(EventInfo):
   #TODO: Handle errors
    return float(EventInfo["BFieldIncl"])

def GetEventBFieldDecl(EventInfo):
   #TODO: Handle errors
    return float(EventInfo["BFieldDecl"])

def GetGroundAltitude(EventInfo):
   #TODO: Handle errors
    return float(EventInfo["GroundAltitude"])

#######################################################################################################################################################################
# SignalSimInfo Getters
#######################################################################################################################################################################
def GetTimeBinSize(SignalSimInfo):
   #TODO: Handle errors
    return float(SignalSimInfo["TimeBinSize"])

def GetTimeWindowMin(SignalSimInfo):
   #TODO: Handle errors
    return float(SignalSimInfo["TimeWindowMin"])

def GetTimeWindowMax(SignalSimInfo):
   #TODO: Handle errors
    return float(SignalSimInfo["TimeWindowMax"])

#######################################################################################################################################################################
# AntennaInfo Getters
#######################################################################################################################################################################

def CreatAntennaInfoMeta(RunName,EventName,VoltageSimulator="N/A",AntennaModel="N/A",EnvironmentNoiseSimulator="N/A",ElectronicsSimulator="N/A",ElectronicsNoiseSimulator="N/A"):
   #TODO: Handle errors
    AntennaInfoMeta = {
           "RunName":RunName,                                        #For cross checking
           "EventName":EventName,                                    #For cross checking
           "VoltageSimulator": VoltageSimulator,                     #TODO: decide what goes here
           "AntennaModel": AntennaModel,
           "EnvironmentNoiseSimulator": EnvironmentNoiseSimulator,
           "ElectronicsSimulator": ElectronicsSimulator,
           "ElectronicsNoiseSimulator": ElectronicsNoiseSimulator
    }
    return AntennaInfoMeta

def CreateAntennaInfo(IDs, antx, anty, antz, slopeA, slopeB, AntennaInfoMeta, P2Pefield=None,P2Pvoltage=None,P2Pfiltered=None,HilbertPeak=None,HilbertPeakTime=None):
   #TODO: Handle errors
    a4=Column(data=IDs,name='ID')
    b4=Column(data=antx,name='X',unit=u.m) #in core cordinates
    c4=Column(data=anty,name='Y',unit=u.m) #in core cordinates
    d4=Column(data=antz,name='Z',unit=u.m) #in core cordinates
    e4=Column(data=slopeA,name='SlopeA',unit=u.m) #in core cordinates
    f4=Column(data=slopeB,name='SlopeB',unit=u.m) #in core cordinates
    data=[a4,b4,c4,d4,e4,f4]

    if P2Pefield is not None:
      P2Pefield32=P2Pefield.astype('f4') #reduce the data type to float 32

      g4=Column(data=P2Pefield32[3,:],name='P2P_efield',unit=u.u*u.V/u.m) #p2p Value of the electric field
      data.append(g4)
      g4=Column(data=P2Pefield32[0,:],name='P2Px_efield',unit=u.u*u.V/u.m) #p2p Value of the electric field
      data.append(g4)
      g4=Column(data=P2Pefield32[1,:],name='P2Py_efield',unit=u.u*u.V/u.m) #p2p Value of the electric field
      data.append(g4)
      g4=Column(data=P2Pefield32[2,:],name='P2Pz_efield',unit=u.u*u.V/u.m) #p2p Value of the electric field
      data.append(g4)
      AntennaInfoMeta.update(P2Pefield=True)

    if P2Pvoltage is not None:
      P2Pvoltage32=P2Pvoltage.astype('f4') #reduce the data type to float 32

      g4=Column(data=P2Pvoltage32[3,:],name='P2P_voltage',unit=u.u*u.V) #p2p Value of the voltage
      data.append(g4)
      g4=Column(data=P2Pvoltage32[0,:],name='P2Px_voltage',unit=u.u*u.V) #p2p Value of the voltage
      data.append(g4)
      g4=Column(data=P2Pvoltage32[1,:],name='P2Py_voltage',unit=u.u*u.V) #p2p Value of the voltage
      data.append(g4)
      g4=Column(data=P2Pvoltage32[2,:],name='P2Pz_voltage',unit=u.u*u.V) #p2p Value of the voltage
      data.append(g4)
      AntennaInfoMeta.update(P2Pvoltage=True)

    if P2Pfiltered is not None:
      P2Pfiltered32=P2Pfiltered.astype('f4') #reduce the data type to float 32

      g4=Column(data=P2Pfiltered32[3,:],name='P2P_filtered',unit=u.u*u.V) #p2p Value of the filtered voltage
      data.append(g4)
      g4=Column(data=P2Pfiltered32[0,:],name='P2Px_filtered',unit=u.u*u.V) #p2p Value of the filtered voltage
      data.append(g4)
      g4=Column(data=P2Pfiltered32[1,:],name='P2Py_filtered',unit=u.u*u.V) #p2p Value of the filtered voltage
      data.append(g4)
      g4=Column(data=P2Pfiltered32[2,:],name='P2Pz_filtered',unit=u.u*u.V) #p2p Value of the filtered voltage
      data.append(g4)
      AntennaInfoMeta.update(P2Pfiltered=True)

    if HilbertPeak is not None:
      HilbertPeak32=HilbertPeak.astype('f4') #reduce the data type to float 32
      g4=Column(data=HilbertPeak32,name='HilbertPeak') #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeak=True)

    if HilbertPeakTime is not None:
      HilbertPeakTime32=HilbertPeakTime.astype('f4') #reduce the data type to float 32
      g4=Column(data=HilbertPeakTime32,name='HilbertPeakTime',unit=u.u*u.s) #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeakTime=True)


    AstropyTable = Table(data=data,meta=AntennaInfoMeta)
    return AstropyTable

def GetNumberOfAntennas(AntennaInfo):
   #TODO: Handle errors
    return len(AntennaInfo)

def GetAntIDFromAntennaInfo(AntennaInfo):
   #TODO: Handle errors
   return AntennaInfo["ID"]

def GetXFromAntennaInfo(AntennaInfo):
   #TODO: Handle errors
   return AntennaInfo["X"]

def GetYFromAntennaInfo(AntennaInfo):
   #TODO: Handle errors
   return AntennaInfo["Y"]

def GetZFromAntennaInfo(AntennaInfo):
   #TODO: Handle errors
   return AntennaInfo["Z"]

def GetSlopesFromTrace(Trace):
   return Trace.meta['slopes']

def GetAntennaID(AntennaInfo,AntennaNumber):
   #TODO: Handle errors
    return AntennaInfo["ID"][AntennaNumber]

def GetAntennaPosition(AntennaInfo,AntennaNumber):
   #TODO: Handle errors
    return (AntennaInfo["X"][AntennaNumber],AntennaInfo["Y"][AntennaNumber],AntennaInfo["Z"][AntennaNumber])

def GetAntennaSlope(AntennaInfo,AntennaNumber):
   #TODO: Handle errors
    return (AntennaInfo["SlopeA"][AntennaNumber] ,AntennaInfo["SlopeB"][AntennaNumber])

def GetAntennaPositions(AntennaInfo):
   #TODO: Handle errors
    return (AntennaInfo["X"][:],AntennaInfo["Y"][:],AntennaInfo["Z"][:])

def GetMetaFromTable(AstropyTable):
   return AstropyTable.meta

def GetAntennaInfoFromEventInfo(EventInfo,nant):
   return EventInfo[nant]

########################################################################################################################

def CreateEfieldTable(efield, EventName, EventNumber, AntennaID, AntennaNumber,FieldSimulator, info={}):
    '''
    Create electric field trace in table with header info (numpy array to astropy table)

    Parameters
    ---------
    efield: numpy array
        electric field trace
    EventName: str
        The Name of the Event, for checking or getting other info on the EventInfo Table
    EventNumber:int
        The number of event in the EventInfo table, for fast access
    AntennaID: str
        The ID of the Antenna, for checking or getting other info from the AntennaInfo Table
    AntennaNumber: int
        The number of antenna in the AntennaInfo table, for fast access
    info: dict
        contains meta info

    Returns
    ---------
    efield_ant: astropy table
        The electric field trace as an astropy table

    '''
    info.update({'FieldSimulator':FieldSimulator,'EventName': EventName, 'EventNumber': EventNumber, 'AntennaID':AntennaID, 'AntennaNumber':AntennaNumber})

    a = Column(data=efield.T[0],unit=u.ns,name='Time',)
    b = Column(data=efield.T[1],unit=u.u*u.V/u.meter,name='Ex')
    c = Column(data=efield.T[2],unit=u.u*u.V/u.meter,name='Ey')
    d = Column(data=efield.T[3],unit=u.u*u.V/u.meter,name='Ez')
    efield_ant = Table(data=(a,b,c,d,), meta=info)

    return efield_ant

def SaveEfieldTable(outputfilename,EventName,antennaID,efield):
   #TODO: HAndle error when "efield" already exists
   #TODO: HAndle error when "outputfilename" is not a file, or a valid file.
   #TODO: Adjust format so that we have the relevant number of significant figures. Maybe float64 is not necesary?. What about using float32 or even float 16?
   efield.write(outputfilename, path=EventName+"/AntennaTraces/"+antennaID+"/efield", format="hdf5", append=True, compression=True,serialize_meta=True)



def CreateVoltageTable(voltage, EventName, EventNumber, AntennaID, AntennaNumber, VoltageSimulator, info={}):
    '''
    Create voltage trace in table with header info  (numpy array to astropy table)

    Parameters
    ---------
    voltage: numpy array
        voltage trace
    EventName: str
        The Name of the Event, for checking or getting other info on the EventInfo Table
    EventNumber:int
        The number of event in the EventInfo table, for fast access
    AntennaID: str
        The ID of the Antenna, for checking or getting other info from the AntennaInfo Table
    AntennaNumber: int
        The number of antenna in the AntennaInfo table, for fast access
    info: dict
        contains meta info

    Returns
    ---------
    voltage_ant: astropy table
        The voltage trace as an Astropy table

    '''
    info.update({'VoltageSimulator':VoltageSimulator,'EventName': EventName, 'EventNumber': EventNumber, 'AntennaID':AntennaID, 'AntennaNumber':AntennaNumber})

    a = Column(data=voltage.T[0],unit=u.ns,name='Time')
    b = Column(data=voltage.T[1],unit=u.u*u.V,name='Vx')
    c = Column(data=voltage.T[2],unit=u.u*u.V,name='Vy')
    d = Column(data=voltage.T[3],unit=u.u*u.V,name='Vz')
    voltage_ant = Table(data=(a,b,c,d,), meta=info)
    return voltage_ant

def SaveVoltageTable(outputfilename,EventName,antennaID,voltage):
   #TODO: HAndle error when "voltage" already exists
   #TODO: HAndle error when "outputfilename" is not a file, or a valid file.
   voltage.write(outputfilename, path=EventName+"/AntennaTraces/"+antennaID+"/voltage", format="hdf5", append=True,compression=True,serialize_meta=True)

def SaveFilteredVoltageTable(outputfilename,EventName,antennaID,filteredvoltage):
   #TODO: HAndle error when "voltage" already exists
   #TODO: HAndle error when "outputfilename" is not a file, or a valid file.
   filteredvoltage.write(outputfilename, path=EventName+"/AntennaTraces/"+antennaID+"/filteredvoltage", format="hdf5", append=True,compression=True,serialize_meta=True)

#######################################################################################################################################################################
# Other Stuff to see how things could be done
#######################################################################################################################################################################

def get_p2p_hdf5(InputFilename,antennamax='All',antennamin=0,usetrace='efield'):

    #TODO: Handle Errors
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
    CurrentRunInfo=GetRunInfo(InputFilename)
    CurrentEventName=GetEventName(CurrentRunInfo,0) #using the first event of each file (there is only one for now)
    CurrentAntennaInfo=GetAntennaInfo(InputFilename,CurrentEventName)

    if(antennamax=='All'):
     antennamax=len(CurrentAntennaInfo)-1

    # create an array
    p2p_Ex = np.zeros(1+antennamax-antennamin)
    p2p_Ey = np.zeros(1+antennamax-antennamin)
    p2p_Ez = np.zeros(1+antennamax-antennamin)
    p2p_total = np.zeros(1+antennamax-antennamin)
    p2pE=np.zeros(1+antennamax-antennamin)

    for i in range(antennamin,antennamax+1):
      AntennaID=GetAntennaID(CurrentAntennaInfo,i)
      if(usetrace=='efield'):
        trace=GetAntennaEfield(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      elif(usetrace=='voltage'):
        trace=GetAntennaVoltage(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      elif(usetrace=='filteredvoltage'):
        trace=GetAntennaFilteredVoltage(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      else:
        print('You must specify either efield, voltage or filteredvoltage, bailing out')

      #transposing takes a lot of time
      #p2p_Ex[i] = max(trace.T[1])-min(trace.T[1])
      #p2p_Ey[i] = max(trace.T[2])-min(trace.T[2])
      #p2p_Ez[i] = max(trace.T[3])-min(trace.T[3])
      p2p= np.amax(trace,axis=0)-np.amin(trace,axis=0)
      p2p_Ex[i-antennamin]= p2p[1]
      p2p_Ey[i-antennamin]= p2p[2]
      p2p_Ez[i-antennamin]= p2p[3]

      #amplitude = np.sqrt(trace.T[1]**2. + trace.T[2]**2. + trace.T[3]**2.) # combined components
      amplitude = np.sqrt(trace[:,1]**2. + trace[:,2]**2. + trace[:,3]**2.) # combined components
      #print(amplitude-amplitude2)

      p2p_total[i-antennamin] = max(amplitude)-min(amplitude)

      #print(p2p_Ex,p2p_Ey,p2p_Ez,p2p_total)

    p2pE = np.stack((p2p_Ex, p2p_Ey, p2p_Ez, p2p_total), axis=0)
    return p2pE

def get_peak_time_hilbert_hdf5(InputFilename, antennamax="All",antennamin=0, usetrace="efield", DISPLAY=False) :
#adapted from Valentin Decoene
    #TODO: Handle Errors
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
    peaktime: numpy array with the time of the maximum of the hilbert amplitude of the strongest channel
    peakamplitude: numpy array with the maximum of the hilbert amplitude of the strongest channel
    '''
    DISPLAY=False
    CurrentRunInfo=GetRunInfo(InputFilename)
    CurrentEventName=GetEventName(CurrentRunInfo,0) #using the first event of each file (there is only one for now)
    CurrentAntennaInfo=GetAntennaInfo(InputFilename,CurrentEventName)

    if(antennamax=='All'):
      antennamax=len(CurrentAntennaInfo)-1

    peaktime= np.zeros(1+antennamax-antennamin)
    peakamplitude= np.zeros(1+antennamax-antennamin)

    for i in range(antennamin,antennamax+1):
      AntennaID=GetAntennaID(CurrentAntennaInfo,i)
      if(usetrace=='efield'):
        trace=GetAntennaEfield(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      elif(usetrace=='voltage'):
        trace=GetAntennaVoltage(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      elif(usetrace=='filteredvoltage'):
        trace=GetAntennaFilteredVoltage(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
      else:
        print('You must specify either efield, voltage or filteredvoltage, bailing out')

      from scipy.signal import hilbert
      #now, this is not doing exactly what i was expecting (the hilbert of each component separately. When i plot it, it seems to be mixing channels up)
      #however, it does get the maximum of the modulus of the signal (but i dont understand whats really going on!)
      hilbert_trace=hilbert(trace[:,1:4])
      hilbert_amp = np.abs(hilbert_trace) 												                     #enveloppe de hilbert x, y, z channels
      peakamplitude[i-antennamin]=max([max(hilbert_amp[:,0]), max(hilbert_amp[:,1]), max(hilbert_amp[:,2])]) #find best peakamp for the 3 channels
      peaktime[i-antennamin]=trace[np.where(hilbert_amp == peakamplitude[i-antennamin])[0],0]                # get the time of the peak amplitude


      #PLOT
      if DISPLAY :
        print(peakamplitude[i-antennamin])
        print('peaktime = ',peaktime[i-antennamin])

        hilbert_trace_x=hilbert(trace[:,1])
        hilbert_amp_x = np.abs(hilbert_trace_x)
        hilbert_trace_y=hilbert(trace[:,2])
        hilbert_amp_y = np.abs(hilbert_trace_y)
        hilbert_trace_z=hilbert(trace[:,3])
        hilbert_amp_z = np.abs(hilbert_trace_z)

        hilbert_amp2=np.zeros(np.shape(trace[:,1:4]))
        hilbert_amp2[:,0]=hilbert_amp_x
        hilbert_amp2[:,1]=hilbert_amp_y
        hilbert_amp2[:,2]=hilbert_amp_z
        #peakamplitude[i-antennamin]=max([max(hilbert_amp2[:,0]), max(hilbert_amp2[:,1]), max(hilbert_amp2[:,2])]) #find best peakamp for the 3 channels
        #peaktime[i-antennamin]=trace[np.where(hilbert_amp2 == peakamplitude[i-antennamin])[0],0]                # get the time of the peak amplitude


        fig1 = plt.figure(1,figsize=(7,5), dpi=100, facecolor='w', edgecolor='k')

        ax1=fig1.add_subplot(221)
        plt.plot(trace[:,0], hilbert_amp[:,0], label = 'Hilbert env channel x')
        plt.plot(trace[:,0], trace[:,1], label = 'channel x')
        plt.plot(trace[:,0], hilbert_amp_x, label = 'Hilbertx env channel x')

        plt.legend(loc = 'best')

        ax1=fig1.add_subplot(222)
        plt.plot(trace[:,0], hilbert_amp[:,1], label = 'Hilbert env channel y')
        plt.plot(trace[:,0], trace[:,2], label = 'channel y')
        plt.plot(trace[:,0], hilbert_amp_y, label = 'Hilbertx env channel y')
        plt.legend(loc = 'best')

        ax1=fig1.add_subplot(223)
        plt.plot(trace[:,0], hilbert_amp[:,2], label = 'Hilbert env channel z')
        plt.plot(trace[:,0], trace[:,3], label = 'channel z')
        plt.plot(trace[:,0], hilbert_amp_z, label = 'Hilbertx env channel z')
        plt.legend(loc = 'best')

        ax1=fig1.add_subplot(224)
        plt.plot(trace[:,0], np.sqrt(trace[:,1]**2 + trace[:,2]**2 + trace[:,3]**2), label = 'modulus signal')
        plt.axvline(peaktime[i-antennamin], color='r', label = 'Timepeak')
        plt.xlabel('Time (ns)')
        plt.ylabel('Amplitude (muV) (s)')
        plt.legend(loc = 'best')
        plt.show()

    return peaktime, peakamplitude





