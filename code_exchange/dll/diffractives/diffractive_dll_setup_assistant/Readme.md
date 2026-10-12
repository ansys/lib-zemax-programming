# Diffractive DLL Setup Assistant 

## Overview

This diffractive DLL models a non-paraxial idealized polarizer that produces a linear polarized transverse electric field. It is an alternative to the Jones matrix, that model polarizers for paraxial fields under normal incidence. This non-paraxial idealized polarizer model supports reflection as well as transmission, material changes (i.e. refraction is considered), and support curved surfaces too.

The diffractive DLL is only a tool used here to compute the electric field. 

## Source Language
C++

## Author
Michael Cheng

## Instructions

Here is a quick user guide about the tool.

1. The cell "From Obj" should be a single integer for object number we want to load DLL parameter settings.

2. The par# is a string only including integer, comma, dash, and spaces. Integers are separated by comma. Dash is used to represent a range of integers.

3. By cliking the button Load Par#, all the parameter numbers from the object defined by "From Obj" will be written in Par# cell.

4. Par Val is a string only including numbers, comma, and spaces. Numbers don't need to be integer and are separaterd by comma.

5. By clicking the button Load Values, the value of parameter number defined by cell Par# in object defined by cell "From Obj" will be collected and written in cell Par Val.

6. The To Objs is a string works similar to Par#. We can define one or multiple objects that the 3 buttons "Set MCE", "Set paraemters", and "Copy paraemters" will use for target.

7. By clicking the button Auto Detect, the tool will automatically collect all objects that uses same DLL as the object defined by cell "From Obj" and write them in the cell To Objs.

8. By clicking the button Set MCE, we can create a series of multi-config operands that load the diffraction DLL parameters for objects defined by "To Objs" and its parameters defined by "Par#".

9. By clicking the button "Set paraemters", the tool will use the settings in "Par#" and the corresonding "Par Val" to set up the DLL parameters for the objects defined by "To Objs".

10. By clicking the button "Copy parameters", the tool will copy the DLL parameter defined by "Par#" from the object "From Obj" to the objects "To Objs".

11. By default all above operation will only consider refelct DLL parameters. When "Also Set Transmission" is checked, the transmission parameters will also be set up.

12. There are 3 shortcuts at the right side of the step 1 block. All 3 will set Par# to 5. Link Lum On (1) will set Par Val to 1. Link Lum On (99) will set it to 99. Link Lum Off will set it to 0.
