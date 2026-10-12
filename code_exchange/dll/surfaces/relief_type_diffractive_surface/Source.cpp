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
Written by Csilla Timar-Fulep
June, 2022
FIXED_DATA5 structure
*/

/*
* Copyright � 2022 <copyright holders>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the �Software�), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED �AS IS�, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/


extern "C"
{
    int __declspec(dllexport) APIENTRY UserDefinedSurface5(USER_DATA* UD, FIXED_DATA5* FD);
}

/* a generic Snells law refraction routine */
int Refract(double thisn, double nextn, double* l, double* m, double* n, double ln, double mn, double nn);

/*
BOOL WINAPI DllMain(HANDLE hInst, ULONG ul_reason_for_call, LPVOID lpReserved)
{
    return TRUE;
}
*/

/* this DLL models a standard ZEMAX surface type, either plane, sphere, or conic */

int __declspec(dllexport) APIENTRY UserDefinedSurface5(USER_DATA* UD, FIXED_DATA5* FD)
{
    int i, loop;
    double A[6], stepHeight, iter;
    double x, y, r, r2, alpha, power, zStand, zRelief, sag, z, dz, x0, y0, z0, t, tr, tp, l, m, n, mm, mx, my, z2, a, b, c, rad, zc, casp;
    

    switch (FD->type)
    {
    case 0:
        /* ZEMAX is requesting general information about the surface */
        switch (FD->numb)
        {
        case 0:
            /* ZEMAX wants to know the name of the surface */
             /* do not exceed 12 characters */
            strcpy(UD->string, "Relief Diffr");
            break;
        case 1:
            /* ZEMAX wants to know if this surface is rotationally symmetric */
           /* it is, so return any character in the string; otherwise, return a null string */
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
         /* they are all "Unused" for this surface type */
         /* returning a null string indicates that the parameter is unused. */
        switch (FD->numb)
        {
        case 1:
            strcpy(UD->string, "2nd Order Term");
            break;
        case 2:
            strcpy(UD->string, "4th Order Term");
            break;
        case 3:
            strcpy(UD->string, "6th Order Term");
            break;
        case 4:
            strcpy(UD->string, "8th Order Term");
            break;
        case 5:
            strcpy(UD->string, "10th Order Term");
            break;
        case 6:
            strcpy(UD->string, "Step height");
            break;
        case 7:
            strcpy(UD->string, "Iter");
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

        x = UD->x;
        y = UD->y;
        r2 = x * x + y * y;

        /* aspheric terms */
        for (i = 1; i <= 5; i++)
        {
            A[i] = FD->param[i];
        }

        /* Step height */
        stepHeight = FD->param[6];

        // standard sag
        alpha = 1 - (1 + FD->k) * FD->cv * FD->cv * r2;
        if (fabs(alpha) < 1e-13)
        {
            alpha = 0;
        }
        if (alpha < 0)
        {
            return -1;
        }
        zStand = (FD->cv * r2) / (1 + sqrt(alpha));

        // relief sag
        zRelief = 0.0;
        if (stepHeight != 0)
        {
            for (i = 1; i <= 5; i++)
            {
                zRelief += A[i] * pow(r2, i);
            }
            zRelief = fmod(zRelief, stepHeight);
        }
        
        UD->sag1 = zStand + zRelief;
        // no hyperhemispheric support
        UD->sag2 = UD->sag1;

        break;
    case 4:
        /* ZEMAX wants a paraxial ray trace to this surface */
         /* x, y, z, and the path are unaffected, at least for this surface type */
         /* for paraxial ray tracing, the return z coordinate should always be zero. */
         /* paraxial surfaces are always planes with the following normals */

        UD->ln = 0.0;
        UD->mn = 0.0;
        UD->nn = -1.0;
        power = (FD->n2 - FD->n1) * FD->cv;

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


        /* aspheric terms */
        for (i = 1; i <= 5; i++)
        {
            A[i] = FD->param[i];
        }

        /* Step height */
        stepHeight = FD->param[6];

        /* Iterative? */
        iter = FD->param[7];

        /* if stepHeight is 0, then this is a standard surface, so analytical solution can be used*/
        if (stepHeight == 0.0)
        {
            if (FD->cv == 0.0)
            {
                UD->ln = 0.0;
                UD->mn = 0.0;
                UD->nn = -1.0;
                if (Refract(FD->n1, FD->n2, &UD->l, &UD->m, &UD->n, UD->ln, UD->mn, UD->nn)) return(-FD->surf);
                return(0);
            }

            /* okay, not a plane. */
            a = (UD->n) * (UD->n) * FD->k + 1;
            b = ((UD->n) / FD->cv) - (UD->x) * (UD->l) - (UD->y) * (UD->m);
            c = (UD->x) * (UD->x) + (UD->y) * (UD->y);
            rad = b * b - a * c;
            if (rad < 0) return(FD->surf);  /* ray missed this surface */
            if (FD->cv > 0) t = c / (b + sqrt(rad));
            else          
                t = c / (b - sqrt(rad));
            (UD->x) = (UD->l) * t + (UD->x);
            (UD->y) = (UD->m) * t + (UD->y);
            (UD->z) = (UD->n) * t + (UD->z);
            UD->path = t;
            zc = (UD->z) * FD->cv;
            rad = zc * FD->k * (zc * (FD->k + 1) - 2) + 1;
            casp = FD->cv / sqrt(rad);
            UD->ln = (UD->x) * casp;
            UD->mn = (UD->y) * casp;
            UD->nn = ((UD->z) - ((1 / FD->cv) - (UD->z) * FD->k)) * casp;

        }
        
        /* otherwise, use the surface relief*/

        /* linear approximation method*/
        else if (iter == 0.0)
        {
            /*ray coordinates*/
            x = UD->x;
            y = UD->y;
            z = UD->z;
            r2 = x * x + y * y;
            r = sqrt(r2);

            /*ray direction cosines*/
            l = UD->l;
            m = UD->m;
            n = UD->n;

            /*calculate propagation to standard substrate analytically*/
            /*plane*/
            if (FD->cv == 0.0)
            {
                x0 = x;
                y0 = y;
                z0 = z;
                t = 0.0;
            }
            /* okay, not a plane. */
            else
            {
                a = n * n * FD->k + 1;
                b = (n / FD->cv) - x * l - y * m;
                c = x * x + y * y;
                rad = b * b - a * c;
                if (rad < 0) return(FD->surf);  /* ray missed this surface */
                if (FD->cv > 0) t = c / (b + sqrt(rad));
                else
                    t = c / (b - sqrt(rad));
                x0 = l * t + x;
                y0 = m * t + y;
                z0 = n * t + z;
            }
            
            /*we are at the substrate intersection now*/
            r2 = x0 * x0 + y0 * y0;
            r = sqrt(r2);

            /* now do the normals in the usual way */
            alpha = 1.0 - (1.0 + FD->k) * FD->cv * FD->cv * r2;
            if (alpha < 0) return(-1); /* ray misses */
            alpha = sqrt(alpha);

            /* dz/dr = mm * r */
            /*standard surface*/
            mm = (FD->cv / (1.0 + alpha)) * (2.0 + (FD->cv * FD->cv * r2 * (1.0 + FD->k)) / (alpha * (1.0 + alpha)));

            /*plus surface relief */
            z2 = 0;
            for (i = 1; i <= 5; i++)
            {
                z2 += A[i] * 2.0 * ((double)i) * pow(r2, i - 1);
            }
            mm += z2;

            // mm now holds (1/r)*(dz/dr)
            /* dz/dx = dz/dr * dr/dx = mm * r */
            mx = x0 * mm;
            my = y0 * mm;

            UD->nn = -sqrt(1 / (1 + (mx * mx) + (my * my)));
            UD->ln = -mx * UD->nn;
            UD->mn = -my * UD->nn;

            /*linear approxiamtion of propagation in relief*/
            // relief sag
            zRelief = 0.0;
            for (i = 1; i <= 5; i++)
            {
                zRelief += A[i] * pow(r2, i);
            }
            zRelief = fmod(zRelief, stepHeight);

            /*solving linear equations for approximation*/
            tr = (UD->nn * zRelief) / (UD->ln * l + UD->mn * m + UD->nn * n);

            /*propagation to approximate intersection*/
            (UD->x) = l * tr + x0;
            (UD->y) = m * tr + y0;
            (UD->z) = n * tr + z0;
            
            UD->path = t + tr;           
        }


        /*iterative algorithm*/
        /* make sure we do at least 1 loop */
        else
        {
            /*ray coordinates*/
            x = UD->x;
            y = UD->y;
            z = UD->z;
            r2 = x * x + y * y;
            r = sqrt(r2);


            tp = 0.0;
            t = 100.0;
            loop = 0;

            while (fabs(t) > 1e-10)
            {
                
                // standard sag
                alpha = 1 - (1 + FD->k) * FD->cv * FD->cv * r2;
                if (fabs(alpha) < 1e-13)
                {
                    alpha = 0;
                }
                if (alpha < 0)
                {
                    return -1;
                }
                zStand = (FD->cv * r2) / (1 + sqrt(alpha));

                // relief sag
                zRelief = 0.0;
                for (i = 1; i <= 5; i++)
                {
                    zRelief += A[i] * pow(r2, i);
                }
                zRelief = fmod(zRelief, stepHeight);
                

                sag = zStand + zRelief;

                /* okay, now with sag in hand, how far are we away in z? */
                dz = sag - z;

                /* now compute how far along the z axis this is */
                /* note this will crash if n == 0!! */
                t = dz / (UD->n);

                /* for some aspheres, it is safer to use dz directly, as it is a smaller number */
                /* the convergence will be slower if the ray angle is steep, fast if near parallel to the axis */


                /* propagate the additional "t" distance */
                x += UD->l * t;
                y += UD->m * t;
                z += UD->n * t;

                r2 = x * x + y * y;
                r = sqrt(r2);

                /* add in the optical path */
                tp += t;

                /* prevent infinte loop if no convergence */
                loop++;
                if (loop > 1000) return(-1);
            }

            /* okay, we should be at the intercept coordinates now */
            UD->x = x;
            UD->y = y;
            UD->z = z;
            
            r2 = x * x + y * y;
            r = sqrt(r2);
            
            /* don't forget the path! */
            UD->path = tp;

            /* now do the normals in the usual way */
            alpha = 1.0 - (1.0 + FD->k) * FD->cv * FD->cv * r2;
            if (alpha < 0) return(-1); /* ray misses */
            alpha = sqrt(alpha);

            /* dz/dr = mm * r */
            /*standard surface*/
            mm = (FD->cv / (1.0 + alpha)) * (2.0 + (FD->cv * FD->cv * r2 * (1.0 + FD->k)) / (alpha * (1.0 + alpha)));

            /*plus surface relief */
            z2 = 0;
            for (i = 1; i <= 5; i++)
            {
                z2 += A[i]* 2.0 * ((double) i) * pow(r2, i-1);
            }
            mm += z2;

            // mm now holds (1/r)*(dz/dr)
            /* dz/dx = dz/dr * dr/dx = mm * r */
            mx = x * mm;
            my = y * mm;

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
        for (i = 0; i <= FD->max_parameter; i++) FD->param[i] = 0.0;
        //for (i = 0; i <= FD->max_extradata; i++) FD->xdata[i] = 0.0;
        break;
    case 8:
        /* ZEMAX is calling the DLL for the first time, do any memory or data initialization here. */
        break;
    case 9:
        /* ZEMAX is calling the DLL for the last time, do any memory release here. */
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

