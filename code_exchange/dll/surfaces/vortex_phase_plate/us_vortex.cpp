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
Written by Michael Cheng
2021-03-20
*/

#define PI 3.141592654

extern "C"
{
	int __declspec(dllexport) APIENTRY UserDefinedSurface5(USER_DATA* UD, FIXED_DATA5* FD);
}

int sgn(double v) { return (((v) < 0) ? -1 : ((v) > 0)); }
int __declspec(dllexport) APIENTRY UserDefinedSurface5(USER_DATA* UD, FIXED_DATA5* FD)
{
	int i;
	switch (FD->type)
	{
	case 0:
		/* ZEMAX is requesting general information about the surface */
		switch (FD->numb)
		{
		case 0:
			/* ZEMAX wants to know the name of the surface */
			/* do not exceed 12 characters */
			strcpy(UD->string, "Vortex");
			break;
		case 1:
			/* ZEMAX wants to know if this surface is rotationally symmetric */
			/* it is so return any string */
			strcpy(UD->string, "\0");
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
		case 0:
			strcpy(UD->string, "Order");
			break;
		/*case 1:
			strcpy(UD->string, "Bending rays");
			break;*/
		default:
			UD->string[0] = '\0';
			break;
		}
		break;
	case 2:
		/* ZEMAX is requesting the names of the extra data columns */
		 /* the value FD->numb will indicate which value ZEMAX wants. */
		 /* they are all "Unused" for this surface type */
		 /* returning a null string indicates that the extradata value is unused. */
		UD->string[0] = '\0';
		break;
	case 3:
		// requesting sag
		// This is always a plane
		UD->sag1 = 0.0;
		UD->sag2 = 0.0;
		break;
	case 4:
		/* ZEMAX wants a paraxial ray trace to this surface */
		UD->ln = 0.0;
		UD->mn = 0.0;
		UD->nn = -1.0;
		break;
	case 5:
	{
		/* Convention in OpticStudio is that ray vectors are reversed in MIRROR space.
		I don't want to handle it, so I reverse it to positve if rays come from MIRROR space. */
		bool isFrMIRROR = (FD->is_a_mirror && !FD->is_in_mirror_space) || (!FD->is_a_mirror && FD->is_in_mirror_space);
		if (isFrMIRROR)
		{
			UD->l *= -1;
			UD->m *= -1;
			UD->n *= -1;
		}

		/* ZEMAX wants a real ray trace to this surface */
		// This is a plane.
		UD->ln = 0;
		UD->mn = 0;
		UD->nn = -1;

		double M, L;
		M = FD->param[0];
		L = FD->wavelength * 1e-3;
		bool bend = FD->param[1] != 0;

		double phase, dpdx, dpdy, wavnum;
		wavnum = 2 * PI / L;
		if (UD->x == 0 && UD->y == 0)
		{
			phase = 0;
			UD->path = 0;

		}
		else
		{
			phase = atan2(UD->y, UD->x) * M;

			UD->path = phase / wavnum / FD->n1;

			//if (bend)
			//{
				double r2 = UD->x * UD->x + UD->y * UD->y;
				dpdx = -UD->y / r2 * M; // this is (d/dx)atan2(y,x)
				dpdy = UD->x / r2 * M;  // this is (d/dy)atan2(y,x)

				UD->l = (UD->l * fabs(FD->n1) + dpdx / wavnum) / fabs(FD->n2);
				UD->m = (UD->m * fabs(FD->n1) + dpdy / wavnum) / fabs(FD->n2);
				double tmp = 1 - UD->l * UD->l - UD->m * UD->m;
				if (tmp <= 0) return -1;
				if (FD->is_a_mirror)
					UD->n = sqrt(tmp) * sgn(UD->n) * -1;
				else
					UD->n = sqrt(tmp) * sgn(UD->n);
			//}
		}
	
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
		for (i = 1; i <= 8; i++) FD->param[i] = 0.0;
		break;
	}
	return 0;
}
