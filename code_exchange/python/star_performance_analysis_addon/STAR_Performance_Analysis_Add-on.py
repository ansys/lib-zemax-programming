# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# -*- coding: utf-8 -*-
"""
STAR Performance Analysis Package . This script aims to recreate the STAR-performance analysis in the ZOS-API. 

To run the script make sure you define the correct parameters at the end of this file. 

@author: Tony Chatzikostas (R&D Engineer - Ansys, Part of Synopsys)
"""

# ============================================================================
# IMPORT LIBRARIES
# ============================================================================
import clr, os, winreg
import numpy as np 
import tkinter as tk 
from tkinter import ttk 
import matplotlib.pyplot as plt 
import time
from itertools import islice


# ============================================================================
# ZOS-API CONNECTOR CLASS (Integrated)
# ============================================================================
class ZOSConnector:
    """
    ZOS-API connector class for connecting to Ansys Zemax OpticStudio
    """
    class LicenseException(Exception):
        pass
    class ConnectionException(Exception):
        pass
    class InitializationException(Exception):
        pass
    class SystemNotPresentException(Exception):
        pass

    def __init__(self, path=None, is_ext_mode=False, instance=0, use_custom_directory=False, custom_directory=None):
        """
        Initialize ZOS-API connection
        
        Parameters:
        -----------
        path : str, optional
            Path to ZOS-API initialization
        is_ext_mode : bool, optional
            Whether to connect as extension (default: False)
        instance : int, optional
            Instance number for extension mode (default: 0)
        use_custom_directory : bool, optional
            Whether to use a custom OpticStudio directory (default: False)
        custom_directory : str, optional
            Custom OpticStudio directory path if use_custom_directory is True
        """
        # Determine location of ZOSAPI_NetHelper.dll & add as reference
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
            isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(path)
        
        # Determine the ZOS root directory
        if isInitialized:
            if use_custom_directory and custom_directory is not None:
                dir = custom_directory
                print(f"Using custom Zemax directory: {dir}")
            else:
                dir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
                print(f"Zemax directory set to: {dir}")
        else:
            raise ZOSConnector.InitializationException("Unable to locate Zemax OpticStudio. Try using a hard-coded path.")
        
        # Add ZOS-API references
        clr.AddReference(os.path.join(os.sep, dir, r'ZOSAPI.dll'))
        clr.AddReference(os.path.join(os.sep, dir, r'ZOSAPI_Interfaces.dll'))
        import ZOSAPI

        self.ZOSAPI = ZOSAPI

        if is_ext_mode:
            self.TheConnection = ZOSAPI.ZOSAPI_Connection()
            self.TheApplication = self.TheConnection.ConnectAsExtension(instance)
        else:
            self.TheConnection = ZOSAPI.ZOSAPI_Connection()
            self.TheApplication = self.TheConnection.CreateNewApplication()

        if not self.TheApplication:
            raise ZOSConnector.InitializationException("Unable to acquire ZOSAPI application")
        
        if not self.TheApplication.IsValidLicenseForAPI:
            raise ZOSConnector.LicenseException("License is not valid for ZOSAPI use")

        self.TheSystem = self.TheApplication.PrimarySystem
        if not self.TheSystem:
            raise ZOSConnector.SystemNotPresentException("Unable to acquire Primary system")
    
    def __del__(self):
        if self.TheApplication is not None:
            self.TheApplication.CloseApplication()
            self.TheApplication = None
        self.TheConnection = None

    def OpenFile(self, filepath, saveIfNeeded):
        if self.TheSystem is None:
            raise ZOSConnector.SystemNotPresentException("Unable to acquire Primary system")
        self.TheSystem.LoadFile(filepath, saveIfNeeded)

    def CloseFile(self, save):
        if self.TheSystem is None:
            raise ZOSConnector.SystemNotPresentException("Unable to acquire Primary system")
        self.TheSystem.Close(save)

    def SamplesDir(self):
        if self.TheApplication is None:
            raise ZOSConnector.InitializationException("Unable to acquire ZOSAPI application")
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





class Metrics: 
    #CLASS METRICS 
    #This class contains the metrics that will be used. The user can create his own "custom" 
    #metric here and plug it in the main code. The main metric intoduced here is the MF_Operand 
    #which allows to plug in any kind of operand and use it as a metric.
    def __init__(self,zos_connector):
        self.zos= zos_connector 
        self.ZOSAPI= zos_connector.ZOSAPI 
        self.TheSystem = zos_connector.TheSystem 

    def RMS_Spot_Size(self): 
        #This metric calculates the RMS Spot Size Radius
        ZOSAPI = self.ZOSAPI 
        TheSystem = self.TheSystem 
        #Create the spot diagram analysis- CHECK API HELP FILES for more info
        spot=TheSystem.Analyses.New_Analysis(ZOSAPI.Analysis.AnalysisIDM.StandardSpot)
        spot_setting=spot.GetSettings()
        spot_setting.ReferTo=ZOSAPI.Analysis.Settings.RMS.ReferTo.Centroid #Refer to controid to calculate the spot size
        #Continue with the analysis
        spot.ApplyAndWaitForCompletion() 
        spot_resutls=spot.GetResults() 
        #Get the RMS value for field 1, wvl 1
        rms_value= spot_resutls.SpotData.GetRMSSpotSizeFor(1,1) 
        return rms_value
    
    def MF_Value(self):
        #This metric returns the value of the Merif function  
        TheSystem= self.TheSystem 
        theMFE = TheSystem.MFE 
        MF_current_value = theMFE.CalculateMeritFunction() 
        print(f"Merit function value is {MF_current_value}")
        return MF_current_value 
    
    def MF_operand(self, operand="EFFL",S=[0,0,0,0,0,0,0,0]): 
        #This option allows to use a specific MF operand as metric
        ZOSAPI =self.ZOSAPI 
        TheSystem= self.TheSystem 
        theMFE=TheSystem.MFE 
        if len(S)!=8 : 
            raise ValueError("S must have 8 elements")
        try: 
            operand_type=getattr(ZOSAPI.Editors.MFE.MeritOperandType,operand) 
        except AttributeError:
            raise ValueError(f"Invalid operand type : {operand}")
        custom_operand_value=theMFE.GetOperandValue(operand_type, *S) 
        return custom_operand_value

class STAR_Performance_Analysis_Back_End_Tool : 

    #This class recreates the back end functionality of the STAR Performance Analysis 
    def __init__(self, zos_connector, metrics_tool,Debug_Mode=False,metric_type="RMS_Spot_Size"
                 ,metric_operand_type="EPDI",S=[0,0,0,0,0,0,0,0],SAMP=1,Wave=1,Field=1,
                 Freq=50,Scl=0,Grid=0):
        self.zos = zos_connector
        self.ZOSAPI = zos_connector.ZOSAPI
        self.TheSystem = zos_connector.TheSystem
        self.LDE = self.TheSystem.LDE
        self.metrics = metrics_tool
        self.Debug_Mode=Debug_Mode
        self.metric_operand_type=metric_operand_type
        self.S=S
        self.SAMP=SAMP 
        self.Wave=Wave 
        self.Field = Field 
        self.Freq = Freq 
        self.Scl = Scl 
        self.Grid = Grid 
        self.metric_type=metric_type
        self.surfaces_with_star_deformations = []
        self.surfaces_with_star_deformations_RBM_only = [] 
        self.surfaces_with_star_deformations_RBM_disabled = []
        self.surfaces_with_star_temperature = []
        self.surfaces_with_star_stress = []
        self.surfaces_with_direct_index = []
        self.results = {}

    def measure_metric(self):
        # Use MF_operand for metrics configured in metric_configs
        if self.metric_type.lower()=="mf_value":
            return self.metrics.MF_Value()
        else:
            # All other metrics (RMS_Spot_Size, MF_Operand, etc.) use MF_operand
            return self.metrics.MF_operand(operand=self.metric_operand_type, S=self.S)
        
    def detect_surfaces_with_STOP_effects(self): 
        #Identify the surfaces of the optical system with STOP data applied.
        for i in range(1,self.LDE.NumberOfSurfaces+1): 
            surf = self.LDE.GetSurfaceAt(i)
            star_surf = surf.STARData
            if star_surf.Deformations.FEAData.AreDeformationsImported:
                self.surfaces_with_star_deformations.append(i)
            if star_surf.Temperatures.FEAData.AreTemperaturesImported:
                self.surfaces_with_star_temperature.append(i)
            if star_surf.Stress.FEAData.IsStressImported: #IsStressImported #IsStressTensorApplied
                self.surfaces_with_star_stress.append(i)
            if star_surf.DirectIndex.FEAData.IsDirectIndexImported:
                self.surfaces_with_direct_index.append(i)

    def Calculate_contributions_For_Each_Surface(self,error_type="Individual"):
        #This is the back end function for the "Show Error For -> Surface" option. 
        surfaces= sorted(set(self.surfaces_with_star_deformations+ 
                             self.surfaces_with_star_temperature
                             +self.surfaces_with_star_stress))
        print(f"Surfaces-> {surfaces}")
        deformation_results=[] 
        temperature_results=[]
        stress_results=[] 
        direct_index_results=[]
        deformation_results_RBM_only=[] 
        deformation_results_RBM_disabled=[] 

        time_deformation=0
        time_temperature=0 
        time_stress = 0
        time_direct_index=0 
        time_deformation_RBM_only=0
        time_deformation_RBM_disabled=0
        table_deformation= [] 
        table_temperature=[] 
        table_stress=[]
        table_direct_index=[]
        table_deformation_RBM_only = [] 
        table_deformation_RBM_disabled = []

        #First step: Measue the metric with all the STOP effects removed
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Deformations.Fits.RemoveDeformations() 
            star_surf.Temperatures.Fits.RemoveTemperatures() 
            star_surf.Stress.Fits.RemoveStress() 
            star_surf.DirectIndex.Fits.RemoveIndex()

            full_metric = self.measure_metric() 

        for surf_num in surfaces: 
            surf=self.LDE.GetSurfaceAt(surf_num)
            star_surf = surf.STARData 

            if error_type.lower()=="individual": # Option for the "Error Type -> Individual" option. For more info visit the HELP FILES.
            
                #Calculating idvividual contribution for DEFORMATION
                if surf_num in self.surfaces_with_star_deformations:
                    t_d_s = time.time()
                    star_surf.Deformations.Fits.ApplyDeformations()
                    modified_metric = self.measure_metric() 
                    contribution = modified_metric 
                    deformation_results.append(contribution)
                    star_surf.Deformations.Fits.RemoveDeformations()
                    t_d_e= time.time()
                    t_d=t_d_e-t_d_s
                    time_deformation+= t_d 
                    table_deformation.append(time_deformation)
                    print(f"Deformation->Surf{surf_num}->time: {time_deformation}")
                else:
                    deformation_results.append(0)

                #calculating individual contribution for DEFORMATION RBM ONLY 
                if surf_num in self.surfaces_with_star_deformations:
                    t_d_rbm_s=time.time()
                    star_surf.Deformations.Fits.ApplyDeformations()
                    star_surf.Deformations.Fits.Options=self.ZOSAPI.Editors.LDE.STARDeformationOption.OnlyRBMs
                    modified_metric = self.measure_metric()
                    contribution = modified_metric 
                    deformation_results_RBM_only.append(contribution)
                    star_surf.Deformations.Fits.RemoveDeformations()
                    t_d_rbm_e=time.time() 
                    t_d_rbm= t_d_rbm_e - t_d_rbm_s 
                    time_deformation_RBM_only+= t_d_rbm
                    table_deformation_RBM_only.append(time_deformation_RBM_only)
                    print(f"Deformation RBM Only->Surf{surf_num}->Time: {time_deformation_RBM_only}")
                else:
                    deformation_results_RBM_only.append(0)

                #Calculating individual contribution for DEFORMATION RBM DISABLED
                if surf_num in self.surfaces_with_star_deformations:
                    t_d_rbm_d_s=time.time()
                    star_surf.Deformations.Fits.ApplyDeformations()
                    star_surf.Deformations.Fits.Options=self.ZOSAPI.Editors.LDE.STARDeformationOption.DeformationWithoutRBMs 
                    modified_metric = self.measure_metric()
                    contribution = modified_metric 
                    deformation_results_RBM_disabled.append(contribution)
                    star_surf.Deformations.Fits.RemoveDeformations()
                    t_d_rbm_d_e=time.time() 
                    t_d_rbm_d= t_d_rbm_d_e - t_d_rbm_d_s 
                    time_deformation_RBM_disabled+= t_d_rbm_d
                    table_deformation_RBM_disabled.append(time_deformation_RBM_disabled)
                    print(f"Deformation RBM Disabled->Surf{surf_num}->Time: {time_deformation_RBM_disabled}")
                else:
                    deformation_results_RBM_disabled.append(0)

                #Caclulating individual contribution for TEMPERATURE 
                if surf_num in self.surfaces_with_star_temperature:
                    t_t_s=time.time()
                    star_surf.Temperatures.Fits.ApplyTemperatures()
                    modified_metric = self.measure_metric()
                    contribution = modified_metric 
                    temperature_results.append(contribution)
                    star_surf.Temperatures.Fits.RemoveTemperatures()
                    t_t_e=time.time()
                    t_t= t_t_e-t_t_s 
                    time_temperature+= t_t 
                    table_temperature.append(time_temperature)
                    print(f"Temperature->Surf{surf_num}->Time: {time_temperature}")
                else:
                    temperature_results.append(0)

                #Calculating individual contribution for STRESS
                if surf_num in self.surfaces_with_star_stress:
                    t_s_s=time.time()
                    star_surf.Stress.Fits.ApplyStress()
                    modified_metric = self.measure_metric()
                    contribution = modified_metric 
                    stress_results.append(contribution)
                    star_surf.Stress.Fits.RemoveStress()
                    t_s_e=time.time() 
                    t_s = t_s_e - t_s_s 
                    time_stress+= t_s
                    table_stress.append(time_stress)
                    print(f"Stress->Surf{surf_num}->Time: {time_stress}")
                else:
                    stress_results.append(0)

                #Calculating individual contribution for DIRECT INDEX 
                if surf_num in self.surfaces_with_direct_index:
                    t_di_s=time.time()
                    star_surf.DirectIndex.Fits.ApplyIndex()
                    modified_metric = self.measure_metric()
                    contribution = modified_metric 
                    direct_index_results.append(contribution)
                    star_surf.DirectIndex.Fits.RemoveIndex()
                    t_di_e=time.time() 
                    t_di = t_di_e - t_di_s 
                    time_direct_index+= t_di
                    table_direct_index.append(time_direct_index)
                    print(f"Direct Index->Surf{surf_num}->Time: {time_direct_index}")
                else:
                    direct_index_results.append(0)

            elif error_type.lower()=="cumulative": # Option for the "Error Type -> Cumulative" option. For more info visit the HELP FILES.
                # Remove all STOP effects to start fresh
                # (This is done once at the beginning, not inside the loop)
                pass  # Removal will happen before the loop below
        
        # Handle cumulative mode properly
        if error_type.lower()=="cumulative":
            # First, remove all STOP effects to start fresh
            for surf_num in surfaces:
                surf = self.LDE.GetSurfaceAt(surf_num)
                star_surf = surf.STARData
                star_surf.Deformations.Fits.RemoveDeformations()
                star_surf.Temperatures.Fits.RemoveTemperatures()
                star_surf.Stress.Fits.RemoveStress()
                star_surf.DirectIndex.Fits.RemoveIndex()
            
            # For each surface, apply effects in correct order: Deformation (RBM modes) → Temperature → Stress → Direct Index
            for surf_num in surfaces:
                surf = self.LDE.GetSurfaceAt(surf_num)
                star_surf = surf.STARData
                
                # STEP 1: DEFORMATION - RBM Only
                if surf_num in self.surfaces_with_star_deformations:
                    star_surf.Deformations.Fits.ApplyDeformations()
                    star_surf.Deformations.Fits.Options = self.ZOSAPI.Editors.LDE.STARDeformationOption.OnlyRBMs
                    modified_metric = self.measure_metric()
                    deformation_results_RBM_only.append(modified_metric)
                else:
                    deformation_results_RBM_only.append(0)
                
                # STEP 2: DEFORMATION - Full (with RBMs) - this is the standard deformation
                if surf_num in self.surfaces_with_star_deformations:
                    star_surf.Deformations.Fits.ApplyDeformations()
                    # Default option (with RBMs)
                    modified_metric = self.measure_metric()
                    deformation_results.append(modified_metric)
                    deformation_results_RBM_disabled.append(modified_metric)  # Store same value for full deformation
                else:
                    deformation_results.append(0)
                    deformation_results_RBM_disabled.append(0)
                
                # STEP 3: TEMPERATURE (applied on top of deformation)
                if surf_num in self.surfaces_with_star_temperature:
                    star_surf.Temperatures.Fits.ApplyTemperatures()
                    modified_metric = self.measure_metric()
                    temperature_results.append(modified_metric)
                else:
                    temperature_results.append(0)
                
                # STEP 4: STRESS (applied on top of deformation + temperature)
                if surf_num in self.surfaces_with_star_stress:
                    star_surf.Stress.Fits.ApplyStress()
                    modified_metric = self.measure_metric()
                    stress_results.append(modified_metric)
                else:
                    stress_results.append(0)
                
                # STEP 5: DIRECT INDEX (applied on top of deformation + temperature + stress)
                if surf_num in self.surfaces_with_direct_index:
                    star_surf.DirectIndex.Fits.ApplyIndex()
                    modified_metric = self.measure_metric()
                    direct_index_results.append(modified_metric)
                else:
                    direct_index_results.append(0)
        
        # Store the results AFTER all calculations (works for both Individual and Cumulative)
        self.results = { "surfaces": surfaces,
        "deformation": deformation_results,
        "deformation_RBM_only": deformation_results_RBM_only,
        "deformation_RBM_disabled": deformation_results_RBM_disabled,
        "temperature": temperature_results,
        "stress": stress_results,
        "direct_index": direct_index_results,
        "metric_type": self.metric_type,
        "starting_metric":full_metric}
            
        #print(f"Time deformation table: {table_deformation}")
        #print(f"TIme temperature table: {table_temperature}") 
        #print(f"Time Stress Table: {table_stress}")
        #print(f"Time Direct Index Table: {table_direct_index}")
        print(f"Deformation RBM Only Results: {self.results['deformation_RBM_only']}")
        print(f"Deformation RBM Disabled Results: {self.results['deformation_RBM_disabled']}")
        print(f"Deformation with RBM Results :{self.results['deformation']} ")
        print(f"Stress Results :{self.results['stress']} ") 
        print(f"Temperature Results :{self.results['temperature']} ") 
        print(f"Direct Index Results :{self.results['direct_index']} ")


    def Calculate_Errors_For_System(self, metric_type="RMS_Spot_Size"): 
        #This is the back end function for the "Show Error For -> System" option.

        surfaces= sorted(set(self.surfaces_with_star_deformations+ 
                             self.surfaces_with_star_temperature
                             +self.surfaces_with_star_stress
                             +self.surfaces_with_direct_index))

        #1st step: Remove every STOP effect
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Deformations.Fits.RemoveDeformations() 
            star_surf.Temperatures.Fits.RemoveTemperatures() 
            star_surf.Stress.Fits.RemoveStress() 
            star_surf.DirectIndex.Fits.RemoveIndex()
        starting_metric = self.measure_metric() # Measuring metric with no STOP effects

        #2nd step: Enable only Deformations in the system.
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Deformations.Fits.ApplyDeformations()

        total_deformation =  self.measure_metric() # Measuring metric with Deformations only applied

        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Deformations.Fits.RemoveDeformations() #Remove deformations

        #2.1 step: Enable only Deformations RBM ONLY in the system.
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Deformations.Fits.ApplyDeformations()
            star_surf.Deformations.Fits.Options=self.ZOSAPI.Editors.LDE.STARDeformationOption.OnlyRBMs

        total_deformation_RBM_only =  self.measure_metric() # Measuring metric with Deformations RBM ONLY applied
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Deformations.Fits.RemoveDeformations() #Remove deformations RBM only

        #2.2 step: Enable only Deformations Without RBMs in the system.
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Deformations.Fits.ApplyDeformations()
            star_surf.Deformations.Fits.Options=self.ZOSAPI.Editors.LDE.STARDeformationOption.DeformationWithoutRBMs
        total_deformation_without_RBMs =  self.measure_metric() # Measuring metric with Deformations Without RBMs applied
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Deformations.Fits.RemoveDeformations() #Remove deformations Without RBMs
        
        #3rd step: Enable only Temperature in the system.
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Temperatures.Fits.ApplyTemperatures()

        total_temperature =  self.measure_metric() # Measuring metric with Temperature only applied

        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Temperatures.Fits.RemoveTemperatures() #Remove Temperature

        #4th step: Enable only Stress in the system.
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Stress.Fits.ApplyStress()

        total_stress =  self.measure_metric() # Measuring metric with Stress only applied

        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.Stress.Fits.RemoveStress() #Remove Stress

        #5th step: Enable only Direct Index in the system.
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.DirectIndex.Fits.ApplyIndex()

        total_direct_index =  self.measure_metric() # Measuring metric with Direct Index only applied

        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num) 
            star_surf=surf.STARData 
            star_surf.DirectIndex.Fits.RemoveIndex() #Remove Direct Index

        #6th step : Calculate metric with all STOP effects
        for surf_num in surfaces:
            surf = self.LDE.GetSurfaceAt(surf_num)
            star_surf = surf.STARData
            star_surf.Deformations.Fits.ApplyDeformations()
            star_surf.Temperatures.Fits.ApplyTemperatures()
            star_surf.Stress.Fits.ApplyStress()
            star_surf.DirectIndex.Fits.ApplyIndex()
    
        all_spot_data_metric = self.measure_metric()

        self.results = {
            "starting_metric": starting_metric,
            "all_star_metric": all_spot_data_metric,
            "deformation": total_deformation,
            "deformation_RBM_only": total_deformation_RBM_only,
            "deformation_without_RBMs": total_deformation_without_RBMs,
            "temperature": total_temperature,
            "stress": total_stress,
            "direct_index": total_direct_index,
            "metric_type": metric_type
        }

    def plot_resutls_for_surface_option(self, error_type="Individual", show_error_for="surface"):
        #Main back end PLOTTING function  for "Show Error For -> Surface" option.

        #Load Data
        surfaces = self.results["surfaces"]
        deformation_results = self.results["deformation"]
        deformation_results_RBM_only = self.results["deformation_RBM_only"] 
        deformation_results_RBM_disabled = self.results["deformation_RBM_disabled"]
        temperature_results = self.results["temperature"]
        stress_results = self.results["stress"]
        direct_index_results = self.results["direct_index"]
        metric_type = self.results["metric_type"]
        starting_metric = self.results["starting_metric"]

        # Determine which STOP effects are present in the system
        has_deformations = len(self.surfaces_with_star_deformations) > 0
        has_temperatures = len(self.surfaces_with_star_temperature) > 0
        has_stress = len(self.surfaces_with_star_stress) > 0
        has_direct_index = len(self.surfaces_with_direct_index) > 0
        
        # Determine if RBM details should be shown
        show_rbm_details = getattr(self, 'show_rbm_details', False)
        
        # Count how many STOP effects exist to determine bar positioning
        stop_effects = []
        if has_deformations:
            if show_rbm_details:
                stop_effects.append('deformation_RBM_only')
                stop_effects.append('deformation_without_RBMs')
            else:
                stop_effects.append('deformation')
        if has_temperatures:
            stop_effects.append('temperature')
        if has_stress:
            stop_effects.append('stress')
        if has_direct_index:
            stop_effects.append('direct_index')
        
        num_effects = len(stop_effects)
        
        # Calculate bar width and positions based on number of effects
        if num_effects == 1:
            bar_width = 0.5
            offsets = [0]
        elif num_effects == 2:
            bar_width = 0.35
            offsets = [-0.175, 0.175]
        elif num_effects == 3:
            bar_width = 0.25
            offsets = [-0.25, 0, 0.25]
        elif num_effects == 4:
            bar_width = 0.2
            offsets = [-0.3, -0.1, 0.1, 0.3]
        else:  # 5 effects
            bar_width = 0.15
            offsets = [-0.3, -0.15, 0, 0.15, 0.3]

        #Calculate max and min Y values for the Plot
        all_values = [starting_metric]
        if has_deformations and deformation_results:
            all_values.extend([v for v in deformation_results if v is not None])
            if show_rbm_details:
                all_values.extend([v for v in deformation_results_RBM_only if v is not None])
                all_values.extend([v for v in deformation_results_RBM_disabled if v is not None])
        if has_temperatures and temperature_results:
            all_values.extend([v for v in temperature_results if v is not None])
        if has_stress and stress_results:
            all_values.extend([v for v in stress_results if v is not None])
        if has_direct_index and direct_index_results:
            all_values.extend([v for v in direct_index_results if v is not None])
        
        # Filter out None values just in case
        all_values = [v for v in all_values if v is not None]
        
        max_y_value = np.max(all_values) if all_values else starting_metric
        min_y_value = np.min(all_values) if all_values else 0

        fig1=plt.figure(figsize=(10,6)) 

        #Plot the STARTING METRIC at the first position(-1)-> SIMILAR TO ZOS STAR PERFORMANCE ANALYSIS UI
        plt.bar(-1,starting_metric,width=0.5,color="gray",label="Starting Metric")

        #Plot grouped bars for surfaces at the next positions (0,1,2,...)
        x_surfaces = range(len(surfaces))
        
        # Plot only the STOP effects that exist
        effect_idx = 0
        if has_deformations:
            if show_rbm_details:
                # Show RBM details: RBM Only and Without RBMs separately
                plt.bar([xi + offsets[effect_idx] for xi in x_surfaces], deformation_results_RBM_only, 
                       width=bar_width, color="darkgreen", label="Deformation (RBM Only)")
                effect_idx += 1
                plt.bar([xi + offsets[effect_idx] for xi in x_surfaces], deformation_results_RBM_disabled, 
                       width=bar_width, color="lightgreen", label="Deformation (Without RBMs)")
                effect_idx += 1
            else:
                # Show combined deformation
                plt.bar([xi + offsets[effect_idx] for xi in x_surfaces], deformation_results, 
                       width=bar_width, color="green", label="Deformation")
                effect_idx += 1
        if has_temperatures:
            plt.bar([xi + offsets[effect_idx] for xi in x_surfaces], temperature_results, 
                   width=bar_width, color="blue", label="Thermal")
            effect_idx += 1
        if has_stress:
            plt.bar([xi + offsets[effect_idx] for xi in x_surfaces], stress_results, 
                   width=bar_width, color="red", label="Stress")
            effect_idx += 1
        if has_direct_index:
            plt.bar([xi + offsets[effect_idx] for xi in x_surfaces], direct_index_results, 
                   width=bar_width, color="orange", label="Direct Index")

        #Add X-axis ticks and labels 
        all_x = [-1] + list(x_surfaces)
        all_labels = ["0-Starting"] + [f"Surf {s}" for s in surfaces]
        plt.xticks(all_x, all_labels)
        plt.xlabel("Surface") 

        if metric_type=="MF_Operand": #Properly name the labels to match the MF operand type
            plt.title(f"STAR Performance Analysis | Show Error For: {show_error_for.capitalize()} | Error Type: {error_type}\n({metric_type}): {self.metric_operand_type}")
            plt.ylabel(f" {metric_type.replace("_", " ")} : {self.metric_operand_type}")
        else :
             plt.title(f"STAR Performance Analysis | Show Error For: {show_error_for.capitalize()} | Error Type: {error_type}\n({metric_type})")
             plt.ylabel(f" {metric_type.replace("_", " ")}")

        # Set Y-axis limits and ticks: from min to 1.1*max with 10 ticks
        # Handle both positive and negative values correctly
        if max_y_value > 0 and min_y_value >= 0:
            # All positive values
            y_max = max_y_value * 1.2
            y_min = 0
        elif max_y_value <= 0 and min_y_value < 0:
            # All negative values
            y_max = 0
            y_min = min_y_value * 1.2  # Make more negative (increase magnitude)
        else:
            # Mixed positive and negative values
            y_max = max_y_value * 1.2 if max_y_value > 0 else max_y_value * 0.8
            y_min = min_y_value * 1.2 if min_y_value < 0 else min_y_value * 0.8
        
        plt.ylim(y_min, y_max)
        
        # Create better tick values with cleaner decimals
        from matplotlib.ticker import MaxNLocator
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(nbins=10, prune='both'))
        
        # Add thin gray grid lines for better readability
        plt.grid(True, which='major', linestyle='-', linewidth=0.5, color='lightgray', alpha=0.7)
        plt.axhline(0, color='black', linewidth=1.2, linestyle='--')
        
        plt.legend()
        plt.tight_layout()
        
        # Add "Show Data Table" button below the plot
        button_ax = plt.axes([0.4, 0.02, 0.2, 0.04])
        button = plt.Button(button_ax, 'Show Data Table')
        button.on_clicked(lambda event: self.show_surface_data_table())
        
        plt.show()
    
    def show_surface_data_table(self):
        """Display a table with surface-by-surface data in a new window"""
        import tkinter as tk
        from tkinter import ttk
        
        # Create new window
        table_window = tk.Toplevel()
        table_window.title("STAR Performance Analysis - Data Table")
        table_window.geometry("800x600")
        
        # Create frame for table
        frame = tk.Frame(table_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview with scrollbars
        tree_scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
        tree_scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        
        tree = ttk.Treeview(frame, 
                           columns=("Surface", "Data Type", "Metric Value"),
                           show="headings",
                           yscrollcommand=tree_scroll_y.set,
                           xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Define column headings
        tree.heading("Surface", text="Surface")
        tree.heading("Data Type", text="Data Type")
        tree.heading("Metric Value", text="Metric Value")
        
        # Set column widths
        tree.column("Surface", width=150, anchor=tk.CENTER)
        tree.column("Data Type", width=300, anchor=tk.W)
        tree.column("Metric Value", width=200, anchor=tk.CENTER)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load data from results
        surfaces = self.results["surfaces"]
        starting_metric = self.results["starting_metric"]
        deformation_results = self.results["deformation"]
        deformation_results_RBM_only = self.results["deformation_RBM_only"]
        deformation_results_RBM_disabled = self.results["deformation_RBM_disabled"]
        temperature_results = self.results["temperature"]
        stress_results = self.results["stress"]
        direct_index_results = self.results["direct_index"]
        
        show_rbm_details = getattr(self, 'show_rbm_details', False)
        
        # Add starting metric row
        tree.insert("", tk.END, values=("Starting", "None (No STOP Effects)", f"{starting_metric:.6e}"))
        
        # Add data for each surface
        for i, surf_num in enumerate(surfaces):
            # Deformation data
            if show_rbm_details:
                if deformation_results_RBM_only[i] != 0:
                    tree.insert("", tk.END, values=(f"Surface {surf_num}", "Deformation (RBM Only)", f"{deformation_results_RBM_only[i]:.6e}"))
                if deformation_results_RBM_disabled[i] != 0:
                    tree.insert("", tk.END, values=(f"Surface {surf_num}", "Deformation (Without RBMs)", f"{deformation_results_RBM_disabled[i]:.6e}"))
            else:
                if deformation_results[i] != 0:
                    tree.insert("", tk.END, values=(f"Surface {surf_num}", "Deformation (With RBMs)", f"{deformation_results[i]:.6e}"))
            
            # Temperature data
            if temperature_results[i] != 0:
                tree.insert("", tk.END, values=(f"Surface {surf_num}", "Thermal", f"{temperature_results[i]:.6e}"))
            
            # Stress data
            if stress_results[i] != 0:
                tree.insert("", tk.END, values=(f"Surface {surf_num}", "Stress", f"{stress_results[i]:.6e}"))
            
            # Direct Index data
            if direct_index_results[i] != 0:
                tree.insert("", tk.END, values=(f"Surface {surf_num}", "Direct Index", f"{direct_index_results[i]:.6e}"))
        
        # Add close button
        close_btn = tk.Button(table_window, text="Close", command=table_window.destroy)
        close_btn.pack(pady=5)

    def plot_results_for_system_option(self, show_error_for="system"):
        #Main back end PLOTTING function  for "Show Error For -> SYSTEM" option.

        #Load results
        res = self.results
        metric_type = res["metric_type"]

        # Determine which STOP effects are present in the system
        has_deformations = len(self.surfaces_with_star_deformations) > 0
        has_temperatures = len(self.surfaces_with_star_temperature) > 0
        has_stress = len(self.surfaces_with_star_stress) > 0
        has_direct_index = len(self.surfaces_with_direct_index) > 0
        
        # Determine if RBM details should be shown
        show_rbm_details = getattr(self, 'show_rbm_details', False)

        # Build labels and values in the correct order: None → Deformation (RBM Only) → Deformation (Without RBMs) → Thermal → Direct Index → Stress → All STOP Data
        labels = ["None"]
        values = [res["starting_metric"]]
        colors = ["gray"]
        
        if has_deformations:
            if show_rbm_details:
                # Show RBM details: RBM Only first, then Without RBMs
                labels.append("Deformation (RBM Only)")
                values.append(res["deformation_RBM_only"])
                colors.append("darkgreen")
                
                labels.append("Deformation (Without RBMs)")
                values.append(res["deformation_without_RBMs"])
                colors.append("lightgreen")
            else:
                # Show combined deformation
                labels.append("Total Deformation")
                values.append(res["deformation"])
                colors.append("green")
        
        if has_temperatures:
            labels.append("Total Thermal")
            values.append(res["temperature"])
            colors.append("blue")
        
        if has_direct_index:
            labels.append("Total Direct Index")
            values.append(res["direct_index"])
            colors.append("orange")
        
        if has_stress:
            labels.append("Total Stress")
            values.append(res["stress"])
            colors.append("red")
        
        labels.append("All STOP Data")
        values.append(res["all_star_metric"])
        colors.append("purple")

        fig1=plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=colors)
        
        # Determine ylabel and title based on metric type
        if metric_type == "MF_Operand":
            plt.ylabel(f"{metric_type.replace('_', ' ')} : {self.metric_operand_type}")
            plt.title(f"STAR Performance Analysis | Show Error For: {show_error_for.capitalize()} | Error Type: Individual\n({metric_type}): {self.metric_operand_type}")
        else:
            plt.ylabel(metric_type.replace("_", " "))
            plt.title(f"STAR Performance Analysis | Show Error For: {show_error_for.capitalize()} | Error Type: Individual\n({metric_type})")
        
        # Set Y-axis limits and ticks with better decimal formatting
        max_y_value = np.max(values)
        min_y_value = np.min(values)
        
        # Handle both positive and negative values correctly
        if max_y_value > 0 and min_y_value >= 0:
            # All positive values
            y_max = max_y_value * 1.2
            y_min = 0
        elif max_y_value <= 0 and min_y_value < 0:
            # All negative values
            y_max = 0
            y_min = min_y_value * 1.2  # Make more negative (increase magnitude)
        else:
            # Mixed positive and negative values
            y_max = max_y_value * 1.2 if max_y_value > 0 else max_y_value * 0.8
            y_min = min_y_value * 1.2 if min_y_value < 0 else min_y_value * 0.8
        
        plt.ylim(y_min, y_max)
        
        # Create better tick values with cleaner decimals
        from matplotlib.ticker import MaxNLocator
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(nbins=10, prune='both'))
        
        # Add thin gray grid lines for better readability
        plt.grid(True, which='major', linestyle='-', linewidth=0.5, color='lightgray', alpha=0.7)
        plt.axhline(0, color='black', linewidth=1.2, linestyle='--')
        
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        
        # Add "Show Data Table" button below the plot
        button_ax = plt.axes([0.4, 0.02, 0.2, 0.04])
        button = plt.Button(button_ax, 'Show Data Table')
        button.on_clicked(lambda event: self.show_system_data_table())
        
        plt.show()
    
    def show_system_data_table(self):
        """Display a table with system-level data in a new window"""
        import tkinter as tk
        from tkinter import ttk
        
        # Create new window
        table_window = tk.Toplevel()
        table_window.title("STAR Performance Analysis - System Data Table")
        table_window.geometry("700x500")
        
        # Create frame for table
        frame = tk.Frame(table_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview with scrollbars
        tree_scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
        tree_scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        
        tree = ttk.Treeview(frame, 
                           columns=("Data Type", "Metric Value"),
                           show="headings",
                           yscrollcommand=tree_scroll_y.set,
                           xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Define column headings
        tree.heading("Data Type", text="Data Type")
        tree.heading("Metric Value", text="Metric Value")
        
        # Set column widths
        tree.column("Data Type", width=350, anchor=tk.W)
        tree.column("Metric Value", width=200, anchor=tk.CENTER)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load data from results
        res = self.results
        show_rbm_details = getattr(self, 'show_rbm_details', False)
        
        has_deformations = len(self.surfaces_with_star_deformations) > 0
        has_temperatures = len(self.surfaces_with_star_temperature) > 0
        has_stress = len(self.surfaces_with_star_stress) > 0
        has_direct_index = len(self.surfaces_with_direct_index) > 0
        
        # Add data rows in same order as plot
        tree.insert("", tk.END, values=("None (No STOP Effects)", f"{res['starting_metric']:.6e}"))
        
        if has_deformations:
            if show_rbm_details:
                tree.insert("", tk.END, values=("Deformation (RBM Only)", f"{res['deformation_RBM_only']:.6e}"))
                tree.insert("", tk.END, values=("Deformation (Without RBMs)", f"{res['deformation_without_RBMs']:.6e}"))
            else:
                tree.insert("", tk.END, values=("Total Deformation", f"{res['deformation']:.6e}"))
        
        if has_temperatures:
            tree.insert("", tk.END, values=("Total Thermal", f"{res['temperature']:.6e}"))
        
        if has_direct_index:
            tree.insert("", tk.END, values=("Total Direct Index", f"{res['direct_index']:.6e}"))
        
        if has_stress:
            tree.insert("", tk.END, values=("Total Stress", f"{res['stress']:.6e}"))
        
        tree.insert("", tk.END, values=("All STOP Data", f"{res['all_star_metric']:.6e}"))
        
        # Add close button
        close_btn = tk.Button(table_window, text="Close", command=table_window.destroy)
        close_btn.pack(pady=5)

    def run(self,error_type="Individual",show_error_for="surface"):
        #MAIN FUNCTION
        self.detect_surfaces_with_STOP_effects()
        if show_error_for.lower()=="surface":
            time_start_surface_errors=time.time()
            self.Calculate_contributions_For_Each_Surface(error_type=error_type)
            time_end_surface_errors=time.time() 
            print(f"Time-> {error_type}-> {time_end_surface_errors-time_start_surface_errors}")
            self.plot_resutls_for_surface_option(error_type=error_type, show_error_for=show_error_for)
        elif show_error_for.lower()=="system": 
            time_start_system_errors= time.time()
            #self.Calculate_contributions_For_Each_Surface(error_type=error_type)
            self.Calculate_Errors_For_System(metric_type=self.metric_type)
            time_end_system_errors=time.time() 
            print(f"Time ->System->{time_end_system_errors-time_start_system_errors}")
            self.plot_results_for_system_option(show_error_for=show_error_for)
        else:
            print("Select the Show Error Method. Surface or System")


class STAR_Performance_Analysis_UI : 
    #This is the main class used to generate the GUI 

    def __init__(self,master, performance_tool):
        #Initialzing the main frame
        self.master = master
        self.master.title("STAR Performance Analysis Tool")
        self.tool = performance_tool
        
        # ========== DISPLAY NAME MAPPING ==========
        # Map display names (shown in dropdown) to internal keys (used in code)
        self.display_name_map = {
            "RMS Spot Size": "RMS_Spot_Size",
            "Geometric MTF": "Geom_MTF",
            "Diffraction MTF": "Diff_MTF",
            "Telecentricity": "Telecentricity",
            "Centroid X Position": "Centroid_X_Position",
            "Centroid Y Position": "Centroid_Y_Position",
            "MF Operand": "MF_Operand",
            "MF Value": "MF_Value"
        }
        
        # Reverse mapping: internal key -> display name (for converting back)
        self.internal_to_display = {v: k for k, v in self.display_name_map.items()}
        # ===========================================
        
        # ========== METRIC CONFIGURATION SYSTEM ========== 
        # Define metric configurations for easy extensibility
        # Each metric can have custom operand, parameter names, and default values
        self.metric_configs = {
            "RMS_Spot_Size": {
                "operand": "RSCE",
                "operand_editable": True,  # User cannot change operand type for RMS_Spot_Size
                "parameters": [
                    {"name": "Ring", "default": "5"},
                    {"name": "Wave", "default": "1"},
                    {"name": "Hx", "default": "0"},
                    {"name": "Hy", "default": "0"}
                    # Only 4 parameters shown, P5-P8 will be set to 0 internally
                ],
                "show_help_link": True,
                "show_text": True,
                "text_content": "You might want to use RSCH"
            },
            "MF_Operand": {
                "operand": "EFFL",  # Default operand, user can change it
                "operand_editable": True,  # User can change operand type
                "parameters": [
                    {"name": "P1", "default": "0"},
                    {"name": "P2", "default": "0"},
                    {"name": "P3", "default": "0"},
                    {"name": "P4", "default": "0"},
                    {"name": "P5", "default": "0"},
                    {"name": "P6", "default": "0"},
                    {"name": "P7", "default": "0"},
                    {"name": "P8", "default": "0"}
                ],
                "show_help_link": True,
                "show_text": True,
                "text_content": "Type in the MF operand along with its parameters."
            },
            # TO ADD MORE METRICS IN THE FUTURE, just add a new entry here:
            # Example with custom text:
            "Diff_MTF": {
                "operand": "MTFA",
                "operand_editable": True,
                "parameters": [
                    {"name": "Samp", "default": "1"},
                    {"name": "Wave", "default": "0"},
                    {"name": "Field", "default": "1"},
                    {"name": "Freq", "default": "30"},
                    {"name": "Grid", "default": "0"},
                    {"name": "Data Type", "default": "0"}
                ],
                "show_help_link": True,
                "show_text": True,
                "text_content": "You might want to use MTFS or MTFT for different analysis types. Ensure that SAMP size is sufficient through the UI to ensure accurate calculation."
            },
            "Geom_MTF": {
                "operand": "GMTA",
                "operand_editable": True,
                "parameters": [
                 {"name": "Samp", "default": "1"},
                    {"name": "Wave", "default": "0"},
                    {"name": "Field", "default": "1"},
                    {"name": "Freq", "default": "30"},
                    {"name": "Scale", "default": "0"},
                    {"name": "Grid", "default": "0"}
                ],
                "show_help_link": True,
                "show_text": True,
                "text_content": "You might want to use GMTS or GMTT for different analysis types. Ensure that SAMP size is sufficient through the UI to ensure accurate calculation."
            },
            
            "Telecentricity": {
                "operand": "RANG",
                "operand_editable": False,
                "parameters": [
                 {"name": "SURF", "default": "1"},
                    {"name": "Wave", "default": "1"},
                    {"name": "Hx", "default": "0"},
                    {"name": "Px", "default": "0"},
                    {"name": "Hy", "default": "0"},
                    {"name": "Py", "default": "0"}
                ],
                "show_help_link": True,
                "show_text": True,
                "text_content": "Select the correct plane surface, and choose the other parameters accordingly."
            }
            ,
            
            "Centroid_X_Position": {
                "operand": "CENX",
                "operand_editable": False,
                "parameters": [
                 {"name": "SURF", "default": "1"},
                    {"name": "Wave", "default": "1"},
                    {"name": "Field", "default": "1"},
                    {"name": "Samp", "default": "5"},
                    {"name": "Pol", "default": "0"}
                ],
                "show_help_link": True,
                "show_text": True,
                "text_content": "Select the correct plane surface, and choose the other parameters accordingly."
            }
            ,
            
            "Centroid_Y_Position": {
                "operand": "CENY",
                "operand_editable": False,
                "parameters": [
                 {"name": "SURF", "default": "1"},
                    {"name": "Wave", "default": "1"},
                    {"name": "Field", "default": "1"},
                    {"name": "Samp", "default": "5"},
                    {"name": "Pol", "default": "0"}
                ],
                "show_help_link": True,
                "show_text": True,
                "text_content": "Select the correct plane surface, and choose the other parameters accordingly."
            }
        }
        # =================================================
        
        self.settings_frame = tk.Frame(master)
        self.settings_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        #Building the metric types section 
        tk.Label(self.settings_frame,text="Metric:").pack(side=tk.LEFT,padx=5) 
        self.metric_var = tk.StringVar() 
        
        # Use display names in the dropdown
        display_names = list(self.display_name_map.keys())
        self.metric_dropdown = ttk.Combobox(
            self.settings_frame, textvariable=self.metric_var,
            values=display_names,
            state="readonly"
        )
        self.metric_dropdown.set("RMS Spot Size")  # Set default using display name
        self.metric_dropdown.pack(side=tk.LEFT)
        self.metric_dropdown.bind("<<ComboboxSelected>>", self.update_parameter_fields)

        #Adding the "Error Type" Section 
        tk.Label(self.settings_frame, text="Error Type:").pack(side=tk.LEFT, padx=5)
        self.error_type_var = tk.StringVar()
        self.error_dropdown = ttk.Combobox(
            self.settings_frame, textvariable=self.error_type_var,
            values=["Individual", "Cumulative"], state="readonly"
        )
        self.error_dropdown.set("Individual")
        self.error_dropdown.pack(side=tk.LEFT)

        #Adding the "Show Error For" section
        tk.Label(self.settings_frame, text="Show Error For:").pack(side=tk.LEFT, padx=5)
        self.show_error_var = tk.StringVar()
        self.show_error_dropdown = ttk.Combobox(
            self.settings_frame, textvariable=self.show_error_var,
            values=["Surface", "System"], state="readonly"
        )
        self.show_error_dropdown.set("Surface")
        self.show_error_dropdown.pack(side=tk.LEFT)
        self.show_error_dropdown.bind("<<ComboboxSelected>>", self.update_error_type_options)

        #Adding the "Show RBM Details" checkbox
        self.show_rbm_details_var = tk.BooleanVar()
        self.show_rbm_details_var.set(False)
        self.rbm_checkbox = tk.Checkbutton(
            self.settings_frame, 
            text="Show Details for RBMs (if deformation loaded)", 
            variable=self.show_rbm_details_var
        )
        self.rbm_checkbox.pack(side=tk.LEFT, padx=10)

        #Adding the "Run" button 
        self.run_button = tk.Button(self.settings_frame, text="Run", command=self.run_analysis)
        self.run_button.pack(side=tk.LEFT, padx=10) 

        # Create dynamic operand parameter frame (replaces mf_operand_frame)
        self.operand_param_frame = tk.Frame(master)
        self.operand_label = None
        self.operand_entry = None
        self.param_entries = []
        
        # Add custom text info frame (displayed before help link)
        self.text_info_frame = tk.Frame(master)
        
        # Add help link frame
        self.help_link_frame = tk.Frame(master)
        help_text = tk.Label(self.help_link_frame, text="See the full operand list ")
        help_text.pack(side=tk.LEFT)
        
        # Create clickable link button
        self.link_button = tk.Label(self.help_link_frame, text="here", fg="blue", cursor="hand2", font=("Arial", 9, "underline"))
        self.link_button.pack(side=tk.LEFT)
        self.link_button.bind("<Button-1>", self.open_operand_documentation)
        
        # Initially hide extra fields
        self.update_parameter_fields()

    def open_operand_documentation(self, event=None):
        """Opens the Zemax operands documentation in the default web browser"""
        import webbrowser
        url = "https://ansyshelp.ansys.com/public/account/secured?returnurl=//Views/Secured/Zemax/v251/en/OpticStudio_User_Guide/OpticStudio_Help/topics/Optimization_Operands_Summary_Table.html"
        webbrowser.open(url)

    def update_error_type_options(self, event=None):
        """Update Error Type dropdown based on Show Error For selection"""
        show_for = self.show_error_var.get()
        if (show_for == "System"):
            # Disable Cumulative option for System
            self.error_dropdown.config(values=["Individual"])
            self.error_type_var.set("Individual")
        else:
            # Enable both options for Surface
            self.error_dropdown.config(values=["Individual", "Cumulative"])

    def update_parameter_fields(self, event=None):
        # Get display name from dropdown and convert to internal key
        display_name = self.metric_var.get()
        metric = self.display_name_map.get(display_name, display_name)  # Convert to internal key
        config = self.metric_configs.get(metric, {})
        
        # Hide frames first
        self.operand_param_frame.pack_forget()
        self.text_info_frame.pack_forget()
        self.help_link_frame.pack_forget()
        
        # Clear previous operand and parameter fields
        for widget in self.operand_param_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()
        
        # Check if this metric has a configuration
        if not config:
            # No configuration, don't show anything (e.g., MF_Value)
            self.master.update_idletasks()
            required_height = self.settings_frame.winfo_reqheight() + 40
            current_width = self.master.winfo_width()
            self.master.geometry(f"{current_width}x{required_height}")
            return
        
        # Add operand label (editable or fixed)
        if config.get("operand_editable", False):
            self.operand_label = tk.Label(self.operand_param_frame, text="Operand Type:")
            self.operand_label.pack(side=tk.LEFT)
            self.operand_entry = tk.Entry(self.operand_param_frame, width=6)
            self.operand_entry.insert(0, config.get("operand", ""))
            self.operand_entry.pack(side=tk.LEFT, padx=(0, 10))
        else:
            # Fixed operand, just show the operand type
            operand_text = f"Operand Type: {config.get('operand', '')}"
            self.operand_label = tk.Label(self.operand_param_frame, text=operand_text, font=("Arial", 9, "bold"))
            self.operand_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add parameter fields
        for param in config.get("parameters", []):
            param_label = tk.Label(self.operand_param_frame, text=f"{param['name']}:")
            param_label.pack(side=tk.LEFT, padx=(5, 1))  
            entry = tk.Entry(self.operand_param_frame, width=3)
            entry.insert(0, param.get("default", "0"))
            entry.pack(side=tk.LEFT, padx=(0, 5))  
            self.param_entries.append(entry)
        
        # Show operand parameter frame
        self.operand_param_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Show or hide custom text info
        if config.get("show_text", False):
            for widget in self.text_info_frame.winfo_children():
                widget.destroy()
            text_label = tk.Label(self.text_info_frame, text=config.get("text_content", ""), font=("Arial", 9))
            text_label.pack(side=tk.LEFT, padx=0)
            self.text_info_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Show or hide help link
        if config.get("show_help_link", False):
            self.help_link_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Auto-resize window to accommodate the fields
        self.master.update_idletasks()
        required_height = self.settings_frame.winfo_reqheight() + self.operand_param_frame.winfo_reqheight()
        if config.get("show_text", False):
            required_height += self.text_info_frame.winfo_reqheight()
        if config.get("show_help_link", False):
            required_height += self.help_link_frame.winfo_reqheight()
        required_height += 40
        
        current_width = self.master.winfo_width()
        # Set minimum width based on number of parameters
        num_params = len(config.get("parameters", []))
        if config.get("operand_editable", False):
            min_width = 800 if num_params >= 6 else 600
        else:
            min_width = 700 if num_params >= 4 else 500
        
        self.master.geometry(f"{max(current_width, min_width)}x{required_height}")

    def run_analysis(self):
        #Main function that runs tha analysis 
        # Get display name from dropdown and convert to internal key
        display_name = self.metric_var.get()
        metric = self.display_name_map.get(display_name, display_name)  # Convert to internal key
        
        error_type = self.error_type_var.get()
        show_for = self.show_error_var.get()
        show_rbm_details = self.show_rbm_details_var.get()

        self.tool.metric_type = metric  # Use internal key
        self.tool.show_rbm_details = show_rbm_details

        # Handle operand metrics
        config = self.metric_configs.get(metric, {})  # Use internal key
        if config.get("operand_editable", False):
            operand = self.operand_entry.get()
            self.tool.metric_operand_type = operand
        else:
            self.tool.metric_operand_type = config.get("operand", None)
        
        # Handle parameters
        S = [int(entry.get()) for entry in self.param_entries]
        self.tool.S = S + [0] * (8 - len(S))  # Pad to 8 parameters if needed

        self.tool.run(error_type=error_type, show_error_for=show_for.lower())


if __name__ == "__main__":
    # ========== CONFIGURATION SETTINGS ==========
    # Set these parameters (Zemax Version + TestFile) before running the script
    
    # Custom OpticStudio Directory Configuration
    USE_CUSTOM_VERSION = False  # Set to True to use custom OpticStudio directory
    CUSTOM_DIRECTORY = r"C:\Program Files\Ansys Zemax OpticStudio 2025 R1.01" # Only used if USE_CUSTOM_VERSION is True
    
    # Test file to load
    testFile = r".............\Desktop\Projects\OpticStudio\STAR Performance Analysis API\Example\ZemaxFile.zmx"
    
    # ============================================
    
    # Display startup information
    print("STAR Performance Analysis ZOS-API Package ")
    
    # Connect to ZOS with configurable directory
    if USE_CUSTOM_VERSION:
        print(f"Using custom OpticStudio version")
        print(f"Custom Directory: {CUSTOM_DIRECTORY}")
        zos = ZOSConnector(use_custom_directory=True, custom_directory=CUSTOM_DIRECTORY)
    else:
        print("Using default OpticStudio version from registry")
        zos = ZOSConnector()
    
    print("Loading UI application... Please wait couple of seconds")

    # Load system
    TheSystem = zos.TheSystem
    TheSystem.LoadFile(testFile, False)
    print(f"Loaded file: {testFile}")
    print("=" * 70)
    print()

    # Create Metrics instance
    metrics_tool = Metrics(zos)

    # Run the STAR Performance Analysis tool
    star_tool = STAR_Performance_Analysis_Back_End_Tool(zos, metrics_tool)
    root = tk.Tk()
    app = STAR_Performance_Analysis_UI(root, star_tool)
    root.mainloop()

    # Cleanup
    del zos
    zos = None
