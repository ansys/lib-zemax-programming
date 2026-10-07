# Monte Carlo Step-Wise Compensator Analysis ZPL Macro
## Overview

This macro applies incremental changes to a compensator in Monte Carlo files, then reports the updated criterion. It will cycle through Monte Carlo files and apply a discretely-valued compensator to a particular surface. Then, the criterion will be analyzed and reported. (Note, the report could use some formatting updates). This code may be used to represent step-wise compensation tools. For example, a mirror's tilt may be applied as a compensator to a change in the system. However, it may be the case that the mirror's housing makes it so that the mirror is only allowed to tilt in increments of 2 degrees. This macro will cycle through the MC files, apply the incremented compensation up to a particular boundary, and will report the result. The changes to each file are NOT saved.

## Author

Alexandra Culler

## Instructions

#### 1. Installation
Copy the macros to the \Documents\Zemax\Macros folder.

#### 2. How to use
In OpticStudio, navigate to Programming…Edit/Run and open the macro for editing. Change the "path$", "prefix$", and "number_of_files" variables to match with the location and number of the Monte Carlo files you want to apply the change to. (Note: this portion of the macro is discussed in the Knowledgebase article "How to open consecutively-named lens files using a ZPL macro").
Then, report the nominal criterion. Currently, this is hard-coded into the macro, but could be updated to be automatic. This value will be given at the top of the Tolerance Report:

![Alt text](code.png)

Next, specify the type of compensation you want to apply, and the allowed increments. In this file, the X tilt of surface 3 is being updated to 0, 2, 4, 6, 8, 10 degree values. The update is applied with SETSURFACEPROPERTY. See the Help System file "The Programming Tab > About the ZPL > KEYWORDS (about the zpl) > SETSURFACEPROPERTY, SURP" for more information on this keyword. 