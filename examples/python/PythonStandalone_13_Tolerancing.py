import clr, os, winreg
from itertools import islice 

""" If clr is not found, check that pythonnet is installed correctly, 
or for newer python versions, install the latest pre-release with the line:
pip install --pre pythonnet
"""

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
    
    # load local variables
    ZOSAPI = zos.ZOSAPI
    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem
    if not os.path.exists(TheApplication.SamplesDir + r"\API\Python"):
        os.makedirs(TheApplication.SamplesDir + r"\API\Python")
    
    # Open Double Gauss sample file
    samplesFolder = TheApplication.SamplesDir
    DGfile = samplesFolder + r"\Sequential\Objectives\Double Gauss 28 degree field.zmx"
    TheSystem.LoadFile(DGfile, False)

    # Create a e13_tolerancing folder to save the tolerancing data to 
    folder_path = samplesFolder + r"\API\Python\e13_tolerancing"
    os.makedirs(folder_path, exist_ok=True)

    # Save the file in the before-tolerancing state
    TheSystem.SaveAs(samplesFolder + r"\API\Python\e13_tolerancing\Double_Gauss28_before_Tolerancing.zmx")
    samplesFolder = TheApplication.SamplesDir

    # Update path to new file and load it
    DGfile = samplesFolder + r"\\API\Python\e13_tolerancing\Double_Gauss28_before_Tolerancing.zmx"
    TheSystem.LoadFile(DGfile, False)

    """
    To Get a quick estimate of the sensitivity of the optical system, we can run Quick Sensitivity
    This tool is similar to the Tolerancing tool, but while the Tolerancing tool includes several controls to precisely calculate sensitivity, 
    the Quick Sensitivity tool is instead streamlined for maximum speed.
    This tool provides a sensitivity-only analysis with Paraxial Focus compensation.
    """

    # Run Quick Sensitivity tool and save data 
    qsst = TheSystem.Tools.OpenQuickSensitivity()
    qsst.Criterion = ZOSAPI.Tools.Tolerancing.QSCriterions.RMSSpotRadius
    qsst.Sampling= 3
    qsst.Configuration = 1
    qsst.Field = ZOSAPI.Tools.Tolerancing.CriterionFields.XY_Symmetric
    qsst.ZTDFile = str("qsst.ztd")
    qsst.RunAndWaitForCompletion()
    qsst.Close()

    # Read Resulting Sensitivity data
    qtdv = TheSystem.Tools.OpenToleranceDataViewer()
    qtdv.FileName = samplesFolder + r"\\API\Python\e13_tolerancing\qsst.ztd"
    qtdv.RunAndWaitForCompletion()
    # Access the summary
    summary = str(qtdv.Summary)
    # Note: Uncomment the following line to print the result summary of the Quick Sensitivity Tool analysis
    #print(summary)
    qtdv.Close()
    

    """ To easily set up the Tolerance Function, we can use the Tolerance Wizard"""
    # Set up Tolerance Wizard
    tWiz = TheSystem.TDE.SEQToleranceWizard
    # Select Tolerance Vendor
    tWiz.SelectTolerancePreset= ZOSAPI.Wizards.ToleranceVendor.Generic,ZOSAPI.Wizards.ToleranceGrade.Precision
    # Specify surface tolerances
    tWiz.SurfaceRadius = 0.1
    tWiz.SurfaceThickness = 0.1
    tWiz.SurfaceDecenterX = 0.1
    tWiz.SurfaceDecenterY = 0.1
    tWiz.SurfaceTiltX = 0.2
    tWiz.SurfaceTiltY = 0.2
    # Specify element tolerances
    tWiz.ElementDecenterX = 0.1
    tWiz.ElementDecenterY = 0.1
    tWiz.ElementTiltXDegrees = 0.2
    tWiz.ElementTiltYDegrees = 0.2
    # Specify tolerances not to be used
    tWiz.IsSurfaceSandAIrregularityUsed = False
    tWiz.IsIndexUsed = False
    tWiz.IsIndexAbbePercentageUsed = False
    tWiz.OK()

    """
    Quick Yield Computes the predicted Monte Carlo yield of the system using a faster, approximate calculation.
    This analysis uses sensitivity results to fit the wavefront error. 
    The fit is extrapolated using a modified Rimmer's approach and based on this fit the Monte Carlo outcome can be reconstructed.
    """
    print("Quick Yield tool: ----------------------------------------------------------------")

    # Access the Quick Yield Tool
    qy = TheSystem.Analyses.New_QuickYield()
    # Access Quick Yield Tool settings
    qy_set = qy.GetSettings().__implementation__  
    qy_set = ZOSAPI.Analysis.Tolerancing.IAS_QuickYield(qy_set)
    qy_set.Wavelength.SetWavelengthNumber=0
    qy_set.QYField.SetFieldSymmetricXY=ZOSAPI.Analysis.Tolerancing.QuickYield.XYSymmetricField.YPositive70Percent
    qy_set.Precision = ZOSAPI.Analysis.Tolerancing.QYPrecisions.VeryHigh
    qy_set.PupilSampling = 1
    qy_set.NumMonteCarlo = 1000
    qy_set.Statistic = ZOSAPI.Tools.Tolerancing.MonteCarloStatistics.Uniform
    qy_set.Compensation = ZOSAPI.Analysis.Tolerancing.QYCompensations.VeryHigh    
    qy_set.CompensatorStrategy = ZOSAPI.Analysis.Tolerancing.QYCompensatorStrategy.OptimizeAllDampedLeastSquares
    qy_set.Save()
    qy.ApplyAndWaitForCompletion()
    
    # Access Quick Yield Tool Results
    qy_results= qy.GetResults().__implementation__ 
    qy_results.GetTextFile(samplesFolder + r"\\API\Python\e13_tolerancing\qyield.txt")
    numQY = qy_results.NumberOfDataSeries
    print("Result Data: Quick Yield Tool---------------------------------")
    print("RMS Wavefront [Waves]	   Yield[%]")
    # loop through the data and print in terminal
    for i in range(numQY):
        series = qy_results.DataSeries[i]
        numCurves = series.NumSeries
        xData = series.XData.Data
        yData = series.YData.Data
        numPoints = xData.Length
        for j in range(numPoints):
            print(f"{xData[j]}:  {[yData[j, k] for k in range(numCurves)]}%")
    
    #Close the Quick Yield Window
    qy.Close()

    """ Set up and run the Tolerancing Tool """
    # Open Tolerancing Tool
    tol = TheSystem.Tools.OpenTolerancing()
    # Select Tolerancing mode, we choose 'Sensitivity' here
    tol.SetupMode =  ZOSAPI.Tools.Tolerancing.SetupModes.Sensitivity
    # Select Criterion and related settings
    tol.Criterion = ZOSAPI.Tools.Tolerancing.Criterions.RMSSpotRadius
    tol.CriterionSampling = 3
    tol.CriterionComp = ZOSAPI.Tools.Tolerancing.CriterionComps.OptimizeAll_DLS
    tol.CriterionCycle = 2
    tol.CriterionField = ZOSAPI.Tools.Tolerancing.CriterionFields.UserDefined
    # Select number of MC runs and files to save
    tol.NumberOfRuns = 20
    tol.NumberToSave = 20

    # Set to save ZTD file and Txt file
    tol.SaveTolDataFile = True
    tol.TolDataFile = "myFile.ztd"
    tol.OutputFile = "OutputName.TXT"

    # Run the Tolerancing analysis
    tol.RunAndWaitForCompletion()
    tol.Close()

    # Open the Tolerance Data Viewer
    tdv = TheSystem.Tools.OpenToleranceDataViewer()
    tdv.FileName = samplesFolder + r"\\API\Python\e13_tolerancing\myFile.ztd"
    tdv.RunAndWaitForCompletion()

    # Access Sensitivity Data
    sdata = tdv.SensitivityData

    # Access criterion
    criterion = sdata.GetCriterion(0)
    criterionName = str(criterion.Name)
    nomVal = criterion.NominalValue
    print("Tolerance analysis----------------------------------------------------------------------------------")
    print("Criteria:", criterionName)

    # Compensator data – access the first compensator in the list
    compData = sdata.GetCompensator(0)
    compType = str(compData.OperandType)
    compMin = compData.Minimum
    compMax = compData.Maximum
    compMean = compData.Mean

    # Operand data – access the first operand in the list
    sdOp = sdata.GetOperand(0)
    sdOpType = str(sdOp.OperandType)
    print("First Operand Type:", sdOpType)
    sdOpMin = sdOp.Minimum
    sdOpMax = sdOp.Maximum
    sdOpComment = str(sdOp.Comment)
    sdEffect = sdOp.GetEffectOnCriterion(0)
    sdEffectMax = sdEffect.EstimatedChangeMaximum
    sdEffectMin = sdEffect.EstimatedChangeMinimum

    # Grab some worst offender data as it applies to the first (and only) criterion
    numCriteria = sdOp.NumberOfCriteria
    effect = sdOp.GetEffectOnCriterion(0)
    estChangeMin = effect.EstimatedChangeMinimum
    estChangeMax = effect.EstimatedChangeMaximum

    # Access the summary
    summary = str(tdv.Summary)
    #print(summary)

    #Access the Monte Carlo Data
    mcdata = tdv.MonteCarloData
    metadata= mcdata.GetMetadata(0)
    metadataName = str(metadata.Name)
    print("Meta Data Name:",metadataName)
    Numberofpara= str(metadata.NumberOfParameters)
    print("Number of Parameters:", Numberofpara)

    tdv.Close()

    #Histogram
    #The analysis displays a histogram of any data saved during a Monte Carlo tolerance run. 
    #This includes all tolerance operands, compensators, and reported operands from a tolerance script.
    print("Histogram tool: ---------------------------------------------------")

    #Get Tol Histogram Settings
    print("Getting Tolerance Histogram Settings...........")
    newTolHistogram = TheSystem.Analyses.New_TolerancingHistogram()
    newTolHistogramSettings = newTolHistogram.GetSettings().__implementation__ 
    newTolHistogramSettings.UseSystemTolerances()
    newTolHistogramSettings.GetOperands()

    # available tolerance files
    tolFiles = newTolHistogramSettings.GetToleranceFiles()
    if (len(tolFiles) > 0):
        for i in range(len(tolFiles)):
            TolFileName = tolFiles[i]
            newTolHistogramSettings.Filename = TolFileName
            print("Available Filename " + str(i+1) + ": " + tolFiles[i])
    else:
        newTolHistogramSettings.UseSystemTolerances()
        print("No Available Filenames...")

    # available operands
    tolerancingOperands = newTolHistogramSettings.GetOperands()
    numOfOperands = tolerancingOperands.NumberOfOperands
    print("Available Operand for Tolerance Histogram")
    for i in range(numOfOperands):
        operand = tolerancingOperands.GetOperand(i+1)
        operandName = operand.OperandName
        print("Operand " + str(i+1) + ": " + operandName)

    # settings
    TolHistogramFile = newTolHistogramSettings.Filename
    TolHistogramOperand = newTolHistogramSettings.Operand
    TolMinValue = newTolHistogramSettings.MinValue
    TolMaxValue = newTolHistogramSettings.MaxValue
    TolNumBins = newTolHistogramSettings.NumBins

    # Set Tol Hist settings
    print("Setting Tolerance Histogram Settings............")
    newTolHistogramSettings.Filename = "myFile.ztd"
    newTolHistogramSettings.Operand = 5
    newTolHistogramSettings.MinValue = 0
    newTolHistogramSettings.MaxValue = 0
    newTolHistogramSettings.NumBins = 25
    TolHistogramFile2 = newTolHistogramSettings.Filename
    TolHistogramOperand2 = newTolHistogramSettings.Operand
    TolMinValue2 = newTolHistogramSettings.MinValue
    TolMaxValue2 = newTolHistogramSettings.MaxValue
    TolNumBins2 = newTolHistogramSettings.NumBins
    newTolHistogram.ApplyAndWaitForCompletion()

    # test Tol Hist Analisys results
    TolHistogramResults = newTolHistogram.GetResults().__implementation__
    numDS = TolHistogramResults.NumberOfDataSeries

    print("Result Data: Tolerancing Histogram...............")
    for i in range(numDS):
        series = TolHistogramResults.DataSeries[i]
        numCurves = series.NumSeries
        xData = series.XData.Data
        yData = series.YData.Data
        numPoints = xData.Length
        print("Operand:", sdOpType,	"               Count")
        for j in range(numPoints):
            print(f"{xData[j]}:   {[yData[j, k] for k in range(numCurves)]}")

    # Tolerance Yield
    #This analysis displays a cumulative distribution function, or yield curve, of all the data saved during a Monte Carlo run.
    #This includes all tolerance operands, compensators, and reported operands from a tolerance script.
    print("Tolerance Yield tool: ---------------------------------------------")

    newTolYield = TheSystem.Analyses.New_TolerancingYield()
    print("Getting Tolerance Yield Settings.................")    
    newTolYieldSettings = newTolYield.GetSettings().__implementation__
    newTolYieldSettings.UseSystemTolerances()
    newTolYieldSettings.GetOperands()

    # available tol files
    tolFiles = newTolYieldSettings.GetToleranceFiles()
    if len(tolFiles) > 0:
        for i in range (len(tolFiles)):
            TolFileName = tolFiles[i]
            newTolYieldSettings.Filename = TolFileName
            print(f"Available Filename {i+1}: {tolFiles[i]}")
    else:
        newTolYieldSettings.UseSystemTolerances()
        print("No Available Filenames...")

    # available operands:
    tolerancingOperands = newTolYieldSettings.GetOperands()
    numOperands = tolerancingOperands.NumberOfOperands
    print("Available Operands for Tolerance Yield..........")
    for i in range(numOperands):
        operand = tolerancingOperands.GetOperand(i+1)
        operandName = operand.OperandName
        print(f"Operand {i+1}: {operandName}")

    # settings
    TolYieldFile = newTolYieldSettings.Filename
    TolYieldOperand = newTolYieldSettings.Operand

    # set Tol Yield settings
    print("Setting Tolerance Yield Settings..................")
    newTolYieldSettings.Filename = "myFile.ZTD"
    newTolYieldSettings.Operand = 3
    TolYieldFile2 = newTolYieldSettings.Filename
    TolYieldOperand2 = newTolYieldSettings.Operand
    newTolYield.ApplyAndWaitForCompletion()

    # Tol Yield Analysis results
    print("Result Data: Tolerancing Yield....................")
    TolYieldResults = newTolYield.GetResults().__implementation__
    numDS = TolYieldResults.NumberOfDataSeries
    for i in range(numDS):
        series = TolYieldResults.DataSeries[i]
        numCurves = series.NumSeries

        xData = series.XData.Data
        yData = series.YData.Data
        #print("First Operand Type:", sdOpType)
        print("Operand:", sdOpType,	"                  Yield [%]")
        numPoints = len(xData)
        for j in range(numPoints):
            print(f"{xData[j]}:      {[yData[j,k] for k in range(numCurves)]}%")

    TheSystem.SaveAs(samplesFolder + r"\\API\Python\e13_tolerancing\Double_Gauss_After_Tolerancing.zmx")

    del zos
    zos = None