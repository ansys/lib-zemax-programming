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


#define _USE_MATH_DEFINES
#include <windows.h>
#include <math.h>
#include <string.h>
#include "usersurf.h"

/*
Written by Kenneth E. Moore
Oct 11, 1996

This DLL models an arbitrary number of lens elements in a lens array.
The individual lenses are generally conic aspheres.

The user provides the number of elements in x and y, the size in x and y of
each element, and the radius, conic, and glass.

This surface breaks up the beam into numerous separate
beams, and so most ZEMAX features will fail to work with this surface.

However, the spot diagrams, image analysis, etc, all work okay.

Modified GetCellCenter 9-25-01 KEM to accept rays at edge of lenses
Modified GetCellCenter 2-07-06 KEM to bound cell values to valid range, useful for very fast lenslets
Modified GetCellCenter 6-01-18 MC to make array hexagonal

*/

extern "C" {
	int __declspec(dllexport) APIENTRY UserDefinedSurface(USER_DATA *UD, FIXED_DATA *FD);
}
int GetCellCenter(int col, int row, double wid, double x, double y, double *cx, double *cy);

/* a generic Snells law refraction routine */
int Refract(double thisn, double nextn, double *l, double *m, double *n, double ln, double mn, double nn);

//BOOL WINAPI DllMain(HANDLE hInst, ULONG ul_reason_for_call, LPVOID lpReserved)
//{
//	return TRUE;
//}

/* this DLL models a lens array surface type */

int  __declspec(dllexport) APIENTRY UserDefinedSurface(USER_DATA *UD, FIXED_DATA *FD)
{
	int i, col, row, error, miss_flag;
	double p2, alpha, power, a, b, c, rad, casp, t, zc;
	double wid, cx, cy, x, y, z;
	switch (FD->type)
	{
	case 0:
		/* ZEMAX is requesting general information about the surface */
		switch (FD->numb)
		{
		case 0:
			/* ZEMAX wants to know the name of the surface */
				/* do not exceed 12 characters */
			strcpy(UD->string, "Lens Array (Hexagonal)");
			break;
		case 1:
			/* ZEMAX wants to know if this surface is rotationally symmetric */
			/* it is not, so return a null string */
			UD->string[0] = '\0';
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
			/* they are all "Unused" for this surface type */
			/* returning a null string indicates that the parameter is unused. */
		switch (FD->numb)
		{
		case 1:
			strcpy(UD->string, "Column #");
			break;
		case 2:
			strcpy(UD->string, "Row #");
			break;
		case 3:
			strcpy(UD->string, "Width");
			break;
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
		switch (FD->numb)
		{
		default:
			UD->string[0] = '\0';
			break;
		}
		break;
	case 3:
		/* ZEMAX wants to know the sag of the surface */
			/* if there is an alternate sag, return it as well */
			/* otherwise, set the alternate sag identical to the sag */
			/* The sag is sag1, alternate is sag2. */

		UD->sag1 = 0.0;
		UD->sag2 = 0.0;

		/* if a plane, just return */
		if (FD->cv == 0) return(0);

		/* figure out the center coordinates of which "cell" we are in */
		col = (int)FD->param[1];
		row = (int)FD->param[2];
		wid = FD->param[3];
		x = UD->x;
		y = UD->y;

		/* make sure col and row are both odd, otherwise the chief ray is a problem... */
		if (!col & 1)col++;
		if (!row & 1)row++;
		if (wid <= 0.0) return(-1);
		error = GetCellCenter(col, row, wid, UD->x, UD->y, &cx, &cy);

		if (error) return(0);

		/* offset the coordinates */
		x -= cx;
		y -= cy;

		p2 = x*x + y*y;
		alpha = 1 - (1 + FD->k)*FD->cv*FD->cv*p2;
		if (alpha < 0)
		{
			/* lens is not big enough to fill the cell, radius is too short */
			/* assume it is plane between lenses */
			alpha = 0.0;
		}
		UD->sag1 = (FD->cv*p2) / (1 + sqrt(alpha));
		/* forget supporting a hyper hemisphere! */
		UD->sag2 = UD->sag1;
		break;
	case 4:
		/* ZEMAX wants a paraxial ray trace to this surface */
			/* x, y, z, and the optical path are unaffected, at least for this surface type */
			/* for paraxial ray tracing, the return z coordinate should always be zero. */
			/* paraxial surfaces are always planes with the following normals */

			/* for a lens array, only consider the single lens on axis */
		UD->ln = 0.0;
		UD->mn = 0.0;
		UD->nn = -1.0;
		power = (FD->n2 - FD->n1)*FD->cv;
		if ((UD->n) != 0.0)
		{
			(UD->l) = (UD->l) / (UD->n);
			(UD->m) = (UD->m) / (UD->n);

			(UD->l) = (FD->n1*(UD->l) - (UD->x)*power) / (FD->n2);
			(UD->m) = (FD->n1*(UD->m) - (UD->y)*power) / (FD->n2);

			/* normalize */
			(UD->n) = sqrt(1 / (1 + (UD->l)*(UD->l) + (UD->m)*(UD->m)));
			/* de-paraxialize */
			(UD->l) = (UD->l)*(UD->n);
			(UD->m) = (UD->m)*(UD->n);
		}
		break;
	case 5:
		/* ZEMAX wants a real ray trace to this surface */

			/* clear the multiple intercept test flag */
		miss_flag = 0;

		if (FD->cv == 0.0)
		{
		outofbounds:;
			UD->ln = 0.0;
			UD->mn = 0.0;
			UD->nn = -1.0;
			if (Refract(FD->n1, FD->n2, &UD->l, &UD->m, &UD->n, UD->ln, UD->mn, UD->nn)) return(-FD->surf);
			return(0);
		}
		/* okay, not a plane. */
		col = (int)FD->param[1];
		row = (int)FD->param[2];
		wid = FD->param[3];
		x = UD->x;
		y = UD->y;

		/* make sure nx and ny are both odd, otherwise the chief ray is a problem... */
		if (!col & 1)col++;
		if (!row & 1)row++;
		if (wid <= 0.0) return(-1);
		error = GetCellCenter(col, row, wid, UD->x, UD->y, &cx, &cy);
		if (error) goto outofbounds;

	try_again:;

		/* offset the coordinates */
		x -= cx;
		y -= cy;
		z = 0.0;

		a = (UD->n) * (UD->n) * FD->k + 1;
		b = ((UD->n) / FD->cv) - (x) * (UD->l) - (y) * (UD->m);
		c = (x) * (x)+(y) * (y);
		rad = b * b - a * c;
		if (rad < 0) return(FD->surf);  /* ray missed this surface */
		if (FD->cv > 0) t = c / (b + sqrt(rad));
		else           t = c / (b - sqrt(rad));
		(x) = (UD->l) * t + (x);
		(y) = (UD->m) * t + (y);
		(z) = (UD->n) * t + (z);
		UD->path = t;

		/* okay, if the ray makes a steep angle of intercept,
		we may actually have hit the wrong element. Check it again! */
		if (miss_flag == 0)
		{
			double new_cx, new_cy;

			/* avoid infinite loop */
			miss_flag = 1;

			/* restore global coordinates prior to test */
			UD->x = x + cx;
			UD->y = y + cy;
			error = GetCellCenter(col, row, wid, UD->x, UD->y, &new_cx, &new_cy);
			if (error) goto outofbounds;
			if (new_cx != cx || new_cy != cy)
			{
				/* we hit the wrong one! */
				/* go back to the tangent plane */
				t = -t;
				(x) = (UD->l) * t + (x);
				(y) = (UD->m) * t + (y);

				x = x + cx;
				y = y + cy;

				cx = new_cx;
				cy = new_cy;

				goto try_again;
			}
		}

		zc = (z)* FD->cv;
		rad = zc * FD->k * (zc * (FD->k + 1) - 2) + 1;
		casp = FD->cv / sqrt(rad);
		UD->ln = (x)* casp;
		UD->mn = (y)* casp;
		UD->nn = ((z)-((1 / FD->cv) - (z)* FD->k)) * casp;

		/* restore coordinates */
		UD->x = x + cx;
		UD->y = y + cy;
		UD->z = z;

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
		FD->param[1] = 5;
		FD->param[2] = 5;
		if (FD->cv == 0.0) FD->param[3] = 100.0;
		else FD->param[3] = 0.5 / FD->cv;
		FD->param[4] = FD->param[3];
		for (i = 5; i <= 8; i++) FD->param[i] = 0.0;
		for (i = 1; i <= 200; i++) FD->xdata[i] = 0.0;
		break;
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

int GetCellCenter(int col, int row, double width, double x, double y, double *cx, double *cy)
{
	double width1, width2, width3, ty, tx;
	int tny, tnx;

	*cx = 0.0;
	*cy = 0.0;

	tny = 0;
	tnx = 0;

	width1 = width * 0.5;
	width2 = width * 1 / sqrt(3);
	width3 = width * sqrt(3) / 2;

	tx = x;
	ty = y;

	/* do for y*/
	if (fabs(ty) > width2)
	{
		if (ty > 0)
		{
			while (ty > width2)
			{
				tny++;
				ty -= width3;
			}
		}
		else
		{
			while (ty < -width2)
			{
				tny--;
				ty += width3;
			}
		}

		*cy += tny * width3;
		if (tny & 1)
		{
			tx += width1;
			*cx -= width1;
		}
	}

	/* do for x */
	if (fabs(tx) > width1)
	{
		if (tx > 0)
		{
			while (tx > width1)
			{
				tnx++;
				tx -= width;
			}
		}
		else
		{
			while (tx < -width1)
			{
				tnx--;
				tx += width;
			}
		}
		*cx += tnx * width;
	}

	/* now the ray is at central rect box of (width1*2) x (width2*2),
	but the ray can still be outside of the central hexagonal, check it! */
	if (fabs(tx)*0.5 + fabs(ty)*sqrt(3)/2 > width1)
	{
		if (tx > 0) *cx += width1;
		else *cx -= width1;
		if (ty > 0) *cy += width3;
		else *cy -= width3;
	}

	/* outside of boundary? */
	if (fabs(x) > (width * (col - 1) / 2) || fabs(y) > 
		(width * sqrt(3) / 2 * (row - 1) / 2)) return -1;
	else return 0;
}

