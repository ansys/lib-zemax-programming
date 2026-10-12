using System;
using System.IO;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZOSAPI;
using ZOSAPI.Analysis;
using ZOSAPI.Common;
using ZOSAPI.Editors.NCE;
using System.Reflection;

namespace RadianceCamera
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
            if (TheApplication.PrimarySystem.Mode != SystemType.NonSequential)
            {
                System.Windows.Forms.MessageBox.Show("The Analysis only works in non-sequential mode.");
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

        static double[] triY_wav = new double[] 
        {
            360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,697,698,699,700,701,702,703,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,754,755,756,757,758,759,760,761,762,763,764,765,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811,812,813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830
        };
        static double[] triY_Y = new double[] 
        {
            0.000003917,0.000004393581,0.000004929604,0.000005532136,0.000006208245,0.000006965,0.000007813219,0.000008767336,0.000009839844,0.00001104323,0.00001239,0.00001388641,0.00001555728,0.00001744296,0.00001958375,0.00002202,0.00002483965,0.00002804126,0.00003153104,0.00003521521,0.000039,0.0000428264,0.0000469146,0.0000515896,0.0000571764,0.000064,0.00007234421,0.00008221224,0.00009350816,0.0001061361,0.00012,0.000134984,0.000151492,0.000170208,0.000191816,0.000217,0.0002469067,0.00028124,0.00031852,0.0003572667,0.000396,0.0004337147,0.000473024,0.000517876,0.0005722187,0.00064,0.00072456,0.0008255,0.00094116,0.00106988,0.00121,0.001362091,0.001530752,0.001720368,0.001935323,0.00218,0.0024548,0.002764,0.0031178,0.0035264,0.004,0.00454624,0.00515932,0.00582928,0.00654616,0.0073,0.008086507,0.00890872,0.00976768,0.01066443,0.0116,0.01257317,0.01358272,0.01462968,0.01571509,0.01684,0.01800736,0.01921448,0.02045392,0.02171824,0.023,0.02429461,0.02561024,0.02695857,0.02835125,0.0298,0.03131083,0.03288368,0.03452112,0.03622571,0.038,0.03984667,0.041768,0.043766,0.04584267,0.048,0.05024368,0.05257304,0.05498056,0.05745872,0.06,0.06260197,0.06527752,0.06804208,0.07091109,0.0739,0.077016,0.0802664,0.0836668,0.0872328,0.09098,0.09491755,0.09904584,0.1033674,0.1078846,0.1126,0.117532,0.1226744,0.1279928,0.1334528,0.13902,0.1446764,0.1504693,0.1564619,0.1627177,0.1693,0.1762431,0.1835581,0.1912735,0.199418,0.20802,0.2171199,0.2267345,0.2368571,0.2474812,0.2586,0.2701849,0.2822939,0.2950505,0.308578,0.323,0.3384021,0.3546858,0.3716986,0.3892875,0.4073,0.4256299,0.4443096,0.4633944,0.4829395,0.503,0.5235693,0.544512,0.56569,0.5869653,0.6082,0.6293456,0.6503068,0.6708752,0.6908424,0.71,0.7281852,0.7454636,0.7619694,0.7778368,0.7932,0.8081104,0.8224962,0.8363068,0.8494916,0.862,0.8738108,0.8849624,0.8954936,0.9054432,0.9148501,0.9237348,0.9320924,0.9399226,0.9472252,0.954,0.9602561,0.9660074,0.9712606,0.9760225,0.9803,0.9840924,0.9874182,0.9903128,0.9928116,0.9949501,0.9967108,0.9980983,0.999112,0.9997482,1,0.9998567,0.9993046,0.9983255,0.9968987,0.995,0.9926005,0.9897426,0.9864444,0.9827241,0.9786,0.9740837,0.9691712,0.9638568,0.9581349,0.952,0.9454504,0.9384992,0.9311628,0.9234576,0.9154,0.9070064,0.8982772,0.8892048,0.8797816,0.87,0.8598613,0.849392,0.838622,0.8275813,0.8163,0.8047947,0.793082,0.781192,0.7691547,0.757,0.7447541,0.7324224,0.7200036,0.7074965,0.6949,0.6822192,0.6694716,0.6566744,0.6438448,0.631,0.6181555,0.6053144,0.5924756,0.5796379,0.5668,0.5539611,0.5411372,0.5283528,0.5156323,0.503,0.4904688,0.4780304,0.4656776,0.4534032,0.4412,0.42908,0.417036,0.405032,0.393032,0.381,0.3689184,0.3568272,0.3447768,0.3328176,0.321,0.3093381,0.2978504,0.2865936,0.2756245,0.265,0.2547632,0.2448896,0.2353344,0.2260528,0.217,0.2081616,0.1995488,0.1911552,0.1829744,0.175,0.1672235,0.1596464,0.1522776,0.1451259,0.1382,0.1315003,0.1250248,0.1187792,0.1127691,0.107,0.1014762,0.09618864,0.09112296,0.08626485,0.0816,0.07712064,0.07282552,0.06871008,0.06476976,0.061,0.05739621,0.05395504,0.05067376,0.04754965,0.04458,0.04175872,0.03908496,0.03656384,0.03420048,0.032,0.02996261,0.02807664,0.02632936,0.02470805,0.0232,0.02180077,0.02050112,0.01928108,0.01812069,0.017,0.01590379,0.01483718,0.01381068,0.01283478,0.01192,0.01106831,0.01027339,0.009533311,0.008846157,0.00821,0.007623781,0.007085424,0.006591476,0.006138485,0.005723,0.005343059,0.004995796,0.004676404,0.004380075,0.004102,0.003838453,0.003589099,0.003354219,0.003134093,0.002929,0.002738139,0.002559876,0.002393244,0.002237275,0.002091,0.001953587,0.00182458,0.00170358,0.001590187,0.001484,0.001384496,0.001291268,0.001204092,0.001122744,0.001047,0.0009765896,0.0009111088,0.0008501332,0.0007932384,0.00074,0.0006900827,0.00064331,0.000599496,0.0005584547,0.00052,0.0004839136,0.0004500528,0.0004183452,0.0003887184,0.0003611,0.0003353835,0.0003114404,0.0002891656,0.0002684539,0.0002492,0.0002313019,0.0002146856,0.0001992884,0.0001850475,0.0001719,0.0001597781,0.0001486044,0.0001383016,0.0001287925,0.00012,0.0001118595,0.0001043224,0.0000973356,0.00009084587,0.0000848,0.00007914667,0.000073858,0.000068916,0.00006430267,0.00006,0.00005598187,0.0000522256,0.0000487184,0.00004544747,0.0000424,0.00003956104,0.00003691512,0.00003444868,0.00003214816,0.00003,0.00002799125,0.00002611356,0.00002436024,0.00002272461,0.0000212,0.00001977855,0.00001845285,0.00001721687,0.00001606459,0.00001499,0.00001398728,0.00001305155,0.00001217818,0.00001136254,0.0000106,0.000009885877,0.000009217304,0.000008592362,0.000008009133,0.0000074657,0.000006959567,0.000006487995,0.000006048699,0.000005639396,0.0000052578,0.000004901771,0.00000456972,0.000004260194,0.000003971739,0.0000037029,0.000003452163,0.000003218302,0.0000030003,0.000002797139,0.0000026078,0.00000243122,0.000002266531,0.000002113013,0.000001969943,0.0000018366,0.00000171223,0.000001596228,0.00000148809,0.000001387314,0.0000012934,0.00000120582,0.000001124143,0.000001048009,0.000000977058,0.00000091093,0.000000849251,0.000000791721,0.00000073809,0.00000068811,0.00000064153,0.00000059809,0.000000557575,0.000000519808,0.000000484612,0.00000045181
        };

        static double LuminousFunc(double wavelength)
        {
            wavelength = wavelength * 1000; // nanometer
            if (wavelength <= triY_wav.First() || wavelength >= triY_wav.Last())
                return 0;

            for (int i = 0; i < triY_wav.Length - 1; i++)
                if (triY_wav[i + 1] > wavelength)
                    return (
                        triY_Y[i] * (triY_wav[i + 1] - wavelength) +
                        triY_Y[i + 1] * (wavelength - triY_wav[i])
                        )  * 683;
            return -1;
        }

        static void RunUserAnalysis(IZOSAPI_Application TheApplication)
        {
            IOpticalSystem TheSystem = TheApplication.PrimarySystem;
            INonSeqEditor TheNCE = TheSystem.NCE;
            IUserAnalysisData TheAnalysisData = TheApplication.UserAnalysisData;
            ISettingsData TheSettings = TheAnalysisData.UserSettings;

            // Set Title and check if it's first time start
            TheAnalysisData.WindowTitle = "Radiance Camera";

            // Get parameters
            int xpix, ypix, objnum, wavnum, smooth;
            double xwid, ywid, tarz;
            string sourcepath;
            bool islog, isirr;
            if (!(
                TheSettings.GetIntegerValue("xpix", out xpix) &&
                TheSettings.GetIntegerValue("ypix", out ypix) &&
                TheSettings.GetIntegerValue("objnum", out objnum) &&
                TheSettings.GetIntegerValue("wavnum", out wavnum) &&
                TheSettings.GetIntegerValue("smooth", out smooth) &&
                TheSettings.GetDoubleValue("xwid", out xwid) &&
                TheSettings.GetDoubleValue("ywid", out ywid) &&
                TheSettings.GetDoubleValue("tarz", out tarz) &&
                TheSettings.GetStringValue("sourcepath", out sourcepath) &&
                TheSettings.GetBooleanValue("islog", out islog) &&
                TheSettings.GetBooleanValue("isirr", out isirr)
                ))
            {
                System.Windows.Forms.MessageBox.Show("Click the Settings to set up the parameters.");
                return;
            }

            // make a log if the option is checked
            string logpath = TheSystem.TheApplication.ZemaxDataDir + "\\Objects\\Sources\\Source Files\\radiance_camera.log";
            if (islog)
            {
                File.WriteAllText(logpath, "Source file path: " + sourcepath + "\n");
                File.AppendAllText(logpath, "Log time: " + DateTime.Now.ToString("yyyy'-'MM'-'dd HH':'mm':'ss' (GMT'z')'") + "\n");
                var builttime = new FileInfo(Assembly.GetExecutingAssembly().Location).LastWriteTime;
                File.AppendAllText(logpath, "Tool built time: " + builttime.ToString("yyyy'-'MM'-'dd HH':'mm':'ss' (GMT'z')'") + "\n");
                File.AppendAllText(logpath, "X Pixel: " + xpix.ToString() + "\n");
                File.AppendAllText(logpath, "Y Pixel: " + ypix.ToString() + "\n");
                File.AppendAllText(logpath, "Annulus object #: " + objnum.ToString() + "\n");
                File.AppendAllText(logpath, "Wave#: " + wavnum.ToString() + "\n");
                File.AppendAllText(logpath, "X Width: " + xwid.ToString() + "\n");
                File.AppendAllText(logpath, "Y Width: " + ywid.ToString() + "\n");
                File.AppendAllText(logpath, "Target Z Position: " + tarz.ToString() + "\n");
                File.AppendAllText(logpath, "Show Log " + islog.ToString() + "\n");
                File.AppendAllText(logpath, "Irradiance: " + isirr.ToString() + "\n");
                File.AppendAllText(logpath, "Smooth: " + smooth.ToString() + "\n");
                File.AppendAllText(logpath, "=========================================\n\n");
            }

            // Error Check
            if (objnum > TheNCE.NumberOfObjects)
            {
                System.Windows.Forms.MessageBox.Show(
                    "Error: The object # is larger than number of objects in NCE.");
                return;
            }
            if (!File.Exists(sourcepath))
            {
                System.Windows.Forms.MessageBox.Show("Cannot find file: " + sourcepath);
                return;
            }
            if (TheNCE.GetObjectAt(objnum).Type != ZOSAPI.Editors.NCE.ObjectType.Annulus)
            {
                System.Windows.Forms.MessageBox.Show(
                    "Error: Object #" + objnum.ToString() + " is not a Annulus.");
                return;
            }
            if (TheNCE.GetObjectAt(objnum).GetObjectCell(ObjectColumn.Par1).DoubleValue != 
                TheNCE.GetObjectAt(objnum).GetObjectCell(ObjectColumn.Par2).DoubleValue)
            {
                System.Windows.Forms.MessageBox.Show(
                    "Error: Annulus's Maximum X and Y Half Width are different.");
                return;
            }
            if (TheNCE.GetObjectAt(objnum).GetObjectCell(ObjectColumn.Par3).DoubleValue != 0 ||
                TheNCE.GetObjectAt(objnum).GetObjectCell(ObjectColumn.Par4).DoubleValue != 0)
            {
                System.Windows.Forms.MessageBox.Show(
                    "Error: Annulus's Mininum X and Y Half Width are not both zero.");
                return;
            }
            if (TheSystem.SystemData.Units.LensUnits != ZOSAPI.SystemData.ZemaxSystemUnits.Millimeters)
            {
                System.Windows.Forms.MessageBox.Show(
                    "Erorr: This analysis assumes the Lens Unit is Millimeters.\n" +
                    "To change Lens Unit, goto System Expolrer > Unit.");
                return;
            }
            if (TheSystem.SystemData.Units.SourceUnits == ZOSAPI.SystemData.ZemaxSourceUnits.Joules)
            {
                System.Windows.Forms.MessageBox.Show(
                    "Erorr: This analysis assumes the Source Unit is either Watts or Lumens.\n" +
                    "To change Source Unit, goto System Expolrer > Unit.");
                return;
            }

            // OK start read file, first read header
            BinaryReader br;
            try
            {
                br = new BinaryReader(File.Open(sourcepath, FileMode.Open, FileAccess.Read, FileShare.None));
            }
            catch (Exception e)
            {
                // if fail, this will show a dialog and let's see what's the message given by BinaryReader
                System.Windows.Forms.MessageBox.Show(e.Message);
                return;
            }
            int Identifier = br.ReadInt32();
            if (Identifier != 1010)
            {
                // I have seen some source files are with wrong Identifier but the content is correct.
                // So here we provide an option for users to continue or stop.
                DialogResult dialog = MessageBox.Show("Invalid Identifier (" + Identifier.ToString() + ")" +
                    "\n\nMaybe this is not a Zemax source file. Continue?",
                    "Warning", MessageBoxButtons.YesNo,
                    MessageBoxIcon.None,
                    MessageBoxDefaultButton.Button2);

                if (dialog == DialogResult.No)
                { br.Close(); return; }
            }

            // These are all header data
            UInt32 NbrRays = br.ReadUInt32();
            char[] Description = br.ReadChars(100);
            float SourceFlux = br.ReadSingle(); // The total flux in watts of this source
            float RaySetFlux = br.ReadSingle(); // The flux in watts represented by this Ray Set
            float Wavelength = br.ReadSingle(); // The wavelength in micrometers, 0 if a composite
            float InclinationBeg = br.ReadSingle(), 
                InclinationEnd = br.ReadSingle(); // Angular range for ray set (Degrees)
            float AzimuthBeg = br.ReadSingle(), 
                AzimuthEnd = br.ReadSingle(); // Angular range for ray set (Degrees)
            int DimensionUnits = br.ReadInt32(); // METERS=0, IN=1, CM=2, FEET=3, MM=4
            float LocX = br.ReadSingle(), 
                LocY = br.ReadSingle(), 
                LocZ = br.ReadSingle(); // Coordinate Translation of the source
            float RotX = br.ReadSingle(),
                RotY = br.ReadSingle(),
                RotZ = br.ReadSingle(); // Source rotation (Radians)
            float ScaleX = br.ReadSingle(),
                ScaleY = br.ReadSingle(),
                ScaleZ = br.ReadSingle(); // Currently unused
            float unused1 = br.ReadSingle(),
                unused2 = br.ReadSingle(),
                unused3 = br.ReadSingle(),
                unused4 = br.ReadSingle();
            int ray_format_type = br.ReadInt32(),
                flux_type = br.ReadInt32();
            int reserved1 = br.ReadInt32(),
                reserved2 = br.ReadInt32();

            // Make Log
            if (islog)
            {
                File.AppendAllText(logpath, "Identifier: " + Identifier.ToString() + "\n");
                File.AppendAllText(logpath, "NbrRays: " + NbrRays.ToString() + "\n");
                File.AppendAllText(logpath, "Description: " + Description.ToString() + "\n");
                File.AppendAllText(logpath, "SourceFlux: " + SourceFlux.ToString() + "\n");
                File.AppendAllText(logpath, "RaySetFlux: " + RaySetFlux.ToString() + "\n");
                File.AppendAllText(logpath, "Wavelength: " + Wavelength.ToString() + "\n");
                File.AppendAllText(logpath, "InclinationBeg: " + InclinationBeg.ToString() + "\n");
                File.AppendAllText(logpath, "InclinationEnd: " + InclinationEnd.ToString() + "\n");
                File.AppendAllText(logpath, "AzimuthBeg: " + AzimuthBeg.ToString() + "\n");
                File.AppendAllText(logpath, "AzimuthEnd: " + AzimuthEnd.ToString() + "\n");
                File.AppendAllText(logpath, "DimensionUnits: " + DimensionUnits.ToString() + "\n");
                File.AppendAllText(logpath, "LocX: " + LocX.ToString() + "\n");
                File.AppendAllText(logpath, "LocY: " + LocY.ToString() + "\n");
                File.AppendAllText(logpath, "LocZ: " + LocZ.ToString() + "\n");
                File.AppendAllText(logpath, "RotX: " + RotX.ToString() + "\n");
                File.AppendAllText(logpath, "RotY: " + RotY.ToString() + "\n");
                File.AppendAllText(logpath, "RotZ: " + RotZ.ToString() + "\n");
                File.AppendAllText(logpath, "ScaleX: " + ScaleX.ToString() + "\n");
                File.AppendAllText(logpath, "ScaleY: " + ScaleY.ToString() + "\n");
                File.AppendAllText(logpath, "ScaleZ: " + ScaleZ.ToString() + "\n");
                File.AppendAllText(logpath, "unused1: " + unused1.ToString() + "\n");
                File.AppendAllText(logpath, "unused2: " + unused2.ToString() + "\n");
                File.AppendAllText(logpath, "unused3: " + unused3.ToString() + "\n");
                File.AppendAllText(logpath, "unused4: " + unused4.ToString() + "\n");
                File.AppendAllText(logpath, "ray_format_type: " + ray_format_type.ToString() + "\n");
                File.AppendAllText(logpath, "flux_type: " + flux_type.ToString() + "\n");
                File.AppendAllText(logpath, "reserved1: " + reserved1.ToString() + "\n");
                File.AppendAllText(logpath, "reserved2: " + reserved2.ToString() + "\n");
                File.AppendAllText(logpath, "=========================================\n\n");
            }

            // format check
            bool
                formatiscolor = false, 
                typeiswatt = false,
                fileisdat = Path.GetExtension(sourcepath).ToLower() == ".dat",
                showlumen = TheSystem.SystemData.Units.SourceUnits == ZOSAPI.SystemData.ZemaxSourceUnits.Lumens;
            if (Path.GetExtension(sourcepath).ToLower() != ".sdf" && !fileisdat)
            {
                // extension file name is neither sdf nor dat
                System.Windows.Forms.MessageBox.Show(
                    "Erorr: Please select either .sdf or .dat file.");
                return;
            }

            // ray_format_type can only be 0 or 2. This is defined in Help.
            if (ray_format_type == 0)
                formatiscolor = false;
            else if (ray_format_type == 2)
                formatiscolor = true;
            else
            {
                System.Windows.Forms.MessageBox.Show(
                    "Erorr: invalid ray_format_type: " + ray_format_type.ToString());
                return;
            }

            // flux_type can only be 0 or 1. This is defiend in Help.
            if (flux_type == 0)
                typeiswatt = true;
            else if (flux_type == 1)
                typeiswatt = false;
            else
            {
                System.Windows.Forms.MessageBox.Show(
                    "Erorr: invalid flux_type: " + ray_format_type.ToString());
                return;
            }

            if (formatiscolor && !typeiswatt)
            {
                // This is impossible. Defiend in Help.
                System.Windows.Forms.MessageBox.Show(
                    "Erorr: ray_format_type is 2 (spectral color), while flux_type is 1 (lumen).");
                return;
            }

            if(fileisdat == formatiscolor)
            {
                // as explained in error message below.
                if (fileisdat)
                    System.Windows.Forms.MessageBox.Show(
                        "Erorr: Extension filename is .dat, but the ray_format_type is " + ray_format_type.ToString());
                else
                    System.Windows.Forms.MessageBox.Show(
                        "Erorr: Extension filename is .sdf, but the ray_format_type is " + ray_format_type.ToString());
                return;
            }


            if (br.BaseStream.Position + NbrRays * (ray_format_type == 0 ? 7 : 8) * 4 > br.BaseStream.Length)
            {
                // I checked if the file size matches what NbrRays say. It should be exact. No more and no less.
                System.Windows.Forms.MessageBox.Show(
                    "Erorr: Data incomplete.\n" +
                    "Position: " + br.BaseStream.Position.ToString() + "\n" +
                    "Length: " + br.BaseStream.Length.ToString());
                return;
            }

            // Make Log
            if (islog)
            {
                File.AppendAllText(logpath, "OpticStudio Source Unit: " + TheSystem.SystemData.Units.SourceUnits.ToString() + "\n");
                File.AppendAllText(logpath, "Source File Size: " + br.BaseStream.Length.ToString() + "\n");
                File.AppendAllText(logpath, "Expected Source File Size: " + 
                    (br.BaseStream.Position + NbrRays * (ray_format_type == 0 ? 7 : 8) * 4).ToString() + "\n");
                File.AppendAllText(logpath, "=========================================\n\n");
            }

            // Get object inverse rotation matrix, shift, and wavelength
            // first get rotation matrix
            double r11, r12, r13, r21, r22, r23, r31, r32, r33, x0, y0, z0;
            TheNCE.GetMatrix(objnum,
                out r11, out r12, out r13,
                out r21, out r22, out r23,
                out r31, out r32, out r33,
                out x0, out y0, out z0);

            double ir11, ir12, ir13, ir21, ir22, ir23, ir31, ir32, ir33;
            // get inverse matrix
            ir11 = r22 * r33 - r23 * r32;
            ir12 = r13 * r32 - r12 * r33;
            ir13 = r12 * r23 - r13 * r22;
            ir21 = r23 * r31 - r21 * r33;
            ir22 = r11 * r33 - r13 * r31;
            ir23 = r13 * r21 - r11 * r23;
            ir31 = r21 * r32 - r22 * r31;
            ir32 = r12 * r31 - r11 * r32;
            ir33 = r11 * r22 - r12 * r21;

            // make log
            if (islog)
            {
                File.AppendAllText(logpath, "Shift of Annulus: \n");
                File.AppendAllText(logpath, x0 + "\t" + y0 + "\t" + z0 + "\n\n");
                File.AppendAllText(logpath, "Rotation Matrix of Annulus: \n");
                File.AppendAllText(logpath, r11 + "\t" + r12 + "\t" + r13 + "\n");
                File.AppendAllText(logpath, r21 + "\t" + r22 + "\t" + r23 + "\n");
                File.AppendAllText(logpath, r31 + "\t" + r32 + "\t" + r33 + "\n\n");
                File.AppendAllText(logpath, "Inverse Rotation Matrix of Annulus: \n");
                File.AppendAllText(logpath, ir11 + "\t" + ir12 + "\t" + ir13 + "\n");
                File.AppendAllText(logpath, ir21 + "\t" + ir22 + "\t" + ir23 + "\n");
                File.AppendAllText(logpath, ir31 + "\t" + ir32 + "\t" + ir33 + "\n\n");
                File.AppendAllText(logpath, "=========================================\n\n");
            }

            // there are many situation
            // I'm mainly trying to guess what wavelength I should use.
            // The wavelength is used to convert between watt and lumen.
            double source_wave = 0;
            if (wavnum == -1)
            {
                int i;
                for (i = 1; i <= TheSystem.SystemData.Wavelengths.NumberOfWavelengths; i++)
                    if (TheSystem.SystemData.Wavelengths.GetWavelength(i).IsPrimary)
                        source_wave = TheSystem.SystemData.Wavelengths.GetWavelength(i).Wavelength;
                if (islog) File.AppendAllText(logpath,
                    "Wave# is set to -1. Use primary wavelength (#" + i.ToString() + "): " + source_wave.ToString() + "\n");
            }
            else if (wavnum == 0)
            {
                source_wave = Wavelength;
                if (islog) File.AppendAllText(logpath,
                    "Wave# is set to 0. Use wavelength data from the source file : " + source_wave.ToString() + "\n");
            }
            else
            { 
                source_wave = TheSystem.SystemData.Wavelengths.GetWavelength(wavnum).Wavelength;
                if (islog) File.AppendAllText(logpath,
                    "Wave# is set to " + wavnum.ToString() + ". Corresponded wavelength: " + source_wave.ToString() + "\n"
                    + "Corresponded luminous efficiency: " + LuminousFunc(source_wave).ToString() + "\n");
            }

            // Now read raydata
            double[,] fluxarray = new double[ypix, xpix];
            double
                x, y, z, l, m, n, flux, raywave = 0,
                tx, ty, tz, tl, tm, tn, // temporary x, temporary y, ... etc
                PSA, shift, t1, t2, v1x, v1y, v2x, v2y, phi, // temporary 1, temporary 2
                radius = TheNCE.GetObjectAt(objnum).GetObjectCell(ObjectColumn.Par1).DoubleValue, // radius of Annulus object
                radius_t = radius / tarz, // normalized radius
                px = xwid / xpix, // pixel width x in mm
                py = ywid / ypix, // pixel width y in mm
                area_M = xwid * ywid * 1e-6 / xpix / ypix, // pixel area in m^2
                hwx = xwid / 2, 
                hwy = ywid / 2;
            int binx, biny,
                phisamp = 100; // phi sampling
                // these are counter of error rays that cannot be added to any pixel on the target plane for any reason.
                // Just for debug. 
            int eray = 0,
                eray_tn = 0,
                eray_txty = 0,
                eray_binxy = 0;

            // make log
            if (islog) File.AppendAllText(logpath, "Raidus of the Annulus: " + radius + "\n");

            for (int i = 1; i <= NbrRays; i++)
            {
                x = br.ReadSingle(); // ray x position
                y = br.ReadSingle(); // ray y position
                z = br.ReadSingle(); // ray z position
                l = br.ReadSingle(); // ray l
                m = br.ReadSingle(); // ray m
                n = br.ReadSingle(); // ray n
                if (Math.Abs(Math.Sqrt(l * l + m * m + n * n) - 1) > 1e-3)
                {
                    System.Windows.Forms.MessageBox.Show(
                        "Erorr: Invalid Direction Cosine. The lenght of (l,m,n) should be 1.0.\n" +
                        "Direction Cosine of ray# " + i + ": (" + l + ", " + m + ", " + n + ")");
                    return;
                }

                flux = br.ReadSingle();

                // if ray_format_type is 2, wavelength is given by source file
                if (formatiscolor)
                    raywave = br.ReadSingle();

                // convert ray coordiante from global to local of Annulus object (xyzlmn)->(txtytztltmtn)
                // xyz(G) = xyz(Shift) + Rotation * xyz(L)
                // xyz(L) = InverseRoataion * (xyz(G) - xyz(Shift))
                tx = ir11 * (x - x0) + ir12 * (y - y0) + ir13 * (z - z0);
                ty = ir21 * (x - x0) + ir22 * (y - y0) + ir23 * (z - z0);
                tz = ir31 * (x - x0) + ir32 * (y - y0) + ir33 * (z - z0);
                tl = ir11 * l + ir12 * m + ir13 * n;
                tm = ir21 * l + ir22 * m + ir23 * n;
                tn = ir31 * l + ir32 * m + ir33 * n;

                // all rays should be on the Annulus
                // if it's not. somehting is wrong.
                // In my test, usually this happens if I forgot to re-trace and save new SDF file after I moved the Annulus object's position.
                if (Math.Abs(tz) > 1e-3 || Math.Sqrt(tx * tx + ty * ty) > radius * 1.01)
                {
                    System.Windows.Forms.MessageBox.Show(
                        "Erorr: Source ray #" + i + " not on the Annulus object.\n" +
                        "Ray global coordinate: \n(" +
                        x + ", " + y + ", " + z + ")\n" +
                        "Ray local coordinate \n(" +
                        tx + ", " + ty + ", " + tz + ")");
                    return;
                }

                // I re-cycle the variable of x and y
                // now their meaning is the ray's (x,y) on the target plane
                // I just back propagate it
                x = tx - tarz * tl / tn;
                y = ty - tarz * tm / tn;

                // If it's outside of the taget plane, count the error and report later
                if (Math.Abs(x) > hwx || Math.Abs(y) > hwy)
                { eray++; eray_txty++; continue; }

                // If the rays is propagated to +z direction in Annulus' local coordinate, stop and count the error
                if (tn <= 0)
                { eray++; eray_tn++; continue; }

                // check which bin this ray hit
                binx = (int)Math.Floor((x + hwx) / px);
                biny = (int)Math.Floor((y + hwy) / py);

                // This probably will not happen, but I count the error if I get bin# that is outside of the defined value
                if (binx >= xpix || biny >= ypix)
                { eray++; eray_binxy++; continue; }

                // now start to calculate PSA for this pixel
                // Note this code can be improved. The PSA should not be calculated for each ray.
                // I only need to calculate once for each pixel.

                // shift is the lateral distance on xy coordinate from the pixel center to the Annulus center
                // you can also see my slides for more explanations.
                t1 = (binx + 0.5) * px - hwx;
                t2 = (biny + 0.5) * py - hwy;
                shift = Math.Sqrt(t1 * t1 + t2 * t2);
                shift /= tarz;

                // the area of each triangle is calculated by using determinant as explained in slides
                // Calculate vector v2 first
                // in the end of each loop, I just copy v1 to v2, but only for first loop, I need to pre-calculate it.
                t1 = shift * shift + radius_t * radius_t + 1;
                t2 = 2 * shift * radius_t;
                v2x = (shift + radius_t) / Math.Sqrt(t1 + t2);
                v2y = 0;

                if (!isirr) // this is for debug. I provide an option to users to ignore PSA and thus get irradiance
                {
                    PSA = 0;
                    for (int j = 1; j <= phisamp; j++)
                    {
                        phi = 2 * Math.PI * j / phisamp;
                        v1x = v2x;
                        v1y = v2y;
                        v2x = (shift + radius_t * Math.Cos(phi)) / Math.Sqrt(t1 + t2 * Math.Cos(phi));
                        v2y = radius_t * Math.Sin(phi) / Math.Sqrt(t1 + t2 * Math.Cos(phi));
                        PSA += (v1x * v2y - v2x * v1y) / 2;
                    }
                }
                else
                    PSA = 1;

                // FInally! radiance = flux / area / PSA!
                // If user want to see luminance but the source file provide only watt data, I nee dto convert and vice versa.
                if (showlumen != typeiswatt)
                    fluxarray[biny, binx] += flux / area_M / PSA;
                else if (!showlumen) // means luminous data, but want to show watt data
                    fluxarray[biny, binx] += flux / area_M / PSA / LuminousFunc(source_wave);
                else if (formatiscolor) // means watt data with full spectrum data, want to show luminous data
                    fluxarray[biny, binx] += flux / area_M / PSA * LuminousFunc(raywave);
                else // means watt data with no full spectrum data, want to show luminous data
                    fluxarray[biny, binx] += flux / area_M / PSA * LuminousFunc(source_wave);
            }

            // close the binary reader
            br.Close();

            if (islog)
            {
                File.AppendAllText(logpath, "Rays removed (all): " + eray + "(" + (double)eray / NbrRays + ")\n");
                File.AppendAllText(logpath, "Rays removed (propagate in -z): " + eray_tn + "(" + (double)eray_tn / NbrRays + ")\n");
                File.AppendAllText(logpath, "Rays removed (not on detector): " + eray_txty + "(" + (double)eray_txty / NbrRays + ")\n");
                File.AppendAllText(logpath, "Rays removed (error): " + eray_binxy + "(" + (double)eray_binxy / NbrRays + ")\n");
            }


            // Do smooth
            for (int i = 0; i < smooth; i++)
            {
                double[,] tmpary = new double[ypix, xpix];
                for (int ix = 0; ix < xpix; ix++)
                    for (int iy = 0; iy < ypix; iy++)
                    {
                        for (int ix2 = ix - 1; ix2 <= ix + 1; ix2++)
                        {
                            if (ix2 < 0 || ix2 >= xpix)
                                continue;
                            for (int iy2 = iy - 1; iy2 <= iy + 1; iy2++)
                            {
                                if (iy2 < 0 || iy2 >= ypix)
                                    continue;
                                tmpary[iy, ix] += fluxarray[iy2, ix2];
                            }
                        }
                        if ((ix == 0 || ix == xpix - 1) && (iy == 0 || iy == ypix - 1))
                            tmpary[iy, ix] /= 4;
                        else if (ix == 0 || ix == xpix - 1 || iy == 0 || iy == ypix - 1)
                            tmpary[iy, ix] /= 6;
                        else
                            tmpary[iy, ix] /= 9;
                    }
                fluxarray = tmpary;
            }

            // Draw in the window
            IUserGridData plotData = null;
            if (showlumen)
                plotData = TheApplication.UserAnalysisData.MakeGridPlot("Luminance [nits]");
            else
                plotData = TheApplication.UserAnalysisData.MakeGridPlot("Radiance [Watts/M^2/Steradian]");
            plotData.ShowAsType = GridPlotType.FalseColor;
            plotData.XLabel = "X coordinate [mm]";
            plotData.YLabel = "Y coordinate [mm]";
            plotData.SetXDataDimensions(-hwx, hwx);
            plotData.SetYDataDimensions(-hwy, hwy);
            plotData.SetDataSafe(fluxarray);
            plotData.XYAspectRatio = hwx / hwy;
            plotData.ZAxisMinAuto = false;
            plotData.ZAxisMin = 0;

            // Other information in the window
            TheAnalysisData.FeatureDescription = "Radiance Camera";
            List<string> header = new List<string>();
            header.Add("Annulus Obj#: " + objnum.ToString() + "      Target Distance: " + tarz.ToString());
            header.Add("Pixels: " + xpix.ToString() + " x " + ypix.ToString() + "     Width: " + xwid.ToString() + " x " + ywid.ToString());
            if (showlumen)
                header.Add("Z-axis is Luminance [nits (Lumen/M^2/Steradian)]");
            else
                header.Add("Z-axis is Radiance [Watts/M^2/Steradian]");
            header.Add("Considered rays/Total Rays: " + (NbrRays-eray) + "/" + NbrRays);
            TheAnalysisData.HeaderData = header.ToArray();

            // Export log file
            if (islog)
            {
                File.AppendAllText(logpath, "Start writing array data."); // 1
                string result_path = TheSystem.SystemFile.Substring(0, TheSystem.SystemFile.Length - 4) + "_radiance_camera_result_1.txt";
                int fileindex = 1;
                while (System.IO.File.Exists(result_path))
                {
                    result_path = TheSystem.SystemFile.Substring(0, TheSystem.SystemFile.Length - 4) +
                        "_radiance_camera_result_" + fileindex.ToString() + ".txt";
                    fileindex += 1;
                }
                File.AppendAllText(logpath, " ."); // 2

                // export raw data of fluxarray
                // this is like GETTEXTFILE :)
                List<string> exp_txt = new List<string>();
                exp_txt.Add("Radiance Camera result");
                exp_txt.Add("System File: " + TheSystem.SystemFile);
                exp_txt.Add(DateTime.Now.ToString("yyyy'-'MM'-'dd HH':'mm':'ss' (GMT'z')'"));
                exp_txt.Add("");
                exp_txt.Add("Annulus Obj#: " + objnum.ToString());
                exp_txt.Add("Target Distance: " + tarz.ToString());
                exp_txt.Add("Pixels: " + xpix.ToString() + " x " + ypix.ToString());
                exp_txt.Add("Width: " + xwid.ToString() + " x " + ywid.ToString());
                exp_txt.Add("Smooth: " + smooth.ToString());
                exp_txt.Add("Considered rays/Total Rays: " + (NbrRays - eray) + "/" + NbrRays);
                File.AppendAllText(logpath, " ."); // 3
                if (showlumen)
                    exp_txt.Add("Unit: Luminance [nits]");
                else
                    exp_txt.Add("Unit: Radiance [Watts/M^2/Steradian]");
                File.AppendAllText(logpath, " ."); // 4
                exp_txt.Add("");
                exp_txt.Add("First row is the data at -y side.");
                exp_txt.Add("First column is the data at -x side.");
                File.AppendAllText(logpath, " ."); // 5
                for (int iy = 0; iy < ypix; iy++)
                {
                    string tmpstr = fluxarray[iy, 0].ToString();
                    for (int ix = 1; ix < xpix; ix++)
                        tmpstr += "\t" + fluxarray[iy, ix].ToString();
                    exp_txt.Add(tmpstr);
                }
                File.AppendAllText(logpath, " . done!\n"); // 6
                try
                {
                    File.WriteAllLines(result_path, exp_txt.ToArray());
                }
                catch (Exception e)
                {
                    File.AppendAllText(logpath, "Cannot export array data in " + result_path + "\n");
                    File.AppendAllText(logpath, e.Message.ToString());
                }
                File.AppendAllText(logpath, "Array data is exported in " + result_path + "\n");
            }
        }

        static void ShowUserAnalysisSettings(IZOSAPI_Application TheApplication)
        {
            IOpticalSystem TheSystem = TheApplication.PrimarySystem;

            IUserAnalysisData TheAnalysisData = TheApplication.UserAnalysisData;
            ISettingsData TheSettings = TheAnalysisData.UserSettings;

            setting_dialog aaa = new setting_dialog(TheSettings, TheSystem);
            System.Windows.Forms.Application.Run(aaa);

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
