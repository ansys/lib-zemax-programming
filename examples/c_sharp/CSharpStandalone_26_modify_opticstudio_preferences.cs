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
using ZOSAPI.Preferences;

namespace CSharpStandaloneApplication4
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
            
            // Define a Preferences File.
            // Preferences file is defined on the IZOSAPIConnection interface (prior to connecting to the API)
            // If no PreferencesFile is defined it will use the default OpticStudio.CFG file however changes will not persist between sessions. 
            // If a PreferencesFile is defined, then any changes will save automatically. 
            //! [e26s05_cs]
            Console.WriteLine("===PreferencesFile===");
            string cfgFile = @"C:\Users\Documents\Zemax\Configs\OpticStudio.CFG";
            if (System.IO.File.Exists(cfgFile))
            {
                TheConnection.PreferencesFile = cfgFile;
                Console.WriteLine("PreferencesFile: " + TheConnection.PreferencesFile);
            }
            else
            {
                Console.WriteLine("Default OpticStudio.CFG prefernces used");
            }
            //! [e26s05_cs]

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

            //! [e26s01_cs]
            // Define variables for OpticStudio Preferences
            IPreferences Preference = TheApplication.Preferences;
            IPreferencesGeneral PrefG = Preference.General;
            //! [e26s01_cs]

            //! [e26s02_cs]
            // Read and print the initial settings
            Console.WriteLine("\n===Check Settings===");
            Console.WriteLine("DateTimeFormat: " + PrefG.DateTimeFormat);
            Console.WriteLine("Language: " + PrefG.Language);
            Console.WriteLine("ZMXFileEncoding: " + PrefG.ZMXFileEncoding);
            Console.WriteLine("TXTFileEncoding: " + PrefG.TXTFileEncoding);
            Console.WriteLine("UseSessionFiles: " + PrefG.UseSessionFiles);
            Console.WriteLine("IncludeCalculatedDataInsession: " + PrefG.IncludeCalculatedDataInSession);
            Console.WriteLine("UpdateMostRecentlyUsedList: " + PrefG.UpdateMostRecentlyUsedList);
            Console.WriteLine("UserPreferences: " + PrefG.UserPreferences);
            //! [e26s02_cs]

            //! [e26s03_cs]
            // Reset the settings to default
            Preference.ResetToDefaults();
            //! [e26s03_cs]

            //! [e26s04_cs]
            // Set the settings            
            PrefG.DateTimeFormat = ZOSAPI.Preferences.DateTimeType.DateTime;
            PrefG.Language = ZOSAPI.Preferences.LanguageType.English;
            PrefG.ZMXFileEncoding = ZOSAPI.Preferences.EncodingType.ANSI;
            PrefG.TXTFileEncoding = ZOSAPI.Preferences.EncodingType.ANSI;
            PrefG.UseSessionFiles = false;
            PrefG.IncludeCalculatedDataInSession = false;
            PrefG.UpdateMostRecentlyUsedList = false;
            PrefG.UserPreferences = "Never gonna run around and desert you";
            //! [e26s04_cs] 

            Console.WriteLine("\n===Final Settings===");
            Console.WriteLine("DateTimeFormat: " + PrefG.DateTimeFormat);
            Console.WriteLine("Language: " + PrefG.Language);
            Console.WriteLine("ZMXFileEncoding: " + PrefG.ZMXFileEncoding);
            Console.WriteLine("TXTFileEncoding: " + PrefG.TXTFileEncoding);
            Console.WriteLine("UseSessionFiles: " + PrefG.UseSessionFiles);
            Console.WriteLine("IncludeCalculatedDataInsession: " + PrefG.IncludeCalculatedDataInSession);
            Console.WriteLine("UpdateMostRecentlyUsedList: " + PrefG.UpdateMostRecentlyUsedList);
            Console.WriteLine("UserPreferences: " + PrefG.UserPreferences);

            Console.WriteLine("\nPress any key to continue...");
            Console.ReadKey();




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
