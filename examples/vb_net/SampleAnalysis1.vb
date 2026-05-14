' Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
' SPDX-License-Identifier: MIT
'
'
' Permission is hereby granted, free of charge, to any person obtaining a copy
' of this software and associated documentation files (the "Software"), to deal
' in the Software without restriction, including without limitation the rights
' to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
' copies of the Software, and to permit persons to whom the Software is
' furnished to do so, subject to the following conditions:
'
' The above copyright notice and this permission notice shall be included in all
' copies or substantial portions of the Software.
'
' THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
' IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
' FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
' AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
' LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
' OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
' SOFTWARE.

Imports ZOSAPI
Imports ZOSAPI.Analysis
Imports ZOSAPI.Common
Imports ZOSAPI.Analysis.Settings.Mtf
Imports System.Windows.Forms
Imports ZOSAPI.Analysis.Data

Module SampleAnalysis1

    Sub Main()
        ' Find the installed version of OpticStudio
        Dim isInitialized As Boolean = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize()
        ' Note -- uncomment the following line to use a custom initialization path
        'bool isInitialized = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(@"C:\Program Files\OpticStudio\");
        If isInitialized Then
            LogInfo("Found OpticStudio at: " + ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory())
        Else
            HandleError("Failed to locate OpticStudio!")
            Return
        End If

        BeginUserAnalysis()
    End Sub

    Private Sub BeginUserAnalysis()
        ' Create the initial connection class
        Dim TheConnection As New ZOSAPI_Connection()

        ' Attempt to connect to the existing OpticStudio instance
        Dim TheApplication As IZOSAPI_Application = Nothing
        Try
            ' this will throw an exception if not launched from OpticStudio
            TheApplication = TheConnection.ConnectToApplication()
        Catch ex As Exception
            HandleError(ex.Message)
            Return
        End Try
        If TheApplication Is Nothing Then
            HandleError("An unknown connection error occurred!")
            Return
        End If

        ' Check the connection status
        If Not TheApplication.IsValidLicenseForAPI Then
            HandleError("Failed to connect to OpticStudio: " + TheApplication.LicenseStatus)
            Return
        End If

        Select Case TheApplication.Mode
            Case ZOSAPI_Mode.UserAnalysis
                RunUserAnalysis(TheApplication)
                Exit Select
            Case ZOSAPI_Mode.UserAnalysisSettings
                ShowUserAnalysisSettings(TheApplication)
                Exit Select
            Case Else
                HandleError("User plugin was started in the wrong mode: expected UserAnalysis, found " + TheApplication.Mode.ToString())
                Return
        End Select

        ' Clean up
        FinishUserAnalysis(TheApplication)
    End Sub

    Const KeyWL As String = "Wavelength"

    Private Sub RunUserAnalysis(TheApplication As IZOSAPI_Application)

        Dim TheSystem As IOpticalSystem = TheApplication.PrimarySystem

        Dim TheAnalysisData As IUserAnalysisData = TheApplication.UserAnalysisData
        Dim TheSettings As ISettingsData = TheAnalysisData.UserSettings

        Dim title As String = "Sample User Analysis"
        TheAnalysisData.WindowTitle = title

        ' Add your custom code here...
        Dim wlID As Integer
        If Not TheSettings.GetIntegerValue(KeyWL, wlID) Then
            wlID = 0
        End If
        If wlID > TheSystem.SystemData.Wavelengths.NumberOfWavelengths Then
            wlID = 0
        End If

        Dim analysis As IA_ = TheSystem.Analyses.New_FftMtfvsField()
        analysis.Terminate()
        Dim analysisSettings As ZOSAPI.Analysis.Settings.Mtf.IAS_FftMtfvsField = TryCast(analysis.GetSettings(), IAS_FftMtfvsField)
        analysisSettings.ScanType = ZOSAPI.Analysis.Settings.ScanTypes.Minus_X
        analysisSettings.UsePolarization = True
        analysisSettings.Wavelength.UseAllWavelengths()
        analysisSettings.SampleSize = SampleSizes.S_64x64
        analysisSettings.RemoveVignetting = True
        analysisSettings.FieldDensity = 10
        analysisSettings.Freq_1 = 10
        analysisSettings.Freq_2 = 20
        analysisSettings.Freq_3 = 30
        analysisSettings.Freq_4 = 40
        analysisSettings.Freq_5 = 50
        analysisSettings.Freq_6 = 60
        If wlID = 0 Then
            analysisSettings.Wavelength.UseAllWavelengths()
        Else
            analysisSettings.Wavelength.SetWavelengthNumber(wlID)
        End If
        analysis.Apply()
        Dim tS As DateTime = DateTime.Now
        While analysis.IsRunning()
            System.Threading.Thread.Sleep(250)
            Dim elapsed As TimeSpan = (DateTime.Now - tS)
            TheAnalysisData.WindowTitle = "Waiting for FFT MFT (" + elapsed.TotalSeconds.ToString("f2") + "s)"
        End While

        TheAnalysisData.WindowTitle = "Generating plot..."
        Dim results As IAR_ = analysis.GetResults()
        If results IsNot Nothing AndAlso results.DataSeries IsNot Nothing AndAlso results.DataSeries.Length > 0 Then
            Dim series0 As IAR_DataSeries = results.DataSeries(0)

            Dim xVals As Double() = series0.XData.Data

            Dim linePlot As IUser2DLineData = TheAnalysisData.Make2DLinePlot("FFT MTF vs Field Example", CUInt(xVals.Length), xVals)
            linePlot.XAxisLog = False
            linePlot.XAxisMaxAuto = True
            linePlot.XAxisMinAuto = True
            linePlot.XAxisReversed = False
            linePlot.XAxisSymmetric = False
            linePlot.XLabel = "X Field in Degrees"
            linePlot.YAxisLog = False
            linePlot.YAxisMaxAuto = True
            linePlot.YAxisMinAuto = False
            linePlot.YAxisReversed = False
            linePlot.YAxisSymmetric = False
            linePlot.YLabel = "Modulus of the OTF"

            For Each origSeries As IAR_DataSeries In results.DataSeries
                Dim blockData As Double(,) = origSeries.YData.Data
                Dim yData As Double() = New Double(xVals.Length - 1) {}
                For i As Integer = 0 To origSeries.NumSeries - 1
                    For j As Integer = 0 To xVals.Length - 1
                        yData(j) = blockData(j, i)
                    Next

                    linePlot.AddSeries(origSeries.SeriesLabels(i), ZemaxColor.Color1 + i, CUInt(origSeries.YData.Rows), yData)
                Next
            Next
        End If

        TheAnalysisData.WindowTitle = title
        TheSettings.SetIntegerValue(KeyWL, wlID)

    End Sub

    Private Sub ShowUserAnalysisSettings(TheApplication As IZOSAPI_Application)
        Dim TheSystem As IOpticalSystem = TheApplication.PrimarySystem

        Dim TheAnalysisData As IUserAnalysisData = TheApplication.UserAnalysisData
        Dim TheSettings As ISettingsData = TheAnalysisData.UserSettings

        ' TODO - retrieve the settings specific to your analysis here

        Dim wlCount As Integer = TheSystem.SystemData.Wavelengths.NumberOfWavelengths
        Dim wlID As Integer
        If Not TheSettings.GetIntegerValue(KeyWL, wlID) Then
            wlID = 0
        End If
        Dim oridID As Integer = wlID
        If wlID > wlCount Then
            wlID = 0
        End If

        Dim fShowSettings As New Form()
        fShowSettings.Size = New System.Drawing.Size(400, 200)

        Dim pnl As New TableLayoutPanel()
        pnl.SuspendLayout()
        pnl.Dock = DockStyle.Fill
        pnl.RowCount = 3
        pnl.RowStyles.Clear()
        pnl.RowStyles.Add(New RowStyle(SizeType.Absolute, 40.0F))
        pnl.RowStyles.Add(New RowStyle(SizeType.Absolute, 20.0F))
        pnl.RowStyles.Add(New RowStyle(SizeType.Percent, 100.0F))
        pnl.ColumnCount = 2
        pnl.ColumnStyles.Clear()
        pnl.ColumnStyles.Add(New ColumnStyle(SizeType.AutoSize, 100.0F))
        pnl.ColumnStyles.Add(New ColumnStyle(SizeType.Percent, 100.0F))
        pnl.AutoSize = False
        fShowSettings.Controls.Add(pnl)

        Dim lbl As New Label()
        lbl.Text = "Wavelength:"
        lbl.Location = New System.Drawing.Point(8, 4)
        pnl.Controls.Add(lbl)

        Dim cbx As New ComboBox()
        cbx.Dock = DockStyle.Fill
        cbx.DropDownStyle = ComboBoxStyle.DropDownList
        cbx.Items.Add("All")
        For i As Integer = 0 To wlCount - 1
            cbx.Items.Add([String].Format("Wavelength {0}", i + 1))
        Next
        cbx.SelectedIndex = wlID
        pnl.Controls.Add(cbx)

        Dim btn As New Button()
        btn.Dock = DockStyle.Fill
        btn.Text = "Okay"
        pnl.Controls.Add(btn)
        AddHandler btn.Click, Function(s, e) (CloseSettings(fShowSettings))

        pnl.SetRow(lbl, 0)
        pnl.SetColumn(lbl, 0)

        pnl.SetRow(cbx, 0)
        pnl.SetColumn(cbx, 1)

        pnl.SetColumnSpan(btn, 2)
        pnl.SetRow(btn, 2)
        pnl.SetColumn(btn, 0)

        pnl.ResumeLayout(True)

        ' Add your custom code here, and to the SettingsForm...
        System.Windows.Forms.Application.Run(fShowSettings)

        wlID = cbx.SelectedIndex
        TheSettings.SetIntegerValue(KeyWL, wlID)
        TheAnalysisData.RunAnalysisOnSettingsClosed = (wlID <> oridID)
    End Sub

    Private Function CloseSettings(ByRef settingsForm As Form) As Boolean
        settingsForm.Close()
        Return True
    End Function


    Private Sub FinishUserAnalysis(TheApplication As IZOSAPI_Application)
        ' Note - OpticStudio will wait for the operand to complete until this application exits 
    End Sub

    Private Sub LogInfo(message As String)
        ' TODO - add custom logging
        Console.WriteLine(message)
    End Sub

    Private Sub HandleError(errorMessage As String)
        ' TODO - add custom error handling
        Throw New Exception(errorMessage)
    End Sub

End Module
