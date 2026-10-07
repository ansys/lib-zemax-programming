# ZPL Macro: Plotting Real Entrance Pupil in 3D Layout

## Overview

This ZPL macro calculates the position, orientation, and semi-diameter of the real entrance pupil for each field in a wide-angle sequential system. It adds coordinate-break and dummy surfaces, then creates one configuration per field so the pupils can be displayed together in a 3D Layout.

## Limitations and Prerequisites

- The system must be axially symmetric.
- Use Y-field data only.
- Object-space field angles must be positive.
- Turn on Ray Aiming before running the macro.
- The macro is intended for the `Angle` and `Object Height` field types.

## Installation

Copy `zt_enp.zpl` into the OpticStudio macro directory, typically `{Zemax}\Macros`.

## How to Use

1. Open a suitable sequential system. The supplied documentation uses `{Zemax}\Samples\Sequential\Objectives\Wide angle lens 210 degree field.zos` as an example.
2. Enable Ray Aiming.
3. Run `zt_enp.zpl`.
4. Open a new 3D Layout and display the central field and all configurations.
5. Select surface 2 to view the real entrance pupil defined for each field.

The macro changes the current lens by adding three surfaces and creating configurations. Run it on a copy if the original system must remain unchanged.

## Contents

- `zt_enp.zpl`: entrance-pupil calculation and configuration-generation macro.
- `image.png`: example output.
- `archive/`: original ZIP package and its PDF/DOCX documentation.

## Author

Michael Cheng - Zemax
