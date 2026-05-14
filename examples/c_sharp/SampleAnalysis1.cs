// Copyright (C) 2026 - 2026 ANSYS, Inc. and/or its affiliates.
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
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZOSAPI;
using ZOSAPI.Analysis;
using ZOSAPI.Analysis.Data;
using ZOSAPI.Analysis.Settings.Mtf;
using ZOSAPI.Common;

namespace CSharp.Samples
{
    static class SampleAnalysis1
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

        const string KeyWL = "Wavelength";

        static void RunUserAnalysis(IZOSAPI_Application TheApplication)
        {
            IOpticalSystem TheSystem = TheApplication.PrimarySystem;

            IUserAnalysisData TheAnalysisData = TheApplication.UserAnalysisData;
            ISettingsData TheSettings = TheAnalysisData.UserSettings;

            string title = "Sample User Analysis";
            TheAnalysisData.WindowTitle = title;

            // Add your custom code here...
            int wlID;
            if (!TheSettings.GetIntegerValue(KeyWL, out wlID))
                wlID = 0;
            if (wlID > TheSystem.SystemData.Wavelengths.NumberOfWavelengths)
                wlID = 0;

            IA_ analysis = TheSystem.Analyses.New_FftMtfvsField();
            analysis.Terminate();
            ZOSAPI.Analysis.Settings.Mtf.IAS_FftMtfvsField analysisSettings = analysis.GetSettings() as IAS_FftMtfvsField;
            analysisSettings.ScanType = ZOSAPI.Analysis.Settings.ScanTypes.Minus_X;
            analysisSettings.UsePolarization = true;
            analysisSettings.Wavelength.UseAllWavelengths();
            analysisSettings.SampleSize = SampleSizes._64x64;
            analysisSettings.RemoveVignetting = true;
            analysisSettings.FieldDensity = 10;
            analysisSettings.Freq_1 = 10;
            analysisSettings.Freq_2 = 20;
            analysisSettings.Freq_3 = 30;
            analysisSettings.Freq_4 = 40;
            analysisSettings.Freq_5 = 50;
            analysisSettings.Freq_6 = 60;
            if (wlID == 0)
            {
                analysisSettings.Wavelength.UseAllWavelengths();
            }
            else
            {
                analysisSettings.Wavelength.SetWavelengthNumber(wlID);
            }
            analysis.Apply();
            DateTime tS = DateTime.Now;
            while (analysis.IsRunning())
            {
                System.Threading.Thread.Sleep(250);
                TimeSpan elapsed = (DateTime.Now - tS);
                TheAnalysisData.WindowTitle = "Waiting for FFT MFT (" + elapsed.TotalSeconds.ToString("f2") + "s)";
            }

            TheAnalysisData.WindowTitle = "Generating plot...";
            IAR_ results = analysis.GetResults();
            if (results != null && results.DataSeries != null && results.DataSeries.Length > 0)
            {
                IAR_DataSeries series0 = results.DataSeries[0];

                double[] xVals = series0.XData.Data;

                IUser2DLineData linePlot = TheAnalysisData.Make2DLinePlot(
                    "FFT MTF vs Field Example",
                    (uint)xVals.Length,
                    xVals);
                linePlot.XAxisLog = false;
                linePlot.XAxisMaxAuto = true;
                linePlot.XAxisMinAuto = true;
                linePlot.XAxisReversed = false;
                linePlot.XAxisSymmetric = false;
                linePlot.XLabel = "X Field in Degrees";
                linePlot.YAxisLog = false;
                linePlot.YAxisMaxAuto = true;
                linePlot.YAxisMinAuto = false;
                linePlot.YAxisReversed = false;
                linePlot.YAxisSymmetric = false;
                linePlot.YLabel = "Modulus of the OTF";

                foreach (IAR_DataSeries origSeries in results.DataSeries)
                {
                    double[,] blockData = origSeries.YData.Data;
                    double[] yData = new double[xVals.Length];
                    for (int i = 0; i < origSeries.NumSeries; ++i)
                    {
                        for (int j = 0; j < xVals.Length; ++j)
                            yData[j] = blockData[j, i];

                        linePlot.AddSeries(
                            origSeries.SeriesLabels[i],
                            ZemaxColor.Color1 + i,
                            (uint)origSeries.YData.Rows,
                            yData);
                    }
                }
            }

            TheAnalysisData.WindowTitle = title;
            TheSettings.SetIntegerValue(KeyWL, wlID);
        }

        static void ShowUserAnalysisSettings(IZOSAPI_Application TheApplication)
        {
            IOpticalSystem TheSystem = TheApplication.PrimarySystem;

            IUserAnalysisData TheAnalysisData = TheApplication.UserAnalysisData;
            ISettingsData TheSettings = TheAnalysisData.UserSettings;

            // TODO - retrieve the settings specific to your analysis here

            int wlCount = TheSystem.SystemData.Wavelengths.NumberOfWavelengths;
            int wlID;
            if (!TheSettings.GetIntegerValue(KeyWL, out wlID))
                wlID = 0;
            int oridID = wlID;
            if (wlID > wlCount)
                wlID = 0;

            Form fShowSettings = new Form();
            fShowSettings.Size = new System.Drawing.Size(400, 200);

            TableLayoutPanel pnl = new TableLayoutPanel();
            pnl.SuspendLayout();
            pnl.Dock = DockStyle.Fill;
            pnl.RowCount = 3;
            pnl.RowStyles.Clear();
            pnl.RowStyles.Add(new RowStyle(SizeType.Absolute, 40f));
            pnl.RowStyles.Add(new RowStyle(SizeType.Absolute, 20f));
            pnl.RowStyles.Add(new RowStyle(SizeType.Percent, 100f));
            pnl.ColumnCount = 2;
            pnl.ColumnStyles.Clear();
            pnl.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize, 100f));
            pnl.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100f));
            pnl.AutoSize = false;
            fShowSettings.Controls.Add(pnl);

            Label lbl = new Label();
            lbl.Text = "Wavelength:";
            lbl.Location = new System.Drawing.Point(8, 4);
            pnl.Controls.Add(lbl);

            ComboBox cbx = new ComboBox();
            cbx.Dock = DockStyle.Fill;
            cbx.DropDownStyle = ComboBoxStyle.DropDownList;
            cbx.Items.Add("All");
            for (int i = 0; i < wlCount; ++i)
                cbx.Items.Add(String.Format("Wavelength {0}", i + 1));
            cbx.SelectedIndex = wlID;
            pnl.Controls.Add(cbx);

            Button btn = new Button();
            btn.Dock = DockStyle.Fill;
            btn.Text = "Okay";
            pnl.Controls.Add(btn);
            btn.Click += (s, e) =>
            {
                fShowSettings.Close();
            };

            pnl.SetRow(lbl, 0);
            pnl.SetColumn(lbl, 0);

            pnl.SetRow(cbx, 0);
            pnl.SetColumn(cbx, 1);

            pnl.SetColumnSpan(btn, 2);
            pnl.SetRow(btn, 2);
            pnl.SetColumn(btn, 0);

            pnl.ResumeLayout(true);

            // Add your custom code here, and to the SettingsForm...
            System.Windows.Forms.Application.Run(fShowSettings);

            wlID = cbx.SelectedIndex;
            TheSettings.SetIntegerValue(KeyWL, wlID);
            TheAnalysisData.RunAnalysisOnSettingsClosed = (wlID != oridID);
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
