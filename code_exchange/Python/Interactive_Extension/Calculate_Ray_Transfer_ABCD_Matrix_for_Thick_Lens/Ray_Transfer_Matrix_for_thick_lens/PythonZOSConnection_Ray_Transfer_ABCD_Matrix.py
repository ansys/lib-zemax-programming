import clr, os, winreg
from itertools import islice

# This boilerplate requires the 'pythonnet' module.
# The following instructions are for installing the 'pythonnet' module via pip:
#    1. Ensure you are running Python 3.4, 3.5, 3.6, or 3.7. PythonNET does not work with Python 3.8 yet.
#    2. Install 'pythonnet' from pip via a command prompt (type 'cmd' from the start menu or press Windows + R and type 'cmd' then enter)
#
#        python -m pip install pythonnet

# determine the Zemax working directory
aKey = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), r"Software\Zemax", 0, winreg.KEY_READ)
zemaxData = winreg.QueryValueEx(aKey, 'ZemaxRoot')
print(zemaxData)
NetHelper = os.path.join(os.sep, zemaxData[0], r'ZOS-API\Libraries\ZOSAPI_NetHelper.dll')
winreg.CloseKey(aKey)
print(NetHelper)

# add the NetHelper DLL for locating the OpticStudio install folder
clr.AddReference(NetHelper)
import ZOSAPI_NetHelper

pathToInstall = ''
# uncomment the following line to use a specific instance of the ZOS-API assemblies
#pathToInstall = r'C:\Program Files\Zemax OpticStudio'
print(pathToInstall)

# connect to OpticStudio
success = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(pathToInstall);

zemaxDir = ''
print('Path',zemaxDir)
if success:
    zemaxDir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory();
    print('Found OpticStudio at:   %s' + zemaxDir);
else:
    raise Exception('Cannot find OpticStudio')

# load the ZOS-API assemblies
clr.AddReference(os.path.join(os.sep, zemaxDir, r'ZOSAPI.dll'))
clr.AddReference(os.path.join(os.sep, zemaxDir, r'ZOSAPI_Interfaces.dll'))
import ZOSAPI

TheConnection = ZOSAPI.ZOSAPI_Connection()
if TheConnection is None:
    raise Exception("Unable to intialize NET connection to ZOSAPI")

TheApplication = TheConnection.ConnectAsExtension(0)
if TheApplication is None:
    raise Exception("Unable to acquire ZOSAPI application")

if TheApplication.IsValidLicenseForAPI == False:
    raise Exception("License is not valid for ZOSAPI use.  Make sure you have enabled 'Programming > Interactive Extension' from the OpticStudio GUI.")

TheSystem = TheApplication.PrimarySystem
if TheSystem is None:
    raise Exception("Unable to acquire Primary system")

def reshape(data, x, y, transpose = False):
    """Converts a System.Double[,] to a 2D list for plotting or post processing
    
    Parameters
    ----------
    data      : System.Double[,] data directly from ZOS-API 
    x         : x width of new 2D list [use var.GetLength(0) for dimension]
    y         : y width of new 2D list [use var.GetLength(1) for dimension]
    transpose : transposes data; needed for some multi-dimensional line series data
    
    Returns
    -------
    res       : 2D list; can be directly used with Matplotlib or converted to
                a numpy array using numpy.asarray(res)
    """
    if type(data) is not list:
        data = list(data)
    var_lst = [y] * x;
    it = iter(data)
    res = [list(islice(it, i)) for i in var_lst]
    if transpose:
        return self.transpose(res);
    return res
    
def transpose(data):
    """Transposes a 2D list (Python3.x or greater).  
    
    Useful for converting mutli-dimensional line series (i.e. FFT PSF)
    
    Parameters
    ----------
    data      : Python native list (if using System.Data[,] object reshape first)    
    
    Returns
    -------
    res       : transposed 2D list
    """
    if type(data) is not list:
        data = list(data)
    return list(map(list, zip(*data)))

print('Connected to OpticStudio')

# The connection should now be ready to use.  For example:
print('Serial #: ', TheApplication.SerialCode)

# Insert Code Here
# Setup  
testFile =r"C:\test\ABCD\ABCD Simple_lens1.zmx"
TheSystem.LoadFile(testFile,False)
test = str(TheSystem.GetCurrentStatus())
print(test)
     # Merit functions
TheMFE = TheSystem.MFE
Operand_1 = TheMFE.GetOperandAt(1)
Operand_2 = TheMFE.GetOperandAt(2)
Operand_3 = TheMFE.GetOperandAt(3)
Operand_4 = TheMFE.GetOperandAt(4)
Operand_5 = TheMFE.GetOperandAt(5)
Operand_6 = TheMFE.GetOperandAt(6)
Operand_7 = TheMFE.GetOperandAt(7)
Operand_8 = TheMFE.GetOperandAt(8)

Y1=Operand_1.Value
Theta1=Operand_3.Value
Y2=Operand_2.Value
Theta2=Operand_4.Value
Y1_p=Operand_5.Value
Theta1_p=Operand_7.Value
Y2_p=Operand_6.Value
Theta2_p=Operand_8.Value

print("Y1 =",Y1)
print("Theta1 =",Theta1)
print("Y2 =",Y2)
print("Theta2 =",Theta2)
print("Y1_p =",Y1_p)
print("Theta1_p =",Theta1_p)
print("Y2_p =",Y2_p)
print("Theta2_p =",Theta2_p,"\n")

#ABCD Matrix Calculation
A=(Y2_p/Y2-Y1_p*Theta2/Y2/Theta1)/(1-Y1*Theta2/Y2/Theta1)
B=(Y1_p-A*Y1)/Theta1
D=(Theta2_p-Y2/Y1*Theta1_p)/(Theta2-Theta1*Y2/Y1)
C=(Theta1_p-D*Theta1)/Y1

import numpy as np
ABCD=np.matrix([[A,B],[C,D]])
print("ABCD Matrix = ",ABCD,"\n")

print("A =",A,"\n")
print("B =",B,"\n")
print("C =",C,"\n")
print("D =",D,"\n")

#Effective Focal Length
EFL = -1/C
print("EFL =",EFL,"\n")
