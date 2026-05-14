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

// UDOC01.cpp : Defines the entry point for the console application.

#include "stdafx.h"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <string>
#include <ctime>
#include <functional>
#include <assert.h>
#include <vector>

#import "C:\\Program Files\\Zemax OpticStudio\\ZOS-API\\Libraries\\ZOSAPII.tlb"
#import "C:\\Program Files\\Zemax OpticStudio\\ZOS-API\\Libraries\\ZOSAPI.tlb"

using namespace std;
using namespace ZOSAPI;
using namespace ZOSAPI_Interfaces;

void handleError(std::string msg);
void logInfo(std::string msg);
void finishUserOperand(IZOSAPI_ApplicationPtr TheApplication, std::vector<double> &resultData);

int APIENTRY _tWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int nCmdShow)
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

	// Add your custom code here...


	// This is an example that calculates the sag value(s) at the specified surface and location

	// Read the operand arguments (Note that we aren't used operand 2)
	int surf = (int)TheApplication->OperandArgument1;
	double x = TheApplication->OperandArgument3;
	double y = TheApplication->OperandArgument4;

	// Initialize the output array
	int maxResultLength = TheApplication->OperandResults->Length;
	std::vector<double> operandResults(maxResultLength);

	IOpticalSystemPtr TheSystem = TheApplication->PrimarySystem;
	if (surf >= 0 && surf < TheSystem->LDE->NumberOfSurfaces)
	{
		TheSystem->LDE->GetSag(surf, x, y, &operandResults[0], &operandResults[1]);
	}
	else
	{
		// invalid input
		operandResults[0] = 1e9;
		operandResults[1] = 1e9;
	}

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
		// Set the result data back.  
		// Note that even though we are using only two values, we get and set the entire vector (1001 elements).
		// This is a requirement - the vector length must be unchanged or an exception will be thrown.
		TheApplication->OperandResults->WriteData(
			(long)resultData.size(),
			&resultData[0]);
	}
}

