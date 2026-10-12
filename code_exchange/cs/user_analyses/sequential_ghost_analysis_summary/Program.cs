using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZOSAPI;
using ZOSAPI.Analysis;
using ZOSAPI.Common;

namespace GhostAnalysisSummary
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
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

            BeginUserAnalysis();
        }

        static void BeginUserAnalysis()
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

            // Check the connection status
            if (!TheApplication.IsValidLicenseForAPI)
            {
                HandleError("Failed to connect to OpticStudio: " + TheApplication.LicenseStatus);
                return;
            }

            switch (TheApplication.Mode)
            {
                case ZOSAPI_Mode.UserAnalysis:
                    RunUserAnalysis(TheApplication);
                    break;
                case ZOSAPI_Mode.UserAnalysisSettings:
                    ShowUserAnalysisSettings(TheApplication);
                    break;
                default:
                    HandleError("User plugin was started in the wrong mode: expected UserAnalysis, found " + TheApplication.Mode.ToString());
                    return;
            }

            // Clean up
            FinishUserAnalysis(TheApplication);
        }

        static void RunUserAnalysis(IZOSAPI_Application TheApplication)
        {
            IOpticalSystem TheSystem = TheApplication.PrimarySystem;

            IUserAnalysisData TheAnalysisData = TheApplication.UserAnalysisData;
            ISettingsData TheSettings = TheAnalysisData.UserSettings;

            // Add your custom code here...
            TheAnalysisData.WindowTitle = "Ghost Analysis Summary";

            //GetOperandValue (MeritOperandType type, int srf, int wave, double Hx, double Hy, double Px, double Py, double Ex, double Ey)                        
            //0 for Pupil Focus and 1 for Image Ghost
            double PupilGhost = 0;
            double ImageGhost = 0;
            int lastsurface = TheSystem.LDE.NumberOfSurfaces;

            //Define (declare and initialize arrays)
            List<double> surf1_list = new List<double>();
            List<double> surf2_list = new List<double>();
            List<double> PupilGhost_list = new List<double>();
            List<double> ImageGhost_list = new List<double>();                    

            // Write a text report
            System.Text.StringBuilder sbReport = new System.Text.StringBuilder();
            sbReport.Append("Running the Ghost Focus Generator for Double Bounce for all the surfaces in the system."+"\n\n");
            sbReport.Append("Pupil Ghost" + "\t\t\t\t\t\t\t" + "Image Ghost"+ "\n");           
            sbReport.Append("No" + "\t" + "Surf1: " + "\t" + "Surf2: " + "\t" + "Pupil Ghost: " + "\t" + "Surf1: " + "\t" + "Surf2: " + "\t" + "Image Ghost: " + "\n");
            
            IUserTextData userText = TheAnalysisData.MakeText();
            int surf1 = 1;
            int surf2=1;
            do
            {
                surf2 = 1;
                do
                { 
                //0 for Pupil Focus and 1 for Image Ghost
                PupilGhost = TheSystem.MFE.GetOperandValue(ZOSAPI.Editors.MFE.MeritOperandType.GPIM, surf1, surf2, 0, 0, 0, 0, 0, 0);
                ImageGhost = TheSystem.MFE.GetOperandValue(ZOSAPI.Editors.MFE.MeritOperandType.GPIM, surf1, surf2, 1, 0, 0, 0, 0, 0);
                //Console.WriteLine(surf1);
                //Console.WriteLine(surf2);
                //Console.WriteLine(value);

                if ((PupilGhost != 0)&&(ImageGhost != 0))
                            
                {
                    PupilGhost = 1 / PupilGhost;
                    ImageGhost = 1 / ImageGhost;                 

                    //Fill the array
                    surf1_list.Add(surf1);
                    surf2_list.Add(surf2);
                    PupilGhost_list.Add(PupilGhost);
                    ImageGhost_list.Add(ImageGhost);

                    //userText.Data = surf1.ToString()+" "+surf2.ToString() + " " + PupilGhost.ToString() + " " + ImageGhost.ToString();
                    //sbReport.Append(surf1.ToString() + "\t" + surf2.ToString() + "\t" + PupilGhost.ToString() + "\t" + ImageGhost.ToString() + "\n");
                    /*surf1++;
                    if (surf1 == surf2)
                    {
                        surf1 = 1;
                        surf2++;
                    }*/
                    }
                    surf2++;
                } while (surf2 <= lastsurface);

                surf1++;
            } while (surf1<= lastsurface);
            //Console.ReadKey();
            //userText.Data = sbReport.ToString();

            // This will give you a double array with the items of the list.
            double[] surf1Array = surf1_list.ToArray();
            double[] surf2Array = surf2_list.ToArray();
            double[] PupilGhostArray = PupilGhost_list.ToArray();
            double[] ImageGhostArray = ImageGhost_list.ToArray();            
            double[] PupilGhostSorted = PupilGhost_list.ToArray();
            double[] ImageGhostSorted = ImageGhost_list.ToArray();
            double[,] surf12PupilSorted = new double [surf1Array.Length, surf1Array.Length];
            double[,] surf12ImageSorted = new double[surf1Array.Length, surf1Array.Length];

            // Sort array in ascending order.
            int[] VectPupilSorted = new int[surf1Array.Length];
            int[] VectImageSorted = new int[surf1Array.Length];

            int size = surf1Array.Length;

            for (int i = 0; i < size; i++)
            {
                VectPupilSorted[i] = i;
                VectImageSorted[i] = i;
            }

            Array.Sort(PupilGhostSorted, VectPupilSorted);
            Array.Sort(ImageGhostSorted, VectImageSorted);

            for (int i = PupilGhostSorted.Length - 1 ; i >=0; i--)
            {
                // Display sorted list
                sbReport.Append((i+1).ToString() + "\t" + Math.Round(surf1Array[VectPupilSorted[size-1-i]],3).ToString() + "\t\t" + Math.Round(surf2Array[VectPupilSorted[size - 1 - i]],3).ToString() + "\t\t" + Math.Round(PupilGhostSorted[size - 1 - i],3).ToString() + "\t\t\t");
                sbReport.Append(Math.Round(surf1Array[VectImageSorted[size-1-i]],3).ToString() + "\t\t" + Math.Round(surf2Array[VectImageSorted[size - 1 - i]],3).ToString() + "\t\t" + Math.Round(ImageGhostSorted[size - 1 - i],3).ToString() + "\n");

            }




            // reverse array 
            //Array.Reverse(PupilGhostSorted);

            //PupilGhostSorted = PupilGhostArray.OrderByDescending(c => c).ToArray();
            //ImageGhostSorted = ImageGhostArray.OrderByDescending(c => c).ToArray();

            // print all element of array 
            //foreach (double value in PupilGhostSorted)
            //{
            //    // Display sorted list 
            //    sbReport.Append(value.ToString() + " \n");
            //}


            //for (int i = 0; i < PupilGhostSorted.Length; i++)
            //{
            //    // Display sorted list 
            //    //sbReport.Append(PupilGhostSorted[i].ToString() + " \n");
            //    int j = 0;
            //    do
            //    {
            //        if (PupilGhostArray[j] == PupilGhostSorted[i])
            //        {
            //            surf12PupilSorted[i,0] = surf1Array[j];
            //            surf12PupilSorted[i,1] = surf2Array[j];
            //            break;
            //        }                  

            //    } while (j < PupilGhostSorted.Length);

            //    j = 0;
            //    do
            //    {
            //        if (ImageGhostArray[j] == ImageGhostSorted[i])
            //        {
            //            surf12ImageSorted[i, 0] = surf1Array[j];
            //            surf12ImageSorted[i, 1] = surf2Array[j];
            //            break;
            //        }
            //        j = j + 1;
            //    } while (j < PupilGhostSorted.Length);                             

            //    sbReport.Append(surf12PupilSorted[i,0].ToString() + "\t" + surf12PupilSorted[i,1].ToString() + "\t" + PupilGhostSorted[i].ToString() + "\t");
            //    sbReport.Append(surf12ImageSorted[i, 0].ToString() + "\t" + surf12ImageSorted[i, 1].ToString() + "\t" + ImageGhostSorted[i].ToString() + "\n");

            //}                                 

            userText.Data = sbReport.ToString();
                                 

            // Use TheAnalysisData to create a specific plot type and populate the data
            //IUser2DLineData linePlot = TheAnalysisData.Make2DLinePlot("New 2D Line Plot", 1, new double[] { 1, 2, 3 });
            //linePlot.AddSeries(...);
        }

        static void ShowUserAnalysisSettings(IZOSAPI_Application TheApplication)
        {
            IOpticalSystem TheSystem = TheApplication.PrimarySystem;

            IUserAnalysisData TheAnalysisData = TheApplication.UserAnalysisData;
            ISettingsData TheSettings = TheAnalysisData.UserSettings;

            // TODO - retrieve the settings specific to your analysis here

            // This will show a form to modify your settings (currently blank)...
            AnalysisSettingsForm SettingsForm = new AnalysisSettingsForm();
            // Add your custom code here, and to the SettingsForm...
            System.Windows.Forms.Application.Run(SettingsForm);            

            // TODO - write settings back to TheSettings
        }

        static void FinishUserAnalysis(IZOSAPI_Application TheApplication)
        {
            // Note - OpticStudio will wait for the operand to complete until this application exits 
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
