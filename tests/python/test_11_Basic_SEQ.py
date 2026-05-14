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
import PythonStandalone_11_BASIC_SEQ as ex11


@pytest.fixture(scope="module")
def CASE11_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase11_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx11Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case11_setup(CASE11_LOGGER, pytestconfig):
    CASE11_LOGGER.info(f"Test Date: {TODAY}")
    CASE11_LOGGER.info("Start to run the example 11")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    data = ex11.main(True, ZOS_PATH)
    CASE11_LOGGER.info("Finish example 11!")

    CASE11_LOGGER.info("Start to check the value in the sample file.")
    
    zos = ex11.PythonStandaloneApplication(ZOS_PATH)
    TheSystem = zos.TheSystem
    ZOSAPI = zos.ZOSAPI

    yield zos, TheSystem, ZOSAPI

    del zos

@pytest.fixture(scope="module")
def case_11(case11_setup):
    zos, TheSystem, ZOSAPI = case11_setup
    TheApplication = zos.TheApplication
    TheSystem.LoadFile(TheApplication.SamplesDir + "/API/Python/e11_basic_seq.zmx", False)
    return zos, TheSystem, ZOSAPI


@pytest.mark.api_case11
@pytest.mark.SystemData
class TestSystemData:
    @pytest.mark.Aperture
    @pytest.mark.ScaleTool
    def test_aperture(self, case_11):
        _, TheSystem, ZOSAPI = case_11

        TheSystemData = TheSystem.SystemData
        
        assert TheSystemData.Aperture.ApertureValue == pytest.approx(0.7874015748031495, abs=1e-8)
        assert TheSystemData.Aperture.ApodizationType == ZOSAPI.SystemData.ZemaxApodizationType.Gaussian
        assert TheSystemData.Aperture.ApodizationFactor == 1

    @pytest.mark.MaterialCatalogs
    def test_material_catalog(self, case_11):
        _, TheSystem, ZOSAPI = case_11
        TheSystemData = TheSystem.SystemData
        assert TheSystemData.MaterialCatalogs.IsCatalogInUse('SCHOTT')

    @pytest.mark.Units
    @pytest.mark.Tools
    @pytest.mark.ScaleTool
    def test_units(self, case_11):
        _, TheSystem, ZOSAPI = case_11
        TheSystemData = TheSystem.SystemData
        unit = TheSystemData.Units.LensUnits

        assert unit == ZOSAPI.SystemData.ZemaxSystemUnits.Inches

@pytest.mark.LDE
@pytest.mark.ScaleTool
class TestLDE:
    def test_surf_1(self, case_11):
        _, TheSystem, ZOSAPI = case_11
        surf = TheSystem.LDE.GetSurfaceAt(1)

        assert surf.IsStop
        assert surf.Thickness == pytest.approx(1.968503937007874E-001, abs=1e-8)
        assert surf.ApertureData.CurrentType == ZOSAPI.Editors.LDE.SurfaceApertureTypes.RectangularAperture
        assert surf.ApertureData.CurrentTypeSettings._S_RectangularAperture.XHalfWidth == .1
        assert surf.ApertureData.CurrentTypeSettings._S_RectangularAperture.YHalfWidth == .1

    def test_surf_2(self, case_11):
        _, TheSystem, ZOSAPI = case_11
        surf = TheSystem.LDE.GetSurfaceAt(2)

        assert surf.Thickness == pytest.approx(1.968503937007874E-001, abs=1e-8)
        assert surf.Radius == pytest.approx(3.937007874015748E+000, abs=1e-8)
        assert surf.Material == "N-BK7"

    def test_surf_3(self, case_11):
        _, TheSystem, ZOSAPI = case_11
        surf = TheSystem.LDE.GetSurfaceAt(3)

        assert surf.Thickness == pytest.approx(1.181102362204724E-001, abs=1e-8)
        assert surf.Radius == pytest.approx(-1.181102362204725E+000, abs=1e-8)
        assert surf.Material == "F2"

    def test_surf_4(self, case_11):
        _, TheSystem, ZOSAPI = case_11
        surf = TheSystem.LDE.GetSurfaceAt(4)
        assert surf.Radius == pytest.approx(-3.149606299212598E+000, abs=1e-8)

    @pytest.mark.Tools
    @pytest.mark.QuickFocusTool
    def test_quick_focus(self, case_11):
        _, TheSystem, ZOSAPI = case_11
        surf = TheSystem.LDE.GetSurfaceAt(4)
        assert surf.Thickness == pytest.approx(4.123743306210278E+000, abs=1e-8)


@pytest.mark.Analyses
class TestOpenedAnalyses:
    def test_analyses(self, case_11):
        _, TheSystem, ZOSAPI = case_11
        
        assert TheSystem.Analyses.NumberOfAnalyses == 2

        analysis = TheSystem.Analyses.Get_AnalysisAtIndex(1)
        assert analysis.AnalysisType == ZOSAPI.Analysis.AnalysisIDM.UniversalPlot1D

        analysis = TheSystem.Analyses.Get_AnalysisAtIndex(2)
        assert analysis.AnalysisType == ZOSAPI.Analysis.AnalysisIDM.StandardSpot
        assert ZOSAPI.Analysis.Settings.Spot.IAS_Spot(analysis.GetSettings()).RayDensity == 15



if __name__ == "__main__":
    pass
