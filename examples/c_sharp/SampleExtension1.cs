// Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
// SPDX-License-Identifier: MIT
//
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;
using ZOSAPI;
using ZOSAPI.Analysis;
using ZOSAPI.Editors;
using ZOSAPI.Editors.LDE;
using ZOSAPI.Editors.MFE;
using ZOSAPI.Tools;
using ZOSAPI.Tools.Optimization;

namespace SampleExtension1
{
    class SampleExtension1
    {
        private static IZOSAPI_Application TheApplication;

        static void Main(string[] args)
        {
            // Find the installed version of OpticStudio
            bool isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize();
            // Note -- uncomment the following line to use a custom initialization path
            //bool isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(@"C:\Program Files\OpticStudio\");
            if (isInitialized)
            {
                LogInfo("Found OpticStudio at: " + ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory());
            }
            else
            {
                HandleError("Failed to locate OpticStudio!");
                return;
            }

            BeginUserExtension();
        }

        static void BeginUserExtension()
        {
            // Create the initial connection class
            ZOSAPI_Connection TheConnection = new ZOSAPI_Connection();

            // Attempt to connect to the existing OpticStudio instance
            TheApplication = null;
            try
            {
                TheApplication = TheConnection.ConnectToApplication(); // this will throw an exception if not launched from OpticStudio
            }
            catch (Exception ex)
            {
                HandleError(ex.Message);
                return;
            }
            if (TheApplication == null)
            {
                HandleError("An unknown connection error occurred!");
                return;
            }
            if (TheApplication.Mode != ZOSAPI_Mode.Plugin)
            {
                HandleError("User plugin was started in the wrong mode: expected Extension, found " + TheApplication.Mode.ToString());
                return;
            }

            // Chech the connection status
            if (!TheApplication.IsValidLicenseForAPI)
            {
                HandleError("Failed to connect to OpticStudio: " + TheApplication.LicenseStatus);
                return;
            }

            TheApplication.ProgressPercent = 0;
            TheApplication.ProgressMessage = "Configuring the new system...";

            IOpticalSystem TheSystem = TheApplication.PrimarySystem;

            //  Identify the primary system and create a fresh one
            TheSystem.MakeSequential();
            TheSystem.New(saveIfNeeded: false);

            //  Set up the System Data
            TheSystem.SystemData.Units.LensUnits = ZOSAPI.SystemData.ZemaxSystemUnits.Millimeters;
            TheSystem.SystemData.Aperture.ApertureType = ZOSAPI.SystemData.ZemaxApertureType.EntrancePupilDiameter;
            TheSystem.SystemData.Aperture.ApertureValue = 10.0;
            TheSystem.SystemData.Fields.SetFieldType(ZOSAPI.SystemData.FieldType.Angle);
            TheSystem.SystemData.Fields.AddField(0.0, 7.0, 1.0);
            TheSystem.SystemData.Fields.AddField(0.0, 10.0, 1.0);
            TheSystem.SystemData.Wavelengths.SelectWavelengthPreset(ZOSAPI.SystemData.WavelengthPreset.FdC_Visible);

            //  Set up the Lens Data
            //  Glasses:  N-BAF10, SF10
            //  Diameter:  10 mm
            //  Solve radii of last surface for F/# = F/5

            //  Assumes a New Lens with three (x3) surfaces

            //  Best design practice is to start out with a good paraxial design
            //  Starting with nothing often causes chaos

            double diamLens = 10.0;
            double fNo = 5.0;
            double efl = diamLens * fNo;

            //  Infinite conjugate and split the power between the elements

            double indexEstimate = 1.5;
            double powerTotal = 1.0 / efl;
            double powerEach = powerTotal / 2.0;
            double rocEach = 1.0 / (powerEach / (indexEstimate - 1.0));
            double thickEach = rocEach / 10.0;

            //  Add the necessary surfaces with reasonable default values

            ILensDataEditor editorLensData = TheSystem.LDE;

            ILDERow surfaceTemp = editorLensData.GetSurfaceAt(1);
            surfaceTemp.Material = "N-BAF10";
            surfaceTemp.Thickness = thickEach;
            surfaceTemp.Radius = rocEach;
            SetVariableSolve(surfaceTemp.ThicknessCell);
            SetVariableSolve(surfaceTemp.RadiusCell);

            editorLensData.InsertNewSurfaceAt(2);
            surfaceTemp = editorLensData.GetSurfaceAt(2);
            surfaceTemp.Material = "SF10";
            surfaceTemp.Thickness = thickEach;
            SetVariableSolve(surfaceTemp.ThicknessCell);
            SetVariableSolve(surfaceTemp.RadiusCell);

            editorLensData.InsertNewSurfaceAt(3);
            surfaceTemp = editorLensData.GetSurfaceAt(3);
            surfaceTemp.Thickness = efl;
            surfaceTemp.Radius = -rocEach;
            SetVariableSolve(surfaceTemp.ThicknessCell);

            //  Add the F/# solve
            ISolveFNumber solveFNo = surfaceTemp.RadiusCell.CreateSolveType(SolveType.FNumber) as ISolveFNumber;
            if (solveFNo == null)
            {
                HandleError("Could not create F# solve!");
                return;
            }
            else
            {
                solveFNo.FNumber = 5.0;
                SolveStatus iSS = surfaceTemp.RadiusCell.SetSolveData(solveFNo); //  Send data to LDE
                if (iSS != ZOSAPI.Editors.SolveStatus.Success)
                {
                    HandleError("Solve Failure");
                    return;
                }
            }

            if (!TheApplication.TerminateRequested)
            {
                TheApplication.ProgressMessage = "Configuring the MFE";

                // Load a previously saved merit fn
                IMeritFunctionEditor editorMeritFn = TheSystem.MFE;

                string zemaxDir = TheApplication.ZemaxDataDir;
                string meritDir = Path.Combine(zemaxDir, "MeritFunction");
                string mfFile = Path.Combine(meritDir, "RMS Spot Size.MF");
                if (File.Exists(mfFile))
                {
                    editorMeritFn.LoadMeritFunction(mfFile);
                }
                else
                {
                    HandleError("Could not find merit function!");
                    return;
                }

                // Lets insert our own boundary constraints
                int operandPos = FindComment(editorMeritFn, "glass boundary constraints");
                if (operandPos <= 0)
                {
                    operandPos = 4;
                }
                ++operandPos; // start at the cell after the BLNK operand
                // min glass thickness of 2
                IMFERow operandTemp = editorMeritFn.InsertNewOperandAt(operandPos++);
                operandTemp.ChangeType(MeritOperandType.MNCG);
                operandTemp.GetOperandCell(MeritColumn.Param1).IntegerValue = 1;
                operandTemp.GetOperandCell(MeritColumn.Param2).IntegerValue = 3;
                operandTemp.Target = 2.0;
                operandTemp.Weight = 1.0;
                // max glass thickness of 10
                operandTemp = editorMeritFn.InsertNewOperandAt(operandPos++);
                operandTemp.ChangeType(MeritOperandType.MXCG);
                operandTemp.GetOperandCell(MeritColumn.Param1).IntegerValue = 1;
                operandTemp.GetOperandCell(MeritColumn.Param2).IntegerValue = 3;
                operandTemp.Target = 10.0;
                operandTemp.Weight = 1.0;
                // minimum edge thickness of .5
                operandTemp = editorMeritFn.InsertNewOperandAt(operandPos++);
                operandTemp.ChangeType(MeritOperandType.MNEG);
                operandTemp.GetOperandCell(MeritColumn.Param1).IntegerValue = 1;
                operandTemp.GetOperandCell(MeritColumn.Param2).IntegerValue = 3;
                operandTemp.GetOperandCell(MeritColumn.Param3).DoubleValue = 0.0;
                operandTemp.Target = .5;
                operandTemp.Weight = 1.0;

                //  Time to optimize using the Local Optimizer ('Optimize' in the UI)
                IOpticalSystemTools tools = TheSystem.Tools;
                ILocalOptimization optimizer = tools.OpenLocalOptimization();

                // keep running 10 fixed cycles until the merit function value stops decreasing
                optimizer.Cycles = OptimizationCycles.Fixed_1_Cycle;
                double currentMF = optimizer.InitialMeritFunction;  //  READ ONLY
                double lastMF = currentMF;
                const int maxCycle = 100;
                const double minDeltaFrac = .0001;
                int currentCycle = 0;
                bool isFinished;
                do
                {
                    ++currentCycle;
                    TheApplication.ProgressMessage = String.Format("Optimizing... (Cycle #{0}, MF: {1:g5})", currentCycle, currentMF);
                    lastMF = currentMF;
                    optimizer.RunAndWaitForCompletion();
                    currentMF = optimizer.CurrentMeritFunction;
                    // stop when the change in the MF value is below the threshold
                    isFinished = (lastMF - currentMF) <= (minDeltaFrac * lastMF);
                } while (!isFinished && currentCycle < maxCycle && !TheApplication.TerminateRequested);
                optimizer.Close();  // should always close any system tool when it is no longer needed, and it must be closed before opening any other tool
            }

            I_Analyses analysisZemax = TheSystem.Analyses;
            if (!TheApplication.TerminateRequested)
            {
                // Create a Huygens PSF
                TheApplication.ProgressMessage = "Running a Huygens PSF";
                IA_ psfHuygens = analysisZemax.New_HuygensPsf();
                psfHuygens.Terminate(); // Stop it if it is already running
                psfHuygens.WaitForCompletion();
                // configure the settings
                ZOSAPI.Analysis.Settings.Psf.IAS_HuygensPsf HuygensPSF_Settings = psfHuygens.GetSettings() as ZOSAPI.Analysis.Settings.Psf.IAS_HuygensPsf;
                HuygensPSF_Settings.ImageSampleSize = SampleSizes._128x128; 
                HuygensPSF_Settings.PupilSampleSize = SampleSizes._128x128;
                HuygensPSF_Settings.ShowAsType = HuygensShowAsTypes.FalseColor;

                // run the analysis with the new settings
                IMessage iM_Apply = psfHuygens.Apply();
                if (iM_Apply != null && iM_Apply.ErrorCode != ErrorType.Success)
                {
                    HandleError(iM_Apply.Text);
                }

                // Create a Huygens MTF
                TheApplication.ProgressMessage = "Running a Huygens MTF";
                IA_ mtfHuygens = analysisZemax.New_HuygensMtf();
                mtfHuygens.Terminate(); // Stop it if it is already running
                mtfHuygens.WaitForCompletion();
                // configure the settings
                ZOSAPI.Analysis.Settings.Mtf.IAS_HuygensMtf HuygensMTF_Settings = mtfHuygens.GetSettings() as ZOSAPI.Analysis.Settings.Mtf.IAS_HuygensMtf;
                HuygensMTF_Settings.ImageSampleSize = SampleSizes._128x128; 
                HuygensMTF_Settings.PupilSampleSize = SampleSizes._128x128;

                // run the analysis with the new settings
                iM_Apply = mtfHuygens.Apply();
                if (iM_Apply != null && iM_Apply.ErrorCode != ErrorType.Success)
                {
                    HandleError(iM_Apply.Text);
                }

                TheApplication.ProgressMessage = "Waiting for the analyses to finish...";
                bool isRunning;
                do
                {
                    isRunning = psfHuygens.IsRunning() || mtfHuygens.IsRunning();
                    if (isRunning) System.Threading.Thread.Sleep(200);
                } while (isRunning && !TheApplication.TerminateRequested);
            }

            // Clean up
            FinishUserExtension(TheApplication);
        }

        private static int FindComment(IMeritFunctionEditor editorMeritFn, string comment)
        {
            int numberOfOperands = editorMeritFn.NumberOfOperands;
            for (int i = 1; i <= numberOfOperands; ++i)
            {
                IMFERow operand = editorMeritFn.GetOperandAt(i);
                if (operand.Type == MeritOperandType.BLNK)
                {
                    if (operand.GetOperandCell(MeritColumn.Comment).Value.Contains(comment))
                        return i;
                }
            }
            return -1;
        }

        private static void SetVariableSolve(IEditorCell cell)
        {
            SortedSet<SolveType> availableSolves = new SortedSet<SolveType>(cell.GetAvailableSolveTypes());
            if (availableSolves.Contains(SolveType.Variable))
                cell.SetSolveData(cell.CreateSolveType(SolveType.Variable));
            else
                HandleError("Could not set Variable solve!");
        }

        static void FinishUserExtension(IZOSAPI_Application TheApplication)
        {
            // Note - OpticStudio will stay in User Extension mode until this application exits
            if (TheApplication != null)
            {
                TheApplication.ProgressMessage = "Complete";
                TheApplication.ProgressPercent = 100;
            }
        }

        static void LogInfo(string message)
        {
            // TODO - add custom logging
            Console.WriteLine(message);
        }

        static void HandleError(string errorMessage)
        {
            TheApplication.ProgressMessage = errorMessage;
            TheApplication.ProgressPercent = 100;
            System.Threading.Thread.Sleep(3000);

        }

    }
}
