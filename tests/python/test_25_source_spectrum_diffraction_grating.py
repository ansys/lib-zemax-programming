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
from pathlib import Path
import json
import os

import pytest
import numpy as np

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_25_source_spectrum_diffraction_grating as ex25

def rms(dataset):
    dataset = np.array(dataset)
    return np.nanmean(dataset ** 2) ** 0.5


@pytest.fixture(scope="module")
def CASE25_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase25_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx25Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case25_setup(CASE25_LOGGER, pytestconfig):
    CASE25_LOGGER.info(f"Test Date: {TODAY}")
    CASE25_LOGGER.info("Start to run the example 25")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    res = ex25.main(True, ZOS_PATH)
    CASE25_LOGGER.info("Finish example 25!")
    with open(CMP_DATA_FOLDER.joinpath('ex25/ex25.json'), 'r') as f:
        expected = json.load(f)
    return res, expected


@pytest.fixture(scope="module")
def case25_file_setup(case25_setup, CASE25_LOGGER,pytestconfig):
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    zos = ex25.PythonStandaloneApplication(ZOS_PATH)
    TheApplication = zos.TheApplication
    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(os.sep, sampleDir, r"API\Python\e25_source_spectrum_diffraction_grating.zmx")
    zos.TheSystem.LoadFile(testFile, False)
    yield zos
    del zos

@pytest.mark.NCE
class TestNCE:
    def test_source_1(self, case25_file_setup):
        zos = case25_file_setup
        ZOSAPI = zos.ZOSAPI
        TheNCE = zos.TheSystem.NCE
        source = TheNCE.GetObjectAt(1)
        source_type = source.Type
        source_color = source.SourcesData.SourceColor

        source_temperature = source.SourcesData.SourceColorSettings._S_BlackBodySpectrum.TemperatureK
        source_wavelength_from = source.SourcesData.SourceColorSettings._S_BlackBodySpectrum.WavelengthFrom
        source_wavelength_to = source.SourcesData.SourceColorSettings._S_BlackBodySpectrum.WavelengthTo

        assert source_type == ZOSAPI.Editors.NCE.ObjectType.SourceDiode
        assert ZOSAPI.Editors.NCE.IObjectSourceDiode(source.ObjectData).XMinusDivergence == 5
        assert source_color == ZOSAPI.Editors.NCE.SourceColorMode.BlackBodySpectrum

        assert source_temperature == 6000
        assert source_wavelength_from == 0.45
        assert source_wavelength_to == 0.65

    def test_source_2(self, case25_file_setup):
        zos = case25_file_setup
        ZOSAPI = zos.ZOSAPI
        TheNCE = zos.TheSystem.NCE
        source = TheNCE.GetObjectAt(2)
        source_type = source.Type
        source_color = source.SourcesData.SourceColor

        source_temperature = source.SourcesData.SourceColorSettings._S_BlackBodySpectrum.TemperatureK
        source_wavelength_from = source.SourcesData.SourceColorSettings._S_BlackBodySpectrum.WavelengthFrom
        source_wavelength_to = source.SourcesData.SourceColorSettings._S_BlackBodySpectrum.WavelengthTo
        source_spectrum_count = source.SourcesData.SourceColorSettings._S_BlackBodySpectrum.SpectrumCount

        assert source_type == ZOSAPI.Editors.NCE.ObjectType.SourceDiode
        assert ZOSAPI.Editors.NCE.IObjectSourceDiode(source.ObjectData).XMinusDivergence == 5
        assert source_color == ZOSAPI.Editors.NCE.SourceColorMode.BlackBodySpectrum

        assert source_temperature == 6000
        assert source_wavelength_from == 0.4
        assert source_wavelength_to == 0.7
        assert source_spectrum_count == 100

    def test_grating(self, case25_file_setup):
        zos = case25_file_setup
        ZOSAPI = zos.ZOSAPI
        TheNCE = zos.TheSystem.NCE
        obj = TheNCE.GetObjectAt(4)
        obj_type = obj.Type


        assert obj_type == ZOSAPI.Editors.NCE.ObjectType.DiffractionGrating
        assert obj.Material == "MIRROR"
        assert obj.RefObject == 3
        assert ZOSAPI.Editors.NCE.IObjectDiffractionGrating(obj.ObjectData).LinesPerMicron == 0.6
        assert ZOSAPI.Editors.NCE.IObjectDiffractionGrating(obj.ObjectData).DiffOrder == 1

    def test_detector(self, case25_file_setup):
        zos = case25_file_setup
        ZOSAPI = zos.ZOSAPI
        TheNCE = zos.TheSystem.NCE
        obj = TheNCE.GetObjectAt(5)
        obj_type = obj.Type
        obj_data = ZOSAPI.Editors.NCE.IObjectDetectorColor(obj.ObjectData)

        assert obj_type == ZOSAPI.Editors.NCE.ObjectType.DetectorColor
        assert obj.YPosition == 8.45
        assert obj.TiltAboutX == 40
        assert obj_data.XHalfWidth == 1.5
        assert obj_data.YHalfWidth == 1.5
        assert obj_data.NumberXPixels == 500
        assert obj_data.NumberYPixels == 500

@pytest.mark.MCE
class TestMCE:
    def test_op_1(self, case25_file_setup):
        zos = case25_file_setup
        ZOSAPI = zos.ZOSAPI
        TheMCE = zos.TheSystem.MCE
        op = TheMCE.GetOperandAt(1)
        op_type = op.Type

        assert op_type == ZOSAPI.Editors.MCE.MultiConfigOperandType.NPAR
        assert op.Param2 == 1
        assert op.Param3 == 1
        assert op.GetOperandCell(1).DoubleValue == 200
        assert op.GetOperandCell(2).DoubleValue == 0

    def test_op_2(self, case25_file_setup):
        zos = case25_file_setup
        ZOSAPI = zos.ZOSAPI
        TheMCE = zos.TheSystem.MCE
        op = TheMCE.GetOperandAt(2)
        op_type = op.Type

        assert op_type == ZOSAPI.Editors.MCE.MultiConfigOperandType.NPAR
        assert op.Param2 == 1
        assert op.Param3 == 2
        assert op.GetOperandCell(1).DoubleValue == 1000000
        assert op.GetOperandCell(2).DoubleValue == 0

    def test_op_3(self, case25_file_setup):
        zos = case25_file_setup
        ZOSAPI = zos.ZOSAPI
        TheMCE = zos.TheSystem.MCE
        op = TheMCE.GetOperandAt(3)
        op_type = op.Type

        assert op_type == ZOSAPI.Editors.MCE.MultiConfigOperandType.NPAR
        assert op.Param2 == 2
        assert op.Param3 == 1
        assert op.GetOperandCell(1).DoubleValue == 0
        assert op.GetOperandCell(2).DoubleValue == 200

    def test_op_4(self, case25_file_setup):
        zos = case25_file_setup
        ZOSAPI = zos.ZOSAPI
        TheMCE = zos.TheSystem.MCE
        op = TheMCE.GetOperandAt(4)
        op_type = op.Type

        assert op_type == ZOSAPI.Editors.MCE.MultiConfigOperandType.NPAR
        assert op.Param2 == 2
        assert op.Param3 == 2
        assert op.GetOperandCell(1).DoubleValue == 0
        assert op.GetOperandCell(2).DoubleValue == 1000000

@pytest.mark.Analyses
class TestNSCDetector:
    def test_true_colors(self, case25_setup):
        res, expected = case25_setup
        np.testing.assert_allclose(rms(res), rms(expected), rtol=10**-0.5)


if __name__ == '__main__':
    pass
