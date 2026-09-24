import clr, os, winreg
from itertools import islice
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

class PythonStandaloneApplication(object):
    class LicenseException(Exception):
        pass
    class ConnectionException(Exception):
        pass
    class InitializationException(Exception):
        pass
    class SystemNotPresentException(Exception):
        pass

    def __init__(self, path=None):
        # determine location of ZOSAPI_NetHelper.dll & add as reference
        aKey = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), r"Software\Zemax", 0, winreg.KEY_READ)
        zemaxData = winreg.QueryValueEx(aKey, 'ZemaxRoot')
        NetHelper = os.path.join(os.sep, zemaxData[0], r'ZOS-API\Libraries\ZOSAPI_NetHelper.dll')
        winreg.CloseKey(aKey)
        clr.AddReference(NetHelper)
        import ZOSAPI_NetHelper
        
        # Find the installed version of OpticStudio
        if path is None:
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize()
        else:
            # Note -- uncomment the following line to use a custom initialization path
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(path)
        
        # determine the ZOS root directory
        if isInitialized:
            dir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
        else:
            raise PythonStandaloneApplication.InitializationException("Unable to locate Zemax OpticStudio.  Try using a hard-coded path.")

        # add ZOS-API referencecs
        clr.AddReference(os.path.join(os.sep, dir, "ZOSAPI.dll"))
        clr.AddReference(os.path.join(os.sep, dir, "ZOSAPI_Interfaces.dll"))
        import ZOSAPI

        # create a reference to the API namespace
        self.ZOSAPI = ZOSAPI

        # create a reference to the API namespace
        self.ZOSAPI = ZOSAPI

        # Create the initial connection class
        self.TheConnection = ZOSAPI.ZOSAPI_Connection()

        if self.TheConnection is None:
            raise PythonStandaloneApplication.ConnectionException("Unable to initialize .NET connection to ZOSAPI")

        self.TheApplication = self.TheConnection.CreateNewApplication()
        if self.TheApplication is None:
            raise PythonStandaloneApplication.InitializationException("Unable to acquire ZOSAPI application")

        if self.TheApplication.IsValidLicenseForAPI == False:
            raise PythonStandaloneApplication.LicenseException("License is not valid for ZOSAPI use")

        self.TheSystem = self.TheApplication.PrimarySystem
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException("Unable to acquire Primary system")

    def __del__(self):
        if self.TheApplication is not None:
            self.TheApplication.CloseApplication()
            self.TheApplication = None
        
        self.TheConnection = None
    
    def OpenFile(self, filepath, saveIfNeeded):
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException("Unable to acquire Primary system")
        self.TheSystem.LoadFile(filepath, saveIfNeeded)

    def CloseFile(self, save):
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException("Unable to acquire Primary system")
        self.TheSystem.Close(save)

    def SamplesDir(self):
        if self.TheApplication is None:
            raise PythonStandaloneApplication.InitializationException("Unable to acquire ZOSAPI application")

        return self.TheApplication.SamplesDir

    def ExampleConstants(self):
        if self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.PremiumEdition:
            return "Premium"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusTypeProfessionalEdition:
            return "Professional"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusTypeStandardEdition:
            return "Standard"
        else:
            return "Invalid"
    
    def reshape(self, data, x, y, transpose = False):
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
    
    def transpose(self, data):
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

if __name__ == '__main__':
    zos = PythonStandaloneApplication()
    
    # ===== Set up =====
    obj_num = 2
    face_num = [4]
    # ===== End of Set up =====

    # TODO: check if obj and face num is valid

    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    file_name, file_ext = os.path.splitext(filepath)

    if file_ext.lower() != '.zrd':
        print('The selected file it not with .zrd as the extension filename.')
        exit()

    # load local variables
    ZOSAPI = zos.ZOSAPI
    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem
    TheSystem.MakeNonSequential()

    ZRDReader = TheSystem.Tools.OpenRayDatabaseReader()
    ZRDReader.ZRDFile = filepath
    
    ZRDReader.RunAndWaitForCompletion()
    if ZRDReader.Succeeded == 0:
        print('Open ZRD failed!\n')
        print(ZRDReader.ErrorMessage)
        ZRDReader.Close()
        exit()
    else:
        print('Open ZRD success!\n')
        
    datapoints = []
    ZRDResult = ZRDReader.GetResults()
    success_NextResult, rayNumber, waveIndex, wlUM, numSegments = ZRDResult.ReadNextResult(0, 0, 0, 0)
    while success_NextResult == True:
        segdata = ZRDResult.ReadNextSegmentFull(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24, 25, 26, 27, 28, 29)
        while segdata[0] == True:
            onum = segdata[3]
            fnum = segdata[4]
            x = segdata[7]
            y = segdata[8]
            z = segdata[9]
            if onum == obj_num and fnum in face_num:
                datapoints.append([x,y,z])

            segdata = ZRDResult.ReadNextSegmentFull(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24, 25, 26, 27, 28, 29)
        success_NextResult, rayNumber, waveIndex, wlUM, numSegments = ZRDResult.ReadNextResult(0, 0, 0, 0)
        
    ZRDReader.Close()

    if (len(datapoints) == 0):
        print('Cannot find any ray hitting object ' + str(obj_num) + ' and face ' + ' '.join(str(e) + ' ' for e in face_num))
    print('Totally ' + str(len(datapoints)) + ' detected!')

    # Export text
    with open(file_name + '_raw_data.txt', 'w') as f:
        f.write('Target object: %d\n' % obj_num)
        f.write('Target face: ' + ' '.join(str(e) for e in face_num) + '\n')
        for point in datapoints:
            f.write(' '.join(str(e) for e in point) + '\n')
    print('Data point exported.')
    
    npdata = np.array(datapoints)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(npdata[:,0],npdata[:,1],npdata[:,2],marker='o')
    plt.show()

    # Fitting system
    TheSystem2 = TheApplication.CreateNewSystem(ZOSAPI.SystemType.Sequential);
    TheSystemData = TheSystem2.SystemData;
    TheSystemData.Aperture.ApertureValue = 2

    TheLDE = TheSystem2.LDE
    TheLDE.InsertNewSurfaceAt(2)
    surf2 = TheLDE.GetSurfaceAt(2)
    SurfaceType_CB = surf2.GetSurfaceTypeSettings(ZOSAPI.Editors.LDE.SurfaceType.CoordinateBreak);
    surf2.ChangeType(SurfaceType_CB);
    surf2.ThicknessCell.MakeSolveVariable()
    surf2.GetSurfaceCell(ZOSAPI.Editors.LDE.SurfaceColumn.Par1).MakeSolveVariable() # Decenter X
    surf2.GetSurfaceCell(ZOSAPI.Editors.LDE.SurfaceColumn.Par2).MakeSolveVariable() # Decenter Y
    surf2.GetSurfaceCell(ZOSAPI.Editors.LDE.SurfaceColumn.Par3).MakeSolveVariable() # Tilt X
    surf2.GetSurfaceCell(ZOSAPI.Editors.LDE.SurfaceColumn.Par4).MakeSolveVariable() # Tilt Y

    TheMFE = TheSystem2.MFE
    for point in datapoints:
        TheMFE.InsertNewOperandAt(1)
        TheMFE.GetOperandAt(1).ChangeType(ZOSAPI.Editors.MFE.MeritOperandType.RAGZ)
        TheMFE.GetOperandAt(1).GetOperandCell (ZOSAPI.Editors.MFE.MeritColumn.Param1).Value = str(3)
        TheMFE.GetOperandAt(1).GetOperandCell (ZOSAPI.Editors.MFE.MeritColumn.Param2).Value = str(1)
        TheMFE.GetOperandAt(1).GetOperandCell (ZOSAPI.Editors.MFE.MeritColumn.Param3).DoubleValue = 0.0
        TheMFE.GetOperandAt(1).GetOperandCell (ZOSAPI.Editors.MFE.MeritColumn.Param4).DoubleValue = 0.0
        TheMFE.GetOperandAt(1).GetOperandCell (ZOSAPI.Editors.MFE.MeritColumn.Param5).DoubleValue = point[0]
        TheMFE.GetOperandAt(1).GetOperandCell (ZOSAPI.Editors.MFE.MeritColumn.Param6).DoubleValue = point[1]
        TheMFE.GetOperandAt(1).GetOperandCell (ZOSAPI.Editors.MFE.MeritColumn.Target).DoubleValue = point[2]
        TheMFE.GetOperandAt(1).GetOperandCell (ZOSAPI.Editors.MFE.MeritColumn.Weight).DoubleValue = 1.0
        

    TheSystem2.SaveAs(file_name + '_fitting.zos')
    print('Fitting system exported.')
