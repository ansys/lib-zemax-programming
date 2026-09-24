# Create Ray File From Zemax SEQ v3.0
## Overview

This tool is intended to enable rayfile generation from sequential zemax mode,
formatted for both non-sequential (.sdf) and Speos (.ray). Because the ray data is
saved in image space, ray data transfer from black-boxed lens models is supported.

This tool has dependencies in ansys-optical-automation; that module must be installed prior to running this tool. Installation instructions can be found at the link below.

https://optics.ansys.com/hc/en-us/articles/24752772596371-Optical-Automation-library-introduction

---
## Author

**Zech Derocher** 

## Notes

Application can be run from 'main.py'; all relevant user settings are found in the
'User Settings' block within that script.

The application is prepared as an Interactive Extension; as such, a zemax model must be 
opened in the Zemax UI, and the Zemax application must be open to external API connection.

Rays are traced from a given field position in the sequential model, randomly filling
the pupil, and towards the sequential system image plane. Rays are unpolarized.
Effects of coatings, frensel losses, vignetting, etc. are considered in intensity transmission.
Ray positions, angles, wavelengths, and intensities are stored at a dummy surface in 
image space and saved to file. 

Wavelengths are chosen based on System Explorer settings.

Ray data is saved to ...\Documents\Zemax\Objects\Sources\Source Files\
