import argparse
import json
from pathlib import Path
import clr, os, winreg
from itertools import islice

# This boilerplate requires the 'pythonnet' module.
# The following instructions are for installing the 'pythonnet' module via pip:
#    1. Ensure you are running Python 3.4, 3.5, 3.6, or 3.7. PythonNET does not work with Python 3.8 yet.
#    2. Install 'pythonnet' from pip via a command prompt (type 'cmd' from the start menu or press Windows + R and type 'cmd' then enter)
#
#        python -m pip install pythonnet

# determine the Zemax working directory
class ZOSConnector():
    def __init__(self, path=None, is_ext_mode=False, instance=0):
        self.is_ext_mode = is_ext_mode
        aKey = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), r"Software\Zemax", 0, winreg.KEY_READ)
        zemaxData = winreg.QueryValueEx(aKey, 'ZemaxRoot')
        NetHelper = os.path.join(os.sep, zemaxData[0], r'ZOS-API\Libraries\ZOSAPI_NetHelper.dll')
        winreg.CloseKey(aKey)

        # add the NetHelper DLL for locating the OpticStudio install folder
        clr.AddReference(NetHelper)
        import ZOSAPI_NetHelper

        
        # uncomment the following line to use a specific instance of the ZOS-API assemblies
        # path = r'C:\Program Files\Zemax OpticStudio'
        # connect to OpticStudio
        if path is None:
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize()
        else:
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(path)
        
        zemaxDir = ''
        if isInitialized:
            zemaxDir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
            print('Found OpticStudio at:   %s' + zemaxDir)
        else:
            raise Exception('Cannot find OpticStudio')

        # load the ZOS-API assemblies
        clr.AddReference(os.path.join(os.sep, zemaxDir, r'ZOSAPI.dll'))
        clr.AddReference(os.path.join(os.sep, zemaxDir, r'ZOSAPI_Interfaces.dll'))
        import ZOSAPI
        self.ZOSAPI = ZOSAPI

        self.__TheConnection = self.ZOSAPI.ZOSAPI_Connection()
        if self.__TheConnection is None:
            raise Exception("Unable to intialize NET connection to ZOSAPI")

        if is_ext_mode:
            self.TheApplication = self.__TheConnection.ConnectAsExtension(instance)
        else:
            self.TheApplication = self.__TheConnection.CreateNewApplication()
            
        if self.TheApplication is None:
                raise Exception("Unable to acquire ZOSAPI application")

        if self.TheApplication.IsValidLicenseForAPI == False:
            raise Exception("License is not valid for ZOSAPI use.  Make sure you have enabled 'Programming > Interactive Extension' from the OpticStudio GUI.")

        self.TheSystem = self.TheApplication.PrimarySystem
        if self.TheSystem is None:
            raise Exception("Unable to acquire Primary system")

        print('Connected to OpticStudio')

        # The connection should now be ready to use.  For example:
        # print('Serial #: ', self.TheApplication.SerialCode)

    def __del__(self):
        if self.TheApplication is not None:
            # if not self.is_ext_mode:
            self.TheApplication.CloseApplication()
            self.TheApplication = None
        self.TheConnection = None
    
    def OpenFile(self, filepath, saveIfNeeded):
        if self.TheSystem is None:
            raise Exception("Unable to acquire Primary system")
        self.TheSystem.LoadFile(filepath, saveIfNeeded)
 
    def CloseFile(self, save):
        if self.TheSystem is None:
            raise Exception("Unable to acquire Primary system")
        self.TheSystem.Close(save)
 
    def SamplesDir(self):
        if self.TheApplication is None:
            raise Exception("Unable to acquire ZOSAPI application")
 
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
        var_lst = [y] * x
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


def load_fea_deformation_with_transform(
    zos,
    surface_id: int,
    fea_file: Path,
    coordinate: str = "local",
    transform_decenter: list = [0, 0, 0],
    transform_rotation: list = [0, 0, 0],
) -> None:
    surface_item = zos.TheSystem.LDE.GetSurfaceAt(surface_id).STARData.Deformations
    surface_item.CoordinateTransform.ResetToDefaultFrameOfReference()

    coordinate = coordinate.lower()
    if coordinate == "local":
        surface_item.SetDataIsLocal()
    elif coordinate == "global":
        surface_item.SetDataIsGlobal()
    else:
        raise ValueError("'coordinate' should be 'global' or 'local'")

    surface_item.CoordinateTransform.SetTransformValuesWithAngles(
        *transform_rotation, *transform_decenter
    )
    surface_item.FEAData.ImportDeformations(str(fea_file.resolve()))


def load_fea_temperature_with_transform(
    zos,
    surface_id: int,
    fea_file: Path,
    coordinate: str = "local",
    transform_decenter: list = [0, 0, 0],
    transform_rotation: list = [0, 0, 0],
) -> None:
    surface_item = zos.TheSystem.LDE.GetSurfaceAt(surface_id).STARData.Temperatures
    surface_item.CoordinateTransform.ResetToDefaultFrameOfReference()

    coordinate = coordinate.lower()
    if coordinate == "local":
        surface_item.SetDataIsLocal()
    elif coordinate == "global":
        surface_item.SetDataIsGlobal()
    else:
        raise ValueError("'coordinate' should be 'global' or 'local'")

    surface_item.CoordinateTransform.SetTransformValuesWithAngles(
        *transform_rotation, *transform_decenter
    )
    surface_item.FEAData.ImportTemperatures(str(fea_file.resolve()))

def load_fea_based_on_config(zos, config_file: Path):
    folder = config_file.parent
    with open(config_file, 'r') as f:
        fea_config = json.load(f)
    for surf in fea_config:
        surface_id = int(surf.lstrip("surface_"))
        deormation_fea = fea_config.get(surf).get("deformation")
        temperature_fea = fea_config.get(surf).get("temperature")
        if deormation_fea != None:
            fea_file = folder.joinpath(deormation_fea.get("fea_file"))
            load_fea_deformation_with_transform(
                zos,
                surface_id,
                fea_file,
                deormation_fea.get("fea_coordinate_system"),
                deormation_fea.get("user-defined_transform_decenter"),
                deormation_fea.get("user-defined_transform_rotation"),
            )

        if temperature_fea != None:
            fea_file = folder.joinpath(temperature_fea.get("fea_file"))
            load_fea_temperature_with_transform(
                zos,
                surface_id,
                fea_file,
                temperature_fea.get("fea_coordinate_system"),
                temperature_fea.get("user-defined_transform_decenter"),
                temperature_fea.get("user-defined_transform_rotation"),
            )


def main(args):
    lens = Path(args.lens_file).resolve()
    config_file = Path(args.fea_folder).joinpath("fea_config.json").resolve()

    zos = ZOSConnector()
    zos.OpenFile(str(lens), False)
    load_fea_based_on_config(zos, config_file)

    if args.output_file == "":
        zos.TheSystem.Save()
    else:
        output_file = Path(args.output_file)
        if not output_file.exists():
            output_file.touch()
        zos.TheSystem.SaveAs(str(output_file.resolve()))
    del zos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import the FEA dataset via STAR module")
    parser.add_argument("lens_file", type=str, help="The input File (zos or zmx file)")
    parser.add_argument("fea_folder", type=str, help="The folder where placed the FEA dataset and configuration file.")
    parser.add_argument("output_file", type=str, default="", help="The output file (zos or zmx file)")

    args = parser.parse_args()
    main(args)
