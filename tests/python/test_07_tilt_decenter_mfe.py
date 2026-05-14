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

import logging
import json
import os

import numpy as np
import pytest

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_07_TiltDecenterAndMFOperand as ex7


@pytest.fixture(scope="module")
def CASE07_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase07_pytest")
    LOGGER.setLevel(logging.INFO)

    test07_log = log_folder.joinpath(f"ZOSPythonEx07Pytest_{TODAY}.log")
    case07_fh = logging.FileHandler(test07_log, mode="w")
    LOGGER.addHandler(case07_fh)
    return LOGGER

@pytest.fixture(scope='module')
def case7_setup(CASE07_LOGGER, pytestconfig):
    image_folder = Path(pytestconfig.getoption("img_folder"))
    image_folder.mkdir(parents=True, exist_ok=True)
    CASE07_LOGGER.info(f"Test Date: {TODAY}")
    CASE07_LOGGER.info("Start to run the example 07")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")

    mfeVal = ex7.main(True, ZOS_PATH)
    CASE07_LOGGER.info("Finish example 07!")
    CASE07_LOGGER.info("Start to check the value in the sample file.")

    zos = ex7.PythonStandaloneApplication(ZOS_PATH)
    ZOSAPI = zos.ZOSAPI
    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem

    inFile = TheApplication.ZemaxDataDir + r"\Samples\API\Python\Python_07_TiltDecenterAndMFOperand.zmx"
    TheSystem.LoadFile(inFile, False)
    yield TheSystem, ZOSAPI, mfeVal

    del zos


@pytest.mark.api_case07
@pytest.mark.xdist_group(name="pyapi_07")
class TestPythonStandalone07TiltDecenterMFE:
    def test_surface_type(self, case7_setup):
        TheSystem, ZOSAPI, *_ = case7_setup
        surface3 = TheSystem.LDE.GetSurfaceAt(3)
        surface6 = TheSystem.LDE.GetSurfaceAt(6)

        surf3_type = surface3.CurrentTypeSettings.Type
        surf6_type = surface6.CurrentTypeSettings.Type

        assert surf3_type == ZOSAPI.Editors.LDE.SurfaceType.CoordinateBreak
        assert surf6_type == ZOSAPI.Editors.LDE.SurfaceType.CoordinateBreak

    def test_surf5_solve(self, case7_setup):
        TheSystem, ZOSAPI, *_ = case7_setup
        surface5_solve = TheSystem.LDE.GetSurfaceAt(5).ThicknessCell.GetSolveData()

        assert surface5_solve.Type == ZOSAPI.Editors.SolveType.Position
        assert surface5_solve._S_Position.FromSurface == 3
        assert surface5_solve._S_Position.Length == 0

    def test_surf6_solve(self, case7_setup):
        TheSystem, ZOSAPI, *_ = case7_setup
        surface5_solve = TheSystem.LDE.GetSurfaceAt(6).ThicknessCell.GetSolveData()

        assert surface5_solve.Type == ZOSAPI.Editors.SolveType.SurfacePickup
        assert surface5_solve._S_SurfacePickup.Surface == 5
        assert surface5_solve._S_SurfacePickup.ScaleFactor == -1
        assert surface5_solve._S_SurfacePickup.Offset == 0
        assert surface5_solve._S_SurfacePickup.Column == ZOSAPI.Editors.LDE.SurfaceColumn.Thickness

    def test_mfe_val(self, case7_setup):
        _, _, mfeVal = case7_setup
        file = CMP_DATA_FOLDER.joinpath("ex07/ex07.json")
        with open(file, 'r') as f:
            expected = json.load(f)

        np.testing.assert_allclose(mfeVal, expected, rtol=1e-8)



if __name__ == "__main__":
    pass
