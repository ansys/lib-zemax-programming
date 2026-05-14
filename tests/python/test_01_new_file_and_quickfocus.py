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

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_01_new_file_and_quickfocus as ex1

@pytest.fixture(scope="module")
def CASE01_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase01_pytest")
    LOGGER.setLevel(logging.INFO)

    test01_log = log_folder.joinpath(f"ZOSPythonEx01Pytest_{TODAY}.log")
    case01_fh = logging.FileHandler(test01_log, mode="w")
    LOGGER.addHandler(case01_fh)
    return LOGGER


@pytest.fixture(scope="class")
def case1_setup(CASE01_LOGGER, pytestconfig):
    CASE01_LOGGER.info(f"Test Date: {TODAY}")
    CASE01_LOGGER.info("Start to run the example 01")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex1.main(True, zos_path = ZOS_PATH)
    CASE01_LOGGER.info("Finish example 01!")

    CASE01_LOGGER.info("Start to check the value in the sample file.")
    zos = ex1.PythonStandaloneApplication()
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e01_new_file_and_quickfocus.zmx"
    )

    CASE01_LOGGER.info(f"testFile: {testFile}")
    CASE01_LOGGER.info(f"Load test file: {testFile}")

    TheSystem.LoadFile(testFile, False)

    yield TheSystem, ZOSAPI

    del zos


@pytest.mark.api_case01
@pytest.mark.xdist_group(name="pyapi_01")
class TestPythonStandalone01NewFileAndQuickFocus:
    @pytest.mark.SystemData
    @pytest.mark.MaterialCatalogs
    def test_SystemData_MaterialCatalogs(self, case1_setup, CASE01_LOGGER):
        TheSystem, *_ = case1_setup
        CASE01_LOGGER.info("\nTest Catalog")

        is_catalog_in_use = TheSystem.SystemData.MaterialCatalogs.IsCatalogInUse(
            "SCHOTT"
        )
        CASE01_LOGGER.info(
            f"Is SCHOTT catalog in use?: {is_catalog_in_use}, expected = True"
        )
        assert is_catalog_in_use == True

    @pytest.mark.SystemData
    @pytest.mark.Aperture
    def test_SystemData_Aperture(self, case1_setup, CASE01_LOGGER):
        TheSystem, *_ = case1_setup
        CASE01_LOGGER.info("\nTest Aperture")

        aperture_val = TheSystem.SystemData.Aperture.ApertureValue
        CASE01_LOGGER.info(f"Aperture Value: {aperture_val}, expected = 40")
        assert aperture_val == 40

    @pytest.mark.SystemData
    @pytest.mark.Fields
    def test_SystemData_Fields(self, case1_setup, CASE01_LOGGER):
        TheSystem, *_ = case1_setup
        CASE01_LOGGER.info("\nTest Field")

        num_of_fields = TheSystem.SystemData.Fields.NumberOfFields
        field2_x = TheSystem.SystemData.Fields.GetField(2).X
        field2_y = TheSystem.SystemData.Fields.GetField(2).Y
        field2_weight = TheSystem.SystemData.Fields.GetField(2).Weight

        CASE01_LOGGER.info(f"Number of fields: {num_of_fields}, expected = 2")
        CASE01_LOGGER.info(f"Field 2 X: {field2_x}, expected = 0.0")
        CASE01_LOGGER.info(f"Field 2 Y: {field2_y}, expected = 5.0")
        CASE01_LOGGER.info(f"Field 2 Weight: {field2_weight}, expected = 1.0")

        assert num_of_fields == 2
        assert field2_x == 0.0
        assert field2_y == 5.0
        assert field2_weight == 1.0

    @pytest.mark.SystemData
    @pytest.mark.Wavelengths
    def test_SystemData_Wavelengths(self, case1_setup, CASE01_LOGGER):
        TheSystem, *_ = case1_setup
        CASE01_LOGGER.info("\nTest Wavelength")

        num_of_wavelengths = TheSystem.SystemData.Wavelengths.NumberOfWavelengths
        wavelength1 = TheSystem.SystemData.Wavelengths.GetWavelength(1).Wavelength

        CASE01_LOGGER.info(f"Number of Wavelengths: {num_of_wavelengths}, expected = 1")
        CASE01_LOGGER.info(f"Wavelength 1: {wavelength1}, expected = 0.58756")

        assert num_of_wavelengths == 1
        assert abs(wavelength1 - 0.58756) < 0.0001

    @pytest.mark.LDE
    def test_LDE(self, case1_setup, CASE01_LOGGER):
        TheSystem, ZOSAPI = case1_setup
        CASE01_LOGGER.info("\nTest LDE")

        num_of_surfaces = TheSystem.LDE.NumberOfSurfaces
        surface1_thickness = TheSystem.LDE.GetSurfaceAt(1).Thickness
        surface1_comment = TheSystem.LDE.GetSurfaceAt(1).Comment
        surface2_radius = TheSystem.LDE.GetSurfaceAt(2).Radius
        surface2_thickness = TheSystem.LDE.GetSurfaceAt(2).Thickness
        surface2_comment = "front of lens"
        surface2_material = "N-BK7"
        surface3_comment = "rear of lens"

        solve = TheSystem.LDE.GetSurfaceAt(3).RadiusCell.GetSolveData()
        solve_type = solve.Type
        solve_fnum = solve._S_FNumber.FNumber

        CASE01_LOGGER.info(f"Number of Surfaces: {num_of_surfaces}, expected = 5")
        CASE01_LOGGER.info(
            f"Surface 1 Thickness: {surface1_thickness}, expected = 50.0"
        )
        CASE01_LOGGER.info(
            f"Surface 1 Comment: '{surface1_comment}', expected = 'Stop is free to move'"
        )
        CASE01_LOGGER.info(f"Surface 2 Radius: {surface2_radius}, expected = 100.0")
        CASE01_LOGGER.info(f"Surface 2 Thickness: {surface2_radius}, expected = 10.0")
        CASE01_LOGGER.info(
            f"Surface 2 Comment: '{surface2_comment}', expected = 'front of lens'"
        )
        CASE01_LOGGER.info(
            f"Surface 2 Material: '{surface2_material}', expected = 'N-BK7'"
        )
        CASE01_LOGGER.info(
            f"Surface 3 Comment: '{surface3_comment}', expected = 'rear of lens'"
        )
        CASE01_LOGGER.info(
            f"Surface 3 Radius Solver Type: {solve_type}, expected = {ZOSAPI.Editors.SolveType.FNumber}"
        )
        CASE01_LOGGER.info(
            f"Surface 3 Radius Solver FNUM: {solve_fnum}, expected = 10.0"
        )

        assert num_of_surfaces == 5
        assert surface1_thickness == 50.0
        assert surface1_comment == "Stop is free to move"
        assert surface2_radius == 100.0
        assert surface2_thickness == 10.0
        assert surface2_comment == "front of lens"
        assert surface2_material == "N-BK7"
        assert surface3_comment == "rear of lens"

        solve = TheSystem.LDE.GetSurfaceAt(3).RadiusCell.GetSolveData()
        assert solve_type == ZOSAPI.Editors.SolveType.FNumber
        assert solve_fnum == 10

    @pytest.mark.SystemPerformance
    @pytest.mark.MFE
    def test_system_performance_with_MFE(self, case1_setup, CASE01_LOGGER):
        CASE01_LOGGER.info("\nTest Performance With MFE")
        TheSystem, ZOSAPI = case1_setup

        center_rsce = TheSystem.MFE.GetOperandValue(
            ZOSAPI.Editors.MFE.MeritOperandType.RSCE, 5, 1, 0, 0, 0, 0, 0, 0
        )
        margin_rsce = TheSystem.MFE.GetOperandValue(
            ZOSAPI.Editors.MFE.MeritOperandType.RSCE, 5, 1, 0, 1, 0, 0, 0, 0
        )

        CASE01_LOGGER.info(f"RSCE (Center): {center_rsce}, expected = 0.153487")
        CASE01_LOGGER.info(f"RSCE (Margin): {margin_rsce}, expected = 0.279069")

        assert abs(center_rsce - 0.153487) < 0.000001
        assert abs(margin_rsce - 0.279069) < 0.000001


if __name__ == "__main__":
    pytest.main(
        args=[
            "-p",
            "no:allure_pytest_bdd",
            "--html",
            os.path.abspath(os.path.join(os.path.dirname( __file__ ), "report_pytest.html")),
            "--self-contained-html",
            os.path.abspath(os.path.join(os.path.dirname( __file__ ), "test_01_new_file_and_quickfocus.py")),
        ],
    )
