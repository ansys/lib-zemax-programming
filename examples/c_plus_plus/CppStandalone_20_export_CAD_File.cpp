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

// Entry point for the console application.

#include "stdafx.h"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <string>
#include <ctime>
#include <functional>
#include <assert.h>

// Note - .tlh files will be generated from the .tlb files (above) once the project is compiled.
// Visual Studio will incorrectly continue to report IntelliSense error messages however until it is restarted.
#include "zosapi.h"

using namespace std;
using namespace ZOSAPI;
using namespace ZOSAPI_Interfaces;

void handleError(std::string msg);
void logInfo(std::string msg);
void finishStandaloneApplication(IZOSAPI_ApplicationPtr TheApplication);

int RunApplication()
{
	CoInitialize(NULL);

	// Create the initial connection class
	IZOSAPI_ConnectionPtr TheConnection(__uuidof(ZOSAPI_Connection));


	// Attempt to create a Standalone connection
	IZOSAPI_ApplicationPtr TheApplication = TheConnection->CreateNewApplication();
	if (TheApplication == nullptr)
	{
		handleError("An unknown error occurred!");
		return -1;
	}

	// Check the connection status
	if (!TheApplication->IsValidLicenseForAPI)
	{
		handleError("License check failed!");
		return -1;
	}
	if (TheApplication->Mode != ZOSAPI_Mode::ZOSAPI_Mode_Server)
	{
		handleError("Standlone application was started in the incorrect mode!");
		return -1;
	}

	IOpticalSystemPtr TheSystem = TheApplication->PrimarySystem;

	// Add your custom code here...

	// Load a non-sequential file
	TheSystem->LoadFile(TheApplication->SamplesDir + "\\Non-Sequential\\Miscellaneous\\Digital_projector_flys_eye_homogenizer.zos", false);


	//! [e20s01_cp]
	// Get interface of IExportCAD
	IExportCADPtr ToolExportCAD = TheSystem->Tools->OpenExportCAD();
	//! [e20s01_cp]

	//! [e20s02_cp]
	// default option settings
	ToolExportCAD->FirstObject = 1;
	ToolExportCAD->LastObject = 8;
	ToolExportCAD->RayLayer = 1;
	ToolExportCAD->LensLayer = 0;
	ToolExportCAD->DummyThickness = 1;
	ToolExportCAD->SplineSegments = SplineSegmentsType_N_032;
	ToolExportCAD->FileType = CADFileType_STEP;
	ToolExportCAD->Tolerance = CADToleranceType_N_TenEMinus4;
	ToolExportCAD->SetCurrentConfiguration();
	// For other configuration choices, use following methods.
	//ToolExportCAD->SetConfigurationAllAtOnce();
	//ToolExportCAD->SetConfigurationAllByFile();
	//ToolExportCAD->SetConfigurationAllByLayer();
	//ToolExportCAD->SetSingleConfiguration(1);
	//! [e20s02_cp]

	//! [e20s03_cp]
	// default check boxes settings
	ToolExportCAD->SurfacesAsSolids = true;
	ToolExportCAD->ScatterNSCRays = false;
	ToolExportCAD->ExportDummySurfaces = false;
	ToolExportCAD->SplitNSCRays = false;
	ToolExportCAD->UsePolarization = false;
	//! [e20s03_cp]

	//! [e20s04_cp]
	// set output file name
	ToolExportCAD->OutputFileName = TheApplication->ObjectsDir + "\\CAD Files\\API_CADexport_sample.step";
	//! [e20s04_cp]

	//! [e20s05_cp]
	// Starting exporting
	// Run with a 3 minites timeout
	// Run() and WaitWithTimeout() is inherited from interface ISystemTool.
	// In C++ we need to cast before using these methods.
	cout << "Starting exporting..." << endl;
	ISystemToolPtr baseTool = ToolExportCAD;
	baseTool->Run();
	RunStatus runstatus = baseTool->WaitWithTimeout(3 * 60);

	// Report the status
	switch (runstatus)
	{
	case RunStatus_Completed:
		cout << "Completed!" << endl;
		break;
	case RunStatus_FailedToStart:
		cout << "Failed To Start!" << endl;
		break;
	case RunStatus_InvalidTimeout:
		cout << "Invalid Timeout!" << endl;
		break;
	case RunStatus_TimedOut:
		cout << "Timed Out!" << endl;
		break;
	}
	cout << "Progress: " << baseTool->Progress << endl;

	// If the exporting is not completed and can be cancelled, cancel the work
	if (runstatus != RunStatus_Completed & baseTool->CanCancel)
	{
		baseTool->Cancel();
	}

	// Close the tool
	baseTool->Close();
	//! [e20s05_cp]

#if defined(_DEBUG)
	// keeps console open when in debug mode
	system("pause");
#endif

	// Clean up
	finishStandaloneApplication(TheApplication);
	

	return 0;
}

void handleError(std::string msg)
{
	throw new exception(msg.c_str());
}

void logInfo(std::string msg)
{
	printf("%s", msg.c_str());
}

void finishStandaloneApplication(IZOSAPI_ApplicationPtr TheApplication)
{
    // Note - TheApplication will close automatically when this application exits, so this isn't strictly necessary in most cases
	if (TheApplication != nullptr)
	{
		TheApplication->CloseApplication();
	}
}

int APIENTRY _tWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int nCmdShow)
{
	return RunApplication();
}

int _tmain(int argc, _TCHAR* argv[])
{
	return RunApplication();
}