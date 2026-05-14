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
import PythonStandalone_12_SEQ_SystemExplorer as ex12


@pytest.fixture(scope="module")
def CASE12_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase12_pytest")
    LOGGER.setLevel(logging.INFO)

    test12_log = log_folder.joinpath(f"ZOSPythonEx12Pytest_{TODAY}.log")
    case12_fh = logging.FileHandler(test12_log, mode="w")
    LOGGER.addHandler(case12_fh)
    return LOGGER


@pytest.fixture(scope="class")
def case12_setup(CASE12_LOGGER, pytestconfig):
    CASE12_LOGGER.info(f"Test Date: {TODAY}")
    CASE12_LOGGER.info("Start to run the example 12")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex12.main(True, ZOS_PATH)
    CASE12_LOGGER.info("Finish example 12!")

    CASE12_LOGGER.info("Start to check the value in the sample file.")
    zos = ex12.PythonStandaloneApplication(ZOS_PATH)
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e12_seq_system_explorer.zmx"
    )

    CASE12_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    yield TheSystem, ZOSAPI

    del zos


@pytest.mark.api_case12
class TestPythonStandalone12SEQSystemExplorer:
    @pytest.mark.SystemData
    @pytest.mark.Wavelength
    def test_SystemData_Wavelength(self, case12_setup, CASE12_LOGGER):
        TheSystem, ZOSAPI, *_ = case12_setup
        CASE12_LOGGER.info("\nTest Wavelength")
        sys_wavelength = TheSystem.SystemData.Wavelengths
        assert sys_wavelength.NumberOfWavelengths == 6

    @pytest.mark.SystemData
    @pytest.mark.Field
    def test_SystemData_Field(self, case12_setup, CASE12_LOGGER):
        TheSystem, ZOSAPI, *_ = case12_setup
        CASE12_LOGGER.info("\nTest Field")
        sys_field = TheSystem.SystemData.Fields
        field1 = sys_field.GetField(1)

        assert field1.X == 1.0
        assert field1.Y == 2.0
        assert sys_field.GetFieldType() == ZOSAPI.SystemData.FieldType.ParaxialImageHeight

    @pytest.mark.SystemData
    @pytest.mark.MaterialCatalogs
    def test_SystemData_MaterialCatalogs(self, case12_setup, CASE12_LOGGER):
        TheSystem, *_ = case12_setup
        CASE12_LOGGER.info("\nTest Material Catalog")

        catalogs_in_use = list(TheSystem.SystemData.MaterialCatalogs.GetCatalogsInUse())
        CASE12_LOGGER.info(
            f"Catalogs in used: {catalogs_in_use}"
        )

        assert 'CORNING' in catalogs_in_use
        assert 'SCHOTT' not in catalogs_in_use

    @pytest.mark.SystemData
    @pytest.mark.TitleNotes
    def test_SystemData_TitleNotes(self, case12_setup, CASE12_LOGGER, ):
        TheSystem, *_ = case12_setup
        CASE12_LOGGER.info("\nTest System title")

        sysTitleNotes = TheSystem.SystemData.TitleNotes
        CASE12_LOGGER.info(
            f"Title: {sysTitleNotes.Title}"
        )
        CASE12_LOGGER.info(
            f"Notes: {sysTitleNotes.Notes}"
        )

        assert sysTitleNotes.Title == "Add Title Here"
        assert sysTitleNotes.Notes == "Add Notes Here"

    @pytest.mark.SystemData
    @pytest.mark.SystemFiles
    def test_SystemData_Files(self, case12_setup, CASE12_LOGGER):
        TheSystem, *_ = case12_setup
        CASE12_LOGGER.info("\nTest System files")

        sysFiles = TheSystem.SystemData.Files
        CASE12_LOGGER.info(f"Coating file: {sysFiles.CoatingFile}")
        CASE12_LOGGER.info(f"Scatter Profile: {sysFiles.ScatterProfile}")
        CASE12_LOGGER.info(f"ABg Data file: {sysFiles.ABgDataFile}")

        assert sysFiles.CoatingFile == "COATING.DAT"
        assert sysFiles.ScatterProfile == "SCATTER_PROFILE.DAT"
        assert sysFiles.ABgDataFile == "ABG_DATA.DAT"

    @pytest.mark.SystemData
    @pytest.mark.SystemUnits
    def test_system_units(self, case12_setup, CASE12_LOGGER):
        TheSystem, ZOSAPI, *_ = case12_setup
        CASE12_LOGGER.info("\nTest System Units")

        sys_units = TheSystem.SystemData.Units
        CASE12_LOGGER.info(f"Units: {sys_units.LensUnits}")

        assert sys_units.LensUnits == ZOSAPI.SystemData.ZemaxSystemUnits.Inches

    @pytest.mark.SystemData
    @pytest.mark.Polarization
    def test_system_polarization(self, case12_setup, CASE12_LOGGER):
        TheSystem, ZOSAPI, *_ = case12_setup
        CASE12_LOGGER.info("\nTest System Polarization")

        sysPol = TheSystem.SystemData.Polarization
        CASE12_LOGGER.info(f"Method: {sysPol.Method}")

        assert sysPol.Method == ZOSAPI.SystemData.PolarizationMethod.YAxisMethod


if __name__ == '__main__':
    pass
