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
import PythonStandalone_23_ray_fan_native_manual_comparison as ex23


@pytest.fixture(scope="module")
def CASE23_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase23_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx23Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case23_setup(CASE23_LOGGER, pytestconfig):
    CASE23_LOGGER.info(f"Test Date: {TODAY}")
    CASE23_LOGGER.info("Start to run the example 23")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    res = ex23.main(True, ZOS_PATH)
    CASE23_LOGGER.info("Finish example 23!")
    with open(CMP_DATA_FOLDER.joinpath('ex23/ex23.json'), 'r') as f:
        expected = json.load(f)
    return res, expected


class TestRayFanNativeManual:
    def test_native_x(self, case23_setup, CASE23_LOGGER):
        res, expected = case23_setup
        res = res['x']
        expected = expected['x']
        np.testing.assert_array_equal(res, expected)

    def test_native_y(self, case23_setup, CASE23_LOGGER):
        res, expected = case23_setup
        res = res['y']
        expected = expected['y']
        np.testing.assert_array_equal(res, expected)

    def test_manual_x(self, case23_setup, CASE23_LOGGER):
        res, expected = case23_setup
        res = res['py_ary']
        expected = expected['py_ary']
        np.testing.assert_array_equal(res, expected)

    def test_manual_y(self, case23_setup, CASE23_LOGGER):
        res, expected = case23_setup
        res = res['y_ary']
        expected = expected['y_ary']
        np.testing.assert_array_equal(res, expected)

