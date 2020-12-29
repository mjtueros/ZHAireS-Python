
from astropy.table import Table, Column
from astropy import units as u
import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt


################################################################################################################################
#### by M. Tueros. Shared with the Wineware licence. Support and feature requests accepted only accompanied by bottles of wine.
################################################################################################################################
FileFormatVersion=0.0
EventFormatVersion=0.0
hdf5io_compression=True #compressing the file externally still gains 50%!
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
# containing details on the electric field computation: index of refraction model, tmin, tbin (this would be the meta of the antenalist)
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

def GetMetaFromTable(AstropyTable):
   return AstropyTable.meta

################################################################################################################################################################
# Table Savers
################################################################################################################################################################

#all the error handling might be easier defined in a general routine: SaveAstropyTable(Tablepath/TableName)
def SaveRunInfo(OutFilename,RunInfo):
   #TODO: Handle error when OutFilename already contains RunInfo
   RunInfo.write(OutFilename, path="RunInfo", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveEventInfo(OutFilename,EventInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/EventInfo
   EventInfo.write(OutFilename, path=EventName+"/EventInfo", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveAntennaInfo(OutFilename,AntennaInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/AntennaInfo
   #if overwrite=True, it will overwrite the contennts in AntennaInfo, but not on the file (becouse append is True)9
   AntennaInfo.write(OutFilename, path=EventName+"/AntennaInfo", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

#left here for compatibility with some old code [deprecated]
def SaveAntennaInfo4(OutFilename,AntennaInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/AntennaInfo
   #if overwrite=True, it will overwrite the contennts in AntennaInfo, but not on the file (becouse append is True)
   AntennaInfo.write(OutFilename, path=EventName+"/AntennaInfo4", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveAntennaP2PInfo(OutFilename,AntennaP2PInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/AntennaInfo
   #if overwrite=True, it will overwrite the contennts in AntennaInfo, but not on the file (becouse append is True)
   AntennaP2PInfo.write(OutFilename, path=EventName+"/AntennaP2PInfo", format="hdf5", append=True, overwrite=True, compression=hdf5io_compression, serialize_meta=True)

def SaveShowerSimInfo(OutFilename,ShowerSimInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerSimInfo
   ShowerSimInfo.write(OutFilename, path=EventName+"/ShowerSimInfo", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveSignalSimInfo(OutFilename,SignalSimInfo,EventName):
   #TODO: Handle error when OutFilename already contains EventName/SignalSimInfo
   SignalSimInfo.write(OutFilename, path=EventName+"/SignalSimInfo", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveNLongitudinal(OutFilename,NLongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/NLongitudinalProfile
   NLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/NLongitudinalProfile", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveELongitudinal(OutFilename,ELongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/ELongitudinalProfile
   ELongitudinal.write(OutFilename, path=EventName+"/ShowerTables/ELongitudinalProfile", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveNlowLongitudinal(OutFilename,NlowLongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/NlowLongitudinalProfile
   NlowLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/NlowLongitudinalProfile", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveElowLongitudinal(OutFilename,ElowLongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/ElowLongitudinalProfile
   ElowLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/ElowLongitudinalProfile", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveEdepLongitudinal(OutFilename,EdepLongitudinal,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/EdepLongitudinalProfile
   EdepLongitudinal.write(OutFilename, path=EventName+"/ShowerTables/EdepLongitudinalProfile", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveLateralDistribution(OutFilename,NLateral,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/NLateral
   NLateral.write(OutFilename, path=EventName+"/ShowerTables/NLateralProfile", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)

def SaveEnergyDistribution(OutFilename,EGround,EventName):
   #TODO: Handle error when OutFilename already contains EventName/ShowerTables/EGRound
   EGround.write(OutFilename, path=EventName+"/ShowerTables/EGround", format="hdf5", append=True,  compression=hdf5io_compression, serialize_meta=True)


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

#if compute=True, it will try to compute the P2PInfo if it was not found
#id compute=Save, it will also try to save it in the file.
def GetAntennaP2PInfo(InputFilename,EventName,compute=False):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaInfo" does not exists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.

   try:
     AntennaInfo=Table.read(InputFilename, path=EventName+"/AntennaP2PInfo")
   except:
     if(compute==True or compute=="Save"):
        print("Computing P2P for "+str(InputFilename))

        OutAntennaInfo=GetAntennaInfo(InputFilename,CurrentEventName)
        OutIDs=hdf5io.GetAntIDFromAntennaInfo(OutAntennaInfo)

        p2pE=get_p2p_hdf5(InputFilename,usetrace='efield')
        p2pV=get_p2p_hdf5(InputFilename,usetrace='voltage')
        p2pFV=get_p2p_hdf5(InputFilename,usetrace='filteredvoltage')

        peaktimeE, peakE=get_peak_time_hilbert_hdf5(InputFilename,usetrace='efield')
        peaktimeV, peakV=get_peak_time_hilbert_hdf5(InputFilename,usetrace='voltage')
        peaktimeFV, peakFV=get_peak_time_hilbert_hdf5(InputFilename,usetrace='filteredvoltage')

        DesiredAntennaInfoMeta=CreatAntennaInfoMeta(InputFilename,EventName,AntennaModel="Unknown")
        AntennaP2PInfo=CreateAntennaP2PInfo(OutIDs, DesiredAntennaInfoMeta, P2Pefield=p2pE,P2Pvoltage=p2pV,P2Pfiltered=p2pFV,HilbertPeakE=peakE,HilbertPeakV=peakV,HilbertPeakFV=peakFV,HilbertPeakTimeE=peaktimeE,HilbertPeakTimeV=peaktimeV,HilbertPeakTimeFV=peaktimeFV)

        if(compute=="Save"):
          SaveAntennaP2PInfo(InputFilename,AntennaP2PInfo,CurrentEventName)
     else:
       print("AntennaP2PInfo not found in ",InputFilename," for ",EventName)
       AntennaInfo=0

   return AntennaInfo


def GetAntennaEfield(InputFilename,EventName,AntennaName,OutputFormat="numpy"):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaTraces" does not exists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName" does not exsists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName/Efield" does not exsists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.

   try:
     EfieldTrace=Table.read(InputFilename, path=str(EventName)+"/AntennaTraces/"+str(AntennaName)+"/efield")
   except:
     EfieldTrace=np.zeros((4,4))
     print("efield trace not found")
     return EfieldTrace


   if(OutputFormat=="numpy"):
     EfieldTrace=np.array([EfieldTrace['Time'], EfieldTrace['Ex'],EfieldTrace['Ey'],EfieldTrace['Ez']]).T
   return EfieldTrace

def GetAntennaVoltage(InputFilename,EventName,AntennaName,OutputFormat="numpy"):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaTraces" does not exists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName" does not exsists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName/Efield" does not exsists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.
   try:
     VoltageTrace=Table.read(InputFilename, path=str(EventName)+"/AntennaTraces/"+str(AntennaName)+"/voltage")
   except:
     VoltageTrace=np.zeros((4,4))
     print("voltage trace not found")
     return VoltageTrace

   if(OutputFormat=="numpy"):
     VoltageTrace=np.array([VoltageTrace['Time'], VoltageTrace['Vx'],VoltageTrace['Vy'],VoltageTrace['Vz']]).T
   return VoltageTrace

def GetAntennaFilteredVoltage(InputFilename,EventName,AntennaName,OutputFormat="numpy"):
   #TODO: Handle error when "EventName" does not exists
   #TODO: Handle error when "EventName/AntennaTraces" does not exists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName" does not exsists
   #TODO: Handle error when "EventName/AntennaTraces/AntennaName/Efield" does not exsists
   #TODO: Handle error when "InputFilename" is not a file, or a valid file.

   try:
     VoltageTrace=Table.read(InputFilename, path=str(EventName)+"/AntennaTraces/"+str(AntennaName)+"/filteredvoltage")
   except:
     VoltageTrace=np.zeros((4,4))
     print("filteredvoltage trace not found")
     return VoltageTrace

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
# RunInfo Creator
#######################################################################################################################################################################

def CreateRunInfoMeta(RunName):
    #TODO: Handle errors
    RunInfoMeta={
            "FileFormatVersion":FileFormatVersion,
            "RunName":RunName                        #for checking
            #TODO: decide what else goes here
        }
    return RunInfoMeta

def CreateRunInfo(EventName,Primary,Energy,Zenith,Azimuth,XmaxDistance,SlantXmax,HadronicModel,InjectionAltitude,RunInfoMeta):

    a=Column(data=[EventName],name='EventName')   #EventName, states the name of the Task of the simulation, that usually dictates the file names
    b=Column(data=["N/A"],name='EventID')    #An event might have some ID?
    c=Column(data=[Primary],name='Primary')
    d=Column(data=[Energy],name='Energy',unit=u.EeV)
    e=Column(data=[Zenith],name='Zenith',unit=u.deg)
    f=Column(data=[Azimuth],name='Azimuth',unit=u.deg)
    g=Column(data=[XmaxDistance],name='XmaxDistance',unit=u.m)
    h=Column(data=[SlantXmax],name='SlantXmax',unit=u.g/(u.cm*u.cm))
    i=Column(data=[HadronicModel],name='HadronicModel')
    j=Column(data=[InjectionAltitude],name='InjectionAltitude',unit=u.m)
    #Number of Triggered Efield Antennas?
    #Number of Triggered Voltage Antennas?
    #Number of Triggered Voltage+Filter Antennas?

    RunInfo = Table(data=(a,b,c,d,e,f,g,h,i,j),meta=RunInfoMeta)

    return RunInfo

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
# EventInfo Creators
#######################################################################################################################################################################

def CreateEventInfoMeta(RunName,EventNumber,EventInfo,ShowerSimInfo,SignalSimInfo,AntennaInfo,AntennaTraces,NLongitudinal,ELongitudinal,NlowLongitudinal,ElowLongitudinal,EdepLongitudinal,LateralDistribution,EnergyDistribution):

    EventInfoMeta = {
        "RunName":RunName,                         #for cross checking
        "EventNumber":EventNumber,                 #Position in the RunInfo Table for easy access
        "EventFormatVersion":EventFormatVersion,   #File Format of the Event (if it might be different)
        "EventInfo": EventInfo,                    #event includes event info
        "ShowerSimInfo":ShowerSimInfo,             #event includes shower simulation info
        "SignalSimInfo":SignalSimInfo,             #event includes signal simulation info
        "AntennaInfo":AntennaInfo,                 #event includes antenna info
        "AntennaTraces":AntennaTraces,             #event includes the traces of each antenna
        "NLongitudinal":NLongitudinal,             #event includes longitudinal tables of number of particles
        "ELongitudinal":ELongitudinal,             #event includes longitudinal tables of energy
        "NlowLongitudinal":NlowLongitudinal,       #event includes longitudinal tables of number discarded low energy particles
        "ElowLongitudinal":ElowLongitudinal,       #event includes longitudinal tables of energy of discarded low energy particles
        "EdepLongitudinal":EdepLongitudinal,       #event includes longitudinal tables of energy deposit
        "LateralDistribution":LateralDistribution, #event includes tables of the lateral distribution of particles at ground
        "EnergyDistribution":EnergyDistribution    #event includes tables of the enertgy distribution of particles at ground
        #TODO: decide what else goes here
        }
    return EventInfoMeta

def CreateEventInfo(EventName,Primary,Energy,Zenith,Azimuth,XmaxDistance,XmaxPosition,XmaxAltitude,SlantXmax,InjectionAltitude,GroundAltitude,Site,Date,Latitude,Longitude,FieldIntensity,FieldInclination,FieldDeclination,AtmosphericModel,EnergyInNeutrinos,EventInfoMeta,CorePosition=(0.0,0.0,0.0)):

    a1=Column(data=[EventName],name='EventName')   #EventName, states the name of the Task of the simulation, that usually dictates the file names
    b1=Column(data=["N/A"],name='EventID')    #An event might have some ID?
    c1=Column(data=[Primary],name='Primary')
    d1=Column(data=[Energy],name='Energy',unit=u.EeV)
    e1=Column(data=[Zenith],name='Zenith',unit=u.deg)
    f1=Column(data=[Azimuth],name='Azimuth',unit=u.deg)
    g1=Column(data=[XmaxDistance],name='XmaxDistance',unit=u.m)
    h1=Column(data=[XmaxPosition],name='XmaxPosition',unit=u.m)
    i1=Column(data=[XmaxAltitude],name='XmaxAltitude',unit=u.m)
    j1=Column(data=[SlantXmax],name='SlantXmax',unit=u.g/(u.cm*u.cm))
    k1=Column(data=[InjectionAltitude],name='InjectionAltitude',unit=u.m)
    l1=Column(data=[GroundAltitude],name='GroundAltitude',unit=u.m)
    m1=Column(data=[Site],name='Site')
    n1=Column(data=[Date],name='Date')
    o1=Column(data=[Latitude],name='Latitude',unit=u.deg)
    p1=Column(data=[Longitude],name='Longitude',unit=u.deg)
    q1=Column(data=[FieldIntensity],name='BField',unit=u.uT)
    r1=Column(data=[FieldInclination],name='BFieldIncl',unit=u.deg)
    s1=Column(data=[FieldDeclination],name='BFieldDecl',unit=u.deg)
    t1=Column(data=[AtmosphericModel],name='AtmosphericModel')
    u1=Column(data=["N/A"],name='AtmosphericModelParameters')
    v1=Column(data=[EnergyInNeutrinos],name='EnergyInNeutrinos',unit=u.EeV)
    w1=Column(data=[CorePosition],name='CorePosition')

    EventInfo = Table(data=(a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1,u1,v1,w1),meta=EventInfoMeta)

    return EventInfo

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

def GetLatitude(EventInfo):
   #TODO: Handle errors
    return float(EventInfo["Latitude"])

def GetLongitude(EventInfo):
   #TODO: Handle errors
    return float(EventInfo["Longitude"])

def GetXmaxPosition(EventInfo):
   #TODO: Handle errors
    return EventInfo["XmaxPosition"]

def GetXmaxAltitude(EventInfo):
   #TODO: Handle errors
    return EventInfo["XmaxAltitude"]

def GetPrimaryFromEventInfo(EventInfo):
   #TODO: Handle errors
    return EventInfo["Primary"]

def GetAzimuthFromEventInfo(EventInfo):
   #TODO: Handle errors
    return float(EventInfo["Azimuth"])

def GetZenithFromEventInfo(EventInfo):
   #TODO: Handle errors
    return float(EventInfo["Zenith"])

def GetEnergyFromEventInfo(EventInfo):
   #TODO: Handle errors
    return float(EventInfo["Energy"])

def GetCorePositionFromEventInfo(EventInfo):
   #TODO: Handle errors
    return EventInfo["CorePosition"]

#######################################################################################################################################################################
# ShowerSim Creators
#######################################################################################################################################################################

def CreateShowerSimInfoMeta(RunName,EventName,ShowerSimulator):

    ShowerSimInfoMeta = {
        "RunName":RunName,                             #For cross checking
        "EventName":EventName,                         #For cross checking
        "ShowerSimulator": ShowerSimulator             #TODO: decide what goes here
    }

    return ShowerSimInfoMeta

def CreateShowerSimInfo(ShowerSimulator,HadronicModel,RandomSeed,RelativeThinning,WeightFactor,GammaEnergyCut,ElectronEnergyCut,MuonEnergyCut,MesonEnergyCut,NucleonEnergyCut,CPUTime,ShowerSimInfoMeta):

    a2=Column(data=[ShowerSimulator],name='ShowerSimulator')
    b2=Column(data=[HadronicModel],name='HadonicModel')
    c2=Column(data=[RandomSeed],name='RandomSeed')
    d2=Column(data=[RelativeThinning],name='RelativeThining') #energy at wich thining starts, relative to the primary energy.
    e2=Column(data=[WeightFactor],name='WeightFactor')
    f2=Column(data=[GammaEnergyCut],name='GammaEnergyCut',unit=u.MeV)
    g2=Column(data=[ElectronEnergyCut],name='ElectronEnergyCut',unit=u.MeV)
    h2=Column(data=[MuonEnergyCut],name='MuonEnergyCut',unit=u.MeV)
    i2=Column(data=[MesonEnergyCut],name='MesonEnergyCut',unit=u.MeV)
    j2=Column(data=[NucleonEnergyCut],name='NucleonEnergyCut',unit=u.MeV)
    k2=Column(data=[CPUTime],name='CPUTime',unit=u.s)
    l2=Column(data=["N/A"],name='OtherParameters')

    ShowerSimInfo = Table(data=(a2,b2,c2,d2,e2,f2,g2,h2,i2,j2,k2,l2),meta=ShowerSimInfoMeta)

    return ShowerSimInfo

#######################################################################################################################################################################
# ShowerSim Getters
#######################################################################################################################################################################

def GetCPUTime(ShowerSimInfo):
   #TODO: Handle errors
    return float(ShowerSimInfo["CPUTime"])


#######################################################################################################################################################################
# SignalSimInfo Creators
#######################################################################################################################################################################
def CreateSignalSimInfoMeta(RunName,EventName,FieldSimulator):
    SignalSimInfoMeta = {
        "RunName":RunName,                             #For cross checking
        "EventName":EventName,                         #For cross checking
        "FieldSimulator": FieldSimulator,            #TODO: decide what goes here
    }
    return SignalSimInfoMeta

def CreateSignalSimInfo(FieldSimulator,RefractionIndexModel,RefractionIndexParameters,TimeBinSize,TimeWindowMin,TimeWindowMax,SignalSimInfoMeta):

    a3=Column(data=[FieldSimulator],name='FieldSimulator')
    b3=Column(data=[RefractionIndexModel],name='RefractionIndexModel')
    c3=Column(data=[RefractionIndexParameters],name='RefractionIndexModelParameters')
    d3=Column(data=[TimeBinSize],name='TimeBinSize',unit=u.ns)
    e3=Column(data=[TimeWindowMin],name='TimeWindowMin',unit=u.ns)
    f3=Column(data=[TimeWindowMax],name='TimeWindowMax',unit=u.ns)
    g3=Column(data=["N/A"],name='OtherParameters')
    #Number of Triggered Efield Antennas
    #Number of Triggered Voltage Antennas
    #Number of Triggered FilteredVoltage Antennas

    SignalSimInfo = Table(data=(a3,b3,c3,d3,e3,f3,g3),meta=SignalSimInfoMeta)

    return SignalSimInfo

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

def GetFieldSimulator(SignalSimInfo):
   #TODO: Handle errors
    return SignalSimInfo["FieldSimulator"]

def GetRefractionIndexModel(SignalSimInfo):
   #TODO: Handle errors
    return SignalSimInfo["RefractionIndexModel"].data[0]

def GetRefractionIndexModelParameters(SignalSimInfo):
   #TODO: Handle errors
    ModelParameters=SignalSimInfo["RefractionIndexModelParameters"]
    return ModelParameters.data[0]

####################################################################################################################################################################################
#AntennaInfo Creators
####################################################################################################################################################################################

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

def CreateAntennaInfo(IDs, antx, anty, antz, antt, slopeA, slopeB, AntennaInfoMeta, P2Pefield=None,P2Pvoltage=None,P2Pfiltered=None,HilbertPeak=None,HilbertPeakTime=None):
   #TODO: Handle errors
    a4=Column(data=IDs,name='ID')
    antx=antx.astype('f4')
    b4=Column(data=antx,name='X',unit=u.m) #in core cordinates
    anty=anty.astype('f4')
    c4=Column(data=anty,name='Y',unit=u.m) #in core cordinates
    antz=antz.astype('f4')
    d4=Column(data=antz,name='Z',unit=u.m) #in core cordinates
    antt=antt.astype('f4')
    e4=Column(data=antt,name='T0',unit=u.ns) #in core cordinates
    sopeA=slopeA.astype('f4')
    f4=Column(data=slopeA,name='SlopeA',unit=u.m) #in core cordinates
    sopeB=slopeB.astype('f4')
    g4=Column(data=slopeB,name='SlopeB',unit=u.m) #in core cordinates
    data=[a4,b4,c4,d4,e4,f4,g4]

    #this is left here for now, but all the P2P section was moved to a separate table
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
      g4=Column(data=HilbertPeakTime32,name='HilbertPeakTime',unit=u.ns) #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeakTime=True)


    AstropyTable = Table(data=data,meta=AntennaInfoMeta)
    return AstropyTable

####################################################################################################################################################################################
#AntennaInfo Getters
####################################################################################################################################################################################

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

def GetT0FromAntennaInfo(AntennaInfo):
   #TODO: Handle errors
   return float(AntennaInfo["T0"])

def GetAntennaID(AntennaInfo,AntennaNumber):
   #TODO: Handle errors
    return str(AntennaInfo["ID"][AntennaNumber])

def GetAntennaPosition(AntennaInfo,AntennaNumber):
   #TODO: Handle errors
    return (AntennaInfo["X"][AntennaNumber],AntennaInfo["Y"][AntennaNumber],AntennaInfo["Z"][AntennaNumber])

def GetAntennaT0(AntennaInfo,AntennaNumber):
   #TODO: Handle errors
    return (AntennaInfo["T0"][AntennaNumber])

def GetAntennaT0s(AntennaInfo):
   #TODO: Handle errors
    return (AntennaInfo["T0"])

def GetAntennaSlope(AntennaInfo,AntennaNumber):
   #TODO: Handle errors
    return (AntennaInfo["SlopeA"][AntennaNumber] ,AntennaInfo["SlopeB"][AntennaNumber])

def GetAntennaPositions(AntennaInfo):
   #TODO: Handle errors
    return (AntennaInfo["X"][:],AntennaInfo["Y"][:],AntennaInfo["Z"][:])

####################################################################################################################################################################################
#AntennaP2PInfo Creators
####################################################################################################################################################################################
def CreateAntennaP2PInfo(IDs, AntennaInfoMeta, P2Pefield=None,P2Pvoltage=None,P2Pfiltered=None,HilbertPeakE=None,HilbertPeakV=None,HilbertPeakFV=None,HilbertPeakTimeE=None,HilbertPeakTimeV=None,HilbertPeakTimeFV=None):
   #TODO: Handle errors
    a4=Column(data=IDs,name='ID')
    data=[a4]

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

    if HilbertPeakE is not None:
      HilbertPeakE32=HilbertPeakE.astype('f4') #reduce the data type to float 32
      g4=Column(data=HilbertPeakE32,name='HilbertPeakE') #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeakE=True)

    if HilbertPeakTimeE is not None:
      HilbertPeakTimeE32=HilbertPeakTimeE.astype('f4') #reduce the data type to float 32
      g4=Column(data=HilbertPeakTimeE32,name='HilbertPeakTimeE',unit=u.ns) #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeakTimeE=True)

    if HilbertPeakV is not None:
      HilbertPeakV32=HilbertPeakV.astype('f4') #reduce the data type to float 32
      g4=Column(data=HilbertPeakV32,name='HilbertPeakV') #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeakV=True)

    if HilbertPeakTimeV is not None:
      HilbertPeakTimeV32=HilbertPeakTimeV.astype('f4') #reduce the data type to float 32
      g4=Column(data=HilbertPeakTimeV32,name='HilbertPeakTimeV',unit=u.ns) #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeakTimeV=True)

    if HilbertPeakFV is not None:
      HilbertPeakFV32=HilbertPeakFV.astype('f4') #reduce the data type to float 32
      g4=Column(data=HilbertPeakFV32,name='HilbertPeakFV') #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeakFV=True)

    if HilbertPeakTimeFV is not None:
      HilbertPeakTimeFV32=HilbertPeakTimeFV.astype('f4') #reduce the data type to float 32
      g4=Column(data=HilbertPeakTimeFV32,name='HilbertPeakTimeFV',unit=u.ns) #
      data.append(g4)
      AntennaInfoMeta.update(HilbertPeakTimeFV=True)


    AstropyTable = Table(data=data,meta=AntennaInfoMeta)
    return AstropyTable

####################################################################################################################################################################################
#AntennaP2PInfo Getters
####################################################################################################################################################################################

def GetHilbertPeakEFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["HilbertPeakE"]

def GetHilbertPeakVFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["HilbertPeakV"]

def GetHilbertPeakFVFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["HilbertPeakFV"]

def GetHilbertPeakTimeEFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["HilbertPeakTimeE"]

def GetHilbertPeakTimeVFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["HilbertPeakTimeV"]

def GetHilbertPeakTimeFVFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["HilbertPeakTimeFV"]

def GetP2P_efieldFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2P_efield"]

def GetP2Px_efieldFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Px_efield"]

def GetP2Py_efieldFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Py_efield"]

def GetP2Pz_efieldFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Pz_efield"]

def GetP2P_voltageFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2P_voltage"]

def GetP2Px_voltageFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Px_voltage"]

def GetP2Py_voltageFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Py_voltage"]

def GetP2Pz_voltageFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Pz_voltage"]

def GetP2P_filteredFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2P_filtered"]

def GetP2Px_filteredFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Px_filtered"]

def GetP2Py_filteredFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Py_filtered"]

def GetP2Pz_filteredFromAntennaP2PInfo(AntennaP2PInfo):
   #TODO: Handle errors
   return AntennaP2PInfo["P2Pz_filtered"]
########################################################################################################################
# Create and Save traces
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
   efield.write(outputfilename, path=EventName+"/AntennaTraces/"+antennaID+"/efield", format="hdf5", append=True, compression=hdf5io_compression,serialize_meta=True)



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
   voltage.write(outputfilename, path=EventName+"/AntennaTraces/"+antennaID+"/voltage", format="hdf5", append=True,compression=hdf5io_compression,serialize_meta=True)

def SaveFilteredVoltageTable(outputfilename,EventName,antennaID,filteredvoltage):
   #TODO: HAndle error when "voltage" already exists
   #TODO: HAndle error when "outputfilename" is not a file, or a valid file.
   filteredvoltage.write(outputfilename, path=EventName+"/AntennaTraces/"+antennaID+"/filteredvoltage", format="hdf5", append=True,compression=hdf5io_compression,serialize_meta=True)

#######################################################################################################################################################################
# Other Stuff to see how things could be done
#######################################################################################################################################################################

#TODO: Split this in 2 functions: GetP2PFromTrace(Trace) to get p2px,p2py,p2pz and p2ptotal (this is not an hdf5io function)
#      used in GetEventP2P(InputFilename, CurrentEventName) to get them for all the antennas in the event
def get_p2p_hdf5(InputFilename,antennamax='All',antennamin=0,usetrace='efield'):

    #TODO: Handle Errors
    #TODO: Handle Errors when the trace type is not found
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
    if(antennamax>len(CurrentAntennaInfo)-1):
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

      p2p= np.amax(trace,axis=0)-np.amin(trace,axis=0)
      p2p_Ex[i-antennamin]= p2p[1]
      p2p_Ey[i-antennamin]= p2p[2]
      p2p_Ez[i-antennamin]= p2p[3]

      amplitude = np.sqrt(trace[:,1]**2. + trace[:,2]**2. + trace[:,3]**2.) # combined components

      p2p_total[i-antennamin] = max(amplitude)-min(amplitude)

    p2pE = np.stack((p2p_Ex, p2p_Ey, p2p_Ez, p2p_total), axis=0)
    return p2pE


#TODO: Split this in 2 functions: GetHilbertFromTrace(Trace) to get hilbert amplitude and time (this is not an hdf5io function)
#      used in GetEventHilbert(InputFilename, CurrentEventName) to get them for all the antennas in the event
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
      peakamplitudelocation=np.where(hilbert_amp == peakamplitude[i-antennamin])
      #this is to assure that there is a maximum amplitude, at that its unique, and that it could be found
      if(peakamplitude[i-antennamin]!=0.0 and np.shape(peakamplitudelocation)==(2,1)):
        peaktime[i-antennamin]=trace[peakamplitudelocation[0],0]                # get the time of the peak amplitude
      else:
        peaktime[i-antennamin]=-1e20

      #PLOT
      DISPLAY=False
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




#TODO: Split this in 2 functions: GeFluenceFromTrace(Trace) to get the fluence (this is not an hdf5io function)
#      use it in GetEventHilbert(InputFilename, CurrentEventName) to get them for all the antennas in the event
def get_fluence_hdf5(InputFilename, antennamax="All",antennamin=0, windowsize="All", usetrace="efield", DISPLAY=False) :

    #TODO: Handle Errors
    '''
    read in all traces from antennamax to antennamin and output the fluence (integral of the square of th emplitude, optionally in a window
    Parameters:
    InputFilename: str
        HDF5File
    antennamin: int
       starting antenna (starts from 0)
    antennamax: int
       final antenna ('All uses all the antennas)
    usetrace: str
       efield, voltage, filteredvoltage
    Windowsize:
       All uses all the trace.
       any number gives the size in nanoseconds of a time window centered arrround the maximum of the hilbert envelope

    Output:
    fluence: numpy array with the fluence, computed as the sum of the trace squared
    fluence(0,:) fluence of the modulus
    fluence(1,:) fluence in x
    fluence(2,:) fluence in y
    fluence(3,:) fluence in z
    '''

    CurrentRunInfo=GetRunInfo(InputFilename)
    CurrentEventName=GetEventName(CurrentRunInfo,0) #using the first event of each file (there is only one for now)
    CurrentAntennaInfo=GetAntennaInfo(InputFilename,CurrentEventName)
    CurrentSignalSimInfo=GetSignalSimInfo(InputFilename,CurrentEventName)
    binsize=GetTimeBinSize(CurrentSignalSimInfo)
    tmin=GetTimeWindowMin(CurrentSignalSimInfo)

    binsize=binsize*1E-9 #need it in seconds
    #now, arrange the units:
    c=299792458 #m*s
    epsilon0=8.854187817E-12 #Farads/m
    #uV2V = 1E-12 #uv to v squared
    #J2eV = 6.241509E+18 #Joules to eV
    if(usetrace=='efield'):
      fluenceunit= c*epsilon0*binsize*6.241509E6 # eV/m2
      if(windowsize!="All" and windowsize!="all"):
        CurrentAntennaP2PInfo=GetAntennaP2PInfo(InputFilename,CurrentEventName)
        tpeak=GetHilbertPeakTimeEFromAntennaP2PInfo(CurrentAntennaP2PInfo)
    elif(usetrace=='voltage'):
      fluenceunit= binsize*6.241509E6/376.73 #eV impedance of free space
      if(windowsize!="All" and windowsize!="all"):
        CurrentAntennaP2PInfo=GetAntennaP2PInfo(InputFilename,CurrentEventName)
        tpeak=GetHilbertPeakTimeVFromAntennaP2PInfo(CurrentAntennaP2PInfo)
    elif(usetrace=='filteredvoltage'):
      fluenceunit= binsize*6.241509E6/376.73 #eV impedance of free space
      if(windowsize!="All" and windowsize!="all"):
        CurrentAntennaP2PInfo=GetAntennaP2PInfo(InputFilename,CurrentEventName)
        tpeak=GetHilbertPeakTimeFVFromAntennaP2PInfo(CurrentAntennaP2PInfo)

    binsize=binsize*1E9 #back to ns

    if(antennamax=='All' or antennamax=='all'):
      antennamax=len(CurrentAntennaInfo)-1

    fluence= np.zeros(1+antennamax-antennamin)
    xfluence= np.zeros(1+antennamax-antennamin)
    yfluence= np.zeros(1+antennamax-antennamin)
    zfluence= np.zeros(1+antennamax-antennamin)


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
        return -1,-1,-1,-1

      #pass time window to bins
      if(windowsize=="All" or windowsize=="all"):
        binmin=0
        binmax=len(trace[:,1])
      else:
        tracestart=trace[0,0]

        binpeak= int((tpeak[i]-tracestart)/binsize)

        binmin= int(binpeak-windowsize/(2.0*binsize))
        binmax= int(binpeak+windowsize/(2.0*binsize)+1)



        if(binmin<0):

         from scipy.signal import hilbert
         #now, this is not doing exactly what i was expecting (the hilbert of each component separately. When i plot it, it seems to be mixing channels up)
         #however, it does get the maximum of the modulus of the signal (but i dont understand whats really going on!)
         hilbert_trace=hilbert(trace[:,1:4])
         hilbert_amp = np.abs(hilbert_trace)

         #print("underflow bin",binmin,binpeak,binmax,tracestart,tpeak[i])
         if(binmin<-windowsize/(4*binsize)):
           binmin=-1
         else:
           binmin=0

        if(binmax>len(trace[:,1])):
         #print("overflow bin",binmin,binpeak,binmax, tracestart,tpeak[i],(tpeak[i]-tracestart) )

         if(binmin==-1 or binmax > len(trace[:,1])+windowsize/(4*binsize)):
          #print(" peak is too close to the limits")
          binmax=-1
          binmin=-1
         else:
          binmax=len(trace[:,1])

        if(binmin==-1):
          binmin=-1
          binmax=-1


        if(DISPLAY and (binmin==-1 or binmax==-1)):
          fig1a=plt.figure(figsize=(8,6))
          ax31 = plt.subplot(2,2,1)
          im=ax31.plot(trace[:,0],trace[:,1])
          tmp=ax31.set(title="X Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

          ax32 = plt.subplot(2,2,2)
          im=ax32.plot(trace[:,0],trace[:,2])
          tmp=ax32.set(title="Y Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

          ax33 = plt.subplot(2,2,3)
          im=ax33.plot(trace[:,0],trace[:,3])
          tmp=ax33.set(title="Z Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

          ax33 = plt.subplot(2,2,4)
          im=ax33.plot(trace[25:-25,0],hilbert_amp[25:-25,0])
          im=ax33.plot(trace[25:-25,0],hilbert_amp[25:-25,1])
          im=ax33.plot(trace[25:-25,0],hilbert_amp[25:-25,2])
          tmp=ax33.set(title="||2 Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

          plt.show()


        #print("result",binmin,binpeak,binmax)

    #i will be computing the square of the trace
      #norm of trace
      norm=np.linalg.norm(trace[binmin:binmax,1:4],axis=1)
      #sum
      fluence[i-antennamin]=np.sum(norm*norm)

    #and then the fluence in each component.
      xtrace=trace[binmin:binmax,1]
      xfluence[i-antennamin]=np.sum(xtrace*xtrace)
      ytrace=trace[binmin:binmax,2]
      yfluence[i-antennamin]=np.sum(ytrace*ytrace)
      ztrace=trace[binmin:binmax,3]
      zfluence[i-antennamin]=np.sum(ztrace*ztrace)
    #end for


    fluence= fluenceunit*fluence
    xfluence= fluenceunit*xfluence
    yfluence= fluenceunit*yfluence
    zfluence= fluenceunit*zfluence


    if(DISPLAY):

      X=GetXFromAntennaInfo(CurrentAntennaInfo)
      Y=GetYFromAntennaInfo(CurrentAntennaInfo)
      X=X[antennamin:antennamax+1]
      Y=Y[antennamin:antennamax+1]

      if(usetrace=='efield'):
        title="Fluence "
        unit= "$meV/m^2$"
      else:
        title="Integrated Power"
        unit= "$meV$"

      #done with event 3419 of the database
      plt.rc('font', family='serif', size=15)
      fig1a=plt.figure(figsize=(8,6))
      ax3a = plt.subplot(2,2,1)
      im=ax3a.scatter(X,Y,c=fluence*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3a.set(title="Energy "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3a.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1a.colorbar(im,ax=ax3a)
      bar.set_label(unit, rotation=270, labelpad=17)


      ax3b = plt.subplot(2,2,2)
      im=ax3b.scatter(X,Y,c=xfluence*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3b.set(title="X Energy "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3b.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1a.colorbar(im,ax=ax3b)
      bar.set_label(unit, rotation=270, labelpad=17)



      ax3c = plt.subplot(2,2,3)
      im=ax3c.scatter(X,Y,c=yfluence*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3c.set(title="Y Energy "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3c.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1a.colorbar(im,ax=ax3c)
      bar.set_label(unit, rotation=270, labelpad=17)


      ax3d = plt.subplot(2,2,4)
      im=ax3d.scatter(X,Y,c=zfluence*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3d.set(title="Z Energy "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3d.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1a.colorbar(im,ax=ax3d)
      bar.set_label(unit, rotation=270, labelpad=17)

      plt.show()


    return fluence, xfluence, yfluence, zfluence




#TODO: Split this in 2 functions: GeFluenceFromTrace(Trace) to get the fluence (this is not an hdf5io function)
#      use it in GetEventHilbert(InputFilename, CurrentEventName) to get them for all the antennas in the event
def get_time_amplitudes_fluence_hdf5(InputFilename, antennamax="All",antennamin=0, windowsize=200, usetrace="efield", DISPLAY=False) :

    #TODO: Handle Errors
    '''
    read in all traces from antennamax to antennamin and output P2P amplitude, The fluence and the peak position,
    taking into account to exclude the borders for windowsize/4 (to avoid fourier glitchs), and asking that the peak is at least  at windowsize/2 from the border.

    Parameters:
    InputFilename: str
        HDF5File
    antennamin: int
       starting antenna (starts from 0)
    antennamax: int
       final antenna ('All uses all the antennas)
    usetrace: str
       efield, voltage, filteredvoltage
    Windowsize:
       All uses all the trace.
       any number gives the size in nanoseconds of a time window centered arrround the maximum of the hilbert envelope

    Output: p2p,peak,fluence

    '''

    CurrentRunInfo=GetRunInfo(InputFilename)
    CurrentEventName=GetEventName(CurrentRunInfo,0) #using the first event of each file (there is only one for now)
    CurrentAntennaInfo=GetAntennaInfo(InputFilename,CurrentEventName)
    CurrentSignalSimInfo=GetSignalSimInfo(InputFilename,CurrentEventName)
    binsize=GetTimeBinSize(CurrentSignalSimInfo)
    tmin=GetTimeWindowMin(CurrentSignalSimInfo)
    tmax=GetTimeWindowMax(CurrentSignalSimInfo)
    windowbin=int(windowsize/binsize)
    qwindowbin=int(windowbin/4)

    #print("binsize:",binsize,"tmin:",tmin,"tmax:",tmax,"wbin:",windowbin,"qwbin:",qwindowbin)

    #now, arrange the units:
    c=299792458 #m*s
    epsilon0=8.854187817E-12 #Farads/m
    #uV2V = 1E-12 #uv to v squared
    #J2eV = 6.241509E+18 #Joules to eV
    if(usetrace=='efield'):
      fluenceunit= c*epsilon0*binsize*1E-9*6.241509E6 # eV/m2
    elif(usetrace=='voltage'):
      fluenceunit= binsize*1E-9*6.241509E6/376.73 #eV impedance of free space
    elif(usetrace=='filteredvoltage'):
      fluenceunit= binsize*1E-9*6.241509E6/376.73 #eV impedance of free space

    #handlte the "all" situation
    if(antennamax=='All' or antennamax=='all'):
      antennamax=len(CurrentAntennaInfo)-1

    peaktime= np.zeros(1+antennamax-antennamin)
    peakamplitude= np.zeros(1+antennamax-antennamin)
    peakbin= np.zeros(1+antennamax-antennamin)

    p2p_x = np.zeros(1+antennamax-antennamin)
    p2p_y = np.zeros(1+antennamax-antennamin)
    p2p_z = np.zeros(1+antennamax-antennamin)
    p2p_total = np.zeros(1+antennamax-antennamin)
    p2p=np.zeros(1+antennamax-antennamin)

    fluence= np.zeros(1+antennamax-antennamin)
    xfluence= np.zeros(1+antennamax-antennamin)
    yfluence= np.zeros(1+antennamax-antennamin)
    zfluence= np.zeros(1+antennamax-antennamin)


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
        return -1,-1,-1


      from scipy.signal import hilbert
      #now, this is not doing exactly what i was expecting (the hilbert of each component separately. When i plot it, it seems to be mixing channels up)
      #however, it does get the maximum of the modulus of the signal (but i dont understand whats really going on!)

      #im cutting one quarter of the time window from each side of the trace, to remove the artifacts from the fourier transform.
      #and im asking that the peak is not half of the time window from the border, to assure that is a safe trace

      tracesize=len(trace[:,0])

      hilbert_trace=hilbert(trace[:,1:4])
      hilbert_amp = np.abs(hilbert_trace) 												                     #enveloppe de hilbert x, y, z channels
      peakamplitude[i-antennamin]=max([max(hilbert_amp[qwindowbin:-qwindowbin,0]), max(hilbert_amp[qwindowbin:-qwindowbin,1]), max(hilbert_amp[qwindowbin:-qwindowbin,2])]) #find best peakamp for the 3 channels
      peakamplitudelocation=np.where(hilbert_amp == peakamplitude[i-antennamin])

      #this is to assure that there is a maximum amplitude, at that its unique, and that it could be found far from the borders
      if(peakamplitude[i-antennamin]!=0.0 and np.shape(peakamplitudelocation)==(2,1)):
        if(peakamplitudelocation[0]>2*qwindowbin and peakamplitudelocation[0]< tracesize-2*qwindowbin ):
          peaktime[i-antennamin]=trace[peakamplitudelocation[0],0]                # get the time of the peak amplitude
          peakbin[i-antennamin]= peakamplitudelocation[0]
        #here, we have the chance that there is a peak glitch in the begining
        elif(peakamplitudelocation[0]>qwindowbin and peakamplitudelocation[0]< tracesize-qwindowbin):

          if(max([max(hilbert_amp[0:qwindowbin,0]), max(hilbert_amp[0:qwindowbin,1]), max(hilbert_amp[0:qwindowbin,2])])<peakamplitude[i-antennamin] and max([max(hilbert_amp[-qwindowbin:,0]), max(hilbert_amp[-qwindowbin:,1]), max(hilbert_amp[-qwindowbin:,2])])<peakamplitude[i-antennamin]):
              print("its close to the border, but there does not seem to be a glitch")
              peaktime[i-antennamin]=trace[peakamplitudelocation[0],0]                # get the time of the peak amplitude
              peakbin[i-antennamin]= peakamplitudelocation[0]

              if(DISPLAY):
                  fig1a=plt.figure(figsize=(8,6))
                  ax31 = plt.subplot(2,2,1)
                  im=ax31.plot(trace[:,0],trace[:,1])
                  im=ax31.plot( np.full(10,peaktime[i-antennamin]), np.linspace(min(trace[:,1]),max(trace[:,1]),10))
                  tmp=ax31.set(title="X Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

                  ax32 = plt.subplot(2,2,2)
                  im=ax32.plot(trace[:,0],trace[:,2])
                  im=ax32.plot(np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  tmp=ax32.set(title="Y Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

                  ax33 = plt.subplot(2,2,3)
                  im=ax33.plot(trace[:,0],trace[:,3])
                  im=ax33.plot(np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,3]),max(trace[:,3]),10))
                  tmp=ax33.set(title="Z Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

                  ax34 = plt.subplot(2,2,4)
                  im=ax34.plot(trace[:,0],hilbert_amp[:,0])
                  im=ax34.plot(trace[:,0],hilbert_amp[:,1])
                  im=ax34.plot(trace[:,0],hilbert_amp[:,2])
                  im=ax34.plot( np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  im=ax34.plot( np.full(10,trace[0,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  im=ax34.plot( np.full(10,trace[qwindowbin,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  im=ax34.plot( np.full(10,trace[2*qwindowbin,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  tmp=ax34.set(title="||2 Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

              plt.show()
          else:
              print("glitch")

              if(DISPLAY):
                  peaktime[i-antennamin]=trace[peakamplitudelocation[0],0]                # get the time of the peak amplitude
                  peakbin[i-antennamin]= peakamplitudelocation[0]

                  fig1a=plt.figure(figsize=(8,6))
                  ax31 = plt.subplot(2,2,1)
                  im=ax31.plot(trace[:,0],trace[:,1])
                  im=ax31.plot( np.full(10,peaktime[i-antennamin]), np.linspace(min(trace[:,1]),max(trace[:,1]),10))
                  tmp=ax31.set(title="X Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

                  ax32 = plt.subplot(2,2,2)
                  im=ax32.plot(trace[:,0],trace[:,2])
                  im=ax32.plot(np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  tmp=ax32.set(title="Y Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

                  ax33 = plt.subplot(2,2,3)
                  im=ax33.plot(trace[:,0],trace[:,3])
                  im=ax33.plot(np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,3]),max(trace[:,3]),10))
                  tmp=ax33.set(title="Z Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

                  ax34 = plt.subplot(2,2,4)
                  im=ax34.plot(trace[:,0],hilbert_amp[:,0])
                  im=ax34.plot(trace[:,0],hilbert_amp[:,1])
                  im=ax34.plot(trace[:,0],hilbert_amp[:,2])
                  im=ax34.plot( np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  im=ax34.plot( np.full(10,trace[0,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  im=ax34.plot( np.full(10,trace[qwindowbin,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  im=ax34.plot( np.full(10,trace[2*qwindowbin,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
                  tmp=ax34.set(title="||2 Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

                  plt.show()

              peaktime[i-antennamin]=-1e22
              peakbin[i-antennamin]=-1e22
              peakamplitude[i-antennamin]=-1e22

              p2p_x[i-antennamin]= -1e22
              p2p_y[i-antennamin]= -1e22
              p2p_z[i-antennamin]= -1e22
              p2p_total[i-antennamin]= -1e22

              fluence[i-antennamin]= -1e22
              xfluence[i-antennamin]= -1e22
              yfluence[i-antennamin]= -1e22
              zfluence[i-antennamin]= -1e22

              continue

        else:
          print("too close to the border")

          if(DISPLAY):
              fig1a=plt.figure(figsize=(8,6))
              ax31 = plt.subplot(2,2,1)
              im=ax31.plot(trace[:,0],trace[:,1])
              im=ax31.plot( np.full(10,peaktime[i-antennamin]), np.linspace(min(trace[:,1]),max(trace[:,1]),10))
              tmp=ax31.set(title="X Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

              ax32 = plt.subplot(2,2,2)
              im=ax32.plot(trace[:,0],trace[:,2])
              im=ax32.plot(np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
              tmp=ax32.set(title="Y Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

              ax33 = plt.subplot(2,2,3)
              im=ax33.plot(trace[:,0],trace[:,3])
              im=ax33.plot(np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,3]),max(trace[:,3]),10))
              tmp=ax33.set(title="Z Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

              ax34 = plt.subplot(2,2,4)
              im=ax34.plot(trace[:,0],hilbert_amp[:,0])
              im=ax34.plot(trace[:,0],hilbert_amp[:,1])
              im=ax34.plot(trace[:,0],hilbert_amp[:,2])
              im=ax34.plot( np.full(10,peaktime[i-antennamin]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
              im=ax34.plot( np.full(10,trace[0,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
              im=ax34.plot( np.full(10,trace[qwindowbin,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
              im=ax34.plot( np.full(10,trace[2*qwindowbin,0]),np.linspace(min(trace[:,2]),max(trace[:,2]),10))
              tmp=ax34.set(title="||2 Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

          peaktime[i-antennamin]=-1e21
          peakbin[i-antennamin]=-1e21
          peakamplitude[i-antennamin]=-1e21

          p2p_x[i-antennamin]= -1e21
          p2p_y[i-antennamin]= -1e21
          p2p_z[i-antennamin]= -1e21
          p2p_total[i-antennamin]= -1e21

          fluence[i-antennamin]= -1e21
          xfluence[i-antennamin]= -1e21
          yfluence[i-antennamin]= -1e21
          zfluence[i-antennamin]= -1e21


          plt.show()

          continue

      else:
        print("multiple peaks, 0, or other error")

        if(DISPLAY):
            fig1a=plt.figure(figsize=(8,6))
            ax31 = plt.subplot(2,2,1)
            im=ax31.plot(trace[:,0],trace[:,1])
            tmp=ax31.set(title="X Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

            ax32 = plt.subplot(2,2,2)
            im=ax32.plot(trace[:,0],trace[:,2])
            tmp=ax32.set(title="Y Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

            ax33 = plt.subplot(2,2,3)
            im=ax33.plot(trace[:,0],trace[:,3])
            tmp=ax33.set(title="Z Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

            ax34 = plt.subplot(2,2,4)
            im=ax34.plot(trace[:,0],hilbert_amp[:,0])
            im=ax34.plot(trace[:,0],hilbert_amp[:,1])
            im=ax34.plot(trace[:,0],hilbert_amp[:,2])
            tmp=ax34.set(title="||2 Antenna "+str(i),xlabel='time[ns]',ylabel='Amplitude ' + usetrace)

        plt.show()

        peaktime[i-antennamin]=-1e20
        peakbin[i-antennamin]=-1e20
        peakamplitude[i-antennamin]=-1e20

        p2p_x[i-antennamin]= -1e20
        p2p_y[i-antennamin]= -1e20
        p2p_z[i-antennamin]= -1e20
        p2p_total[i-antennamin]= -1e20

        fluence[i-antennamin]= -1e20
        xfluence[i-antennamin]= -1e20
        yfluence[i-antennamin]= -1e20
        zfluence[i-antennamin]= -1e20
        continue

      #P2P
      p2p= np.amax(trace[qwindowbin:-qwindowbin],axis=0)-np.amin(trace,axis=0)
      p2p_x[i-antennamin]= p2p[1]
      p2p_y[i-antennamin]= p2p[2]
      p2p_z[i-antennamin]= p2p[3]

      amplitude = np.sqrt(trace[qwindowbin:-qwindowbin,1]**2. + trace[qwindowbin:-qwindowbin,2]**2. + trace[qwindowbin:-qwindowbin,3]**2.) # combined components

      p2p_total[i-antennamin] = max(amplitude)-min(amplitude)

      binpeak= peakbin[i-antennamin]
      binmin= int(binpeak-2*qwindowbin)
      binmax= int(binpeak+2*qwindowbin)

      if(binmin<0):
       print("underflow bin",binmin,binpeak,binmax)
       binmin=0
      if(binmax>tracesize):
       print("overflow bin",binmin,binpeak,binmax)
       binmax=tracesize


      #FLUENCE
      #i will be computing the square of the trace
      #norm of trace
      norm=np.linalg.norm(trace[binmin:binmax,1:4],axis=1)
      #sum
      fluence[i-antennamin]=np.sum(norm*norm)

      #and then the fluence in each component.
      xtrace=trace[binmin:binmax,1]
      xfluence[i-antennamin]=np.sum(xtrace*xtrace)
      ytrace=trace[binmin:binmax,2]
      yfluence[i-antennamin]=np.sum(ytrace*ytrace)
      ztrace=trace[binmin:binmax,3]
      zfluence[i-antennamin]=np.sum(ztrace*ztrace)

    #end for antennas

    p2p = np.stack((p2p_x, p2p_y, p2p_z, p2p_total), axis=0)

    peak = np.stack((peaktime, peakbin, peakamplitude), axis=0)

    fluence_total= fluenceunit*fluence
    xfluence= fluenceunit*xfluence
    yfluence= fluenceunit*yfluence
    zfluence= fluenceunit*zfluence

    fluence= np.stack((xfluence, yfluence, zfluence , fluence_total), axis=0)


    if(DISPLAY):

      X=GetXFromAntennaInfo(CurrentAntennaInfo)
      Y=GetYFromAntennaInfo(CurrentAntennaInfo)
      X=X[antennamin:antennamax+1]
      Y=Y[antennamin:antennamax+1]

      if(usetrace=='efield'):
        title="P2P Amplitude "
        unit= "$\mu V/m$"
      else:
        title="P2P Amplitude"
        unit= "$\mu V$"

      #done with event 3419 of the database
      plt.rc('font', family='serif', size=15)
      fig1a=plt.figure(figsize=(8,6))
      ax3a = plt.subplot(2,2,1)
      im=ax3a.scatter(X,Y,c=p2p_total,s=15,cmap=plt.cm.jet)
      tmp=ax3a.set(title="P2P "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3a.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1a.colorbar(im,ax=ax3a)
      bar.set_label(unit, rotation=270, labelpad=17)


      ax3b = plt.subplot(2,2,2)
      im=ax3b.scatter(X,Y,c=p2p_x,s=15,cmap=plt.cm.jet)
      tmp=ax3b.set(title="P2P X "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3b.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1a.colorbar(im,ax=ax3b)
      bar.set_label(unit, rotation=270, labelpad=17)

      ax3c = plt.subplot(2,2,3)
      im=ax3c.scatter(X,Y,c=p2p_y*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3c.set(title="P2P Y "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3c.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1a.colorbar(im,ax=ax3c)
      bar.set_label(unit, rotation=270, labelpad=17)

      ax3d = plt.subplot(2,2,4)
      im=ax3d.scatter(X,Y,c=p2p_z*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3d.set(title="P2P Z "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3d.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1a.colorbar(im,ax=ax3d)
      bar.set_label(unit, rotation=270, labelpad=17)

      #####################################################################################

      if(usetrace=='efield'):
        title="Fluence "
        unit= "$meV/m^2$"
      else:
        title="Integrated Power"
        unit= "$meV$"

      plt.rc('font', family='serif', size=15)
      fig1b=plt.figure(figsize=(8,6))
      ax3a = plt.subplot(2,2,1)
      im=ax3a.scatter(X,Y,c=fluence_total*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3a.set(title="Energy "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3a.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1b.colorbar(im,ax=ax3a)
      bar.set_label(unit, rotation=270, labelpad=17)


      ax3b = plt.subplot(2,2,2)
      im=ax3b.scatter(X,Y,c=xfluence*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3b.set(title="X Energy "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3b.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1b.colorbar(im,ax=ax3b)
      bar.set_label(unit, rotation=270, labelpad=17)

      ax3c = plt.subplot(2,2,3)
      im=ax3c.scatter(X,Y,c=yfluence*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3c.set(title="Y Energy "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3c.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1b.colorbar(im,ax=ax3c)
      bar.set_label(unit, rotation=270, labelpad=17)

      ax3d = plt.subplot(2,2,4)
      im=ax3d.scatter(X,Y,c=zfluence*1000,s=15,cmap=plt.cm.jet)
      tmp=ax3d.set(title="Z Energy "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3d.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1b.colorbar(im,ax=ax3d)
      bar.set_label(unit, rotation=270, labelpad=17)


      #######################################################################################

      if(usetrace=='efield'):
        title="Time "
        unit= "ns"
      else:
        title="Time"
        unit= "ns"


      plt.rc('font', family='serif', size=15)
      fig1c=plt.figure(figsize=(8,6))
      ax3a = plt.subplot(2,2,1)
      im=ax3a.scatter(X,Y,c=peaktime,s=15,cmap=plt.cm.jet)
      tmp=ax3a.set(title="PeakTime "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3a.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1c.colorbar(im,ax=ax3a)
      bar.set_label(unit, rotation=270, labelpad=17)


      ax3b = plt.subplot(2,2,2)
      im=ax3b.scatter(X,Y,c=peakbin*binsize,s=15,cmap=plt.cm.jet)
      tmp=ax3b.set(title="PeakBin "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3b.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1c.colorbar(im,ax=ax3b)
      bar.set_label(unit, rotation=270, labelpad=17)

      ax3c = plt.subplot(2,2,3)
      im=ax3c.scatter(X,Y,c=peakamplitude,s=15,cmap=plt.cm.jet)
      tmp=ax3c.set(title="PeakAmplitude "+usetrace,xlabel='Northing [m]',ylabel='Easting [m]')
      ax3c.set_ylabel('Easting [m]',labelpad=-7)
      bar=fig1c.colorbar(im,ax=ax3c)
      bar.set_label(unit, rotation=270, labelpad=17)

      plt.show()

    return p2p,peak,fluence


def get_crosscorrelation_hdf5(InputFilename,InterpolatedFilename, usetrace="efield", DISPLAY=False):

    #TODO: Handle Errors
    '''
    designed for the starshape with 160 + 16 antennas. Computes the cross correlation in the test antenas, with the interpolated antenas on the second file

    Parameters:
    InputFilename: str
        HDF5File. A Second file named HDF5File.Interpolated.usetrace.hdf5 is expected to exist, with the interpolated traces
    usetrace: str
       efield, voltage, filteredvoltage

    Output: maxcorrelation,lag, D (average power in the difference),average power of the simulated trace

    '''

    CurrentRunInfo=GetRunInfo(InputFilename)
    CurrentEventName=GetEventName(CurrentRunInfo,0) #using the first event of each file (there is only one for now)
    CurrentAntennaInfo=GetAntennaInfo(InputFilename,CurrentEventName)
    CurrentSignalSimInfo=GetSignalSimInfo(InputFilename,CurrentEventName)
    tbinsize=GetTimeBinSize(CurrentSignalSimInfo)

    maxcorrelationx= np.zeros(16)
    maxcorrelationy= np.zeros(16)
    maxcorrelationz= np.zeros(16)

    lagx= np.zeros(16)
    lagy= np.zeros(16)
    lagz= np.zeros(16)

    Dx= np.zeros(16)
    Dy= np.zeros(16)
    Dz= np.zeros(16)

    powerx=np.zeros(16)
    powery=np.zeros(16)
    powerz=np.zeros(16)

    InterpolatedRunInfo=GetRunInfo(InterpolatedFilename)
    InterpolatedEventName=GetEventName(InterpolatedRunInfo,0) #using the first event of each file (there is only one for now)
    InterpolatedAntennaInfo=GetAntennaInfo(InterpolatedFilename,InterpolatedEventName)
    InterpolatedSignalSimInfo=GetSignalSimInfo(InterpolatedFilename,InterpolatedEventName)

    for i in range(0,16):
      AntennaID=GetAntennaID(CurrentAntennaInfo,i+160)
      InterpolatedAntennaID=GetAntennaID(InterpolatedAntennaInfo,i)
      if(usetrace=='efield'):
        trace=GetAntennaEfield(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
        interpolatedtrace=GetAntennaEfield(InterpolatedFilename,InterpolatedEventName,InterpolatedAntennaID,OutputFormat="numpy")
        if(np.shape(trace) != np.shape(interpolatedtrace)):
          print("trace shape and interpolated shape are not equal",np.shape(trace), np.shape(interpolatedtrace))
          if(np.shape(trace)[0] < np.shape(interpolatedtrace)[0]):
             interpolatedtrace=interpolatedtrace[0:np.shape(trace)[0],:]
          else:
             trace=interpolatedtrace[0:np.shape(interpolatedtrace)[0],:]
          if(np.shape(trace) != np.shape(interpolatedtrace)):
            print("this didnt fix it")
          else:
            print("this fixed it")
      elif(usetrace=='voltage'):
        trace=GetAntennaVoltage(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
        interpolatedtrace=GetAntennaVoltage(InterpolatedFilename,InterpolatedEventName,InterpolatedAntennaID,OutputFormat="numpy")
        if(np.shape(trace) != np.shape(interpolatedtrace)):
          print("trace shape and interpolated shape are not equal",np.shape(trace), np.shape(interpolatedtrace))
          if(np.shape(trace)[0] < np.shape(interpolatedtrace)[0]):
             interpolatedtrace=interpolatedtrace[0:np.shape(trace)[0],:]
          else:
             trace=interpolatedtrace[0:np.shape(interpolatedtrace)[0],:]
          if(np.shape(trace) != np.shape(interpolatedtrace)):
            print("this didnt fix it")
          else:
            print("this fixed it")
      elif(usetrace=='filteredvoltage'):
        trace=GetAntennaFilteredVoltage(InputFilename,CurrentEventName,AntennaID,OutputFormat="numpy")
        interpolatedtrace=GetAntennaFilteredVoltage(InterpolatedFilename,InterpolatedEventName,InterpolatedAntennaID,OutputFormat="numpy")
        if(np.shape(trace) != np.shape(interpolatedtrace)):
          print("trace shape and interpolated shape are not equal",np.shape(trace), np.shape(interpolatedtrace))
          if(np.shape(trace)[0] < np.shape(interpolatedtrace)[0]):
             interpolatedtrace=interpolatedtrace[0:np.shape(trace)[0],:]
          else:
             trace=interpolatedtrace[0:np.shape(interpolatedtrace)[0],:]
          if(np.shape(trace) != np.shape(interpolatedtrace)):
            print("this didnt fix it")
          else:
            print("this fixed it")
      else:
        print('You must specify either efield, voltage or filteredvoltage, bailing out')
        return -1,-1,-1

      #Xcomponent
      tracex=trace[:,1]
      interpolatedx=interpolatedtrace[:,1]

      difference=tracex-interpolatedx
      meanx=tracex.mean()
      interpolatedmeanx=interpolatedx.mean()
      ccovx=np.correlate(tracex - meanx, interpolatedx - interpolatedmeanx, mode='full')
      npts= len(tracex)
      lagsx = np.arange(-npts + 1, npts)
      stdx=tracex.std()
      interpolatedstdx=interpolatedx.std()
      if(stdx!=0 and interpolatedstdx!=0):
        ccorx = ccovx / (npts * stdx * interpolatedstdx)
      else:
        continue
      if(np.max(ccorx)>np.abs(np.min(ccorx))):
        lagx[i] = lagsx[np.argmax(ccorx)]
        maxcorrelationx[i]=np.max(ccorx)
      else:
        lagx[i] = lagsx[np.argmin(ccorx)]
        maxcorrelationx[i]=np.min(ccorx)
      powerx[i]=np.dot(tracex, tracex)/npts
      #power in the diference
      Dx[i]=stdx**2+interpolatedstdx**2 + (meanx**2+interpolatedmeanx**2-2*meanx*interpolatedmeanx)- 2*maxcorrelationx[i]*stdx*interpolatedstdx
      #print("Dx",Dx[i])
      #print("Powerx",powerx[i])

      #Ycomponent
      tracey=trace[:,2]
      interpolatedy=interpolatedtrace[:,2]
      difference=tracey-interpolatedy
      meany=tracey.mean()
      interpolatedmeany=interpolatedy.mean()
      ccovy=np.correlate(tracey - meany, interpolatedy - interpolatedmeany , mode='full')
      npts= len(tracey)
      lagsy = np.arange(-npts + 1, npts)
      stdy=tracey.std()
      interpolatedstdy=interpolatedy.std()
      if(stdy!=0 and interpolatedstdy!=0):
        ccory = ccovy / (npts * stdy * interpolatedstdy)
      else:
        continue
      if(np.max(ccory)>np.abs(np.min(ccory))):
        lagy[i] = lagsy[np.argmax(ccory)]
        maxcorrelationy[i]=np.max(ccory)
      else:
        lagy[i] = lagsy[np.argmin(ccory)]
        maxcorrelationy[i]=np.min(ccory)
      powery[i]=np.dot(tracey, tracey)/npts

      #power in the diference
      #print("stdy",stdy)
      #print("istdy",interpolatedstdy)
      #print("meany",meany)
      #print("imeany",interpolatedmeany)
      #print("maxcorrelationy",maxcorrelationy[i])
      Dy[i]=stdy**2+interpolatedstdy**2 + (meany**2+interpolatedmeany**2-2*meany*interpolatedmeany)- 2*maxcorrelationy[i]*stdy*interpolatedstdy
      #print("Dy",Dy[i])
      #print("Powery",powery[i])


      #Zcomponent
      tracez=trace[:,3]
      interpolatedz=interpolatedtrace[:,3]
      difference=tracez-interpolatedz
      meanz=tracez.mean()
      interpolatedmeanz=interpolatedz.mean()
      ccovz=np.correlate(tracez - meanz, interpolatedz - interpolatedmeanz, mode='full')
      npts= len(tracez)
      lagsz = np.arange(-npts + 1, npts)
      stdz=tracez.std()
      interpolatedstdz=interpolatedz.std()
      if(stdz!=0 and interpolatedstdz!=0):
        ccorz = ccovz / (npts * stdz * interpolatedstdz)
      else:
        continue
      if(np.max(ccorz)>np.abs(np.min(ccorz))):
        lagz[i] = lagsz[np.argmax(ccorz)]
        maxcorrelationz[i]=np.max(ccorz)
      else:
        lagz[i] = lagsz[np.argmin(ccorz)]
        maxcorrelationz[i]=np.min(ccorz)
      powerz[i]=np.dot(tracez, tracez)/npts
      #power in the diference
      Dz[i]=stdz**2+interpolatedstdz**2 + (meanz**2+interpolatedmeanz**2-2*meanz*interpolatedmeanz)- 2*maxcorrelationz[i]*stdz*interpolatedstdz
      #print("Dz",Dz[i])
      #print("Powerz",powerz[i])
      if(DISPLAY):
        fig1, ((ax1, ax2,ax3), (ax4, ax5,ax6))  = plt.subplots(2, 3, sharey='col', sharex='row')
        ax1.plot(interpolatedtrace[:,0], interpolatedx, linestyle='--',color='g', label = "Synthetized")
        ax1.plot(trace[:,0], tracex, label = "Simulation")
        tmp=ax1.set(ylabel=usetrace + ' Signal in X')
        ax4.plot(lagsx, ccorx*np.max(tracex))
        ax4.set_ylabel('cross-correlation')

        ax2.plot(interpolatedtrace[:,0], interpolatedy, linestyle='--',color='g', label = "Synthetized")
        ax2.plot(trace[:,0], tracey, label = "Simulation")
        tmp=ax1.set(ylabel='Signal in Y')
        ax5.plot(lagsy, ccory*np.max(tracey))
        ax5.set_ylabel('cross-correlation')

        ax3.plot(interpolatedtrace[:,0], interpolatedz, linestyle='--',color='g', label = "Synthetized")
        ax3.plot(trace[:,0], tracez, label = "Simulation")
        tmp=ax1.set(ylabel=usetrace +' Signal in Z')
        ax6.plot(lagsz, ccorz*np.max(tracez))
        ax6.set_ylabel('cross-correlation')

        print("X",str(i),maxcorrelationx[i],lagx[i],Dx[i])
        print("Y",str(i),maxcorrelationy[i],lagy[i],Dy[i])
        print("Z",str(i),maxcorrelationz[i],lagz[i],Dz[i])

        plt.show()

    #end for antennas

    maxcorrelation = np.stack((maxcorrelationx, maxcorrelationy, maxcorrelationz), axis=0)
    lag = np.stack((lagx, lagy, lagz), axis=0)
    D= np.stack((Dx, Dy, Dz), axis=0)
    Power=np.stack((powerx, powery, powerz), axis=0)
    return maxcorrelation,lag,D,Power


