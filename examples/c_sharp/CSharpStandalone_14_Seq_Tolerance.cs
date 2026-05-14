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
using ZOSAPI;

namespace CSharpStandaloneApplication
{
    class Program
    {
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

            BeginStandaloneApplication();
        }

        static void BeginStandaloneApplication()
        {
            // Create the initial connection class
            ZOSAPI_Connection TheConnection = new ZOSAPI_Connection();

            // Attempt to create a Standalone connection
            IZOSAPI_Application TheApplication = TheConnection.CreateNewApplication();
            if (TheApplication == null)
            {
                HandleError("An unknown connection error occurred!");
                return;
            }

            // Check the connection status
            if (!TheApplication.IsValidLicenseForAPI)
            {
                HandleError("Failed to connect to OpticStudio: " + TheApplication.LicenseStatus);
                return;
            }
            if (TheApplication.Mode != ZOSAPI_Mode.Server)
            {
                HandleError("User plugin was started in the wrong mode: expected Server, found " + TheApplication.Mode.ToString());
                return;
            }

            IOpticalSystem TheSystem = TheApplication.PrimarySystem;

            // creates new directory
            string strPath = System.IO.Path.Combine(TheApplication.SamplesDir, @"API\CS\e15_Seq_Optimization");
            System.IO.Directory.CreateDirectory(strPath);

            //! [e14s01_cs]
            // Open Double Gauss sample file
            string samplesFolder = TheApplication.SamplesDir;
            string DGfile = System.IO.Path.Combine(samplesFolder, "Sequential\\Objectives\\Double Gauss 28 degree field.zos");
            TheSystem.LoadFile(DGfile, false);
            //! [e14s01_cs]

            //! [e14s02_cs]
            // Set up the Tolerance Wizard and run it
            ZOSAPI.Wizards.ISEQToleranceWizard tWiz = TheSystem.TDE.SEQToleranceWizard;
            // Specify surface tolerances
            tWiz.SurfaceRadius = 0.1;
            tWiz.SurfaceThickness = 0.1;
            tWiz.SurfaceDecenterX = 0.1;
            tWiz.SurfaceDecenterY = 0.1;
            tWiz.SurfaceTiltX = 0.2;
            tWiz.SurfaceTiltY = 0.2;
            // Specify element tolerances
            tWiz.ElementDecenterX = 0.1;
            tWiz.ElementDecenterY = 0.1;
            tWiz.ElementTiltXDegrees = 0.2;
            tWiz.ElementTiltYDegrees = 0.2;
            // Specify tolerances not to be used
            tWiz.IsSurfaceSandAIrregularityUsed = false;
            tWiz.IsIndexUsed = false;
            tWiz.IsIndexAbbePercentageUsed = false;
            // Select OK
            tWiz.OK();
            //! [e14s02_cs]

            //! [e14s03_cs]
            // Create a "Double Gauss" folder in the Samples folder
            string dirLoc = System.IO.Path.Combine(samplesFolder, "API\\CS\\e14_seq_tolerance");
            System.IO.Directory.CreateDirectory(dirLoc);
            // Save a copy of the file in the Double Gauss folder
            string fileNameSeq = System.IO.Path.Combine(dirLoc, "Double Gauss (seq).zos");
            TheSystem.SaveAs(fileNameSeq);
            //! [e14s03_cs]

            //! [e14s04_cs]
            // Set up the Tolerancing analysis and run it
            ZOSAPI.Tools.Tolerancing.ITolerancing tol = TheSystem.Tools.OpenTolerancing();
            // Select Sensitivity mode
            tol.SetupMode = ZOSAPI.Tools.Tolerancing.SetupModes.Sensitivity;
            // Select Criterion and related settings 
            tol.Criterion = ZOSAPI.Tools.Tolerancing.Criterions.RMSSpotRadius;
            tol.CriterionSampling = 3;
            tol.CriterionComp = ZOSAPI.Tools.Tolerancing.CriterionComps.OptimizeAll_DLS;
            tol.CriterionCycle = 2;
            tol.CriterionField = ZOSAPI.Tools.Tolerancing.CriterionFields.UserDefined;
            // Select the number or MC runs and files to save
            tol.NumberOfRuns = 20;
            tol.NumberToSave = 20;
            // Run the Tolerancing analysis
            tol.RunAndWaitForCompletion();
            tol.Close();
            //! [e14s04_cs]

            //! [e14s05_cs]
            // Convert file to Non-sequential mode
            ZOSAPI.Tools.IConvertToNSCGroup convertNSmode = TheSystem.Tools.OpenConvertToNSCGroup();
            convertNSmode.ConvertFileToNSC = true;
            convertNSmode.RunAndWaitForCompletion();
            convertNSmode.Close();
            // Save the Non-sequential file to the Double Gauss folder
            string fileNameNS = System.IO.Path.Combine(dirLoc, "Double Gauss (NS).zos");
            TheSystem.SaveAs(fileNameNS);
            //! [e14s05_cs]

            // Clean up
            FinishStandaloneApplication(TheApplication);
        }

        static void FinishStandaloneApplication(IZOSAPI_Application TheApplication)
        {
            // Note - TheApplication will close automatically when this application exits, so this isn't strictly necessary in most cases
            if (TheApplication != null)
            {
                TheApplication.CloseApplication();
            }
        }

        static void LogInfo(string message)
        {
            // TODO - add custom logging
            Console.WriteLine(message);
        }

        static void HandleError(string errorMessage)
        {
            // TODO - add custom error handling
            throw new Exception(errorMessage);
        }

    }
}
