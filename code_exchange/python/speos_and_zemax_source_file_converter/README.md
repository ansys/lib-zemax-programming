# Python SPEOS and Zemax Source File Converter

## Overview

This example converts ray source files between Ansys Speos and Ansys Zemax OpticStudio. It uses `RayfileConverter` from Ansys optical automation and provides a file-selection dialog for the input ray file.

Supported input extensions are `.ray`, `.sdf`, and `.dat`.

- `.ray` files are converted from Speos to Zemax.
- `.sdf` and `.dat` files are converted from Zemax to Speos.

## Prerequisites

- Python with Tkinter support.
- Ansys optical automation, including `ansys_optical_automation.interop_process.rayfile_converter`.

For information about Ansys optical automation, see the associated Code Exchange article.

## How to Use

1. Run `rayfile_converter_example.py`.
2. Select a `.ray`, `.sdf`, or `.dat` source file in the file-selection dialog.
3. The script detects the extension and runs the corresponding conversion.

## File Format Notes

Zemax source files should preferably use the `.sdf` extension. The `.dat` extension is supported for backward compatibility. Zemax source files can be text or binary.

Speos ray files may be written in a non-binary representation, commonly using the `.ray` extension. Their content can be `.ray`, `.txt`, or `.tm25ray`.

## Troubleshooting

### `Non binary files not supported`

This error indicates that the selected file is not stored as a binary ray file.

- For a Zemax source file, place a detector close to the source, trace rays, and save the ray-tracing data as a new source file to create a binary file.
- For a Speos `.ray` file, open the file in the Speos Ray File Editor and save it again before conversion.

## Contents

- `rayfile_converter_example.py`: interactive Speos/Zemax ray-file conversion example.
