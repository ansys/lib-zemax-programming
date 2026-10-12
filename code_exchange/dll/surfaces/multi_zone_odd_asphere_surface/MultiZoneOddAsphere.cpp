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
#include <stdio.h>
#include "usersurf.h"

extern "C" {
	int __declspec(dllexport) APIENTRY UserDefinedSurface(USER_DATA* UD, FIXED_DATA* FD);
}

/* a generic Snells law refraction routine */
int Refract(double thisn, double nextn, double* l, double* m, double* n, double ln, double mn, double nn);

/* BOOL WINAPI DllMain(HANDLE hInst, ULONG ul_reason_for_call, LPVOID lpReserved)
{
	return TRUE;
}
*/

/*

This DLL models a multi-zone odd asphere surface.
The first zone starts at r = 0 and extends to Rmax.
Each subsequent zone starts at the previous zone Rmax and extends to the Rmax for the current zone.
Each zone has a sag given by:

Z = N /(1 + sqrt(D)) + A

where

N = c * r^2
D = 1 - (1+k)*(c^2)*(r^2)
A = sum(i = 1 to 12) Ai * r ^ i
Each zone is offset in Z so that the surface is continuous across zone boundaries

There are M zones. The last zone Rmax value is ignored, and the last defined zone is assumed to extend to any r value required for ray tracing.
Up to 15 concentric zones are supported.
*/

typedef struct
{
	double c, k;
	double A[13];
	double Rmax;
	double Zo;
}ZONE_DATA;

#define MAX_ZONES 15


int __declspec(dllexport) APIENTRY UserDefinedSurface(USER_DATA* UD, FIXED_DATA* FD)
{
	int i, loop, M, Z;
	double A, N, D, power, t, tp, x, y, z, dz, sag;
	double dNdx, dNdy, dDdx, dDdy, dAdr, dAdx, dAdy, alpha, mx, my, r1, r2;
	ZONE_DATA zd[MAX_ZONES + 1];

	switch (FD->type)
	{
	case 0:
		/* ZEMAX is requesting general information about the surface */
		switch (FD->numb)
		{
		case 0:
			/* ZEMAX wants to know the name of the surface */
			 /* do not exceed 20 characters */
			strcpy(UD->string, "MultiZoneOddAsphere");
			break;
		case 1:
			/* ZEMAX wants to know if this surface is rotationally symmetric */
		   /* it is, so return any string */
			strcpy(UD->string, "1");
			break;
		case 2:
			/* ZEMAX wants to know if this surface is a gradient index media */
		   /* it is not, so return a null string */
			UD->string[0] = '\0';
			break;
		}
		break;
	case 1:
		/* ZEMAX is requesting the names of the parameter columns */
		 /* the value FD->numb will indicate which value ZEMAX wants. */
		 /* returning a null string indicates that the parameter is unused. */
		switch (FD->numb)
		{
		default:
			UD->string[0] = '\0';
			break;
		}
		break;
	case 2:
		/* ZEMAX is requesting the names of the extra data columns */
		 /* the value FD->numb will indicate which value ZEMAX wants. */
		 /* returning a null string indicates that the extradata value is unused. */
		UD->string[0] = '\0';

		// how may zones are there?
		M = (int)FD->xdata[1];
		if (M < 0) M = 1;
		if (M > MAX_ZONES) M = MAX_ZONES;
		// the data for each zone is
		// radius 2
		// conic 3
		// A1 4
		// A2 5
		// A3 6
		// A4 7
		// A5 8
		// A6 9
		// A7 10
		// A8 11
		// A9 12
		// A10 13
		// A11 14
		// A12 15
		// Rmax 16

		Z = 1;
		i = FD->numb;
		while (i > 16)
		{
			i -= 15;
			Z++;
		}
		if (Z <= M)
		{
			switch (i)
			{
			case 1:
				sprintf(UD->string, "Max Zones");
				break;
			case 2:
				sprintf(UD->string, "Radius %i", Z);
				break;
			case 3:
				sprintf(UD->string, "Conic %i", Z);
				break;
			case 4:
				sprintf(UD->string, "A on r %i", Z);
				break;
			case 5:
				sprintf(UD->string, "A on r^2 %i", Z);
				break;
			case 6:
				sprintf(UD->string, "A on r^3 %i", Z);
				break;
			case 7:
				sprintf(UD->string, "A on r^4 %i", Z);
				break;
			case 8:
				sprintf(UD->string, "A on r^5 %i", Z);
				break;
			case 9:
				sprintf(UD->string, "A on r^6 %i", Z);
				break;
			case 10:
				sprintf(UD->string, "A on r^7 %i", Z);
				break; 
			case 11:
				sprintf(UD->string, "A on r^8 %i", Z);
				break; 
			case 12:
				sprintf(UD->string, "A on r^9 %i", Z);
				break; 
			case 13:
				sprintf(UD->string, "A on r^10 %i", Z);
				break;
			case 14:
				sprintf(UD->string, "A on r^11 %i", Z);
				break;
			case 15:
				sprintf(UD->string, "A on r^12 %i", Z);
				break;
			case 16:
				sprintf(UD->string, "R Max %i", Z);
				break;
			}
		}
		break;
	case 3:
		/* ZEMAX wants to know the sag of the surface */

		UD->sag1 = 0.0;
		UD->sag2 = 0.0;

		// how many zones?
		M = (int)FD->xdata[1];
		if (M < 0) M = 1;
		if (M > MAX_ZONES) M = MAX_ZONES;

		// load the zone data
		ZeroMemory(zd, sizeof(ZONE_DATA) * (MAX_ZONES + 1));
		for (Z = 1; Z <= M; Z++)
		{
			zd[Z].c = FD->xdata[2 + 15 * (Z - 1)];
			if (zd[Z].c != 0.0) zd[Z].c = 1.0 / zd[Z].c;
			zd[Z].k = FD->xdata[3 + 15 * (Z - 1)];
			for (i = 1; i <= 12; i++)
			{
				zd[Z].A[i] = FD->xdata[3 + i + 15 * (Z - 1)];
			}
			zd[Z].Rmax = fabs(FD->xdata[16 + 15 * (Z - 1)]);
		}

		// compute the Zo offsets
		for (Z = 1; Z <= M; Z++)
		{
			// confirm the Rmax values are monotonic
			if (zd[Z].Rmax < zd[Z - 1].Rmax) zd[Z].Rmax = zd[Z - 1].Rmax;

			// compute the offset at the origin of this zone
			r1 = zd[Z - 1].Rmax;
			r2 = r1 * r1;

			// sag from previous zone at this r
			N = zd[Z - 1].c * r1 * r1;
			D = 1.0 - (1.0 + zd[Z - 1].k) * zd[Z - 1].c * zd[Z - 1].c * r1 * r1;
			if (D < 0) return(-1);
			A = 0.0;
			for (i = 12; i >= 1; i--)
			{
				A = zd[Z - 1].A[i] + r1 * A;
			}
			A *= r1;

			zd[Z].Zo += (N / (1.0 + sqrt(D)) + A);

			// sag from this zone at this r
			N = zd[Z].c * r1 * r1;
			D = 1.0 - (1.0 + zd[Z].k) * zd[Z].c * zd[Z].c * r1 * r1;
			if (D < 0) return(-1);
			A = 0.0;
			for (i = 12; i >= 1; i--)
			{
				A = zd[Z].A[i] + r1 * A;
			}
			A *= r1;

			zd[Z].Zo -= (N / (1.0 + sqrt(D)) + A);

			// don't forget the previous offset
			zd[Z].Zo += zd[Z - 1].Zo;
		}

		// compute the sag at the given point

		// what is the radial coordinate?
		r2 = UD->x * UD->x + UD->y * UD->y;
		r1 = sqrt(r2);

		// which zone is this in?
		Z = 1;
		while (r1 > zd[Z].Rmax && Z < M) Z++;

		// compute the sag for this zone
		N = zd[Z].c * r2;
		D = 1.0 - (1.0 + zd[Z].k) * zd[Z].c * zd[Z].c * r2;
		if (D < 0) return(-1);

		A = 0.0;
		for (i = 12; i >= 1; i--)
		{
			A = zd[Z].A[i] + r1 * A;
		}
		A *= r1;
		UD->sag1 = zd[Z].Zo + N / (1.0 + sqrt(D)) + A;
		UD->sag2 = UD->sag1;

		break;
	case 4:
		/* ZEMAX wants a paraxial ray trace to this surface */
		 /* x, y, z, and the optical path are unaffected, at least for this surface type */
		 /* for paraxial ray tracing, the return z coordinate should always be zero. */
		 /* paraxial surfaces are always planes with the following normals */

		UD->ln = 0.0;
		UD->mn = 0.0;
		UD->nn = -1.0;

		// load the zone data... we only need the central zone and the A^2 term
		ZeroMemory(zd, sizeof(ZONE_DATA) * (MAX_ZONES + 1));
		Z = 1;
		zd[Z].c = FD->xdata[2];
		if (zd[Z].c != 0.0) zd[Z].c = 1.0 / zd[Z].c;
		zd[Z].A[2] = FD->xdata[5];

		/* account for quadratic asphere term in power */
		power = (FD->n2 - FD->n1) * (zd[Z].c + 2.0 * zd[Z].A[2]);

		if ((UD->n) != 0.0)
		{
			(UD->l) = (UD->l) / (UD->n);
			(UD->m) = (UD->m) / (UD->n);

			(UD->l) = (FD->n1 * (UD->l) - (UD->x) * power) / (FD->n2);
			(UD->m) = (FD->n1 * (UD->m) - (UD->y) * power) / (FD->n2);

			/* normalize */
			(UD->n) = sqrt(1 / (1 + (UD->l) * (UD->l) + (UD->m) * (UD->m)));
			/* de-paraxialize */
			(UD->l) = (UD->l) * (UD->n);
			(UD->m) = (UD->m) * (UD->n);
		}
		break;
	case 5:
		/* ZEMAX wants a real ray trace to this surface */

			// do not allow vertical rays
		if (fabs(UD->n) < 1E-5) return -1;

		// how many zones?
		M = (int)FD->xdata[1];
		if (M < 0) M = 1;
		if (M > MAX_ZONES) M = MAX_ZONES;

		// load the zone data
		ZeroMemory(zd, sizeof(ZONE_DATA) * (MAX_ZONES + 1));
		for (Z = 1; Z <= M; Z++)
		{
			zd[Z].c = FD->xdata[2 + 15 * (Z - 1)];
			if (zd[Z].c != 0.0) zd[Z].c = 1.0 / zd[Z].c;
			zd[Z].k = FD->xdata[3 + 15 * (Z - 1)];
			for (i = 1; i <= 12; i++)
			{
				zd[Z].A[i] = FD->xdata[3 + i + 15 * (Z - 1)];
			}
			zd[Z].Rmax = fabs(FD->xdata[16 + 15 * (Z - 1)]);
		}

		// compute the Zo offsets
		for (Z = 1; Z <= M; Z++)
		{
			// confirm the Rmax values are monotonic
			if (zd[Z].Rmax < zd[Z - 1].Rmax) zd[Z].Rmax = zd[Z - 1].Rmax;

			// compute the offset at the origin of this zone
			r1 = zd[Z - 1].Rmax;
			r2 = r1 * r1;

			// sag from previous zone at this r
			N = zd[Z - 1].c * r1 * r1;
			D = 1.0 - (1.0 + zd[Z - 1].k) * zd[Z - 1].c * zd[Z - 1].c * r1 * r1;
			if (D < 0) return(-1);
			A = 0.0;
			for (i = 12; i >= 1; i--)
			{
				A = zd[Z - 1].A[i] + r1 * A;
			}
			A *= r1;

			zd[Z].Zo += (N / (1.0 + sqrt(D)) + A);

			// sag from this zone at this r
			N = zd[Z].c * r1 * r1;
			D = 1.0 - (1.0 + zd[Z].k) * zd[Z].c * zd[Z].c * r1 * r1;
			if (D < 0) return(-1);
			A = 0.0;
			for (i = 12; i >= 1; i--)
			{
				A = zd[Z].A[i] + r1 * A;
			}
			A *= r1;

			zd[Z].Zo -= (N / (1.0 + sqrt(D)) + A);

			// don't forget the previous offset
			zd[Z].Zo += zd[Z - 1].Zo;
		}

		x = UD->x;
		y = UD->y;
		z = UD->z;
		tp = 0.0;

		/* make sure we do at least 1 loop */

		t = 9e9;
		loop = 0;

		while (fabs(t) > 1e-10)
		{
			// what is the radial coordinate? Note this might change as we iterate
			r2 = x * x + y * y;
			r1 = sqrt(r2);

			// which zone is this in?
			Z = 1;
			while (r1 > zd[Z].Rmax && Z < M) Z++;

			// compute the sag for this zone
			N = zd[Z].c * r2;
			D = 1.0 - (1.0 + zd[Z].k) * zd[Z].c * zd[Z].c * r2;
			if (D < 0) return(-1);

			A = 0.0;
			for (i = 12; i >= 1; i--)
			{
				A = zd[Z].A[i] + r1 * A;
			}
			A *= r1;
			sag = zd[Z].Zo + N / (1.0 + sqrt(D)) + A;

			// how far are we away in z?
			dz = sag - z;

			/* now compute how far along the ray this is */
			//t = dz / (UD->n); correct but may be too aggressive and may not converge
			t = dz * fabs(UD->n);

			/* propagate the additional "t" distance */
			x += UD->l * t;
			y += UD->m * t;
			z += UD->n * t;

			/* add in the optical path */
			tp += t;

			/* prevent infinte loop if no convergence */
			loop++;
			if (loop > 1000) return(-1);
		}

		// okay, we should be at the intercept coordinates now
		UD->x = x;
		UD->y = y;
		UD->z = z;

		// don't forget the path!
		UD->path = tp;

		// now do the normals
		if (x == 0.0 && y == 0.0)
		{
			UD->ln = 0;
			UD->mn = 0;
			UD->nn = -1;
		}
		else
		{
			r2 = x * x + y * y;
			r1 = sqrt(r2);
			N = zd[Z].c * r2;
			D = 1.0 - (1.0 + zd[Z].k) * zd[Z].c * zd[Z].c * r2;
			if (D < 0) return(-1);
			dNdx = 2.0 * zd[Z].c * x;
			dNdy = 2.0 * zd[Z].c * y;
			dDdx = -2.0 * (1.0 + zd[Z].k) * zd[Z].c * zd[Z].c * x;
			dDdy = -2.0 * (1.0 + zd[Z].k) * zd[Z].c * zd[Z].c * y;

			A = 0.0;
			dAdr = 0.0;
			for (i = 12; i >= 1; i--)
			{
				A = zd[Z].A[i] + r1 * A;
				dAdr = (double)i * zd[Z].A[i] + r1 * dAdr;
			}
			A *= r1;
			

			dAdx = dAdr * x / r1;
			dAdy = dAdr * y / r1;

			alpha = 1 + sqrt(D);
			mx = dNdx / (alpha)-N * (1.0 / (alpha * alpha)) * (0.5 / sqrt(D)) * dDdx + dAdx;
			my = dNdy / (alpha)-N * (1.0 / (alpha * alpha)) * (0.5 / sqrt(D)) * dDdy + dAdy;

			UD->nn = -sqrt(1 / (1 + (mx * mx) + (my * my)));
			UD->ln = -mx * UD->nn;
			UD->mn = -my * UD->nn;
		}
		if (Refract(FD->n1, FD->n2, &UD->l, &UD->m, &UD->n, UD->ln, UD->mn, UD->nn)) return(-FD->surf);
		break;
	case 6:
		/* ZEMAX wants the index, dn/dx, dn/dy, and dn/dz at the given x, y, z. */

		 /* This is only required for gradient index surfaces, so return dummy values */
		UD->index = FD->n2;
		UD->dndx = 0.0;
		UD->dndy = 0.0;
		UD->dndz = 0.0;
		break;
	case 7:
		/* ZEMAX wants the "safe" data. */
		 /* this is used by ZEMAX to set the initial values for all parameters and extra data */
		 /* when the user first changes to this surface type. */
		 /* this is the only time the DLL should modify the data in the FIXED_DATA FD structure */
		for (i = 0; i <= 8; i++) FD->param[i] = 0.0;
		for (i = 0; i <= 240; i++) FD->xdata[i] = 0.0;
		FD->xdata[1] = 1.0; // at least one zone!
		break;
	}
	return 0;
}

int Refract(double thisn, double nextn, double* l, double* m, double* n, double ln, double mn, double nn)
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

