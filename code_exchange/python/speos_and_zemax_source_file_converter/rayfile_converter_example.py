# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import tkinter as tk
from tkinter import filedialog

from ansys_optical_automation.interop_process.rayfile_converter import RayfileConverter


def getfilename(extension, save=False):
    """
    Parameters
    ----------
    extension : str
        containing the which file extension in *.ending format
    save : Bool
        option to define to open(default) or save. The default is False.

    Returns
    -------
    str
        string containing the selected file path
    """
    root = tk.Tk()
    root.withdraw()
    if not save:
        file_path = filedialog.askopenfilename(filetypes=[("Rayfile", extension)])
    else:
        file_path = filedialog.asksaveasfilename(filetypes=[("Rayfile", extension)])
        if not file_path.endswith(extension.strip("*")):
            file_path += extension.strip("*")
    return file_path


def main():
    """Main script to convert a rayfile from speos to Zemax or from zemax to speos"""
    path_to_rayfile = getfilename("*.ray *.sdf *.dat")
    input_file_extension = os.path.splitext(path_to_rayfile)[1].lower()[0:]
    if not (("ray" in input_file_extension) or ("dat" in input_file_extension) or ("sdf" in input_file_extension)):
        msg = "Nonsupported file selected"
        raise TypeError(msg)
    convert = RayfileConverter(path_to_rayfile)
    if "ray" in input_file_extension:
        convert.speos_to_zemax()
    elif ("dat" in input_file_extension) or ("sdf" in input_file_extension):
        convert.zemax_to_speos()


main()
