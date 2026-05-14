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
import PythonStandalone_14_Seq_Tolerance as ex14


@pytest.fixture(scope="module")
def CASE14_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase14_pytest")
    LOGGER.setLevel(logging.INFO)

    test14_log = log_folder.joinpath(f"ZOSPythonEx14Pytest_{TODAY}.log")
    case14_fh = logging.FileHandler(test14_log, mode="w")
    LOGGER.addHandler(case14_fh)
    return LOGGER


@pytest.fixture(scope="class")
def case14_setup(CASE14_LOGGER, pytestconfig):
    CASE14_LOGGER.info(f"Test Date: {TODAY}")
    CASE14_LOGGER.info("Start to run the example 14")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex14.main(True, ZOS_PATH)
    CASE14_LOGGER.info("Finish example 14!")

    CASE14_LOGGER.info("Start to check the value in the sample file.")
    zos = ex14.PythonStandaloneApplication(ZOS_PATH)
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e14_seq_tolerance\Double Gauss (seq).zmx"
    )

    CASE14_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    yield TheSystem, zos, ZOSAPI

    del zos


@pytest.mark.api_case14
class TestPythonStandalone14SEQTolearnce:
    @pytest.mark.tolerance
    def test_tolerance_radius(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(4)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "4: TRAD"
        assert operand_min == -0.1
        assert operand_max == 0.1

    @pytest.mark.tolerance
    def test_tolerance_surface_thickness(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(13)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "13: TTHI"
        assert operand_min == -0.1
        assert operand_max == 0.1

    @pytest.mark.tolerance
    def test_tolerance_surface_decx(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(39)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "39: TSDX"
        assert operand_min == -0.1
        assert operand_max == 0.1

    @pytest.mark.tolerance
    def test_tolerance_surface_decy(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(40)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "40: TSDY"
        assert operand_min == -0.1
        assert operand_max == 0.1


    @pytest.mark.tolerance
    def test_tolerance_surface_tiltx(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(41)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "41: TIRX"
        assert operand_min == -0.2
        assert operand_max == 0.2

    @pytest.mark.tolerance
    def test_tolerance_surface_tilty(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(42)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "42: TIRY"
        assert operand_min == -0.2
        assert operand_max == 0.2

    @pytest.mark.tolerance
    def test_tolerance_element_tiltx(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(25)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "25: TETX"
        assert operand_min == -0.2
        assert operand_max == 0.2

    @pytest.mark.tolerance
    def test_tolerance_element_tilty(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(26)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "26: TETY"
        assert operand_min == -0.2
        assert operand_max == 0.2

    @pytest.mark.tolerance
    def test_tolerance_element_decx(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(23)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "23: TEDX"
        assert operand_min == -0.1
        assert operand_max == 0.1

    @pytest.mark.tolerance
    def test_tolerance_element_decy(self, case14_setup, CASE14_LOGGER):
        TheSystem, *_ = case14_setup

        operand = TheSystem.TDE.GetOperandAt(24)
        operand_type = operand.TypeName
        operand_min = operand.Min
        operand_max = operand.Max

        assert operand_type == "24: TEDY"
        assert operand_min == -0.1
        assert operand_max == 0.1

    @pytest.mark.tolerance
    def test_tolerance_monte_carlo_files_exist(self, case14_setup, CASE14_LOGGER):
        _, zos, *_ = case14_setup
        dir_path = Path(zos.TheApplication.SamplesDir).resolve().joinpath("API/Python/e14_seq_tolerance")

        assert dir_path.joinpath("MC_T0020.zmx").exists()
        
    @pytest.mark.NSCConverter
    def test_convert_to_NSC_tool(self, case14_setup, CASE14_LOGGER):
        _, zos, *_ = case14_setup
        dir_path = Path(zos.TheApplication.SamplesDir).resolve().joinpath("API/Python/e14_seq_tolerance")

        assert dir_path.joinpath("Double Gauss (NS).zmx").exists()


if __name__ == '__main__':
    pass
