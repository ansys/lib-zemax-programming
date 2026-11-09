import clr, os, winreg
from itertools import islice
import random
from System import Enum, Int32, Double
import numpy as np
import time
 
# This boilerplate requires the 'pythonnet' module.
# The following instructions are for installing the 'pythonnet' module via pip:
#    1. Ensure you are running a Python version compatible with PythonNET. Check the article "ZOS-API using Python.NET" or
#    "Getting started with Python" in our knowledge base for more details.
#    2. Install 'pythonnet' from pip via a command prompt (type 'cmd' from the start menu or press Windows + R and type 'cmd' then enter)
#
#        python -m pip install pythonnet

# determine the Zemax working directory
aKey = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), r"Software\Zemax", 0, winreg.KEY_READ)
zemaxData = winreg.QueryValueEx(aKey, 'ZemaxRoot')
NetHelper = os.path.join(os.sep, zemaxData[0], r'ZOS-API\Libraries\ZOSAPI_NetHelper.dll')
winreg.CloseKey(aKey)

# add the NetHelper DLL for locating the OpticStudio install folder
clr.AddReference(NetHelper)
import ZOSAPI_NetHelper

# Note: you may need to adjust this line to your ZOS installation directory
pathToInstall = r'C:\Program Files\ANSYS Inc\v251\Zemax OpticStudio'

# connect to OpticStudio
success = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(pathToInstall);

zemaxDir = ''
if success:
    zemaxDir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory();
    print('Found OpticStudio at:   %s' + zemaxDir);
else:
    raise Exception('Cannot find OpticStudio')

# load the ZOS-API assemblies
clr.AddReference(os.path.join(os.sep, zemaxDir, r'ZOSAPI.dll'))
clr.AddReference(os.path.join(os.sep, zemaxDir, r'ZOSAPI_Interfaces.dll'))
import ZOSAPI

def establish_zosapi_connection():
    theConnection = ZOSAPI.ZOSAPI_Connection()
    if theConnection is None:
        raise Exception("Unable to intialize NET connection to ZOSAPI")

    theApplication = theConnection.ConnectAsExtension(0)
    if theApplication is None:
        raise Exception("Unable to acquire ZOSAPI application")

    if theApplication.IsValidLicenseForAPI == False:
        raise Exception("License is not valid for ZOSAPI use.  Make sure you have enabled 'Programming > Interactive Extension' from the OpticStudio GUI.")

    theSystem = theApplication.PrimarySystem
    if theSystem is None:
        raise Exception("Unable to acquire Primary system")

    print('Connected to OpticStudio')

    # The connection should now be ready to use.  For example:
    print('Serial #: ', theApplication.SerialCode)

    return theApplication

def get_random_circle_coords(R):
    # random r and theta
    length = np.random.uniform(0, R)
    angle = np.pi * np.random.uniform(0, 2)
    # convert to cartesian, using sqrt(r)
    x = np.sqrt(length) * np.cos(angle)
    y = np.sqrt(length) * np.sin(angle)
    return x,y

def get_dimension_flag(theSystem):
    units = theSystem.SystemData.Units.LensUnits
    if units == ZOSAPI.SystemData.ZemaxSystemUnits.Meters:
        dimensionFlag = 0
    elif units == ZOSAPI.SystemData.ZemaxSystemUnits.Inches:
        dimensionFlag = 1
    elif units == ZOSAPI.SystemData.ZemaxSystemUnits.Centimeters:
        dimensionFlag = 2
    elif units == ZOSAPI.SystemData.ZemaxSystemUnits.Millimeters:
        dimensionFlag = 4
    else:
        dimensionFlag = 3
    
    return dimensionFlag

def initialize_ray_data(theApplication, numberOfRays, hx, hy):
    time0 = time.time()
    # for each ray, need 20 data points 
    # [0:5] = X,Y,Z,L,M,N
    # [6]   = intensity
    # [7]   = wavelength
    # [8:9] = hx, hy
    # [10:11] = px, py 
    # [12:13] = exr, exi
    # [14:15] = eyr, eyi
    # [16:17] = ezr, ezi
    # [18]  = wave number (from System Explorer)
    # [19] = ray vignetted? (1=yes)
    rayData = np.zeros((numberOfRays, 20), dtype=np.float64)
    rayData[:,8] = hx*np.ones(numberOfRays)
    rayData[:,9] = hy*np.ones(numberOfRays)

    numberOfWavelengths = theApplication.PrimarySystem.SystemData.Wavelengths.NumberOfWavelengths
    waves = []
    waveNums = []
    waveWeights = []
    for i in range(1, numberOfWavelengths+1):
        waveNums.append(i)
        waves.append(theApplication.PrimarySystem.SystemData.Wavelengths.GetWavelength(i).Wavelength)
        waveWeights.append(theApplication.PrimarySystem.SystemData.Wavelengths.GetWavelength(i).Weight)
    
    # generate the list of selected wavelength indices
    rayData[:,18] = random.choices(population=waveNums, weights=waveWeights, k=numberOfRays)

    for i in range(0, numberOfRays):
        # get the wavelength from wave index
        rayData[i,7] = waves[int(rayData[i,18] - 1)]

        # choose random pupil coordinates 
        px, py = get_random_circle_coords(1)
        rayData[i, 10] = px
        rayData[i, 11] = py

    print("completed in " + str(round(time.time()-time0, 2)) + " sec")
    return rayData

def generate_raydata(theApplication, rayData, targetSurfNum, targetSurfOffset, numberOfRays):
    time0 = time.time()
    # operate on a copy of the optical system
    theSystem = theApplication.PrimarySystem.CopySystem()
    errorRays = 0

    # set up the target surface
    dummySurf = theSystem.LDE.InsertNewSurfaceAt(targetSurfNum)
    targetSurf = theSystem.LDE.InsertNewSurfaceAt(targetSurfNum+1)
    dummySurf.Thickness = -1 * targetSurfOffset
    targetSurf.Thickness = targetSurfOffset

    # initialize the batch ray trace
    # initializing as (Jx, Jy, Phasex, Phasey)=0 will run "unpolarized" ray trace
    # (i.e. traces two orthogonal polarizations, and takes average)
    batchRayTrace = theSystem.Tools.OpenBatchRayTrace()
    normPolData = batchRayTrace.CreateNormPol(numberOfRays, ZOSAPI.Tools.RayTrace.RaysType.Real, 
                                              0, 0, 0, 0, targetSurf.SurfaceNumber)
    for i in range(0, numberOfRays):
        # add the chosen ray to the batch
        normPolData.AddRay(int(rayData[i,18]), rayData[i,8], rayData[i,9], rayData[i,10], rayData[i, 11], 
                           rayData[i, 12], rayData[i,13], rayData[i,14], rayData[i,15], rayData[i, 16], rayData[i, 17])

    # run the batch ray trace
    batchRayTrace.RunAndWaitForCompletion()

    # retrieve the ray data on image plane for each ray
    normPolData.StartReadingResults()
                
    # Python NET requires all arguments to be passed in as reference, so need to have placeholders
    sysInt = Int32(1)
    sysDbl = Double(1.0)

    # read the result data for the first ray
    # output[0] will be a bool, telling us if the ray read successfully
    # output[1:end] values are as follows:
    # raynum, errorcode, X, Y, Z, L, M, N, exr, exi, eyr, eyi, ezr, ezi, intensity
    output = normPolData.ReadNextResultFull(sysInt, sysInt, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, 
                                            sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl)
    i = 0
    while output[0]:  # success
        if (output[2] != 0):
            # the ray encountered an error
            errorRays = errorRays + 1
        else:
            # get the ray data on image plane for this ray
            rayData[i,0] = output[3] # X
            rayData[i,1] = output[4] # Y
            rayData[i,2] = output[5] - targetSurfOffset # Z
            rayData[i,3] = output[6] # L
            rayData[i,4] = output[7] # M
            rayData[i,5] = output[8] # N
            #rayData[i,12] = output[9] # Exr
            #rayData[i,13] = output[10] # Exi
            #rayData[i,14] = output[11] # Eyr
            #rayData[i,15] = output[12] # Eyi
            #rayData[i,16] = output[13] # Ezr
            #rayData[i,17] = output[14] # Ezi
            rayData[i,6] = output[15] # Intensity
        i = i + 1

        # read the next ray
        output = normPolData.ReadNextResultFull(sysInt, sysInt, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, 
                                            sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl)

    # close tool
    batchRayTrace.Close()

    # remove entries with unrecorded ray data (i.e. error/vignetted rays)
    mask = (rayData[:,6] > 0)
    rayData = rayData[mask]

    theSystem.Close(False)

    print("completed in " + str(round(time.time()-time0, 2)) + " sec")
    return rayData, errorRays

def check_vignetting(theApplication, rayData, targetSurfNum, numberOfRays):
    # runs an unpol batch ray trace, to check for ray vignetting
    time0 = time.time()
    # operate on a copy of the optical system
    theSystem = theApplication.PrimarySystem.CopySystem()

    # initialize the batch ray trace
    batchRayTrace = theSystem.Tools.OpenBatchRayTrace()
    normUnpolData = batchRayTrace.CreateNormUnpol(numberOfRays, ZOSAPI.Tools.RayTrace.RaysType.Real, targetSurfNum)
    for i in range(0, numberOfRays):
        # add the chosen ray to the batch
        # wave#, hx, hy, px, py, raytype
        normUnpolData.AddRay(int(rayData[i,18]), rayData[i,8], rayData[i,9], rayData[i,10], rayData[i, 11], Enum.Parse(ZOSAPI.Tools.RayTrace.OPDMode, "None"))

    # run the batch ray trace
    batchRayTrace.RunAndWaitForCompletion()

    # retrieve the ray data on image plane for each ray
    normUnpolData.StartReadingResults()
                
    # Python NET requires all arguments to be passed in as reference, so need to have placeholders
    sysInt = Int32(1)
    sysDbl = Double(1.0)

    # read the result data for the first ray
    # output[0] will be a bool, telling us if the ray read successfully
    # output[1:end] values are as follows:
    # raynum, errorcode, vignettecode, X, Y, Z, L, M, N, l2, m2, n2, opd, intensity
    output = normUnpolData.ReadNextResult(sysInt, sysInt, sysInt,
                    sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl)
    i = 0
    while output[0]:  # success
        # check if ray was vignetted
        if output[3] != 0:
            rayData[i,19] = 1
        i = i+1
    
        # read the next ray
        output = normUnpolData.ReadNextResult(sysInt, sysInt, sysInt,
                    sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl, sysDbl)

    # close tool
    batchRayTrace.Close()

    # remove entries with vignetted ray data (i.e. error/vignetted rays)
    mask = (rayData[:,19] < 1)
    rayData = rayData[mask]

    theSystem.Close(False)

    print("completed in " + str(round(time.time()-time0, 2)) + " sec")
    return rayData, np.size(rayData, 0), numberOfRays - np.size(rayData, 0)
