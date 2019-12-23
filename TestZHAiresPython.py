import AiresInfoFunctions as AiresInfo
import sys
import os
import glob
import logging
import numpy as np
from astropy.table import Table, Column
from astropy import units as u
import hdf5fileinout as hdf5io
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':

  #testing the GetTable Function

  if len(sys.argv)!=2:
    print("Please point me to a directory with some ZHAires output, nothing more, nothing less!")

  else:

    inputfolder=sys.argv[1]
    idffile=glob.glob(inputfolder+"/*.idf")

    if(len(idffile)!=1):
     print("there should be one and only one idf file in the input directory!. cannot continue!")
     exit()

    sryfile=glob.glob(inputfolder+"/*.sry")

    if(len(sryfile)>1):
     print("there should be one and only one sry file in the input directory!. cannot continue!")
     exit()

    if(len(sryfile)==0):
     print("there should be one and only one sry file in the input directory!. cannot continue!")
     exit()

    #RunInfo
    EventNumber=0 #we are writing only one event per file for now
    Primary= AiresInfo.GetPrimaryFromSry(sryfile[0],"GRAND")
    Zenith = AiresInfo.GetZenithAngleFromSry(sryfile[0],"GRAND")
    Azimuth = AiresInfo.GetAzimuthAngleFromSry(sryfile[0],"GRAND")
    Energy = AiresInfo.GetEnergyFromSry(sryfile[0],"GRAND")
    XmaxAltitude, XmaxDistance, XmaxX, XmaxY, XmaxZ = AiresInfo.GetKmXmaxFromSry(sryfile[0])
    XmaxAltitude= float(XmaxAltitude)*1000.0
    XmaxDistance= float(XmaxDistance)*1000.0
    XmaxPosition=[float(XmaxX)*1000.0, float(XmaxY)*1000.0, float(XmaxZ)*1000.0]
    HadronicModel=AiresInfo.GetHadronicModelFromSry(sryfile[0])
    InjectionAltitude=AiresInfo.GetInjectionAltitudeFromSry(sryfile[0])
    #EventInfo
    SlantXmax=AiresInfo.GetSlantXmaxFromSry(sryfile[0])
    GroundAltitude=AiresInfo.GetGroundAltitudeFromSry(sryfile[0])
    Site=AiresInfo.GetSiteFromSry(sryfile[0])
    Date=AiresInfo.GetDateFromSry(sryfile[0])
    FieldIntensity,FieldInclination,FieldDeclination=AiresInfo.GetMagneticFieldFromSry(sryfile[0])
    AtmosphericModel=AiresInfo.GetAtmosphericModelFromSry(sryfile[0])
    EnergyInNeutrinos=AiresInfo.GetEnergyFractionInNeutrinosFromSry(sryfile[0])
    EnergyInNeutrinos=EnergyInNeutrinos*Energy
    #ShowerSimInfo
    ShowerSimulator=AiresInfo.GetAiresVersionFromSry(sryfile[0])
    ShowerSimulator="Aires "+ShowerSimulator
    RandomSeed=AiresInfo.GetRandomSeedFromSry(sryfile[0])
    RelativeThinning=AiresInfo.GetThinningRelativeEnergyFromSry(sryfile[0])
    WeightFactor=AiresInfo.GetWeightFactorFromSry(sryfile[0])
    GammaEnergyCut=AiresInfo.GetGammaEnergyCutFromSry(sryfile[0])
    ElectronEnergyCut=AiresInfo.GetElectronEnergyCutFromSry(sryfile[0])
    MuonEnergyCut=AiresInfo.GetMuonEnergyCutFromSry(sryfile[0])
    MesonEnergyCut=AiresInfo.GetMesonEnergyCutFromSry(sryfile[0])
    NucleonEnergyCut=AiresInfo.GetNucleonEnergyCutFromSry(sryfile[0])
    #SignalSimInfo
    FieldSimulator=AiresInfo.GetZHAireSVersionFromSry(sryfile[0])
    FieldSimulator="ZHAireS "+FieldSimulator
    RefractionIndexModel="Exponential"
    RefractionIndexParameters=[1.0003250,-0.1218]
    TimeBinSize=AiresInfo.GetTimeBinFromSry(sryfile[0])
    TimeWindowMin=AiresInfo.GetTimeWindowMinFromSry(sryfile[0])
    TimeWindowMax=AiresInfo.GetTimeWindowMaxFromSry(sryfile[0])
    #exit()


    print ("****Shower direction (zen, az) = ("+str(Zenith)+','+str(Azimuth) +") deg")


    EventName=AiresInfo.GetTaskNameFromSry(sryfile[0])
    filename=EventName+".hdf5"
    RunName=filename   #for now the name of the run is just the filename

    antposfile="N/A"
    if(antposfile=="N/A"):
         antposfile=glob.glob(inputfolder+"/antpos.dat")

    if(len(antposfile)==1 and os.path.isfile(antposfile[0])):
        positions = np.genfromtxt(inputfolder+"/antpos.dat") #this is not opening correctly the antena ID
        #workarround
        token = open(antposfile[0],'r')
        linestoken=token.readlines()
        tokens_column_number = 1
        IDs=[]
        slopeA=[]
        slopeB=[]
        for x in linestoken:
            IDs.append(x.split()[tokens_column_number])
            slopeA.append(0.0)
            slopeB.append(0.0)
        token.close()
        antx=positions.T[2]
        anty=positions.T[3]
        antz=positions.T[4]

    elif(len(antposfile)>1):
        logging.critical("multiple antpos.dat files " + str(len(antoposfile)) + " found in " +inputfolder + ". ZHAireSHDF5FileWriter cannot continue")
        #return -1
    else:
        logging.critical("antpos.dat file not found in " +inputfolder + ". ZHAireSHDF5FileWriter cannot continue")
        #return -1


    #Table1006=AiresInfo.GetEPlusMinusLongitudinalTable(inputfolder,Slant=True,Precision="Simple")
    #Table1006.write(filename, path="LongitudinalProfile/e_plus", format="hdf5", append=True, compression=True,serialize_meta=True)
    #
    #Table1205=AiresInfo.GetEPlusMinusLongitudinalTable(inputfolder,Slant=True,Precision="Simple")
    #Table1205.write(filename, path="LongitudinalProfile/e_plus-e_minus", format="hdf5", append=True, compression=True,serialize_meta=True)
    #
    #Table1001=AiresInfo.GetGammaLongitudinalTable(inputfolder,Slant=True,Precision="Simple")
    #Table1001.write(filename, path="LongitudinalProfile/gamma", format="hdf5", append=True, compression=True,serialize_meta=True)
    #
    #Table1007=AiresInfo.GetMuPlusLongitudinalTable(inputfolder,Slant=True,Precision="Simple")
    #Table1007.write(filename, path="LongitudinalProfile/mu_plus", format="hdf5", append=True, compression=True,serialize_meta=True)
    #
    #Table1207=AiresInfo.GetMuPlusMinusLongitudinalTable(inputfolder,Slant=True,Precision="Simple")
    #Table1207.write(filename, path="LongitudinalProfile/mu_plus-mu_minus", format="hdf5", append=True, compression=True,serialize_meta=True)
    #
    #Table1291=AiresInfo.GetAllChargedLongitudinalTable(inputfolder,Slant=True,Precision="Simple")
    #Table1291.write(filename, path="LongitudinalProfile/all_charged", format="hdf5", append=True, compression=True,serialize_meta=True)

    #this info can go to the Event meta
    RunInfo=True
    EventInfo=True
    ShowerSimInfo=True
    SignalSimInfo=True
    AntennaInfo=True
    AntennaTraces=True
    NLongitudinal=True
    ELongitudinal=False
    NlowLongitudinal=False
    ElowLongitudinal=False
    EdepLongitudinal=False
    LateralDistribution=True
    EnergyDistribution=False
    FileFormatVersion=0.0
    EventFormatVersion=0.0


    #i save the variables in an astropy table in order to be able to store the units of the parameters in the meta, becouse if i save it as
    # meta information i loose the capabaility of storing units.
    # instead, i will use the meta to store which sections of the event are availale


    #############################################################################################################################
    # RUN INFO
    #############################################################################################################################
    if(RunInfo):
        #all this should be a function call (CreateRunInfo(...). And i have to find a way to add one line to an existing table  !
        RunInfoMeta={
            "FileFormatVersion":FileFormatVersion,
            "RunName":RunName                        #for checking
            #TODO: decide what else goes here
        }

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

        AstropyTable = Table(data=(a,b,c,d,e,f,g,h,i,j),meta=RunInfoMeta)

        hdf5io.SaveRunInfo(filename,AstropyTable)
        #WriteRunInfo(
        #AstropyTable.write(filename, path="RunInfo", format="hdf5", append=True, compression=True,serialize_meta=True)

    #############################################################################################################################
    # Event INFO
    #############################################################################################################################
    if(EventInfo):

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
        o1=Column(data=[FieldIntensity],name='BField',unit=u.uT)
        p1=Column(data=[FieldInclination],name='BFieldIncl',unit=u.deg)
        q1=Column(data=[FieldDeclination],name='BFieldDecl',unit=u.deg)
        r1=Column(data=[AtmosphericModel],name='AtmosphericModel')
        s1=Column(data=["N/A"],name='AtmosphericModelParameters')
        t1=Column(data=[EnergyInNeutrinos],name='EnergyInNeutrinos',unit=u.EeV)
        AstropyTable = Table(data=(a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1),meta=EventInfoMeta)

        hdf5io.SaveEventInfo(filename,AstropyTable,EventName)
        #AstropyTable.write(filename, path=EventName+"/EventInfo", format="hdf5", append=True, compression=True,serialize_meta=True)


    #############################################################################################################################
    # ShowerSimINFO (deals with the details for the simulation
    #############################################################################################################################
    if(ShowerSimInfo):

        ShowerSimInfoMeta = {
            "RunName":RunName,                             #For cross checking
            "EventName":EventName,                         #For cross checking
            "ShowerSimulator": ShowerSimulator             #TODO: decide what goes here
        }

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
        k2=Column(data=["N/A"],name='OtherParameters')

        AstropyTable = Table(data=(a2,b2,c2,d2,e2,f2,g2,h2,i2,j2,k2),meta=ShowerSimInfoMeta)


        hdf5io.SaveShowerSimInfo(filename,AstropyTable,EventName)
        #AstropyTable.write(filename, path=EventName+"/ShowerSimInfo", format="hdf5", append=True, compression=True,serialize_meta=True)

    #############################################################################################################################
    # SignalSimInfo
    #############################################################################################################################
    if(SignalSimInfo):

        SignalSimInfoMeta = {
            "RunName":RunName,                             #For cross checking
            "EventName":EventName,                         #For cross checking
            "FieldSimulator": FieldSimulator,            #TODO: decide what goes here
        }

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

        AstropyTable = Table(data=(a3,b3,c3,d3,e3,f3,g3),meta=SignalSimInfoMeta)

        hdf5io.SaveSignalSimInfo(filename,AstropyTable,EventName)
        #AstropyTable.write(filename, path=EventName+"/SignalSimInfo", format="hdf5", append=True, compression=True,serialize_meta=True)

    ################################################################################################################################
    # AntennaInfo
    #################################################################################################################################
    if(AntennaInfo):
        AntennaInfoMeta = {
           "RunName":RunName,                             #For cross checking
           "EventName":EventName,                         #For cross checking
           "VoltageSimulator": "N/A",     #TODO: decide what goes here
           "AntennaModel": "N/A",
           "EnvironmentNoiseSimulator": "N/A",
           "ElectronicsSimulator": "N/A",
           "ElectronicsNoiseSimulator": "N/A"
        }

        a4=Column(data=IDs,name='ID',unit=u.m) #in core cordinates
        b4=Column(data=antx,name='X',unit=u.m) #in core cordinates
        c4=Column(data=anty,name='Y',unit=u.m) #in core cordinates
        d4=Column(data=antz,name='Z',unit=u.m) #in core cordinates
        e4=Column(data=slopeA,name='SlopeA',unit=u.m) #in core cordinates
        f4=Column(data=slopeB,name='SlopeB',unit=u.m) #in core cordinates

        #g4=Column(data=Ep2p,name='FieldP2P',unit=u.V/u.m) #p2p Value of the electric field #TODO:
        #h4=Column(data=Ep2p,name='VoltageP2P',unit=u.V) #p2p Value of the electric field + antenna response #TODO:
        #h4=Column(data=Ep2p,name='FilteredVoltageP2P',unit=u.V) #p2p Value of the electric field + antenna response + filtering #TODO:

        AstropyTable = Table(data=(a4,b4,c4,d4,e4,f4),meta=SignalSimInfoMeta)

        hdf5io.SaveAntennaInfo(filename,AstropyTable,EventName)
        #AstropyTable.write(filename, path=EventName+"/AntennaInfo", format="hdf5", append=True, compression=True,serialize_meta=True)

    ################################################################################################################################
    # Individual Antennas (here comes the complicated part)
    #################################################################################################################################
    if(AntennaTraces):
       #ZHAIRES DEPENDENT(all this should be part of the ZHAireS reader.
       ending_e = "/a*.trace"
       tracefiles=glob.glob(inputfolder+ending_e)

       if(len(tracefiles)==0):
         logging.critical("no trace files found in "+showerdirectory+" ZHAireSHDF5FileWriter cannot continue")
         #return -1
       for ant in tracefiles:
            #print("\n Read in data from ", ant)

            ant_number = int(ant.split('/')[-1].split('.trace')[0].split('a')[-1]) # index in selected antenna list. this only works if all antenna files are consecutive

            ID = IDs[ant_number]
            ant_position=(antx[ant_number],anty[ant_number],antz[ant_number])
            ant_slope=(slopeA[ant_number],slopeB[ant_number])

            efield = np.loadtxt(ant,dtype='f4') #we read the electric field as a numpy array (this is a problem of ZHAireS)

            #From here on, this should be replaced by a function call to the HDF5 file io.(convert numpy to astropy and save)
            #info={
            #     'position': ant_position,
            #     'slope': ant_slope}   #TODO: decide what goes here

            #a = Column(data=efield.T[0],unit=u.ns,name='Time')
            #b = Column(data=efield.T[1],unit=u.u*u.V/u.meter,name='Ex')
            #c = Column(data=efield.T[2],unit=u.u*u.V/u.meter,name='Ey')
            #d = Column(data=efield.T[3],unit=u.u*u.V/u.meter,name='Ez')
            #efield_table = Table(data=(a,b,c,d,), meta=info)
            #this should be another hdf5 function:
            #efield_table.write(filename, path=EventName+"/AntennaTraces/"+str(ID)+"/efield", format="hdf5", append=True, compression=True,serialize_meta=True)
            efield=hdf5io.CreateEfieldTable(efield, EventName, EventNumber, ID, ant_number,FieldSimulator)
            hdf5io.SaveEfieldTable(filename,EventName,ID,efield)

    ##############################################################################################################################
    # LONGITUDINAL TABLES
    ##############################################################################################################################

    if(NLongitudinal):
        #the gammas
        table=AiresInfo.GetLongitudinalTable(inputfolder,1001,Slant=True,Precision="Simple")
        Na = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='SlantDepth')
        Nc = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ngamma')

        #i call the eplusminus table, in vertical, to store also the vertical depth
        table=AiresInfo.GetLongitudinalTable(inputfolder,1205,Slant=False,Precision="Simple")
        Nb = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='VerticalDepth')
        Nd = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus_minus')

        #the e plus (yes, the positrons)
        table=AiresInfo.GetLongitudinalTable(inputfolder,1006,Slant=True,Precision="Simple")
        Ne = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus')

        #the mu plus mu minus
        table=AiresInfo.GetLongitudinalTable(inputfolder,1207,Slant=True,Precision="Simple")
        Nf = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus_minus')

        #the mu plus
        table=AiresInfo.GetLongitudinalTable(inputfolder,1007,Slant=True,Precision="Simple")
        Ng = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus')

        #the pi plus pi munus
        table=AiresInfo.GetLongitudinalTable(inputfolder,1211,Slant=True,Precision="Simple")
        Nh = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Npi_plus_minus')

        #the pi plus
        table=AiresInfo.GetLongitudinalTable(inputfolder,1011,Slant=True,Precision="Simple")
        Ni = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Npi_plus')

        #and the all charged
        table=AiresInfo.GetLongitudinalTable(inputfolder,1291,Slant=True,Precision="Simple")
        Nj = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nall_charged')

        #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
        AstropyTable = Table(data=(Na,Nb,Nc,Nd,Ne,Nf,Ng,Nh,Ni,Nj))

        #AstropyTable.write(filename, path=EventName+"/ShowerTables/NLongitudinalProfile", format="hdf5", append=True, compression=True,serialize_meta=True)
        hdf5io.SaveNLongitudinal(filename,AstropyTable,EventName)
    ##############################################################################################################################
    # Energy LONGITUDINAL TABLES (very important to veryfy the energy balance of the cascade, and to compute the invisible energy)
    ##############################################################################################################################
    if(ELongitudinal):
        #the gammas
        table=AiresInfo.GetLongitudinalTable(inputfolder,1501,Slant=True,Precision="Simple")
        Ea = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='SlantDepth')
        Ec = Column(data=table.T[1],unit=u.GeV,name='Egamma')

        #i call the eplusminus table, in vertical, to store also the vertical depth
        table=AiresInfo.GetLongitudinalTable(inputfolder,1705,Slant=False,Precision="Simple")
        Eb = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='VerticalDepth')
        Ed = Column(data=table.T[1],unit=u.GeV,name='Ee_plus_minus')

        #the mu plus mu minus
        table=AiresInfo.GetLongitudinalTable(inputfolder,1707,Slant=True,Precision="Simple")
        Ee = Column(data=table.T[1],unit=u.GeV,name='Emu_plus_minus')

        #the pi plus pi minus
        table=AiresInfo.GetLongitudinalTable(inputfolder,1711,Slant=True,Precision="Simple")
        Ef = Column(data=table.T[1],unit=u.GeV,name='Epi_plus_minus')

        #the k plus k minus
        table=AiresInfo.GetLongitudinalTable(inputfolder,1713,Slant=True,Precision="Simple")
        Eg = Column(data=table.T[1],unit=u.GeV,name='Ek_plus_minus')

        #the neutrons
        table=AiresInfo.GetLongitudinalTable(inputfolder,1521,Slant=True,Precision="Simple")
        Eh = Column(data=table.T[1],unit=u.GeV,name='Eneutrons')

        #the protons
        table=AiresInfo.GetLongitudinalTable(inputfolder,1522,Slant=True,Precision="Simple")
        Ei = Column(data=table.T[1],unit=u.GeV,name='Eprotons')

        #the anti-protons
        table=AiresInfo.GetLongitudinalTable(inputfolder,1523,Slant=True,Precision="Simple")
        Ej = Column(data=table.T[1],unit=u.GeV,name='Eanti_protons')

        #the nuclei
        table=AiresInfo.GetLongitudinalTable(inputfolder,1541,Slant=True,Precision="Simple")
        Ek = Column(data=table.T[1],unit=u.GeV,name='Enuclei')

        #the other charged
        table=AiresInfo.GetLongitudinalTable(inputfolder,1591,Slant=True,Precision="Simple")
        El = Column(data=table.T[1],unit=u.GeV,name='Eother_charged')

        #the other charged
        table=AiresInfo.GetLongitudinalTable(inputfolder,1592,Slant=True,Precision="Simple")
        Em = Column(data=table.T[1],unit=u.GeV,name='Eother_neutral')

        #and the all
        table=AiresInfo.GetLongitudinalTable(inputfolder,1793,Slant=True,Precision="Simple")
        En = Column(data=table.T[1],unit=u.GeV,name='Eall')

        #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
        AstropyTable = Table(data=(Ea,Eb,Ec,Ed,Ee,Ef,Eg,Eh,Ei,Ej,Ek,El,Em,En))

        hdf5io.SaveELongitudinal(filename,AstropyTable,EventName)
        #AstropyTable.write(filename, path=EventName+"/ShowerTables/ELongitudinalProfile", format="hdf5", append=True, compression=True,serialize_meta=True)

    ################################################################################################################################
    # NLowEnergy Longitudinal development
    #################################################################################################################################
    if(NlowLongitudinal):
        #the gammas
        table=AiresInfo.GetLongitudinalTable(inputfolder,7001,Slant=True,Precision="Simple")
        Nla = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='SlantDepth')
        Nlc = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nlow_gamma')

        #i call the eplusminus table, in vertical, to store also the vertical depth
        table=AiresInfo.GetLongitudinalTable(inputfolder,7005,Slant=False,Precision="Simple")
        Nlb = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='VerticalDepth')
        Nld = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nlow_e_minus')

        #the positrons (note that they will deposit twice their rest mass!)
        table=AiresInfo.GetLongitudinalTable(inputfolder,7006,Slant=False,Precision="Simple")
        Nle = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nlow_e_plus')

        #the muons
        table=AiresInfo.GetLongitudinalTable(inputfolder,7207,Slant=False,Precision="Simple")
        Nlf = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nlow_mu_plus_minus')

        #Other Chaged
        table=AiresInfo.GetLongitudinalTable(inputfolder,7091,Slant=False,Precision="Simple")
        Nlg = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nlow_other_charged')

        #Other Neutral
        table=AiresInfo.GetLongitudinalTable(inputfolder,7092,Slant=False,Precision="Simple")
        Nlh = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nlow_other_neutral')

        #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
        AstropyTable = Table(data=(Nla,Nlb,Nlc,Nld,Nle,Nlf,Nlg,Nlh))

        #AstropyTable.write(filename, path=EventName+"/ShowerTables/NlowLongitudinalProfile", format="hdf5", append=True, compression=True,serialize_meta=True)
        hdf5io.SaveNlowLongitudinal(filename,AstropyTable,EventName)

    ################################################################################################################################
    # ELowEnergy Longitudinal development
    #################################################################################################################################
    if(ElowLongitudinal):
        #the gammas
        table=AiresInfo.GetLongitudinalTable(inputfolder,7501,Slant=True,Precision="Simple")
        Ela = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='SlantDepth')
        Elc = Column(data=table.T[1],unit=u.GeV,name='Elow_gamma')

        #i call the eplusminus table, in vertical, to store also the vertical depth
        table=AiresInfo.GetLongitudinalTable(inputfolder,7505,Slant=False,Precision="Simple")
        Elb = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='VerticalDepth')
        Eld = Column(data=table.T[1],unit=u.GeV,name='Elow_e_minus')

        #the positrons (note that they will deposit twice their rest mass!)
        table=AiresInfo.GetLongitudinalTable(inputfolder,7506,Slant=False,Precision="Simple")
        Ele = Column(data=table.T[1],unit=u.GeV,name='Elow_e_plus')

        #the muons
        table=AiresInfo.GetLongitudinalTable(inputfolder,7707,Slant=False,Precision="Simple")
        Elf = Column(data=table.T[1],unit=u.GeV,name='Elow_mu_plus_minus')

        #Other Chaged
        table=AiresInfo.GetLongitudinalTable(inputfolder,7591,Slant=False,Precision="Simple")
        Elg = Column(data=table.T[1],unit=u.GeV,name='Elow_other_charged')

        #Other Neutral
        table=AiresInfo.GetLongitudinalTable(inputfolder,7592,Slant=False,Precision="Simple")
        Elh = Column(data=table.T[1],unit=u.GeV,name='Elow_other_neutral')

        #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
        AstropyTable = Table(data=(Ela,Elb,Elc,Eld,Ele,Elf,Elg,Elh))

        #AstropyTable.write(filename, path=EventName+"/ShowerTables/ElowLongitudinalProfile", format="hdf5", append=True, compression=True,serialize_meta=True)
        hdf5io.SaveElowLongitudinal(filename,AstropyTable,EventName)

    ################################################################################################################################
    # EnergyDeposit Longitudinal development
    #################################################################################################################################
    if(EdepLongitudinal):
        #the gammas
        table=AiresInfo.GetLongitudinalTable(inputfolder,7801,Slant=True,Precision="Simple")
        Eda = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='SlantDepth')
        Edc = Column(data=table.T[1],unit=u.GeV,name='Edep_gamma')

        #i call the eplusminus table, in vertical, to store also the vertical depth
        table=AiresInfo.GetLongitudinalTable(inputfolder,7805,Slant=False,Precision="Simple")
        Edb = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='VerticalDepth')
        Edd = Column(data=table.T[1],unit=u.GeV,name='Edep_e_minus')

        #the positrons (note that they will deposit twice their rest mass!)
        table=AiresInfo.GetLongitudinalTable(inputfolder,7806,Slant=False,Precision="Simple")
        Ede = Column(data=table.T[1],unit=u.GeV,name='Edep_e_plus')

        #the muons
        table=AiresInfo.GetLongitudinalTable(inputfolder,7907,Slant=False,Precision="Simple")
        Edf = Column(data=table.T[1],unit=u.GeV,name='Edep_mu_plus_minus')

        #Other Chaged
        table=AiresInfo.GetLongitudinalTable(inputfolder,7891,Slant=False,Precision="Simple")
        Edg = Column(data=table.T[1],unit=u.GeV,name='Edep_other_charged')

        #Other Neutral
        table=AiresInfo.GetLongitudinalTable(inputfolder,7892,Slant=False,Precision="Simple")
        Edh = Column(data=table.T[1],unit=u.GeV,name='Edep_other_neutral')

        #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
        AstropyTable = Table(data=(Eda,Edb,Edc,Edd,Ede,Edf,Edg,Edh))

        #AstropyTable.write(filename, path=EventName+"/ShowerTables/EdepLongitudinalProfile", format="hdf5", append=True, compression=True,serialize_meta=True)
        hdf5io.SaveEdepLongitudinal(filename,AstropyTable,EventName)

    ################################################################################################################################
    # Lateral Tables
    #################################################################################################################################
    if(LateralDistribution):
        #the gammas
        table=AiresInfo.GetLateralTable(inputfolder,2001,Density=False,Precision="Simple")
        La = Column(data=table.T[0],unit=u.m,name='Distance')
        Lb = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ngamma')

        table=AiresInfo.GetLateralTable(inputfolder,2205,Density=False,Precision="Simple")
        Lc = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus_minus')

        table=AiresInfo.GetLateralTable(inputfolder,2006,Density=False,Precision="Simple")
        Ld = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus')

        table=AiresInfo.GetLateralTable(inputfolder,2207,Density=False,Precision="Simple")
        Le = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus_minus')

        table=AiresInfo.GetLateralTable(inputfolder,2007,Density=False,Precision="Simple")
        Lf = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus')

        table=AiresInfo.GetLateralTable(inputfolder,2291,Density=False,Precision="Simple")
        Lg = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nall_charged')

        #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
        AstropyTable = Table(data=(La,Lb,Lc,Ld,Le,Lf,Lg))

        #AstropyTable.write(filename, path=EventName+"/ShowerTables/NLateralProfile", format="hdf5", append=True, compression=True,serialize_meta=True)
        hdf5io.SaveLateralDistribution(filename,AstropyTable,EventName)

    ################################################################################################################################
    # Energy Distribution at ground Tables
    #################################################################################################################################
    if(EnergyDistribution):
        #the gammas
        table=AiresInfo.GetLateralTable(inputfolder,2501,Density=False,Precision="Simple")
        Eda = Column(data=table.T[0],unit=u.GeV,name='Energy')
        Edb = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ngamma')

        table=AiresInfo.GetLateralTable(inputfolder,2705,Density=False,Precision="Simple")
        Edc = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus_minus')

        table=AiresInfo.GetLateralTable(inputfolder,2506,Density=False,Precision="Simple")
        Edd = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus')

        table=AiresInfo.GetLateralTable(inputfolder,2707,Density=False,Precision="Simple")
        Ede = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus_minus')

        table=AiresInfo.GetLateralTable(inputfolder,2507,Density=False,Precision="Simple")
        Edf = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus')

        table=AiresInfo.GetLateralTable(inputfolder,2791,Density=False,Precision="Simple")
        Edg = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nall_charged')

        #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
        AstropyTable = Table(data=(Eda,Edb,Edc,Edd,Ede,Edf,Edg))

        #AstropyTable.write(filename, path=EventName+"/ShowerTables/EGround", format="hdf5", append=True, compression=True,serialize_meta=True)
        hdf5io.SaveEnergyDistribution(filename,AstropyTable,EventName)




