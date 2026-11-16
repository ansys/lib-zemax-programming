# ZPL Macro: Apply Make Thermal tool to Monte Carlo files

## Overview

This macro allows users to apply the "Make Thermal" tool to already-generated Monte Carlo files. The amount of MC files is hard coded into the code. This will apply five Multi-Configuration operands per surface: CRVT, THIC, SDIA, CHZN, MCSD. MC operands for extra data parameters are not included for all surface types.

## Author

Alexandra Culler

## Language
ZPL

## Procedure
Apply Make Thermal: Procedure
1. Enter number of configs, min, and max temperature.
2. Open an MC file for editing.
3. Clear the Multi-Configuration Editor.
4. Insert new configurations based on the input configNUM
5. Apply each standard operand (Radius, Thickness, Clear Semi-Diameter, Chip 
Zone, Mechanical Semi-Diameter).
6. Apply the Thermal Pickup solves.
7. Update lens, and save output

## Can we expand the functionality?
1. The coefficients for Even Aspheres will have additional Multi-Configuration 
operands than the standard ones already added. We can check for the surface 
type with the BUFFER command. 
2. $BUFFER():
    a. Numeric Functions will return numeric values (marked as black in the ZPL)
    b.  Occasionally, certain settings for some Numeric Functions will return a string value. In that case, the string is placed in the "buffer". To extract it, use the String Function $BUFFER()

![Alt text](image1.png)

## Update the macro
1. Add a Numeric Function which checks on surface properties. Use this Numeric Function to 
pull the Surface Type. Use $BUFFER() to return the string. 
2. Add an IF statement to check for an Even Asphere. If one exists, add and edit more Multi
Configuration operands

![Alt text](image2.png)

## Download
<table>

<tr>

<th>Date</th>

<th>Version</th>

<th>OpticStudio Version</th>

<th>Comment</th>

<tr>

<tr>
<td>2019/10/15</td>

<td>1.0</td>

<td>19.4SP2</td>

<td>Creation<td>
<tr>
<td>2020/08/18</td>

<td>2.0</td>

<td>20.2</td>

<td>Updates for OpticsTalk+Envision<br>

- Updates to formatting

- Addition of option to choose not to clear the MCE before applying the Make Thermal tool

- Addition of a loop which will check for the Even Asphere type. This will add parameters to the MCE which correspond to the asphere's extra data parameters

<tr>

