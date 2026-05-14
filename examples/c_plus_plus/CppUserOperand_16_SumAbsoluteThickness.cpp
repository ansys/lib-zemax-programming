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
#include <vector>

// Note - .tlh files will be generated from the .tlb files (above) once the project is compiled.
// Visual Studio will incorrectly continue to report IntelliSense error messages however until it is restarted.
#include "zosapi.h"

using namespace std;
using namespace ZOSAPI;
using namespace ZOSAPI_Interfaces;

void handleError(std::string msg);
void logInfo(std::string msg);
void finishUserOperand(IZOSAPI_ApplicationPtr TheApplication, std::vector<double> &resultData);

int RunOperand()
{
	CoInitialize(NULL);

	// Create the initial connection class
	IZOSAPI_ConnectionPtr TheConnection(__uuidof(ZOSAPI_Connection));


	// Attempt to connect to the existing OpticStudio instance
	IZOSAPI_ApplicationPtr TheApplication = nullptr;
	try
	{
		TheApplication = TheConnection->ConnectToApplication(); // this will throw an exception if not launched from OpticStudio
	}
	catch (exception &ex)
	{
		handleError(ex.what());
		return -1;
	}
	if (TheApplication == nullptr)
	{
		handleError("An unknown connection error occurred!");
		return -1;
	}
	if (TheApplication->Mode != ZOSAPI_Mode::ZOSAPI_Mode_Operand)
	{
		handleError("User Operand started in wrong mode!");
		return -1;
	}

	// Check the connection status
	if (!TheApplication->IsValidLicenseForAPI)
	{
		handleError("License check failed!");
		return -1;
	}


	// Read the operand arguments
	double Hx = TheApplication->OperandArgument1;
	double Hy = TheApplication->OperandArgument2;
	double Px = TheApplication->OperandArgument3;
	double Py = TheApplication->OperandArgument4;

	// Initialize the output array
	int maxResultLength = TheApplication->OperandResults->Length;
	std::vector<double> operandResults(maxResultLength);

	IOpticalSystemPtr TheSystem = TheApplication->PrimarySystem;
	// Add your custom code here...

	// This is an example that calculates the sum of absolute distance between surfaces. 
	// Hx -> Surf1
	// Hy -> Surf2

	//! [e16s01_cp]
	// Read the operand arguments (Note that we aren't using operand 3 and 4)
	int surf1 = (int)TheApplication->OperandArgument1;
	int surf2 = (int)TheApplication->OperandArgument2;
	//double x = (double)TheApplication->OperandArgument3;
	//double y = (double)TheApplication->OperandArgument4;    
	//! [e16s01_cp]

	//! [e16s02_cp]
	//Make the sum of the absolute value of each surface thickness
	ILDERowPtr surf;
	double thic = 0;
	
	if (surf1 <= surf2)
	{
		for (int i = surf1; i <= surf2; i++)
		{
			surf = TheSystem->LDE->GetSurfaceAt(i);
			thic = thic + abs(surf->Thickness);
		}
		operandResults[0] = thic;
	}
	else
	{
		operandResults[0] = 1e9;    // invalid input
	}
	//! [e16s02_cp]   

	// Clean up
	finishUserOperand(TheApplication, operandResults);

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

void finishUserOperand(IZOSAPI_ApplicationPtr TheApplication, std::vector<double> &resultData)
{
	// Note - OpticStudio will wait for the operand to complete until this application exits 
	if (TheApplication != nullptr)
	{
		TheApplication->OperandResults->WriteData(
			(long)resultData.size(),
			&resultData[0]);
	}
}

int APIENTRY _tWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int nCmdShow)
{
	return RunOperand();
}

int _tmain(int argc, _TCHAR* argv[])
{
	return RunOperand();
}