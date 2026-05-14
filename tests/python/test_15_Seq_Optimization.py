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
import glob

import pytest

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_15_Seq_Optimization as ex15


@pytest.fixture(scope="module")
def CASE15_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase15_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx15Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="class")
def case15_setup(CASE15_LOGGER, pytestconfig):
    CASE15_LOGGER.info(f"Test Date: {TODAY}")
    CASE15_LOGGER.info("Start to run the example 15")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex15.main(True, ZOS_PATH)
    CASE15_LOGGER.info("Finish example 15!")

    CASE15_LOGGER.info("Start to check the value in the sample file.")
    zos = ex15.PythonStandaloneApplication(ZOS_PATH)
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e15_Seq_Optimization\OptimizedFile4.zmx"
    )

    CASE15_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    yield TheSystem, zos, ZOSAPI

    del zos


class TestPythonStandalone15SeqOptimization:
    @pytest.mark.LDE
    def test_f_number_solve(self, case15_setup, CASE15_LOGGER):
        TheSystem, _, ZOSAPI = case15_setup
        surf = TheSystem.LDE.GetSurfaceAt(11)
        solver = surf.RadiusCell.GetSolveData()

        f_num = solver._S_FNumber.FNumber
        CASE15_LOGGER.info(f"F# in solver: {f_num}")

        assert solver.Type == ZOSAPI.Editors.SolveType.FNumber 
        assert f_num == 3.1415

    @pytest.mark.LDE
    def test_pick_up_solve(self, case15_setup, CASE15_LOGGER):
        TheSystem, _, ZOSAPI = case15_setup
        surf = TheSystem.LDE.GetSurfaceAt(10)
        solver = surf.ThicknessCell.GetSolveData()

        surface_pickup = solver._S_SurfacePickup.Surface
        scale_factor = solver._S_SurfacePickup.ScaleFactor
        column = solver._S_SurfacePickup.Column

        CASE15_LOGGER.info(f"Pick up (surface): {surface_pickup}")
        CASE15_LOGGER.info(f"Pick up (scale factor): {scale_factor}")

        assert solver.Type == ZOSAPI.Editors.SolveType.SurfacePickup 
        assert surface_pickup == 1
        assert scale_factor == 1
        assert column == ZOSAPI.Editors.LDE.SurfaceColumn.Thickness

    @pytest.mark.LDE
    def test_variable_solve(self, case15_setup):
        TheSystem, _, ZOSAPI = case15_setup

        TheLDE = TheSystem.LDE
        Surface2 = TheLDE.GetSurfaceAt(2)
        Surface5 = TheLDE.GetSurfaceAt(5)
        Surface6 = TheLDE.GetSurfaceAt(6)
        Surface9 = TheLDE.GetSurfaceAt(9)
        Surface11 = TheLDE.GetSurfaceAt(11)

        assert Surface2.ThicknessCell.GetSolveData().Type == ZOSAPI.Editors.SolveType.Variable
        assert Surface5.ThicknessCell.GetSolveData().Type == ZOSAPI.Editors.SolveType.Variable
        assert Surface6.ThicknessCell.GetSolveData().Type == ZOSAPI.Editors.SolveType.Variable
        assert Surface9.ThicknessCell.GetSolveData().Type == ZOSAPI.Editors.SolveType.Variable
        assert Surface11.ThicknessCell.GetSolveData().Type == ZOSAPI.Editors.SolveType.Variable

    @pytest.mark.MFE
    def test_merit_func_MNCA(self, case15_setup):
        TheSystem, _, ZOSAPI = case15_setup
        TheMFE = TheSystem.MFE
        operand = TheMFE.GetOperandAt(4)
        
        assert operand.Type == ZOSAPI.Editors.MFE.MeritOperandType.MNCA
        assert operand.Target == 0.5
        assert operand.Weight == 1

    @pytest.mark.MFE
    def test_merit_func_MXCA(self, case15_setup):
        TheSystem, _, ZOSAPI = case15_setup
        TheMFE = TheSystem.MFE
        operand = TheMFE.GetOperandAt(5)
        
        assert operand.Type == ZOSAPI.Editors.MFE.MeritOperandType.MXCA
        assert operand.Target == 1000
        assert operand.Weight == 1

    @pytest.mark.MFE
    def test_merit_func_MNEA(self, case15_setup):
        TheSystem, _, ZOSAPI = case15_setup
        TheMFE = TheSystem.MFE
        operand = TheMFE.GetOperandAt(6)
        
        assert operand.Type == ZOSAPI.Editors.MFE.MeritOperandType.MNEA
        assert operand.Target == 0.5
        assert operand.Weight == 1

    @pytest.mark.MFE
    def test_merit_func_MNCG(self, case15_setup):
        TheSystem, _, ZOSAPI = case15_setup
        TheMFE = TheSystem.MFE
        operand = TheMFE.GetOperandAt(7)
        
        assert operand.Type == ZOSAPI.Editors.MFE.MeritOperandType.MNCG
        assert operand.Target == 3
        assert operand.Weight == 1

    @pytest.mark.MFE
    def test_merit_func_MXCG(self, case15_setup):
        TheSystem, _, ZOSAPI = case15_setup
        TheMFE = TheSystem.MFE
        operand = TheMFE.GetOperandAt(8)
        
        assert operand.Type == ZOSAPI.Editors.MFE.MeritOperandType.MXCG
        assert operand.Target == 15
        assert operand.Weight == 1

    @pytest.mark.MFE
    def test_merit_func_MNEG(self, case15_setup):
        TheSystem, _, ZOSAPI = case15_setup
        TheMFE = TheSystem.MFE
        operand = TheMFE.GetOperandAt(9)
        
        assert operand.Type == ZOSAPI.Editors.MFE.MeritOperandType.MNEG
        assert operand.Target == 3
        assert operand.Weight == 1

    @pytest.mark.global_opt
    def test_global_opt(self, case15_setup, CASE15_LOGGER):
        _, zos, *_ = case15_setup
        dir_path = Path(zos.TheApplication.SamplesDir).resolve().joinpath("API/Python/e15_Seq_Optimization")

        global_files = glob.glob(str(dir_path) + "/GLOPT_[0-9]*_[0-9]*.zmx")
        CASE15_LOGGER.info(global_files)
        assert len(global_files) == 10



if __name__ == '__main__':
    pass
