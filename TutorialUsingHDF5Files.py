import matplotlib.pyplot as plt
import hdf5fileinout as hdf5io
################################################################################
# Test of Matias functions for simulation and hdf5 files handling (Valentin)
################################################################################

#Shower path
simu_path = './Voltage-Stshp_TheTestInput17-85.hdf5'
InputFilename = simu_path

#Shower event access
RunInfo = hdf5io.GetRunInfo(InputFilename)
print("#RunInfo --> ", RunInfo)
NumberOfEvents = hdf5io.GetNumberOfEvents(RunInfo)
print("#NumberOfEvents --> ", NumberOfEvents)
EventNumber = NumberOfEvents-1
EventName = hdf5io.GetEventName(RunInfo,EventNumber)
print("#EventName --> ", EventName)

print("******")
print("Press Enter")
input()
print("******")

#All simulations info
ShowerSimInfo = hdf5io.GetShowerSimInfo(InputFilename,EventName)
print("#ShowerSimInfo --> ", ShowerSimInfo)
#CPUTime = hdf5io.GetCPUTime(ShowerSimInfo)                                     #needs latest simulated events
#print("#CPUTime --> ", CPUTime)

print("******")
print("Press Enter")
input()
print("******")

#Additional simulation parameters
SignalSimInfo = hdf5io.GetSignalSimInfo(InputFilename,EventName)
print("#SignalSimInfo --> ", SignalSimInfo)
TimeBinSize = hdf5io.GetTimeBinSize(SignalSimInfo)
print("#TimeBinSize --> ", TimeBinSize)
TimeWindowMin = hdf5io.GetTimeWindowMin(SignalSimInfo)
print("#TimeWindowMin --> ", TimeWindowMin)
TimeWindowMin = hdf5io.GetTimeWindowMax(SignalSimInfo)
print("#TimeWindowMin --> ", TimeWindowMin)

print("******")
print("Press Enter")
input()
print("******")

#Shower parameters
Zenith = hdf5io.GetEventZenith(RunInfo,EventNumber)
print("#Zenith --> ", Zenith)
Azimuth = hdf5io.GetEventAzimuth(RunInfo,EventNumber)
print("#Azimuth --> ", Azimuth)
Primary = hdf5io.GetEventPrimary(RunInfo,EventNumber)
print("#Primary --> ", Primary)
Energy = hdf5io.GetEventEnergy(RunInfo,EventNumber)
print("#Energy --> ", Energy)
XmaxDistance = hdf5io.GetEventXmaxDistance(RunInfo,EventNumber)
print("#XmaxDistance --> ", XmaxDistance)
SlantXmax = hdf5io.GetEventSlantXmax(RunInfo,EventNumber)
print("#SlantXmax --> ", SlantXmax)
Energy = hdf5io.GetEventEnergy(RunInfo,EventNumber)
print("#Energy --> ", Energy)
HadronicModel = hdf5io.GetEventHadronicModel(RunInfo,EventNumber)
print("#HadronicModel --> ", HadronicModel)

print("******")
print("Press Enter")
input()
print("******")

#Shower info
EventInfo = hdf5io.GetEventInfo(InputFilename,EventName)
print("#EventInfo --> ", EventInfo)
BFieldIncl = hdf5io.GetEventBFieldIncl(EventInfo)
print("#BFieldIncl --> ", BFieldIncl)
BFieldDecl = hdf5io.GetEventBFieldDecl(EventInfo)
print("#BFieldDecl --> ", BFieldDecl)
GroundAltitude = hdf5io.GetGroundAltitude(EventInfo)
print("#GroundAltitude --> ", GroundAltitude)

print("******")
print("Press Enter")
input()
print("******")

#Antannas info
AntennaInfo = hdf5io.GetAntennaInfo(InputFilename,EventName)
print("#AntennaInfo --> ", AntennaInfo)
AntennaInfoMeta = AntennaInfo.meta
print("#AntennaInfoMeta --> ", AntennaInfoMeta)
IDs = AntennaInfo['ID'].data
print("#IDs --> ", IDs)
# AntennaInfo4 = hdf5io.GetAntennaInfo4(InputFilename,EventName)                #needs the table written
# print("#AntennaInfo4 --> ", AntennaInfo4)
NumberOfAntennas = hdf5io.GetNumberOfAntennas(AntennaInfo)
print("#NumberOfAntennas --> ", NumberOfAntennas)
IDs_bis = hdf5io.GetAntIDFromAntennaInfo(AntennaInfo)
print("#IDs_bis --> ", IDs_bis)
X = hdf5io.GetXFromAntennaInfo(AntennaInfo)
print("#X --> ", X)
Y = hdf5io.GetYFromAntennaInfo(AntennaInfo)
print("#Y --> ", Y)
Z = hdf5io.GetZFromAntennaInfo(AntennaInfo)
print("#Z --> ", Z)
Positions = hdf5io.GetAntennaPositions(AntennaInfo)
print("#Positions --> ", Positions)

print("******")
print("Press Enter")
input()
print("******")

#One antenna info
AntennaNumber = 12
Position = hdf5io.GetAntennaPosition(AntennaInfo,AntennaNumber)
print("#Position --> ", Position)
Slope = hdf5io.GetAntennaSlope(AntennaInfo,AntennaNumber)
print("#Slope --> ", Slope)
AntennaInfo_bis = hdf5io.GetAntennaInfoFromEventInfo(EventInfo,0)
print("#AntennaInfo_bis --> ", AntennaInfo_bis)

print("******")
print("Press Enter")
input()
print("******")

#Traces
AntennaID = IDs_bis[0]
Efield_trace = hdf5io.GetAntennaEfield(InputFilename,EventName,AntennaID,OutputFormat="numpy")
print("See plots at the end")
Voltages_trace = hdf5io.GetAntennaVoltage(InputFilename,EventName,AntennaID,OutputFormat="numpy")
print("See plots at the end")
Filtered_trace = hdf5io.GetAntennaFilteredVoltage(InputFilename,EventName,AntennaID,OutputFormat="numpy")
print("See plots at the end")

# Slopes = hdf5io.GetSlopesFromTrace(Trace)                                     #no yet working
# print("Second methode for getting the slopes of the antenna (from meta of Table)")
# print("#Slopes --> ", Slopes)

print("******")
print("Press Enter")
input()
print("******")

# P2PInfo = hdf5io.GetAntennaP2PInfo(InputFilename,EventName)                   #needs tha table already written
# print("#P2PInfo --> ", P2PInfo)
p2p = hdf5io.get_p2p_hdf5(InputFilename,antennamax='All',antennamin=0,usetrace='efield')
print("#p2p --> ", p2p)
peaktime, peakamplitude = hdf5io.get_peak_time_hilbert_hdf5(InputFilename, antennamax="All",antennamin=0, usetrace="efield", DISPLAY=False)
print("#peak time hilbert --> ", peaktime)
print("#peak amplitude hilbert --> ", peakamplitude)

print("******")
print("Press Enter")
input()
print("******")

#Creations/Savings
# hdf5io.CreateRunInfoMeta(RunName)
# hdf5io.CreateEventInfoMeta(RunName,EventNumber,EventInfo,ShowerSimInfo,SignalSimInfo,AntennaInfo,AntennaTraces,NLongitudinal,ELongitudinal,NlowLongitudinal,ElowLongitudinal,EdepLongitudinal,LateralDistribution,EnergyDistribution)
# hdf5io.CreateEventInfo(EventName,Primary,Energy,Zenith,Azimuth,XmaxDistance,XmaxPosition,XmaxAltitude,SlantXmax,InjectionAltitude,GroundAltitude,Site,Date,FieldIntensity,FieldInclination,FieldDeclination,AtmosphericModel,EnergyInNeutrinos,EventInfoMeta)
# hdf5io.CreateShowerSimInfoMeta(RunName,EventName,ShowerSimulator)
# hdf5io.CreateShowerSimInfo(ShowerSimulator,HadronicModel,RandomSeed,RelativeThinning,WeightFactor,GammaEnergyCut,ElectronEnergyCut,MuonEnergyCut,MesonEnergyCut,NucleonEnergyCut,CPUTime,ShowerSimInfoMeta)
# hdf5io.CreateSignalSimInfoMeta(RunName,EventName,FieldSimulator)
# hdf5io.CreateSignalSimInfo(FieldSimulator,RefractionIndexModel,RefractionIndexParameters,TimeBinSize,TimeWindowMin,TimeWindowMax,SignalSimInfoMeta)
# hdf5io.CreatAntennaInfoMeta(RunName,EventName,VoltageSimulator="N/A",AntennaModel="N/A",EnvironmentNoiseSimulator="N/A",ElectronicsSimulator="N/A",ElectronicsNoiseSimulator="N/A")
# hdf5io.CreateAntennaInfo(IDs, antx, anty, antz, slopeA, slopeB, AntennaInfoMeta, P2Pefield=None,P2Pvoltage=None,P2Pfiltered=None,HilbertPeak=None,HilbertPeakTime=None)
# hdf5io.CreateAntennaP2PInfo(IDs, AntennaInfoMeta, P2Pefield=None,P2Pvoltage=None,P2Pfiltered=None,HilbertPeakE=None,HilbertPeakV=None,HilbertPeakFV=None,HilbertPeakTimeE=None,HilbertPeakTimeV=None,HilbertPeakTimeFV=None)
# hdf5io.CreateEfieldTable(efield, EventName, EventNumber, AntennaID, AntennaNumber,FieldSimulator, info={})
# hdf5io.CreateVoltageTable(voltage, EventName, EventNumber, AntennaID, AntennaNumber, VoltageSimulator, info={})
#
# hdf5io.SaveEfieldTable(outputfilename,EventName,antennaID,efield)
# hdf5io.SaveVoltageTable(outputfilename,EventName,antennaID,voltage)
# hdf5io.SaveFilteredVoltageTable(outputfilename,EventName,antennaID,filteredvoltage)

################################################################################
#PLOTS exemples
fa, ax = plt.subplots()
ax.plot(Efield_trace.T[0,:], Efield_trace.T[1,:], label='X-channel')
ax.plot(Efield_trace.T[0,:], Efield_trace.T[2,:], label='Y-channel')
ax.plot(Efield_trace.T[0,:], Efield_trace.T[3,:], label='Z-channel')
ax.set_xlabel(r"$\rm time\ (ns)$")
ax.set_ylabel(r"$\rm \vec{E}\ (\mu V/m)$")
ax.set_title(r"$\rm Electric-field\ trace$")
ax.legend()

fb, bx = plt.subplots()
bx.plot(Voltages_trace.T[0,:], Voltages_trace.T[1,:], label='X-channel')
bx.plot(Voltages_trace.T[0,:], Voltages_trace.T[2,:], label='Y-channel')
bx.plot(Voltages_trace.T[0,:], Voltages_trace.T[3,:], label='Z-channel')
bx.set_xlabel(r"$\rm time\ (ns)$")
bx.set_ylabel(r"$\rm V\ (\mu V)$")
bx.set_title(r"$\rm voltage\ trace$")
bx.legend()

fc, cx = plt.subplots()
cx.plot(Filtered_trace.T[0,:], Filtered_trace.T[1,:], label='X-channel')
cx.plot(Filtered_trace.T[0,:], Filtered_trace.T[2,:], label='Y-channel')
cx.plot(Filtered_trace.T[0,:], Filtered_trace.T[3,:], label='Z-channel')
cx.set_xlabel(r"$\rm time\ (ns)$")
cx.set_ylabel(r"$\rm V (\mu V)$")
cx.set_title(r"$\rm Filtered\ voltage\ trace$")
cx.legend()

fd, dx = plt.subplots()
dx.scatter(peaktime, peakamplitude)
dx.set_xlabel(r"$\rm Peak\ time\ (ns)$")
dx.set_ylabel(r"$\rm Peak\ amplitude\ (\mu V/m)$")
dx.set_title(r"$\rm Electric-field$")

plt.show()
