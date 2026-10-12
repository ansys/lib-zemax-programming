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
#include <math.h>
#include <string.h>
#include "usersurf.h"

/*
Written by Michael Cheng, start from us_binary.c
August 5, 2020
*/

#define PI 3.141592654
extern "C" { 
	int __declspec(dllexport) APIENTRY UserDefinedSurface5(USER_DATA *UD, FIXED_DATA5 *FD); 
}
int Refract(double thisn, double nextn, double *l, double *m, double *n, double ln, double mn, double nn);
BOOL WINAPI DllMain(HANDLE hInst, ULONG ul_reason_for_call, LPVOID lpReserved) { return TRUE; }
int sgn(double v) { return (((v) < 0) ? -1 : ((v) > 0)); }

int __declspec(dllexport) APIENTRY UserDefinedSurface5(USER_DATA *UD, FIXED_DATA5 *FD)
{
	int i, loop;
	double dz, tp;
	double p2, alpha, a, b, c, rad, casp, t, zc, mx, my, k, dpdn2, factor;
	double nx, ny, nz, L, R, phase, dpdrho2, dpdx, dpdy;
	double rho1, rho2, n, n2, n4, n6, ux, uy, uz,nn;
	double tmp;
	double y1, y2, y3, y4, y5, x1, x2, x3, x4, x5, x6;
	double M;

	switch (FD->type)
	{
	case 0:
		switch (FD->numb)
		{
		case 0:
			/* Name of the surface */
			strcpy(UD->string, "Binary mix 1&2");
			break;
		case 1:
			/* rotationally symmetric? Yes.*/
			strcpy(UD->string, "\0");
			break;
		case 2:
			/* gradient index media? No. */
			UD->string[0] = '\0';
			break;
		}
		break;
	case 1:
		/* Names of the parameters */
		switch (FD->numb)
		{
		case 0:
			strcpy(UD->string, "Norm Radius");
			break;
		case 1:
			strcpy(UD->string, "r^2");
			break;
		case 2:
			strcpy(UD->string, "r^4");
			break;
		case 3:
			strcpy(UD->string, "r^6");
			break;
		case 4:
			strcpy(UD->string, "r^8");
			break;
		case 5:
			strcpy(UD->string, "r^10");
			break;
		case 6:
			strcpy(UD->string, "r^12");
			break;
		case 7:
			strcpy(UD->string, "r^14");
			break;
		case 8:
			strcpy(UD->string, "r^16");
			break;
		case 9:
			strcpy(UD->string, "r^18");
			break;
		case 10:
			strcpy(UD->string, "r^20");
			break;
		case 11:
			strcpy(UD->string, "Diff Order");
			break;
		case 12:
			strcpy(UD->string, "X0Y1");
			break;
		case 13:
			strcpy(UD->string, "X0Y2");
			break;
		case 14:
			strcpy(UD->string, "X0Y3");
			break;
		case 15:
			strcpy(UD->string, "X0Y4");
			break;
		case 16:
			strcpy(UD->string, "X0Y5");
			break;
		case 17:
			strcpy(UD->string, "X2Y0");
			break;
		case 18:
			strcpy(UD->string, "X2Y1");
			break;
		case 19:
			strcpy(UD->string, "X2Y2");
			break;
		case 20:
			strcpy(UD->string, "X2Y3");
			break;
		case 21:
			strcpy(UD->string, "X2Y4");
			break;
		case 22:
			strcpy(UD->string, "X2Y5");
			break;
		case 23:
			strcpy(UD->string, "X4Y0");
			break;
		case 24:
			strcpy(UD->string, "X4Y1");
			break;
		case 25:
			strcpy(UD->string, "X4Y2");
			break;
		case 26:
			strcpy(UD->string, "X4Y3");
			break;
		case 27:
			strcpy(UD->string, "X4Y4");
			break;
		case 28:
			strcpy(UD->string, "X4Y5");
			break;
		case 29:
			strcpy(UD->string, "X6Y0");
			break;
		case 30:
			strcpy(UD->string, "X6Y1");
			break;
		case 31:
			strcpy(UD->string, "X6Y2");
			break;
		case 32:
			strcpy(UD->string, "X6Y3");
			break;
		case 33:
			strcpy(UD->string, "X6Y4");
			break;
		case 34:
			strcpy(UD->string, "X6Y5");
			break;
		case 35:
			strcpy(UD->string, "Par. Pow. Mode");
			break;
		case 36:
			strcpy(UD->string, "Custom Pow.");
			break;
		case 37:
			strcpy(UD->string, "X1");
			break;
		case 38:
			strcpy(UD->string, "X3");
			break;
		default:
			UD->string[0] = '\0';
			break;
		}
		break;
	case 2:
		/* Names of the extra data columns */
		switch (FD->numb)
		{
		default:
			UD->string[0] = '\0';
			break;
		}
		break;
	case 3:
		/* Sag of the surface */
		UD->sag1 = 0.0;
		UD->sag2 = 0.0;
		break;
	case 4:
	{
		/* Paraxial ray trace to this surface */
		/* x, y, z, and the optical path are unaffected, at least for this surface type */
		/* for paraxial ray tracing, the return z coordinate should always be zero. */
		/* paraxial surfaces are always planes with the following normals */

		/* for paraxial ray tracing, grating effects are ignored */
		/* this is exactly like the standard surface code */
		UD->ln = 0.0;
		UD->mn = 0.0;
		UD->nn = -1.0;
		//power = (FD->n2 - FD->n1)*FD->cv;
		M = FD->param[11];
		int ParPowMode = FD->param[35];
		double powerx = 0;
		double powery = 0;
		if (ParPowMode == 1) // use Y power
		{
			powerx = 0;
			powery = -M * FD->wavelength * 1e-3 * (FD->param[1] + FD->param[13]) / (PI * FD->param[0] * FD->param[0]);
		}
		else if (ParPowMode == 2) // use X power
		{
			powerx = -M * FD->wavelength * 1e-3 * (FD->param[1] + FD->param[17]) / (PI * FD->param[0] * FD->param[0]);
			powery = 0;
		}
		else if (ParPowMode == 3) // customize power
		{
			powerx = FD->param[36];
			powery = powerx;
		}
		else if (ParPowMode == 4)
		{

		}

		if ((UD->n) != 0.0)
		{
			(UD->l) = (UD->l) / (UD->n);
			(UD->m) = (UD->m) / (UD->n);

			(UD->l) = (FD->n1 * (UD->l) - (UD->x) * powerx) / (FD->n2);
			(UD->m) = (FD->n1 * (UD->m) - (UD->y) * powery) / (FD->n2);

			/* normalize */
			(UD->n) = sqrt(1 / (1 + (UD->l) * (UD->l) + (UD->m) * (UD->m)));
			/* de-paraxialize */
			(UD->l) = (UD->l) * (UD->n);
			(UD->m) = (UD->m) * (UD->n);
		}
		break;
	}
	case 5:
	{
		/* Real ray trace to this surface */

		// This is a plane.
		UD->ln = 0;
		UD->mn = 0;
		UD->nn = -1;

		// Diffraction
			/* Convention in OpticStudio is that ray vectors are reversed in MIRROR space.
			I don't wnat to handle it, so I reverse it to positve if rays come from MIRROR space. */
		if ((FD->is_a_mirror && !FD->is_in_mirror_space) || (!FD->is_a_mirror && FD->is_in_mirror_space))
		{
			UD->l *= -1;
			UD->m *= -1;
			UD->n *= -1;
		}

		// Read order, norm radius, wavelength
		R = FD->param[0];
		L = FD->wavelength * 1e-3;
		M = FD->param[11];
		if (R <= 0.0) R = 1e8;

		if (fabs(UD->x) > 1e-8 || fabs(UD->y) > 1e-8)
		{
			rho2 = (UD->x * UD->x + UD->y * UD->y) / (R * R);
			rho1 = sqrt(rho2);
			phase = FD->param[10];
			dpdrho2 = 10.0 * FD->param[10];
			for (int i = 9; i > 0; i--)
			{
				phase = FD->param[i] + rho2 * phase;
				dpdrho2 = double(i) * FD->param[i] + rho2 * dpdrho2;
			}
			phase *= rho2 * M;

			tmp = M * L / (PI * R * R * fabs(FD->n2)) * dpdrho2;  // 2 * L / (2 * PI * R * R * fabs(FD->n2))
			dpdx = tmp * UD->x;
			dpdy = tmp * UD->y;
		}
		else
		{
			phase = 0;
			dpdx = 0;
			dpdy = 0;
		}

		x1 = UD->x / R;
		x2 = x1 * x1;
		x3 = x1 * x2;
		x4 = x2 * x2;
		x5 = x2 * x3;
		x6 = x3 * x3;
		y1 = UD->y / R;
		y2 = y1 * y1;
		y3 = y1 * y2;
		y4 = y2 * y2;
		y5 = y2 * y3;

		phase += M *
			(FD->param[34] * x6 * y5 + FD->param[33] * x6 * y4
				+ FD->param[32] * x6 * y3 + FD->param[28] * x4 * y5
				+ FD->param[31] * x6 * y2 + FD->param[27] * x4 * y4
				+ FD->param[30] * x6 * y1 + FD->param[26] * x4 * y3 + FD->param[22] * x2 * y5
				+ FD->param[29] * x6 + FD->param[25] * x4 * y2 + FD->param[21] * x2 * y4
				+ FD->param[24] * x4 * y1 + FD->param[20] * x2 * y3 + FD->param[16] * y5
				+ FD->param[23] * x4 + FD->param[19] * x2 * y2 + FD->param[15] * y4
				+ FD->param[18] * x2 * y1 + FD->param[14] * y3
				+ FD->param[17] * x2 + FD->param[13] * y2 + FD->param[12] * y1)
			+ FD->param[37] * x1 + FD->param[38] * x3;

		tmp = M * L / (2 * PI * R * fabs(FD->n2));
		dpdx += (6 * FD->param[34] * x5 * y5 + 6 * FD->param[33] * x5 * y4
			+ 6 * FD->param[32] * x5 * y3 + 4 * FD->param[28] * x3 * y5
			+ 6 * FD->param[31] * x5 * y2 + 4 * FD->param[27] * x3 * y4
			+ 6 * FD->param[30] * x5 * y1 + 4 * FD->param[26] * x3 * y3 + 2 * FD->param[22] * x1 * y5
			+ 6 * FD->param[29] * x5 + 4 * FD->param[25] * x3 * y2 + 2 * FD->param[21] * x1 * y4
			+ 4 * FD->param[24] * x3 * y1 + 2 * FD->param[20] * x1 * y3
			+ 4 * FD->param[23] * x3 + 2 * FD->param[19] * x1 * y2
			+ 2 * FD->param[18] * x1 * y1
			+ 2 * FD->param[17] * x1
			+ 1 * FD->param[37] + 3 * FD->param[38] * x2) * tmp;

		dpdy += (5 * FD->param[34] * x6 * y4 + 4 * FD->param[33] * x6 * y3
			+ 3 * FD->param[32] * x6 * y2 + 5 * FD->param[28] * x4 * y4
			+ 2 * FD->param[31] * x6 * y1 + 4 * FD->param[27] * x4 * y3
			+ 1 * FD->param[30] * x6 + 3 * FD->param[26] * x4 * y2 + 5 * FD->param[22] * x2 * y4
			+ 2 * FD->param[25] * x4 * y1 + 4 * FD->param[21] * x2 * y3
			+ 1 * FD->param[24] * x4 + 3 * FD->param[20] * x2 * y2 + 5 * FD->param[16] * y4
			+ 2 * FD->param[19] * x2 * y1 + 4 * FD->param[15] * y3
			+ 1 * FD->param[18] * x2 + 3 * FD->param[14] * y2
			+ 2 * FD->param[13] * y1 + 1 * FD->param[12]) * tmp;

		UD->l = UD->l * fabs(FD->n1 / FD->n2) + dpdx;
		UD->m = UD->m * fabs(FD->n1 / FD->n2) + dpdy;
		tmp = 1 - UD->l * UD->l - UD->m * UD->m;
		if (tmp <= 0) return -1;
		if (FD->is_a_mirror)
			UD->n = sqrt(tmp) * sgn(UD->n) * -1;
		else
			UD->n = sqrt(tmp) * sgn(UD->n);

		UD->path = phase * L / (2 * PI) / FD->n1;

		// Reverse the output lmn if it's mirror space after the surface
		// This is OpticStudio sign convention
		if (FD->is_in_mirror_space)
		{
			UD->l *= -1;
			UD->m *= -1;
			UD->n *= -1;
		}
		break;
	}
	case 6:
	{
		/* ZEMAX wants the index, dn/dx, dn/dy, and dn/dz at the given x, y, z. */
		 /* This is only required for gradient index surfaces, so return dummy values */
		UD->index = FD->n2;
		UD->dndx = 0.0;
		UD->dndy = 0.0;
		UD->dndz = 0.0;
		break;
	}
	case 7:
	{
		/* ZEMAX wants the "safe" data. */
		 /* this is used by ZEMAX to set the initial values for all parameters and extra data */
		 /* when the user first changes to this surface type. */
		 /* this is the only time the DLL should modify the data in the FIXED_DATA FD structure */
		for (i = 1; i <= 100; i++) FD->param[i] = 0.0;
		FD->param[11] = 1.0;
		break;
	}
	}
	return 0;
}

int Refract(double thisn, double nextn, double *l, double *m, double *n, double ln, double mn, double nn)
{
	double nr, cosi, cosi2, rad, cosr, gamma;
	if (thisn != nextn)
	{
		nr = thisn / nextn;
		cosi = fabs((*l) * ln + (*m) * mn + (*n) * nn);
		cosi2 = cosi * cosi;
		if (cosi2 > 1) cosi2 = 1;
		rad = 1 - ((1 - cosi2) * (nr * nr));
		if (rad < 0) return(-1);
		cosr = sqrt(rad);
		gamma = nr * cosi - cosr;
		(*l) = (nr * (*l)) + (gamma * ln);
		(*m) = (nr * (*m)) + (gamma * mn);
		(*n) = (nr * (*n)) + (gamma * nn);
	}
	return 0;
}
