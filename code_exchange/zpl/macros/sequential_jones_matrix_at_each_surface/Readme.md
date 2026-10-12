# ZPL Macro: Sequential Jones Matrix at Each Surface

## Overview

This ZPL macro traces one ray through a sequential system and calculates a Jones matrix at every surface. It reports the matrix in a coordinate system normal to the traced ray and compares the result with Polarization Ray Trace (`POLTRACE`).

The electric field after each surface can be obtained by multiplying the electric field before the surface by the corresponding Jones matrix.

## Coordinate System

The macro initially assumes propagation along the Z axis. For rays travelling in another direction, it defines transverse Jones axes using the vectors `vecjx` and `vecjy`; the ray direction cosines form the propagation vector. These three vectors are perpendicular. The macro rotates the Jones basis after reflection or refraction and converts the calculated s/p coefficients into this Jones-axis basis.

## Installation

Copy `ZT_track_Jones_matrix.ZPL` into the OpticStudio macro directory, typically `{Zemax}\Macros`.

## How to Use

1. Open `ZT_track_Jones_matrix.ZPL` in OpticStudio.
2. Edit the ray coordinates `hx`, `hy`, `px`, and `py` as required.
3. Edit the input polarization values `pol_jx`, `pol_jy`, `pol_phax`, and `pol_phay` as required.
4. Run the macro.
5. Review the output in the OpticStudio Text Viewer, including the `POLTRACE` comparison.

The macro uses the primary wavelength by default because `PLEN` only returns data for the primary wavelength.

## Version

Version 1.0 was created for OpticStudio 19.4 SP2. The macro source also records later maintenance updates from January and September 2020.

## Contents

- `ZT_track_Jones_matrix.ZPL`: per-surface Jones-matrix calculation macro.
- `archive/`: original ZIP package and PDF documentation.

## Author

Michael Cheng - Zemax
