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
using ZOSAPI.Editors;
using ZOSAPI.Editors.LDE;
using ZOSAPI.SystemData;
using ZOSAPI.Tools.General;

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

            // Add your custom code here...

            // creates a new API directory
            string strPath = System.IO.Path.Combine(TheApplication.SamplesDir, @"API\\CS");
            System.IO.Directory.CreateDirectory(strPath);

            // Set up primary optical system
            string sampleDir = TheApplication.SamplesDir;
            string testFile = sampleDir + "\\API\\CS\\e01_new_file_and_quickfocus.zos";

            //! [e01s01_cs]
            // Make new file
            TheSystem.New(false);
            TheSystem.SaveAs(testFile);
            //! [e01s01_cs]

            TheSystem.SystemData.MaterialCatalogs.AddCatalog("SCHOTT");

            //! [e01s02_cs]
            // Aperture
            ISystemData TheSystemData = TheSystem.SystemData;
            TheSystemData.Aperture.ApertureValue = 40;
            //! [e01s02_cs]

            //! [e01s03_cs]
            // Fields
            IField Field_1 = TheSystemData.Fields.GetField(1);
            IField NewField_2 = TheSystemData.Fields.AddField(0, 5.0, 1.0);
            //! [e01s03_cs]

            //! [e01s04_cs]
            // Wavelength preset
            bool slPreset = TheSystemData.Wavelengths.SelectWavelengthPreset(WavelengthPreset.d_0p587);
            //! [e01s04_cs]

            //! [e01s05_cs]
            // Lens data 
            ILensDataEditor TheLDE = TheSystem.LDE;
            TheLDE.InsertNewSurfaceAt(2);
            TheLDE.InsertNewSurfaceAt(2);
            ILDERow Surface_1 = TheLDE.GetSurfaceAt(1);
            ILDERow Surface_2 = TheLDE.GetSurfaceAt(2);
            ILDERow Surface_3 = TheLDE.GetSurfaceAt(3);
            //! [e01s05_cs]

            //! [e01s06_cs]
            // Changes surface cells in LDE
            Surface_1.Thickness = 50.0;
            Surface_1.Comment = "Stop is free to move";
            Surface_2.Radius = 100.0;
            Surface_2.Thickness = 10.0;
            Surface_2.Comment = "front of lens";
            Surface_2.Material = "N-BK7";
            Surface_3.Comment = "rear of lens";
            //! [e01s06_cs]

            //! [e01s07_cs]
            // Solver
            ISolveData Solver = Surface_3.RadiusCell.CreateSolveType(SolveType.FNumber);
            Solver._S_FNumber.FNumber = 10;
            Surface_3.RadiusCell.SetSolveData(Solver);
            //! [e01s07_cs]

            //! [e01s08_cs]
            // QuickFocus
            IQuickFocus quickFocus = TheSystem.Tools.OpenQuickFocus();
            quickFocus.Criterion = QuickFocusCriterion.SpotSizeRadial;
            quickFocus.UseCentroid = true;
            quickFocus.RunAndWaitForCompletion();
            quickFocus.Close();
            //! [e01s08_cs]

            //! [e01s09_cs]
            // Save and close
            TheSystem.Save();
            //! [e01s09_cs]

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
