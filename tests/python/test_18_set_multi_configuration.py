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
import PythonStandalone_18_SetMultiConfiguration as ex18


@pytest.fixture(scope="module")
def CASE18_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase18_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx18Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case18_setup(CASE18_LOGGER, pytestconfig):
    CASE18_LOGGER.info(f"Test Date: {TODAY}")
    CASE18_LOGGER.info("Start to run the example 18")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex18.main(True, ZOS_PATH)
    CASE18_LOGGER.info("Finish example 18!")
    zos = ex18.PythonStandaloneApplication(ZOS_PATH)
    yield zos
    del zos

@pytest.fixture(scope="class")
def case18_double_gauss(case18_setup, CASE18_LOGGER):
    CASE18_LOGGER.info("Start to check the value in the sample file.")
    zos = case18_setup
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = TheApplication.CreateNewSystem(ZOSAPI.SystemType.Sequential)

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e18_Double_Gauss_28_degree_field_MultiConfig.zmx"
    )

    CASE18_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    return TheSystem, zos, ZOSAPI


@pytest.fixture(scope="class")
def case18_thermal(case18_setup, CASE18_LOGGER):
    CASE18_LOGGER.info("Start to check the value in the sample file.")
    zos = case18_setup
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = TheApplication.CreateNewSystem(ZOSAPI.SystemType.Sequential)

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e18_Doublet_MakeTermal.zmx"
    )

    CASE18_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    yield TheSystem, zos, ZOSAPI

class TestPythonStandalone17SetMultiConfig:
    def test_mce_status(self, case18_double_gauss, CASE18_LOGGER):
        TheSystem, zos, ZOSAPI = case18_double_gauss
        TheMCE = TheSystem.MCE
        current_config = TheMCE.CurrentConfiguration
        number_of_configs = TheMCE.NumberOfConfigurations
        number_of_rows = TheMCE.NumberOfRows

        CASE18_LOGGER.info(f"Current Config: {current_config}")
        CASE18_LOGGER.info(f"Number of Configs: {number_of_configs}")
        CASE18_LOGGER.info(f"Number of Rows {number_of_rows}")

        assert current_config == 3
        assert number_of_configs == 3
        assert number_of_rows == 2


    def test_mce_operand1(self, case18_double_gauss, CASE18_LOGGER):
        TheSystem, _, ZOSAPI = case18_double_gauss
        TheMCE = TheSystem.MCE
        op = TheMCE.GetOperandAt(1)
        
        op_type = op.Type
        type_name = op.TypeName
        op_param = op.Param1

        op_value1 = op.GetOperandCell(1).DoubleValue
        op_value2 = op.GetOperandCell(2).DoubleValue
        op_value3 = op.GetOperandCell(3).DoubleValue

        CASE18_LOGGER.info(f"Operand Type: {type_name}")
        CASE18_LOGGER.info(f"Operand Param1: {op_param}")
        CASE18_LOGGER.info(f"Operand Value (Config 1): {op_value1}")
        CASE18_LOGGER.info(f"Operand Value (Config 2): {op_value2}")
        CASE18_LOGGER.info(f"Operand Value (Config 3): {op_value3}")

        assert op_type == ZOSAPI.Editors.MCE.MultiConfigOperandType.THIC
        assert op_param == 0
        assert op_value1 == 10000.0
        assert op_value2 == 5000.0
        assert op_value3 == 1000.0

    def test_mce_operand2(self, case18_double_gauss, CASE18_LOGGER):
        TheSystem, _, ZOSAPI = case18_double_gauss
        TheMCE = TheSystem.MCE
        op = TheMCE.GetOperandAt(2)
        
        op_type = op.Type
        type_name = op.TypeName
        op_param = op.Param1
        
        CASE18_LOGGER.info(f"Operand Type: {type_name}")
        CASE18_LOGGER.info(f"Operand Param1: {op_param}")
        
        assert op_type == ZOSAPI.Editors.MCE.MultiConfigOperandType.THIC
        assert op_param == 11
        

class TestThermal:
    def test_operand_types(self, case18_thermal, CASE18_LOGGER):
        TheSystem, _, ZOSAPI = case18_thermal
        TheMCE = TheSystem.MCE
        op_types = [TheMCE.GetOperandAt(i).Type for i in range(1, 14)]
        
        operandTypes = [ZOSAPI.Editors.MCE.MultiConfigOperandType.TEMP, ZOSAPI.Editors.MCE.MultiConfigOperandType.PRES,
                   ZOSAPI.Editors.MCE.MultiConfigOperandType.CRVT, ZOSAPI.Editors.MCE.MultiConfigOperandType.THIC,
                   ZOSAPI.Editors.MCE.MultiConfigOperandType.GLSS, ZOSAPI.Editors.MCE.MultiConfigOperandType.SDIA,
                   ZOSAPI.Editors.MCE.MultiConfigOperandType.CRVT, ZOSAPI.Editors.MCE.MultiConfigOperandType.THIC,
                   ZOSAPI.Editors.MCE.MultiConfigOperandType.GLSS, ZOSAPI.Editors.MCE.MultiConfigOperandType.SDIA,
                   ZOSAPI.Editors.MCE.MultiConfigOperandType.CRVT, ZOSAPI.Editors.MCE.MultiConfigOperandType.THIC,
                   ZOSAPI.Editors.MCE.MultiConfigOperandType.SDIA]
        
        check = [op_type == operandType for op_type, operandType in zip(op_types, operandTypes)]

        CASE18_LOGGER.info(f"ZOS: {op_types}")
        CASE18_LOGGER.info(f"Expected: {operandTypes}")

        assert all(check)

    def test_operand_solves(self, case18_thermal, CASE18_LOGGER):
        TheSystem, _, ZOSAPI = case18_thermal
        TheMCE = TheSystem.MCE
        ThermalPickup_num = [3, 4, 6, 7, 8, 10, 11, 12, 13]
        thermal_solves = [TheMCE.GetOperandAt(i).GetOperandCell(2).GetSolveData() for i in ThermalPickup_num]
        thermal_types = [solve.Type for solve in thermal_solves]
        thermal_cmp = [data == ZOSAPI.Editors.SolveType.ThermalPickup for data in thermal_types]

        ConfigPickup_num = [5, 9]
        config_solves = [TheMCE.GetOperandAt(i).GetOperandCell(2).GetSolveData() for i in ConfigPickup_num]
        config_types = [solve.Type for solve in config_solves]
        config_cmp = [data == ZOSAPI.Editors.SolveType.ConfigPickup for data in config_types]
        
        assert all(thermal_cmp), f"Thermal Types: {thermal_types}"
        assert all(config_cmp), f"Config Types: {thermal_types}"



if __name__ == '__main__':
    pass
