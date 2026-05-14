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
import PythonStandalone_04_pull_data_from_FFTMTF as ex4


@pytest.fixture(scope="module")
def CASE04_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase04_pytest")
    LOGGER.setLevel(logging.INFO)

    test04_log = log_folder.joinpath(f"ZOSPythonEx04Pytest_{TODAY}.log")
    case04_fh = logging.FileHandler(test04_log, mode="w")
    LOGGER.addHandler(case04_fh)
    return LOGGER


@pytest.mark.api_case04
@pytest.mark.xdist_group(name="pyapi_04")
def test_fftmtf_data(CASE04_LOGGER, pytestconfig, extra):
    image_folder = Path(pytestconfig.getoption("img_folder"))
    image_folder.mkdir(parents=True, exist_ok=True)
    CASE04_LOGGER.info(f"Test Date: {TODAY}")
    CASE04_LOGGER.info("Start to run the example 04")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    fftmtf_data = ex4.main(True, ZOS_PATH)
    CASE04_LOGGER.info("Finish example 04!")

    CASE04_LOGGER.info("Start to check the value in the sample file.")

    # Expected
    with open(CMP_DATA_FOLDER.joinpath("ex04/ex04.json"), 'r') as f:
        loaded = json.load(f)
    expected_x = loaded['x']
    expected_y = loaded['y']
    CASE04_LOGGER.info('expected\n')
    CASE04_LOGGER.info(expected_x)

    # Real
    real_x = fftmtf_data['x']
    real_y = fftmtf_data['y']
    CASE04_LOGGER.info('real\n')
    CASE04_LOGGER.info(real_x)

    np.testing.assert_allclose(real_x, expected_x, atol=1e-8)
    np.testing.assert_allclose(real_y, expected_y, atol=1e-8)


if __name__ == "__main__":
    pass
