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
import os

import pytest

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_09_NSC_CAD as ex9


@pytest.fixture(scope="module")
def CASE09_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase09_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx09Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case09_setup(CASE09_LOGGER, pytestconfig):
    CASE09_LOGGER.info(f"Test Date: {TODAY}")
    CASE09_LOGGER.info("Start to run the example 09")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex9.main(True, ZOS_PATH)
    CASE09_LOGGER.info("Finish example 09!")

    CASE09_LOGGER.info("Start to check the value in the sample file.")
    zos = ex9.PythonStandaloneApplication(ZOS_PATH)
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e09_NSC_CAD.zmx"
    )

    CASE09_LOGGER.info(f"testFile: {testFile}")
    CASE09_LOGGER.info(f"Load test file: {testFile}")

    TheSystem.LoadFile(testFile, False)

    yield TheSystem, ZOSAPI

    del zos

@pytest.mark.api_case00
class TestCADObjects:
    def test_object01(self, case09_setup, CASE09_LOGGER):
        system, ZOSAPI, *_ = case09_setup
        obj = system.NCE.GetObjectAt(1)
        cad_file = obj.CurrentTypeSettings.FileName1

        CASE09_LOGGER.info(f'cad_file: {cad_file}')
        assert obj.Type == ZOSAPI.Editors.NCE.ObjectType.CADPartSTEPIGESSAT
        assert obj.ZPosition == -5
        assert cad_file == 'ExtPoly.stp'
        
    def test_object02(self, case09_setup, CASE09_LOGGER):
        system, ZOSAPI, *_ = case09_setup
        obj = system.NCE.GetObjectAt(2)
        cad_file = obj.CurrentTypeSettings.FileName1

        CASE09_LOGGER.info(f'cad_file: {cad_file}')
        assert obj.Type == ZOSAPI.Editors.NCE.ObjectType.PolygonObject
        assert cad_file == 'API_cube_demo.POB'


if __name__ == "__main__":
    pass
