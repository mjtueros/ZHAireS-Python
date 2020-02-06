
from astropy.table import Table, Column
from astropy import units as u
import numpy as np


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

def SaveAntennaInfo(OutFilename,AntennaInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/AntennaInfo
   AntennaInfo.write(OutFilename, path=EventName+"/AntennaInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

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

def CreateAntennaInfo(IDs, antx, anty, antz, slopeA, slopeB, AntennaInfoMeta):
   #TODO: Handle errors
    a4=Column(data=IDs,name='ID')
    b4=Column(data=antx,name='X',unit=u.m) #in core cordinates
    c4=Column(data=anty,name='Y',unit=u.m) #in core cordinates
    d4=Column(data=antz,name='Z',unit=u.m) #in core cordinates
    e4=Column(data=slopeA,name='SlopeA',unit=u.m) #in core cordinates
    f4=Column(data=slopeB,name='SlopeB',unit=u.m) #in core cordinates

    #g4=Column(data=Ep2p,name='FieldP2P',unit=u.V/u.m) #p2p Value of the electric field #TODO:
    #h4=Column(data=Ep2p,name='VoltageP2P',unit=u.V) #p2p Value of the electric field + antenna response #TODO:
    #h4=Column(data=Ep2p,name='FilteredVoltageP2P',unit=u.V) #p2p Value of the electric field + antenna response + filtering #TODO:

    AstropyTable = Table(data=(a4,b4,c4,d4,e4,f4),meta=AntennaInfoMeta)
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







