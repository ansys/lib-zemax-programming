from ansys_optical_automation.interop_process import rayfile_converter
import generate_raydata_pol
import write_binary_source_file
import os
import numpy as np
import sys

# ===== USER SETTINGS ===== #
hx = 0.0 # normalized field X coordinate
hy = 1.0 # normalized field Y coordinate
sourcePower = 1 # Watts; total power launched from object space
imageSurfOffset = 10 # lens units; ray start coordinates distance from image plane
numRays = 100000 # number of rays included in the sequential batch ray trace
outFile = 'Rayfile_Generate_Sample' # saves as .sdf (zemax) and as .ray (speos)
# ========================= #

# establish connection with Zemax
theApplication = generate_raydata_pol.establish_zosapi_connection()
imSurfNum = theApplication.PrimarySystem.LDE.NumberOfSurfaces - 1

# initialize data container
print("initializing random ray seeds...")
rayData = generate_raydata_pol.initialize_ray_data(theApplication, numRays, hx, hy)

# get the system dimension units
dimensionFlag = generate_raydata_pol.get_dimension_flag(theApplication.PrimarySystem)
if dimensionFlag != 4:
    # to do: add support for all lens units (current issue is on Speos .ray file generation side)
    print("\nError: Zemax lens unit are not mm \nPlease scale zemax lens to mm using Scale Lens tool\n")
    sys.exit()

# run the batch ray trace
print("running the batch ray trace...")
generate_raydata_pol.generate_raydata(theApplication, rayData, imSurfNum, imageSurfOffset, numRays)

# remove rays which will be vignetted by the system
print("analyzing ray vignetting...")
rayData, numUnvignettedRays, numVignettedRays = generate_raydata_pol.check_vignetting(theApplication, rayData, imSurfNum, numRays)

# scale so that total input power is 1 
# i.e. each ray initialized with I = sourcePower/numRays Watts 
# (default is each input ray has 1 W)
rayData[:,6] = rayData[:,6] * (sourcePower*np.ones(np.size(rayData, 0)))*(1/numRays)

# logging
print()
print("Ray file generation completed")
print("Number of rays successfully saved: " + str(np.size(rayData, 0)))
print("Total transmitted power (W): " + str(round(np.sum(rayData[:,6]), 6)))
print("Average ray transmission (%): " + str(round(100*np.average(rayData[:,6])*numRays, 6)))
#print(str(round(100*(numErrorRays/numRays), 4)) + "% of rays lost due to trace error")
print("Vignetted rays (%): " + str(round(100*(numVignettedRays/numRays), 4)))
print()

# where to save the data
outPath = theApplication.ObjectsDir + "\\Sources\\Source Files\\" + outFile
speosOutPath = outPath + '.ray'
zemaxOutPath = outPath + '.sdf'

# delete previous ray file
if os.path.exists(speosOutPath):
    os.remove(speosOutPath)
if os.path.exists(zemaxOutPath):
    os.remove(zemaxOutPath)

# write binary zemax source file (.dat or .sdf)
print("saving rays to .sdf file...")
write_binary_source_file.write_binary_source_file(rayData, zemaxOutPath, dimensionFlag)

# convert the binary source file to a speos ray file
print("saving rays to .ray file...")
convert = rayfile_converter.RayfileConverter(zemaxOutPath)
convert.zemax_to_speos()
print("")
print("ray files (*.sdf, *.ray) saved successfully to:")
print(outPath)
print("")