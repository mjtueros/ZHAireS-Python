import AiresInfoFunctions as AiresInfo
import sys
import glob
import logging
import numpy as np
import astropy as ap
import h5py
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



    Zenith = AiresInfo.GetZenithAngleFromSry(sryfile[0],"Aires")
    Azimuth = AiresInfo.GetAzimuthAngleFromSry(sryfile[0],"Aires")

    print ("****Shower direction (zen, az) = ("+str(Zenith)+','+str(Azimuth) +") deg")


    Task=AiresInfo.GetTaskNameFromSry(sryfile[0])
    filename=Task+".hdf5"


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


    #lets try a compound version:
    from astropy.table import Table, Column
    from astropy import units as u
    #i first call the positron data in slant

    ##############################################################################################################################
    # LONGITUDINAL TABLES
    ##############################################################################################################################

    #the gammas
    table=AiresInfo.GetLongitudinalTable(inputfolder,1001,Slant=True,Precision="Simple")
    a = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='SlantDepth')
    c = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ngamma')

    #i call the eplusminus table, in vertical, to store also the vertical depth
    table=AiresInfo.GetLongitudinalTable(inputfolder,1205,Slant=False,Precision="Simple")
    b = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='VerticalDepth')
    d = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus_minus')

    table=AiresInfo.GetLongitudinalTable(inputfolder,1006,Slant=True,Precision="Simple")
    e = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus')

    #the mu plus mu minus
    table=AiresInfo.GetLongitudinalTable(inputfolder,1207,Slant=True,Precision="Simple")
    f = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus_minus')

    #the mu plus
    table=AiresInfo.GetLongitudinalTable(inputfolder,1007,Slant=True,Precision="Simple")
    g = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus')

    #and the all charged
    table=AiresInfo.GetLongitudinalTable(inputfolder,1291,Slant=True,Precision="Simple")
    h = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nall_charged')

    #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
    AstropyTable = Table(data=(a,b,c,d,e,f,g,h))
    filename=Task+"consolidated.hdf5"
    AstropyTable.write(filename, path=Task+"/NLongitudinalProfile", format="hdf5", append=True, compression=True,serialize_meta=True)



    ##############################################################################################################################
    # Energy LONGITUDINAL TABLES
    ##############################################################################################################################

    #the gammas
    table=AiresInfo.GetLongitudinalTable(inputfolder,1501,Slant=True,Precision="Simple")
    a = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='SlantDepth')
    c = Column(data=table.T[1],unit=u.GeV,name='Egamma')

    #i call the eplusminus table, in vertical, to store also the vertical depth
    table=AiresInfo.GetLongitudinalTable(inputfolder,1705,Slant=False,Precision="Simple")
    b = Column(data=table.T[0],unit=u.g/(u.cm*u.cm),name='VerticalDepth')
    d = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ee_plus_minus')

    table=AiresInfo.GetLongitudinalTable(inputfolder,1506,Slant=True,Precision="Simple")
    e = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ee_plus')

    #the mu plus mu minus
    table=AiresInfo.GetLongitudinalTable(inputfolder,1707,Slant=True,Precision="Simple")
    f = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Emu_plus_minus')

    #the mu plus
    table=AiresInfo.GetLongitudinalTable(inputfolder,1507,Slant=True,Precision="Simple")
    g = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Emu_plus')

    #and the all charged
    table=AiresInfo.GetLongitudinalTable(inputfolder,1791,Slant=True,Precision="Simple")
    h = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Eall_charged')

    #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
    AstropyTable = Table(data=(a,b,c,d,e,f,g,h))
    filename=Task+"consolidated.hdf5"
    AstropyTable.write(filename, path=Task+"/ELongitudinalProfile", format="hdf5", append=True, compression=True,serialize_meta=True)


    ################################################################################################################################
    # NLowEnergy Longitudinal development
    #################################################################################################################################

    ################################################################################################################################
    # ELowEnergy Longitudinal development
    #################################################################################################################################

    ################################################################################################################################
    # EnergyDeposit Longitudinal development
    #################################################################################################################################


    ################################################################################################################################
    # Lateral Tables
    #################################################################################################################################

    #the gammas
    table=AiresInfo.GetLateralTable(inputfolder,2001,Density=False,Precision="Simple")
    a = Column(data=table.T[0],unit=u.m,name='Distance')
    b = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ngamma')

    table=AiresInfo.GetLateralTable(inputfolder,2205,Density=False,Precision="Simple")
    c = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus_minus')

    table=AiresInfo.GetLateralTable(inputfolder,2006,Density=False,Precision="Simple")
    d = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus')

    table=AiresInfo.GetLateralTable(inputfolder,2207,Density=False,Precision="Simple")
    e = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus_minus')

    table=AiresInfo.GetLateralTable(inputfolder,2007,Density=False,Precision="Simple")
    f = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus')

    table=AiresInfo.GetLateralTable(inputfolder,2291,Density=False,Precision="Simple")
    g = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nall_charged')

    #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
    AstropyTable = Table(data=(a,b,c,d,e,f,g))
    filename=Task+"consolidated.hdf5"
    AstropyTable.write(filename, path=Task+"/NLateralProfile", format="hdf5", append=True, compression=True,serialize_meta=True)


    ################################################################################################################################
    # Energy Distribution at ground Tables
    #################################################################################################################################

    #the gammas
    table=AiresInfo.GetLateralTable(inputfolder,2501,Density=False,Precision="Simple")
    a = Column(data=table.T[0],unit=u.m,name='Distance')
    b = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ngamma')

    table=AiresInfo.GetLateralTable(inputfolder,2705,Density=False,Precision="Simple")
    c = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus_minus')

    table=AiresInfo.GetLateralTable(inputfolder,2506,Density=False,Precision="Simple")
    d = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Ne_plus')

    table=AiresInfo.GetLateralTable(inputfolder,2707,Density=False,Precision="Simple")
    e = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus_minus')

    table=AiresInfo.GetLateralTable(inputfolder,2507,Density=False,Precision="Simple")
    f = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nmu_plus')

    table=AiresInfo.GetLateralTable(inputfolder,2791,Density=False,Precision="Simple")
    g = Column(data=table.T[1],unit=u.dimensionless_unscaled,name='Nall_charged')

    #this might get to the hdf5io (later, it should be a method that adds individual tables as a new column, one at time, to make it easier later to add new columns)
    AstropyTable = Table(data=(a,b,c,d,e,f,g))
    filename=Task+"consolidated.hdf5"
    AstropyTable.write(filename, path=Task+"/EGround", format="hdf5", append=True, compression=True,serialize_meta=True)








    #idea: Guardar: Gamma, e- , e+/e-,mu-,mu+/mu-,alcharged,hadronsw,nuclei





