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
import json
import os

import numpy as np
import pytest

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_08_NSCEDetectorData as ex8

def rms(dataset):
    dataset = np.array(dataset)
    return np.nanmean(dataset ** 2) ** 0.5


@pytest.fixture(scope="module")
def CASE08_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase08_pytest")
    LOGGER.setLevel(logging.INFO)

    test08_log = log_folder.joinpath(f"ZOSPythonEx08Pytest_{TODAY}.log")
    case08_fh = logging.FileHandler(test08_log, mode="w")
    LOGGER.addHandler(case08_fh)
    return LOGGER

@pytest.fixture(scope='module')
def case08_setup(CASE08_LOGGER, pytestconfig):
    image_folder = Path(pytestconfig.getoption("img_folder"))
    image_folder.mkdir(parents=True, exist_ok=True)
    CASE08_LOGGER.info(f"Test Date: {TODAY}")
    CASE08_LOGGER.info("Start to run the example 08")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")

    detector_data = ex8.main(True, ZOS_PATH)
    
    with open(CMP_DATA_FOLDER.joinpath("ex08/ex08.json"), 'r') as f:
        expected = json.load(f)

    yield detector_data, expected

@pytest.mark.api_case08
@pytest.mark.xdist_group(name="pyapi_08")
class TestPythonStandalone08NNSCEDetectorData:
    def test_radial_rms(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            detector_data['DetPolarData_RadialRMS'], 
            expected['DetPolarData_RadialRMS'],
            rtol=0.001
            )
        
    def test_chromX(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            detector_data['DetPolarData_ChromX'], 
            expected['DetPolarData_ChromX'],
            rtol=1e-3
            )
        
    def test_chromY(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            detector_data['DetPolarData_ChromY'], 
            expected['DetPolarData_ChromY'],
            rtol=1e-3
            )
        
    def test_trix(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetPolarData_TriX']), 
            rms(expected['DetPolarData_TriX']),
            rtol=1e-3
            )
        
    def test_triy(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetPolarData_TriY']),
            rms(expected['DetPolarData_TriY']),
            rtol=1e-3
            )
        
    def test_triz(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetPolarData_TriZ']), 
            rms(expected['DetPolarData_TriZ']),
            rtol=1e-3
            )
        
    def test_stddev(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetRectangleData_StdDev']), 
            rms(expected['DetRectangleData_StdDev']),
            rtol=10**-0.5
            )
        
    def test_flux(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetRectangleData_Flux']), 
            rms(expected['DetRectangleData_Flux']),
            rtol=1e-3
            )
        
    def test_flux_area(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetRectangleData_FluxArea']), 
            rms(expected['DetRectangleData_FluxArea']),
            rtol=1e-3
            )
        
    def test_flux_sap(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetRectangleData_FluxSAP']), 
            rms(expected['DetRectangleData_FluxSAP']),
            rtol=1e-3
            )
        
    def test_coherent_amplitude(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetRectangle_CoherentAmp']), 
            rms(expected['DetRectangle_CoherentAmp']),
            rtol=1e-3
            )
        
    def test_coherent_power(self, case08_setup):
        detector_data, expected = case08_setup
        np.testing.assert_allclose(
            rms(detector_data['DetRectangle_CoherentPower']), 
            rms(expected['DetRectangle_CoherentPower']),
            rtol=1e-3
            )



if __name__ == "__main__":
    pass
