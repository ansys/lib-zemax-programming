# Python YZ View for POP Simulation

## Overview

OpticStudio Physical Optics Propagation (POP) does not directly provide a YZ view. This standalone Python example loads a Zemax Beam File (ZBF), propagates it over a configurable distance range, and plots the YZ cross-section at the center of the X dimension.

The output includes linear and logarithmic intensity views.

## Prerequisites

- Ansys Zemax OpticStudio with a valid ZOS-API license.
- Python compatible with Python.NET.
- `pythonnet`, `numpy`, and `matplotlib`.
- A ZBF file whose wavelength matches the `wave` setting in the script.

## Settings

Edit the settings at the start of the `if __name__ == '__main__':` block.

| Setting | Unit | Description |
| --- | --- | --- |
| `d1` | mm | Start of the propagation range. |
| `d2` | mm | End of the propagation range. |
| `samp` | - | Number of propagation samples between `d1` and `d2`. |
| `wave` | um | Wavelength used by POP. It must match the selected ZBF file. |
| `UseAngularSpectrumPropagator` | - | Must remain `True` for this example. Supporting `False` requires a more complex stitching method. |

## How to Use

1. Set `d1`, `d2`, `samp`, and `wave` for the desired propagation range.
2. Run `YZ view for ZBF.py`.
3. Select a `.zbf` file when prompted. The script copies it into the OpticStudio POP directory when needed.
4. Review the generated Matplotlib figure for the YZ cross-section in linear and logarithmic scales.

The script creates `Test System.zos` next to the Python file while it runs POP repeatedly.

## Contents

- `YZ view for ZBF.py`: standalone ZOS-API and POP post-processing script.
- `image.png`: configurable propagation settings.
- `image-1.png`: example YZ plots.
- `archive/`: original downloaded ZIP package.
