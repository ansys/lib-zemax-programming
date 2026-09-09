import clr, os, winreg
from itertools import islice

from zrd_processing import (
    read_zrd_ray_directions,
    run_source_ray_trace,
    set_source_ray_counts,
)
from diopter_map import calculate_diopter_map, plot_diopter_map


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
        # Determine location of ZOSAPI_NetHelper.dll and add as reference.
        aKey = winreg.OpenKey(
            winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER),
            r"Software\Zemax",
            0,
            winreg.KEY_READ,
        )
        zemaxData = winreg.QueryValueEx(aKey, "ZemaxRoot")
        NetHelper = os.path.join(
            os.sep,
            zemaxData[0],
            r"ZOS-API\Libraries\ZOSAPI_NetHelper.dll",
        )
        winreg.CloseKey(aKey)
        clr.AddReference(NetHelper)
        import ZOSAPI_NetHelper

        # Find the installed version of OpticStudio.
        if path is None:
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize()
        else:
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(path)

        if isInitialized:
            zos_directory = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
        else:
            raise PythonStandaloneApplication.InitializationException(
                "Unable to locate Zemax OpticStudio. Try using a hard-coded path."
            )

        clr.AddReference(os.path.join(os.sep, zos_directory, "ZOSAPI.dll"))
        clr.AddReference(
            os.path.join(os.sep, zos_directory, "ZOSAPI_Interfaces.dll")
        )
        import ZOSAPI

        self.ZOSAPI = ZOSAPI
        self.TheConnection = ZOSAPI.ZOSAPI_Connection()

        if self.TheConnection is None:
            raise PythonStandaloneApplication.ConnectionException(
                "Unable to initialize .NET connection to ZOSAPI"
            )

        self.TheApplication = self.TheConnection.CreateNewApplication()
        if self.TheApplication is None:
            raise PythonStandaloneApplication.InitializationException(
                "Unable to acquire ZOSAPI application"
            )

        if self.TheApplication.IsValidLicenseForAPI is False:
            raise PythonStandaloneApplication.LicenseException(
                "License is not valid for ZOSAPI use"
            )

        self.TheSystem = self.TheApplication.PrimarySystem
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException(
                "Unable to acquire Primary system"
            )

    def OpenFile(self, filepath, saveIfNeeded):
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException(
                "Unable to acquire Primary system"
            )
        self.TheSystem.LoadFile(filepath, saveIfNeeded)

    def CloseFile(self, save):
        if self.TheSystem is None:
            raise PythonStandaloneApplication.SystemNotPresentException(
                "Unable to acquire Primary system"
            )
        self.TheSystem.Close(save)

    def SamplesDir(self):
        if self.TheApplication is None:
            raise PythonStandaloneApplication.InitializationException(
                "Unable to acquire ZOSAPI application"
            )
        return self.TheApplication.SamplesDir

    def ExampleConstants(self):
        if (
            self.TheApplication.LicenseStatus
            == self.ZOSAPI.LicenseStatusType.PremiumEdition
        ):
            return "Premium"
        elif (
            self.TheApplication.LicenseStatus
            == self.ZOSAPI.LicenseStatusTypeProfessionalEdition
        ):
            return "Professional"
        elif (
            self.TheApplication.LicenseStatus
            == self.ZOSAPI.LicenseStatusTypeStandardEdition
        ):
            return "Standard"
        return "Invalid"

    def reshape(self, data, x, y, transpose=False):
        if type(data) is not list:
            data = list(data)
        var_lst = [y] * x
        it = iter(data)
        res = [list(islice(it, i)) for i in var_lst]
        if transpose:
            return self.transpose(res)
        return res

    def transpose(self, data):
        if type(data) is not list:
            data = list(data)
        return list(map(list, zip(*data)))


if __name__ == "__main__":
    zos = None

    try:
        zos = PythonStandaloneApplication()

        # Load local variables.
        ZOSAPI = zos.ZOSAPI
        TheApplication = zos.TheApplication
        TheSystem = zos.TheSystem

        # Open file and set Analysis Rays to 1 for each active source.
        testFile = r"D:\PythonProjects\Git-course\WS-DiopterMap\Windshield_Diopter.zmx"
        TheSystem.LoadFile(testFile, False)
        print(f"Loaded model: {TheSystem.SystemFile}")
        print(f"Number of NCE objects: {TheSystem.NCE.NumberOfObjects}")

        # Source 1 is M. Sources 2-5 are the four M-prime positions.
        source_ray_counts = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
        }
        center_source_object = 1
        surrounding_source_objects = [2, 3, 4, 5]

        # IMPORTANT: change this if the detector is not NCE object 7.
        detector_object_number = 7

        source_parent = TheSystem.NCE.GetObjectAt(center_source_object)
        grid_rows = source_parent.SourcesData.ArrayNumberY
        grid_columns = source_parent.SourcesData.ArrayNumberX
        delta_x_m = 12.0 / 1000.0
        model_folder = os.path.dirname(TheSystem.SystemFile)
        all_source_ray_data = {}

        # Run all five sources separately and collect matching ray directions.
        for active_source, number_of_rays in source_ray_counts.items():
            print(
                f"\n{'=' * 70}\n"
                f"Processing source object {active_source}\n"
                f"{'=' * 70}"
            )

            set_source_ray_counts(
                TheSystem,
                ZOSAPI,
                active_source,
                source_ray_counts,
            )

            source_zrd_path = run_source_ray_trace(
                TheSystem,
                model_folder,
                active_source,
                number_of_rays,
            )

            all_source_ray_data[active_source] = read_zrd_ray_directions(
                TheSystem,
                ZOSAPI,
                source_zrd_path,
                active_source,
                detector_object_number,
            )

        # Match the same ray number across the five ZRD files,
        # calculate maximum TL 957 angular distortion, and convert to diopters.
        diopter_results = calculate_diopter_map(
            all_source_ray_data,
            center_source_object,
            surrounding_source_objects,
            delta_x_m,
        )

        plot_diopter_map(
            diopter_results,
            grid_rows,
            grid_columns,
            model_folder,
        )

    finally:
        if zos is not None and zos.TheApplication is not None:
            zos.TheApplication.CloseApplication()
            zos.TheApplication = None
            zos = None
