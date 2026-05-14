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

import pytest
import numpy as np

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_21_White_LED_Phosphor as ex21

def rms(dataset):
    dataset = np.array(dataset)
    return np.nanmean(dataset ** 2) ** 0.5


@pytest.fixture(scope="module")
def CASE21_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase21_pytest")
    LOGGER.setLevel(logging.INFO)

    test21_log = log_folder.joinpath(f"ZOSPythonEx21Pytest_{TODAY}.log")
    case21_fh = logging.FileHandler(test21_log, mode="w")
    LOGGER.addHandler(case21_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case21_setup(CASE21_LOGGER, pytestconfig):
    image_folder = Path(pytestconfig.getoption("img_folder"))
    image_folder.mkdir(parents=True, exist_ok=True)
    CASE21_LOGGER.info(f"Test Date: {TODAY}")
    CASE21_LOGGER.info("Start to run the example 21")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    res = ex21.main(True, ZOS_PATH)
    CASE21_LOGGER.info("Finish example 21!")
    
    zos = ex21.PythonStandaloneApplication(ZOS_PATH)
    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem
    ZOSAPI = zos.ZOSAPI

    TheSystem.LoadFile(TheApplication.SamplesDir + '\\API\\Python\\e21_White_LED_Phosphor.zmx', False)

    return zos, TheSystem, ZOSAPI, res

@pytest.fixture(scope="module")
def case21_expected(case21_setup):
    zos, TheSystem, ZOSAPI, res = case21_setup
    
    with open(CMP_DATA_FOLDER.joinpath('ex21/ex21.json'), 'r') as f:
        expected = json.load(f)

    return res, expected


class TestWhiteLEDPhosphorNCE:
    def test_obj1(self, case21_setup, CASE21_LOGGER):
        _, TheSystem, ZOSAPI, *_ = case21_setup
        TheNCE = TheSystem.NCE
        Object_1 = TheNCE.GetObjectAt(1)
        
        assert Object_1.Type == ZOSAPI.Editors.NCE.ObjectType.SourceFile
        assert Object_1.CurrentTypeSettings.FileName1 == 'RAYFILE_LB_T67C_100K_190608_ZEMAX.DAT'
        assert Object_1.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par1).IntegerValue == 5
        assert Object_1.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par2).IntegerValue == 1000
        assert Object_1.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par3).DoubleValue == 2.485572
        assert Object_1.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par8).DoubleValue == pytest.approx(0.47, abs=1e-8)
        assert Object_1.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par9).DoubleValue == pytest.approx(0.47, abs=1e-8)
        assert Object_1.SourcesData.PrePropagation == -0.2
        assert Object_1.SourcesData.ArrayType == ZOSAPI.Editors.NCE.ArrayMode.Rectangular
        assert Object_1.SourcesData.ArrayNumberX == 5
        assert Object_1.SourcesData.ArrayNumberY == 5

    def test_obj2(self, case21_setup, CASE21_LOGGER):
        _, TheSystem, ZOSAPI, *_ = case21_setup
        TheNCE = TheSystem.NCE
        Object_2 = TheNCE.GetObjectAt(2)
        assert Object_2.Type == ZOSAPI.Editors.NCE.ObjectType.CADPartSTEPIGESSAT
        assert Object_2.TypeData.RaysIgnoreObject == ZOSAPI.Editors.NCE.RaysIgnoreObjectType.Always

    def test_obj3(self, case21_setup, CASE21_LOGGER):
        _, TheSystem, ZOSAPI, *_ = case21_setup
        TheNCE = TheSystem.NCE
        Object_3 = TheNCE.GetObjectAt(3)

        assert Object_3.Type == ZOSAPI.Editors.NCE.ObjectType.CylinderVolume
        assert Object_3.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.ZPosition).DoubleValue == 0.8
        assert Object_3.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Material).Value == 'PMMA'
        assert Object_3.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par1).DoubleValue == 1.2
        assert Object_3.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par2).DoubleValue == 0.1
        assert Object_3.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par3).DoubleValue == 1.2

        assert Object_3.CoatScatterData.GetFaceData(1).CurrentScatterModel == ZOSAPI.Editors.NCE.ObjectScatteringTypes.Lambertian
        assert Object_3.CoatScatterData.GetFaceData(1).CurrentScatterModelSettings._S_Lambertian.ScatterFraction == 1
        assert Object_3.CoatScatterData.GetFaceData(1).NumberOfRays == 1

        assert Object_3.VolumePhysicsData.Model == ZOSAPI.Editors.NCE.VolumePhysicsModelType.PhotoluminescenceModel
        
        Photo_setting = Object_3.VolumePhysicsData.ModelSettings._S_PhotoluminescenceModel
        assert Photo_setting.BasicAlgorithm == False
        assert Photo_setting.AbsorptionFile == '_sample_3.ZAS'
        assert Photo_setting.EmissionFile == '_sample_3.ZES'
        assert Photo_setting.QuantumYield == '_sample_3.ZQE'
        assert Photo_setting.EfficiencySpectrum == ZOSAPI.Editors.NCE.EfficiencySpectrumType.QuantumYield
        assert Photo_setting.ExtinctionCoefficient == 1E+05
        assert Photo_setting.ExtinctionWavelength == 0.47
        assert Photo_setting.PLDensity == 3.1E+017
        assert Photo_setting.ConsiderMieScattering == False

    def test_obj4(self, case21_setup, CASE21_LOGGER):
        _, TheSystem, ZOSAPI, *_ = case21_setup
        TheNCE = TheSystem.NCE
        Object_4 = TheNCE.GetObjectAt(4)

        assert Object_4.Type == ZOSAPI.Editors.NCE.ObjectType.StandardLens
        assert Object_4.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.ZPosition).DoubleValue == 0.9
        assert Object_4.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Material).Solve == ZOSAPI.Editors.SolveType.ObjectPickup
        
        assert Object_4.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par3).DoubleValue == 1.2
        assert Object_4.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par4).DoubleValue == 1.2
        assert Object_4.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par5).DoubleValue == 1.2
        assert Object_4.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par6).DoubleValue == -1.2
        assert Object_4.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par8).DoubleValue == 1.2
        assert Object_4.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par9).DoubleValue == 1.2

    def test_obj5(self, case21_setup, CASE21_LOGGER):
        _, TheSystem, ZOSAPI, *_ = case21_setup
        TheNCE = TheSystem.NCE
        Object_5 = TheNCE.GetObjectAt(5)

        assert Object_5.Type == ZOSAPI.Editors.NCE.ObjectType.DetectorColor
        assert Object_5.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.ZPosition).DoubleValue == 7
        assert Object_5.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Material).Value == 'ABSORB'
        assert Object_5.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par1).DoubleValue == 5
        assert Object_5.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par2).DoubleValue == 5
        assert Object_5.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par3).IntegerValue == 150
        assert Object_5.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par4).IntegerValue == 150
        assert Object_5.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par6).IntegerValue == 4
        assert Object_5.GetObjectCell(ZOSAPI.Editors.NCE.ObjectColumn.Par7).IntegerValue == 3


class TestWhiteLEDPhosphorDetector:
    def test_detector1(self, case21_expected):
        res, expected = case21_expected

        np.testing.assert_allclose(rms(res.get('det1')), rms(expected.get('det1')), rtol=10**-0.5)

    def test_detector2(self, case21_expected):
        res, expected = case21_expected

        np.testing.assert_allclose(rms(res.get('det2')), rms(expected.get('det2')), rtol=10**-0.5)



if __name__ == "__main__":
    pass
