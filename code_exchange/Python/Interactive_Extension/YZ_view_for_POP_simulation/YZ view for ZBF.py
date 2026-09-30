import clr, os, winreg
from itertools import islice
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import numpy as np
import matplotlib.pyplot as plt

# This boilerplate requires the 'pythonnet' module.
# The following instructions are for installing the 'pythonnet' module via pip:
#    1. Ensure you are running a Python version compatible with PythonNET. Check the article "ZOS-API using Python.NET" or
#    "Getting started with Python" in our knowledge base for more details.
#    2. Install 'pythonnet' from pip via a command prompt (type 'cmd' from the start menu or press Windows + R and type 'cmd' then enter)
#
#        python -m pip install pythonnet

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
        #if len(path) == 0:
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
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.EnterpriseEdition:
            return "Enterprise"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.ProfessionalEdition:
            return "Professional"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.StandardEdition:
            return "Standard"
        elif self.TheApplication.LicenseStatus == self.ZOSAPI.LicenseStatusType.OpticStudioHPCEdition:
            return "HPC"
        else:
            return "Invalid"
    
    def reshape(self, data, dim0, dim1, transpose = False):
        """Converts a System.Double[,] to a 2D list for plotting or post processing
        
        Parameters
        ----------
        data      : System.Double[,] data directly from ZOS-API 
        dim0      : x width of new 2D list [use var.GetLength(0) for dimension]
        dim1      : y width of new 2D list [use var.GetLength(1) for dimension]
        transpose : transposes data; needed for some multi-dimensional line series data
        
        Returns
        -------
        res       : 2D list; can be directly used with Matplotlib or converted to
                    a numpy array using numpy.asarray(res)
        """
        if type(data) is not list:
            data = list(data)
        var_lst = [dim1] * dim0
        it = iter(data)
        res = [list(islice(it, i)) for i in var_lst]
        if transpose:
            return self.transpose(res)
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

def ensure_files_in_POPDir(zbfpath):
    file_name = os.path.basename((zbfpath))
    target_path = os.path.join(TheApplication.POPDir, file_name)
    if os.path.normpath(target_path) == os.path.normpath(zbfpath):
        return target_path

    if os.path.exists(target_path):
        root = tk.Tk()
        root.withdraw()

        is_overwrite = messagebox.askyesno(
            title='File already exists',
            message=f'File {file_name} already exists in {target_path}. Overwrite?'
        )
        root.destroy()

        if not is_overwrite:
            return ''

        shutil.copy2(zbfpath, target_path)
    return target_path

if __name__ == '__main__':
    # ========= Setting =========
    d1 = 40  # mm
    d2 = 80  # mm
    samp = 31
    wave = 0.55  # um
    UseAngularSpectrumPropagator = True  # must be true
    # ===========================

    zos = PythonStandaloneApplication()

    # load local variables
    ZOSAPI = zos.ZOSAPI
    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem
    TheAnalyses = TheSystem.Analyses
    TheSystem.SystemData.Wavelengths.GetWavelength(1).Wavelength = wave
    POPDir = TheApplication.POPDir
    print('POP Dir: ' + POPDir)

    # zbfpath
    root = tk.Tk()
    root.withdraw()
    zbfpath = filedialog.askopenfilename(title="Choose the .zbf file",
                                         initialdir=POPDir,
                                         filetypes=[('Zemax Beam Files','*.zbf')])
    root.destroy()
    if not zbfpath:
        raise Exception('Invalid ZBF file.')
    print('ZBF file path: ' + zbfpath)
    zbfpath = ensure_files_in_POPDir(zbfpath)
    if not zbfpath:
        raise Exception('Cannot copy ZBF file to POP folder.')
    print('ZBF file is now in POP Dir.')
    
    # zospath and savefile
    zospath = os.path.abspath(__file__)
    zospath = os.path.dirname(zospath)
    zospath = os.path.join(zospath, 'Test System.zos')
    print('ZOS file path: ' + zospath)
    TheSystem.SaveAs(zospath)

    # create POP simulation
    POP = TheAnalyses.New_Analysis(ZOSAPI.Analysis.AnalysisIDM.PhysicalOpticsPropagation)
    POP_set1 = POP.GetSettings()
    POP_set2 = ZOSAPI.Analysis.PhysicalOptics.IAS_PhysicalOpticsPropagation(POP_set1)
    POP_set1.Reset()
    POP_set2.BeamType = ZOSAPI.Analysis.PhysicalOptics.POPBeamTypes.File
    POP_set2.BeamTypeFilename = os.path.basename(zbfpath)
    if POP_set2.BeamTypeFilename != os.path.basename(zbfpath):
        raise Exception('Set ZBF file failed.')
    print('POP set up done.')

    # Angular spectrum propagation
    TheSystem.LDE.GetSurfaceAt(1).PhysicalOpticsData.UseAngularSpectrumPropagator = UseAngularSpectrumPropagator
    print('Angular Spectrum Propagator: ' + 'Yes' if UseAngularSpectrumPropagator else 'No')

    # Start scan
    array_created = False
    iteration = 1
    for d in np.linspace(d1, d2, samp):
        TheSystem.SaveAs(zospath)
        print(f'Simulation start {iteration}/{samp} ... ', end='')
        iteration += 1
        TheSystem.LDE.GetSurfaceAt(1).Thickness = d
        POP.ApplyAndWaitForCompletion()
        POP_result = POP.GetResults().DataGrids[0]
        POP_Values = POP_result.Values
        XYview = np.array(zos.reshape(POP_Values, POP_Values.GetLength(0), POP_Values.GetLength(1)))
        XYview = XYview[np.newaxis, :]
        if not array_created:
            XYZview = XYview
            hw = POP_result.Nx * POP_result.Dx
            array_created = True
        else:
            XYZview = np.concatenate((XYZview, XYview), axis=0)
        TheSystem.SaveAs(zospath)

        # plt.figure()
        # plt.imshow(XYview[-1,:,:], extent=[-hw,hw,-hw,hw], origin='lower')
        # plt.colorbar()
        # plt.xlabel('x (mm)')
        # plt.ylabel('y (mm)')
        # plt.show(block=False)
        print('done.')

    del zos
    zos = None

    YZview = np.transpose(XYZview[:,:,XYZview.shape[2]//2])
    YZviewlog = np.log(YZview + 1e-6)
    min_val = np.max(YZviewlog)-7
    YZviewlog[YZviewlog < min_val] = min_val

    # dydx_ratio = 0.2
    plt.figure()
    plt.subplots_adjust(hspace=0.6)

    plt.subplot(211)
    # plt.title('true scale')
    plt.title(os.path.basename(zbfpath))
    plt.imshow(YZview + 1e-6, extent=[d1,d2,-hw,hw], origin='lower'
               , aspect='auto')  # auto, equal, ratio of dy/dx = dydx_ratio*(d2-d1)/(2*hw)
    plt.colorbar()
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    plt.show(block=False)

    plt.subplot(212)
    plt.title('log scale')
    plt.imshow(YZviewlog, extent=[d1,d2,-hw,hw], origin='lower'
               , aspect='auto')  # auto, equal, ratio of dy/dx = dydx_ratio*(d2-d1)/(2*hw)
    plt.colorbar()
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
