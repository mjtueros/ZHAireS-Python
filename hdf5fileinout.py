
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
   #ToDO: Handle error when OutFilename already contains RunInfo
   RunInfo.write(OutFilename, path="RunInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveEventInfo(OutFilename,EventInfo,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/EventInfo
   EventInfo.write(OutFilename, path=EventName+"/EventInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveAntennaInfo(OutFilename,AntennaInfo,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/AntennaInfo
   AntennaInfo.write(OutFilename, path=EventName+"/AntennaInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveShowerSimInfo(OutFilename,ShowerSimInfo,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/ShowerSimInfo
   ShowerSimInfo.write(OutFilename, path=EventName+"/ShowerSimInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveSignalSimInfo(OutFilename,SignalSimInfo,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/SignalSimInfo
   SignalSimInfo.write(OutFilename, path=EventName+"/SignalSimInfo", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveNLongitudinal(OutFilename,NLongitudinal,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/ShowerTables/NLongitudinalProfile
   NLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/NLongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveELongitudinal(OutFilename,ELongitudinal,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/ShowerTables/ELongitudinalProfile
   ELongitudinal.write(OutFilename, path=EventName+"/ShowerTables/ELongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveNlowLongitudinal(OutFilename,NlowLongitudinal,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/ShowerTables/NlowLongitudinalProfile
   NlowLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/NlowLongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveElowLongitudinal(OutFilename,ElowLongitudinal,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/ShowerTables/ElowLongitudinalProfile
   ElowLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/ElowLongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveEdepLongitudinal(OutFilename,EdepLongitudinal,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/ShowerTables/EdepLongitudinalProfile
   EdepLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/EdepLongitudinalProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveLateralDistribution(OutFilename,NLateral,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/ShowerTables/NLateral
   NLateral.write(OutFilename, path=EventName+"/ShowerTables/NLateralProfile", format="hdf5", append=True,  compression=True, serialize_meta=True)

def SaveEnergyDistribution(OutFilename,EGround,EventName):
   #ToDO: Handle error when OutFilename already contains EventName/ShowerTables/EGRound
   EGround.write(OutFilename, path=EventName+"/ShowerTables/EGround", format="hdf5", append=True,  compression=True, serialize_meta=True)


######################################################################################################################################################################
# Table Getters
######################################################################################################################################################################

def GetRunInfo(InputFilename):
   #ToDo: Handle error when "RunInfo" does not exists
   #ToDo: Handle error when "InputFilename" is not a file, or a valid file.
   RunInfo=Table.read(InputFilename, path="RunInfo")
   return RunInfo

def GetEventInfo(InputFilename,EventName):
   #ToDo: Handle error when "EventName" does not exists
   #ToDo: Handle error when "EventName/EventInfo" does not exists
   #ToDo: Handle error when "InputFilename" is not a file, or a valid file.
   EventInfo=Table.read(InputFilename, path=EventName+"/EventInfo")
   return EventInfo

def GetAntennaInfo(InputFilename,EventName):
   #ToDo: Handle error when "EventName" does not exists
   #ToDo: Handle error when "EventName/AntennaInfo" does not exists
   #ToDo: Handle error when "InputFilename" is not a file, or a valid file.
   AntennaInfo=Table.read(InputFilename, path=EventName+"/AntennaInfo")
   return AntennaInfo

def GetAntennaEfield(InputFilename,EventName,AntennaName,OutputFormat="numpy"):
   #ToDo: Handle error when "EventName" does not exists
   #ToDo: Handle error when "EventName/AntennaTraces" does not exists
   #ToDo: Handle error when "EventName/AntennaTraces/AntennaName" does not exsists
   #ToDo: Handle error when "EventName/AntennaTraces/AntennaName/Efield" does not exsists
   #ToDo: Handle error when "InputFilename" is not a file, or a valid file.
   EfieldTrace=Table.read(InputFilename, path=EventName+"/AntennaTraces/"+AntennaName+"/efield")
   if(OutputFormat=="numpy"):
     EfieldTrace=np.array([EfieldTrace['Time'], EfieldTrace['Ex'],EfieldTrace['Ey'],EfieldTrace['Ez']]).T
   return EfieldTrace

#######################################################################################################################################################################
# RunInfo Getters
#######################################################################################################################################################################

def GetNumberOfEvents(RunInfo):
    return len(RunInfo)

def GetEventName(RunInfo,EventNumber):
    return RunInfo["EventName"][EventNumber]

def GetEventZenith(RunInfo,EventNumber):
    return RunInfo["Zenith"][EventNumber]

def GetEventAzimuth(RunInfo,EventNumber):
    return RunInfo["Azimuth"][EventNumber]

#######################################################################################################################################################################
# AntennaInfo Getters
#######################################################################################################################################################################

def GetNumberOfAntennas(AntennaInfo):
    return len(AntennaInfo)

def GetAntennaID(AntennaInfo,AntennaNumber):
    return AntennaInfo["ID"][AntennaNumber]

def GetAntennaPosition(AntennaInfo,AntennaNumber):
    return (AntennaInfo["X"][AntennaNumber],AntennaInfo["Y"][AntennaNumber],AntennaInfo["Z"][AntennaNumber])

def GetAntennaSlope(AntennaInfo,AntennaNumber):
    return (AntennaInfo["SlopeA"][AntennaNumber] ,AntennaInfo["SlopeB"][AntennaNumber])









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
   #ToDo: HAndle error when "efield" already exists
   #ToDo: HAndle error when "outputfilename" is not a file, or a valid file.
   #ToDo: Adjust format so that we have the relevant number of significant figures. Maybe float64 is not necesary?. What about using float32 or even float 16?
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
   #ToDo: HAndle error when "voltage" already exists
   #ToDo: HAndle error when "outputfilename" is not a file, or a valid file.
   voltage.write(outputfilename, path=EventName+"/AntennaTraces/"+antennaID+"/voltage", format="hdf5", append=True,compression=True,serialize_meta=True)

def SaveFilteredVoltageTable(outputfilename,EventName,antennaID,filteredvoltage):
   #ToDo: HAndle error when "voltage" already exists
   #ToDo: HAndle error when "outputfilename" is not a file, or a valid file.
   filteredvoltage.write(outputfilename, path=EventName+"/AntennaTraces/"+antennaID+"/filteredvoltage", format="hdf5", append=True,compression=True,serialize_meta=True)

#######################################################################################################################################################################
# Other Stuff to see how things could be done
#######################################################################################################################################################################

def GetMetaFromTable(AstropyTable):
   return AstropyTable.meta

def GetAntennaInfoFromEventInfo(EventInfo,nant):
   return EventInfo[nant]

def GetAntIDFromAntennaInfo(AntennaInfo):
   return AntennaInfo["ant_ID"]

def GetXFromAntennaInfo(AntennaInfo):
   return AntennaInfo["pos_x"]

def GetYFromAntennaInfo(AntennaInfo):
   return AntennaInfo["pos_y"]

def GetZFromAntennaInfo(AntennaInfo):
   return AntennaInfo["pos_z"]


def GetSlopesFromTrace(Trace):
   return Trace.meta['slopes']





