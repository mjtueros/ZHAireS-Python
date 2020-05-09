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



def ZHAiresReader(InputFolder, SignalSimInfo=True, AntennaInfo=True, AntennaTraces=True, NLongitudinal=True, ELongitudinal=False, NlowLongitudinal=False,ElowLongitudinal=False,EdepLongitudinal=False, LateralDistribution=True,EnergyDistribution=False):

    #TODO: Handle when hdf5  file exists
    #TODO: handle how to append an event
    #TODO: allow to specify an output filename

    RunInfo=True            #it makes little sense not to have at least this
    EventInfo=True          #it makes little sense not to have at least this
    ShowerSimInfo=True      #it makes little sense not to have at least this

    idffile=glob.glob(InputFolder+"/*.idf")

    if(len(idffile)!=1):
      logging.critical("there should be one and only one idf file in the input directory!. cannot continue!")
      return -1

    sryfile=glob.glob(inputfolder+"/*.sry")

    if(len(sryfile)>1):
      logging.critical("there should be one and only one sry file in the input directory!. cannot continue!")
      return -1

    if(len(sryfile)==0):
      logging.critical("there should be one and only one sry file in the input directory!. cannot continue!")
      return -1

    EventName=AiresInfo.GetTaskNameFromSry(sryfile[0])
    filename=EventName+".hdf5"
    RunName=filename   #for now the name of the run is just the filename

    inpfile=glob.glob(InputFolder+"/*.inp")
    if(len(idffile)!=1):
      logging.critical("we can only get the core position from the input file, at it should be in the same directory as the sry")
      logging.critical("defaulting to (0.0,0)")
      inpfile[0]=None
      CorePosition=(0.0,0.0,0.0)


    #############################################################################################################################
    # RUN INFO
    #############################################################################################################################
    #Getting all the information i Need to create RunInfo
    EventNumber=0 #we are writing only one event per file for now
    Primary= AiresInfo.GetPrimaryFromSry(sryfile[0],"GRAND")
    Zenith = AiresInfo.GetZenithAngleFromSry(sryfile[0],"GRAND")
    Azimuth = AiresInfo.GetAzimuthAngleFromSry(sryfile[0],"GRAND")
    Energy = AiresInfo.GetEnergyFromSry(sryfile[0],"GRAND")
    XmaxAltitude, XmaxDistance, XmaxX, XmaxY, XmaxZ = AiresInfo.GetKmXmaxFromSry(sryfile[0])
    XmaxAltitude= float(XmaxAltitude)*1000.0
    XmaxDistance= float(XmaxDistance)*1000.0
    XmaxPosition=[float(XmaxX)*1000.0, float(XmaxY)*1000.0, float(XmaxZ)*1000.0]
    SlantXmax=AiresInfo.GetSlantXmaxFromSry(sryfile[0])
    HadronicModel=AiresInfo.GetHadronicModelFromSry(sryfile[0])
    InjectionAltitude=AiresInfo.GetInjectionAltitudeFromSry(sryfile[0])
    Lat,Long=AiresInfo.GetLatLongFromSry(sryfile[0])

    if(RunInfo):

        RunInfoMeta=hdf5io.CreateRunInfoMeta(RunName)

        RunInfoTable=hdf5io.CreateRunInfo(EventName,Primary,Energy,Zenith,Azimuth,XmaxDistance,SlantXmax,HadronicModel,InjectionAltitude,RunInfoMeta)

        hdf5io.SaveRunInfo(filename,RunInfoTable)

    #############################################################################################################################
    # Event INFO
    #############################################################################################################################
    #Getting all the information i need to create EventInfo
    GroundAltitude=AiresInfo.GetGroundAltitudeFromSry(sryfile[0])
    Site=AiresInfo.GetSiteFromSry(sryfile[0])
    Date=AiresInfo.GetDateFromSry(sryfile[0])
    FieldIntensity,FieldInclination,FieldDeclination=AiresInfo.GetMagneticFieldFromSry(sryfile[0])
    AtmosphericModel=AiresInfo.GetAtmosphericModelFromSry(sryfile[0])
    EnergyInNeutrinos=AiresInfo.GetEnergyFractionInNeutrinosFromSry(sryfile[0])
    EnergyInNeutrinos=EnergyInNeutrinos*Energy

    if(inpfile[0]!=None):
      CorePosition=AiresInfo.GetCorePositionFromInp(inpfile[0])

    print("CorePosition:",CorePosition)


    if(EventInfo):

        EventInfoMeta=hdf5io.CreateEventInfoMeta(RunName,EventNumber,EventInfo,ShowerSimInfo,SignalSimInfo,AntennaInfo,AntennaTraces,NLongitudinal,ELongitudinal,NlowLongitudinal,ElowLongitudinal,EdepLongitudinal,LateralDistribution,EnergyDistribution)

        EventInfo=hdf5io.CreateEventInfo(EventName,Primary,Energy,Zenith,Azimuth,XmaxDistance,XmaxPosition,XmaxAltitude,SlantXmax,InjectionAltitude,GroundAltitude,Site,Date,Lat,Long,FieldIntensity,FieldInclination,FieldDeclination,AtmosphericModel,EnergyInNeutrinos,EventInfoMeta,CorePosition=CorePosition)

        hdf5io.SaveEventInfo(filename,EventInfo,EventName)

    #############################################################################################################################
    # ShowerSimInfo (deals with the details for the simulation). This might be simulator-dependent (CoREAS has different parameters)
    #############################################################################################################################

    #Getting the information i need for ShowerSimInfo
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
    CPUTime=AiresInfo.GetTotalCPUTimeFromSry(sryfile[0],"N/A")


    if(ShowerSimInfo):

        ShowerSimInfoMeta=hdf5io.CreateShowerSimInfoMeta(RunName,EventName,ShowerSimulator)

        ShowerSimInfo=hdf5io.CreateShowerSimInfo(ShowerSimulator,HadronicModel,RandomSeed,RelativeThinning,WeightFactor,GammaEnergyCut,ElectronEnergyCut,MuonEnergyCut,MesonEnergyCut,NucleonEnergyCut,CPUTime,ShowerSimInfoMeta)

        hdf5io.SaveShowerSimInfo(filename,ShowerSimInfo,EventName)

    #############################################################################################################################
    # SignalSimInfo
    #############################################################################################################################
    if(SignalSimInfo):
        #Getting all the information i need for SignalSimInfo
        FieldSimulator=AiresInfo.GetZHAireSVersionFromSry(sryfile[0])
        FieldSimulator="ZHAireS "+str(FieldSimulator)
        RefractionIndexModel="Exponential"
        RefractionIndexParameters=[1.0003250,-0.1218]
        TimeBinSize=AiresInfo.GetTimeBinFromSry(sryfile[0])
        TimeWindowMin=AiresInfo.GetTimeWindowMinFromSry(sryfile[0])
        TimeWindowMax=AiresInfo.GetTimeWindowMaxFromSry(sryfile[0])

        SignalSimInfoMeta=hdf5io.CreateSignalSimInfoMeta(RunName,EventName,FieldSimulator)

        SignalSimInfo=hdf5io.CreateSignalSimInfo(FieldSimulator,RefractionIndexModel,RefractionIndexParameters,TimeBinSize,TimeWindowMin,TimeWindowMax,SignalSimInfoMeta)

        hdf5io.SaveSignalSimInfo(filename,SignalSimInfo,EventName)

    ################################################################################################################################
    # AntennaInfo
    #################################################################################################################################
    if(AntennaInfo):

        #Getting info from aires sry instead (much tidier)

        IDs,antx,anty,antz,antt=AiresInfo.GetAntennaInfoFromSry(sryfile[0])

        antx=np.array(antx, dtype=np.float32)
        anty=np.array(anty, dtype=np.float32)
        antz=np.array(antz, dtype=np.float32)
        antt=np.array(antt, dtype=np.float32)
        #ZHAireS does not support slopes in the antennas, but you can put them here after you computed the antenna response
        slopeA=np.zeros(np.shape(antt))
        slopeB=np.zeros(np.shape(antt))

        #Getting the information I need
        #antposfile="N/A"
        #if(antposfile=="N/A"):
        #    antposfile=glob.glob(inputfolder+"/antpos.dat")

        #if(len(antposfile)==1 and os.path.isfile(antposfile[0])):
        #    positions = np.genfromtxt(inputfolder+"/antpos.dat") #this is not opening correctly the antena ID
        #    #workarround
        #    token = open(antposfile[0],'r')
        #    linestoken=token.readlines()
        #    tokens_column_number = 1
        #    IDs=[]
        #    slopeA=[]
        #    slopeB=[]
        #    for x in linestoken:
        #        IDs.append(x.split()[tokens_column_number])
        #        slopeA.append(0.0)
        #        slopeB.append(0.0)
        #    token.close()
        #    antx=positions.T[2]
        #    anty=positions.T[3]
        #     antz=positions.T[4]
        #
        #elif(len(antposfile)>1):
        #    logging.critical("multiple antpos.dat files " + str(len(antoposfile)) + " found in " +inputfolder + ". ZHAireSHDF5FileWriter cannot continue")
        #    return -1
        #else:
        #    logging.critical("antpos.dat file not found in " +inputfolder + ". ZHAireSHDF5FileWriter cannot continue")
        #    return -1


        AntennaInfoMeta= hdf5io.CreatAntennaInfoMeta(RunName,EventName)

        AntennaInfo=hdf5io.CreateAntennaInfo(IDs, antx, anty, antz, antt,slopeA, slopeB, AntennaInfoMeta)

        hdf5io.SaveAntennaInfo(filename,AntennaInfo,EventName)

    #################################################################################################################################
    # Individual Antennas (here comes the complicated part)
    #################################################################################################################################
    if(AntennaTraces):
       #ZHAIRES DEPENDENT
       ending_e = "/a*.trace"
       tracefiles=glob.glob(inputfolder+ending_e)

       if(len(tracefiles)==0):
         logging.critical("no trace files found in "+showerdirectory+" ZHAireSHDF5FileWriter cannot continue")

       for ant in tracefiles:

            ant_number = int(ant.split('/')[-1].split('.trace')[0].split('a')[-1]) # index in selected antenna list. this only works if all antenna files are consecutive

            ID = IDs[ant_number]
            ant_position=(antx[ant_number],anty[ant_number],antz[ant_number])
            ant_slope=(slopeA[ant_number],slopeB[ant_number])

            efield = np.loadtxt(ant,dtype='f4') #we read the electric field as a numpy array

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

    return filename

if __name__ == '__main__':

  if (len(sys.argv)>3 or len(sys.argv)<2) :
    print("Please point me to a directory with some ZHAires output, and indicate the mode...nothing more, nothing less!")
    print("i.e ZHAireSReader ./MyshowerDir full")

  elif len(sys.argv)==3 :
    inputfolder=sys.argv[1]
    mode=sys.argv[2]

  elif len(sys.argv)==2 :
    inputfolder=sys.argv[1]
    mode="standard"


  if(mode=="standard"):

      ZHAiresReader(inputfolder)

  elif(mode=="full"):

      ZHAiresReader(inputfolder, SignalSimInfo=True, AntennaInfo=True, AntennaTraces=True, NLongitudinal=True, ELongitudinal=True, NlowLongitudinal=True, ElowLongitudinal=True, EdepLongitudinal=True, LateralDistribution=True, EnergyDistribution=True)

  elif(mode=="minimal"):

      ZHAiresReader(inputfolder, SignalSimInfo=True, AntennaInfo=True, AntennaTraces=True, NLongitudinal=False, ELongitudinal=False, NlowLongitudinal=False, ElowLongitudinal=False, EdepLongitudinal=False, LateralDistribution=False, EnergyDistribution=False)


  else:

      print("please enter one of these modes: standard, full or minimal")

