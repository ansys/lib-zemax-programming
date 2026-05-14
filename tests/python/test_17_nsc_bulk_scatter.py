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
import PythonStandalone_17_NSC_BulkScatter as ex17


@pytest.fixture(scope="module")
def CASE17_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase17_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx17Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="class")
def case17_setup(CASE17_LOGGER, pytestconfig):
    CASE17_LOGGER.info(f"Test Date: {TODAY}")
    CASE17_LOGGER.info("Start to run the example 17")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex17.main(True, ZOS_PATH)
    CASE17_LOGGER.info("Finish example 17!")

    CASE17_LOGGER.info("Start to check the value in the sample file.")
    zos = ex17.PythonStandaloneApplication(ZOS_PATH)
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = zos.TheSystem

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e17_NSC_BulkScatter.zmx"
    )

    CASE17_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    yield TheSystem, zos, ZOSAPI

    del zos


class TestPythonStandalone17NSCBulkScatter:
    def test_NSC_source(self, case17_setup, CASE17_LOGGER):
        TheSystem, _, ZOSAPI = case17_setup
        obj = TheSystem.NCE.GetObjectAt(1)
        data = ZOSAPI.Editors.NCE.IObjectSourcePoint(obj.ObjectData)

        num_of_layout_rays = data.NumberOfLayoutRays
        num_of_analysis_rays = data.NumberOfAnalysisRays
        obj_type = obj.Type

        CASE17_LOGGER.info("Object 1")
        CASE17_LOGGER.info(f"Number Of Layout Rays: {num_of_layout_rays}")
        CASE17_LOGGER.info(f"Number Of Analysis Rays: {num_of_analysis_rays}")

        assert num_of_layout_rays == 3
        assert num_of_analysis_rays == 1000000
        assert obj_type == ZOSAPI.Editors.NCE.ObjectType.SourcePoint

    def test_NSC_volume(self, case17_setup, CASE17_LOGGER):
        TheSystem, _, ZOSAPI = case17_setup
        obj = TheSystem.NCE.GetObjectAt(2)
        data = ZOSAPI.Editors.NCE.IObjectRectangularVolume(obj.ObjectData)

        x1_half_width = data.X1HalfWidth
        y1_half_width = data.Y1HalfWidth
        z_length = data.ZLength
        x2_half_width = data.X2HalfWidth
        y2_half_width = data.Y2HalfWidth

        CASE17_LOGGER.info("Object 2")
        CASE17_LOGGER.info(f"X1 Half Width: {x1_half_width}")
        CASE17_LOGGER.info(f"Y1 Half Width: {y1_half_width}")
        CASE17_LOGGER.info(f"Z Length: {z_length}")
        CASE17_LOGGER.info(f"X2 Half Width: {x2_half_width}")
        CASE17_LOGGER.info(f"Y2 Half Width: {y2_half_width}\n")

        vol_data = ZOSAPI.Editors.NCE.INCEVolumePhysicsData(obj.VolumePhysicsData)
        vol_model = vol_data.Model
        vol_model_mean_path = vol_data.ModelSettings._S_AngleScattering.MeanPath
        vol_model_angle = vol_data.ModelSettings._S_AngleScattering.Angle

        CASE17_LOGGER.info(f"Model Mean Path: {vol_model_mean_path}")
        CASE17_LOGGER.info(f"Model Angle: {vol_model_angle}\n")

        draw_data = obj.DrawData
        draw_data_opacity = draw_data.Opacity

        assert x1_half_width == 12
        assert y1_half_width == 12
        assert z_length == 40
        assert x2_half_width == 12
        assert y2_half_width == 12

        assert vol_model == ZOSAPI.Editors.NCE.VolumePhysicsModelType.AngleScattering
        assert vol_model_mean_path == 5
        assert vol_model_angle == 30

        assert draw_data_opacity == ZOSAPI.Common.ZemaxOpacity.P50

    def test_NSC_detector(self, case17_setup, CASE17_LOGGER):
        TheSystem, _, ZOSAPI = case17_setup
        obj = TheSystem.NCE.GetObjectAt(3)
        data = ZOSAPI.Editors.NCE.IObjectDetectorRectangle(obj.ObjectData)

        ref_obj = obj.RefObject
        z_pos = obj.ZPosition
        material = obj.Material
        obj_type = obj.Type

        CASE17_LOGGER.info(f'Detector')
        CASE17_LOGGER.info(f'Reference Object: {ref_obj}')
        CASE17_LOGGER.info(f'Z Position: {z_pos}')
        CASE17_LOGGER.info(f'Material: {material}\n')


        number_x_pixels = data.NumberXPixels
        number_y_pixels = data.NumberYPixels
        data_type = data.DataType
        color = data.Color
        smoothing = data.Smoothing

        CASE17_LOGGER.info(f"Number X Pixels: {number_x_pixels}")
        CASE17_LOGGER.info(f"Number Y Pixels: {number_y_pixels}")
        CASE17_LOGGER.info(f"Data Type: {data_type}")
        CASE17_LOGGER.info(f"Color: {color}")
        CASE17_LOGGER.info(f"Smoothing: {smoothing}")

        assert ref_obj == 2
        assert z_pos == 42
        assert material == "ABSORB"
        assert obj_type == ZOSAPI.Editors.NCE.ObjectType.DetectorRectangle

        assert number_x_pixels == 25
        assert number_y_pixels == 25
        assert data_type == 0
        assert color == 2
        assert smoothing == 1


if __name__ == '__main__':
    pass
