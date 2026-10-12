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


#include <windows.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <array>
#include <complex>
using namespace std;

/*
2021-09-16 Written by Michael Cheng
This is an ideal polarizer in NSC mode.

2022-08-03 Updated by Michael Cheng
Update to support curved surface, change medium, and reflection.

*/

extern "C" {
	int __declspec(dllexport) APIENTRY UserDiffraction(double *data);
	int __declspec(dllexport) APIENTRY UserParamNames(char *data);
}

BOOL WINAPI DllMain(HANDLE hInst, ULONG ul_reason_for_call, LPVOID lpReserved) {return TRUE;}

/* the data is stored as follows:
data[0]  = the total number of values in the passed data array
data[1]  = x position
data[2]  = y position
data[3]  = z position
data[4]  = x cosine
data[5]  = y cosine
data[6]  = z cosine
data[7]  = x cosine surface normal
data[8]  = y cosine surface normal
data[9]  = z cosine surface normal
data[10] = wavelength in micron
data[11] = 0 if refractive surface, 1 for reflective. May be set by DLL if data[31] = 1 or 2
data[12] = approach side index
data[13] = exit side index
data[14] = order to be traced now
data[15] = starting order
data[16] = stopping order
data[17] = millimeters per unit length (1.0 for mm, 25.4 for inches, 10.0 for cm and 1000.0 for meters)
data[18] = a random value to use as a seed

data[20] = incident Ex real
data[21] = incident Ex imaginary
data[22] = incident Ey real
data[23] = incident Ey imaginary
data[24] = incident Ez real
data[25] = incident Ez imaginary

data[30] = relative energy (to be computed by the dll and returned)
data[31] = flag = 1 if DLL returns phase and phase derivatives; = 2 if complete output ray data

if the DLL sets data[31] = 1; then the DLL must return the phase and derivative.
if the DLL sets data[31] = 2; then the DLL must return complete ray data.

data 32-34 only need to be computed if the DLL sets data[31] = 1 or 2
data[32] = output phase added to ray
data[33] = derivative of the phase with respect to x
data[34] = derivative of the phase with respect to y

data 35-45 only need to be computed if the DLL sets data[31] = 2
data[35] = output x cosine
data[36] = output y cosine
data[37] = output z cosine

data[40] = output Ex real
data[41] = output Ex imaginary
data[42] = output Ey real
data[43] = output Ey imaginary
data[44] = output Ez real
data[45] = output Ez imaginary

data[51] = input parameter 1 from user
data[52] = input parameter 2 from user
etc... up to data[maxdata] where maxdata = int(data[0])

The DLL must set data 30 and 31 given the other data, and possibly data 32-45.

Return 0 if it works; else return -1.

*/
double DotProduct(array<double, 3> v1, array<double, 3> v2)
{
	return (v1[0] * v2[0] + v1[1] * v2[1]) + v1[2] * v2[2];
}
bool Normalize(array<double, 3>* v)
{
	double temp;
	temp = sqrt(DotProduct(*v, *v));
	temp = 1.0 / temp;
	(*v)[0] *= temp;
	(*v)[1] *= temp;
	(*v)[2] *= temp;
	return true;
}
array<double, 3> CrossProduct(array<double, 3> v1, array<double, 3> v2)
{
	array<double, 3> v3;
	v3[0] = v1[1] * v2[2] - v1[2] * v2[1];
	v3[1] = v1[2] * v2[0] - v1[0] * v2[2];
	v3[2] = v1[0] * v2[1] - v1[1] * v2[0];
	return v3;
}
int sgn(double v) { return (((v) < 0) ? -1 : ((v) > 0)); }
int __declspec(dllexport) APIENTRY UserDiffraction(double *data)
{
	if (abs(abs(data[8]) - 1.0) < 1e-8)
		return -1;
	if (data[14] != data[15])	// no diffraction
	{
		data[30] = 0;
		return 0;
	}

	// Parameter
	double leakT = data[51];
	double leakR = data[52];
	if (leakT < 0 || leakT > 1)
		leakT = 0;
	if (leakR < 0 || leakR > 1)
		leakR = 0;

	// Get data ready
	array<double, 3> vi, nvec, xvec, yvec;
	array<complex<double>, 3> Ei;
	for (int i = 0; i < 3; i++)
		nvec[i] = data[7 + i];
	bool isref = data[11] == 1;
	double
		n_appr = data[12],
		n_exit = data[13];

	// 3 local vectors (nvec = zvec)
	xvec = CrossProduct(nvec, { 0,1,0 });
	Normalize(&xvec);
	yvec = CrossProduct(nvec, xvec);

	// Project data to local coordinate
	vi[0] = data[4] * xvec[0] + data[5] * xvec[1] + data[6] * xvec[2];
	vi[1] = data[4] * yvec[0] + data[5] * yvec[1] + data[6] * yvec[2];
	vi[2] = data[4] * nvec[0] + data[5] * nvec[1] + data[6] * nvec[2];
	Ei[0] = complex<double>(
		xvec[0] * data[20] + xvec[1] * data[22] + xvec[2] * data[24],
		xvec[0] * data[21] + xvec[1] * data[23] + xvec[2] * data[25]);
	Ei[1] = complex<double>(
		yvec[0] * data[20] + yvec[1] * data[22] + yvec[2] * data[24],
		yvec[0] * data[21] + yvec[1] * data[23] + yvec[2] * data[25]);
	Ei[2] = complex<double>(
		nvec[0] * data[20] + nvec[1] * data[22] + nvec[2] * data[24],
		nvec[0] * data[21] + nvec[1] * data[23] + nvec[2] * data[25]);

	// Calcualte transmission data
	array<double, 3> vt;
	array<complex<double>, 3> Et;
	vt[0] = vi[0] * n_appr / n_exit;
	vt[1] = vi[1] * n_appr / n_exit;
	vt[2] = 1.0 - vt[0] * vt[0] - vt[1] * vt[1];
	if (vt[2] <= 0)
	{
		data[30] = 0;
		return 0;
	}
	vt[2] = sqrt(vt[2]) * sgn(vi[2]);
	
	double 
		WB = vi[0] * vi[1] / (vi[0] * vi[0] - 1.0);

	Et[0] = leakT * Ei[0];
	Et[1] = (WB * (leakT - (1 - leakR)) * Ei[0] + Ei[1] * (1 - leakR));
	Et[2] = -(Et[0] * vt[0] + Et[1] * vt[1]) / vt[2];

	array<double, 3> vr;
	array<complex<double>, 3> Er;
	vr[0] = vi[0];
	vr[1] = vi[1];
	vr[2] = -vi[2];

	Er[0] = Et[0] - Ei[0];
	Er[1] = Et[1] - Ei[1];
	Er[2] = -(Er[0] * vr[0] + Er[1] * vr[1]) / vr[2];

	double normlize_ratio = sqrt((norm(Ei[0]) + norm(Ei[1]) + norm(Ei[2])) / 
		(norm(Er[0]) + norm(Er[1]) + norm(Er[2]) + norm(Et[0]) + norm(Et[1]) + norm(Et[2])));

	if (!isref)
		for (int i = 0; i < 3; i++)
		{
			data[35 + i] = vt[0] * xvec[i] + vt[1] * yvec[i] + vt[2] * nvec[i];
			data[40 + i * 2] = (Et[0].real() * xvec[i] + Et[1].real() * yvec[i] + Et[2].real() * nvec[i]) * normlize_ratio;
			data[41 + i * 2] = (Et[0].imag() * xvec[i] + Et[1].imag() * yvec[i] + Et[2].imag() * nvec[i]) * normlize_ratio;
		}
	else
		for (int i = 0; i < 3; i++)
		{
			data[35 + i] = vr[0] * xvec[i] + vr[1] * yvec[i] + vr[2] * nvec[i];
			data[40 + i * 2] = (Er[0].real() * xvec[i] + Er[1].real() * yvec[i] + Er[2].real() * nvec[i]) * normlize_ratio;
			data[41 + i * 2] = (Er[0].imag() * xvec[i] + Er[1].imag() * yvec[i] + Er[2].imag() * nvec[i]) * normlize_ratio;
		}

	data[31] = 2;

	return 0;
}
int __declspec(dllexport) APIENTRY UserParamNames(char *data)
{
	int i = (int)data[0];
	switch (i)
	{
	case 1: strcpy(data, "T Leak");	break;
	case 2: strcpy(data, "R Leak");	break;
	default:strcpy(data, "");
	}
	return 0;
}
