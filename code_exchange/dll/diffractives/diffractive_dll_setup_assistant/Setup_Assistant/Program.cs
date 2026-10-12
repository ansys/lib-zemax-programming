using System;
using ZOSAPI;

namespace Diffractive_DLL_Setup_Assistant
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
            
            BeginUserExtension();
        }

        static void BeginUserExtension()
        {
            // Create the initial connection class
            ZOSAPI_Connection TheConnection = new ZOSAPI_Connection();

            // Attempt to connect to the existing OpticStudio instance
            IZOSAPI_Application TheApplication = null;
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
                HandleError("User plugin was started in the wrong mode: expected Plugin, found " + TheApplication.Mode.ToString());
                return;
            }
			
            // Chech the connection status
            if (!TheApplication.IsValidLicenseForAPI)
            {
                HandleError("Failed to connect to OpticStudio: " + TheApplication.LicenseStatus);
                return;
            }

            TheApplication.ProgressPercent = 0;
            TheApplication.ProgressMessage = "Running Extension...";

            IOpticalSystem TheSystem = TheApplication.PrimarySystem;
            if (TheSystem.Mode != SystemType.NonSequential)
            {
                System.Windows.Forms.MessageBox.Show("The extension only works in non-sequential mode.");
                return;
            }
            Form1 aaa = new Form1(TheSystem);
            System.Windows.Forms.Application.Run(aaa);


            // Clean up
            FinishUserExtension(TheApplication);
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
            // TODO - add custom error handling
            throw new Exception(errorMessage);
        }

    }
}
