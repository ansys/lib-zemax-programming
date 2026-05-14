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

// c_plus_plus_user_analysis.cpp : Defines the entry point for the console application.

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

//void handleError(std::string msg);
void logInfo(std::string msg);
void runUserAnalysis(IZOSAPI_ApplicationPtr TheApplication);
void showUserAnalysisSettings(IZOSAPI_ApplicationPtr TheApplication);
void finishUserAnalysis(IZOSAPI_ApplicationPtr TheApplication);

int RunAnalysis()
{
	CoInitialize(nullptr);

	// Create the initial connection class
	IZOSAPI_ConnectionPtr TheConnection(__uuidof(ZOSAPI_Connection));


	// Attempt to create a Standalone connection
	IZOSAPI_ApplicationPtr TheApplication = nullptr;
	try {
		TheApplication = TheConnection->ConnectToApplication();
	}
	catch (exception &ex)
	{
		handleError(ex.what());
		return -1;
	}

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
	switch (TheApplication->Mode)
	{
	case ZOSAPI_Mode::ZOSAPI_Mode_UserAnalysis:
		runUserAnalysis(TheApplication);
		break;
	case ZOSAPI_Mode::ZOSAPI_Mode_UserAnalysisSettings:
		showUserAnalysisSettings(TheApplication);
		break;
	default:
		handleError("User analysis was started in the wrong mode!");
		return -1;
	}

	// Clean up
	finishUserAnalysis(TheApplication);

	return 0;
}

void runUserAnalysis(IZOSAPI_ApplicationPtr TheApplication)
{
	IOpticalSystemPtr TheSystem = TheApplication->PrimarySystem;

	// Use TheAnalysisData to create a specific plot type and populate the data
	IUserAnalysisDataPtr TheAnalysisData = TheApplication->UserAnalysisData;
	ISettingsDataPtr TheSettings = TheAnalysisData->UserSettings;

	// Add your custom code here...

	//std::wstring plotTitle(L"New 2D Line Plot");
	//double xVals[] = { 1.0, 2.0, 3.0 };
	//IUser2DLineDataPtr linePlot = TheAnalysisData->Make2DLinePlot(plotTitle.c_str(), 3, xVals);
	//linePlot->AddSeries(...);
}

void showUserAnalysisSettings(IZOSAPI_ApplicationPtr TheApplication)
{
	std::wstring key;

	IOpticalSystemPtr TheSystem = TheApplication->PrimarySystem;

	IUserAnalysisDataPtr TheAnalysisData = TheApplication->UserAnalysisData;

	// TODO - retrieve the settings specific to your analysis here
	ISettingsDataPtr TheSettings = TheAnalysisData->UserSettings;
	//key.assign(L"FloatValue1");
	//float val1;
	//TheSettings->GetFloatValue(key.c_str(), &val1);

	// show a UI to modify settings...


	// TODO - write settings back to TheSettings
	//TheSettings->SetFloatValue(key.c_str(), val1);
}

void handleError(std::string msg)
{
	throw exception(msg.c_str());
}

void logInfo(std::string msg)
{
	printf("%s", msg.c_str());
}

void finishUserAnalysis(IZOSAPI_ApplicationPtr TheApplication)
{
	// Note - OpticStudio will wait for the operand to complete until this application exits 
}

int APIENTRY _tWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int nCmdShow)
{
	return RunAnalysis();
}

int _tmain(int argc, _TCHAR* argv[])
{
	return RunAnalysis();
}