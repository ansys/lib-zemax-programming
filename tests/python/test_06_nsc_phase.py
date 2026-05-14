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

import numpy as np
import pytest

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_06_nsc_phase as ex6


@pytest.fixture(scope="module")
def CASE06_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase06_pytest")
    LOGGER.setLevel(logging.INFO)

    test06_log = log_folder.joinpath(f"ZOSPythonEx06Pytest_{TODAY}.log")
    case06_fh = logging.FileHandler(test06_log, mode="w")
    LOGGER.addHandler(case06_fh)
    return LOGGER


@pytest.mark.api_case06
@pytest.mark.xdist_group(name="pyapi_06")
def test_nsc_phase_data(CASE06_LOGGER, pytestconfig, extra):
    image_folder = Path(pytestconfig.getoption("img_folder"))
    image_folder.mkdir(parents=True, exist_ok=True)
    CASE06_LOGGER.info(f"Test Date: {TODAY}")
    CASE06_LOGGER.info("Start to run the example 06")

    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")

    # Real
    irradiance, phase = ex6.main(True, ZOS_PATH)
    CASE06_LOGGER.info("Finish example 06!")
    CASE06_LOGGER.info("Start to check the value in the sample file.")

    # Expected
    with open(CMP_DATA_FOLDER.joinpath("ex06/ex06.json"), 'r') as f:
        expected = json.load(f)
    expected_phase = expected['phase']
    expected_irradiance = expected['irradiance']

    np.testing.assert_allclose(irradiance, expected_irradiance, rtol=1e-8)
    np.testing.assert_allclose(phase, expected_phase, rtol=1e-8)


if __name__ == "__main__":
    pass
