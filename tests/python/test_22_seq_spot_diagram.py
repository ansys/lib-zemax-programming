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
import PythonStandalone_22_seq_spot_diagram as ex22


@pytest.fixture(scope="module")
def CASE22_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase22_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx22Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case22_setup(CASE22_LOGGER, pytestconfig):
    CASE22_LOGGER.info(f"Test Date: {TODAY}")
    CASE22_LOGGER.info("Start to run the example 22")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    res = ex22.main(True, ZOS_PATH)
    CASE22_LOGGER.info("Finish example 22!")
    with open(CMP_DATA_FOLDER.joinpath('ex22/ex22.json'), 'r') as f:
        expected = json.load(f)
    return res, expected


class TestSeqSpotDiamgram:
    def test_rms(self, case22_setup, CASE22_LOGGER):
        res, expected = case22_setup
        res = res['rms']
        expected = expected['rms']
        CASE22_LOGGER.info(f'res: {res}')
        CASE22_LOGGER.info(f'expected: {expected}')
        np.testing.assert_array_equal(res, expected)

    def test_geo(self, case22_setup, CASE22_LOGGER):
        res, expected = case22_setup
        res = res['geo']
        expected = expected['geo']
        CASE22_LOGGER.info(f'res: {res}')
        CASE22_LOGGER.info(f'expected: {expected}')
        np.testing.assert_array_equal(res, expected)

    def test_x_ary(self, case22_setup, CASE22_LOGGER):
        res, expected = case22_setup
        res = res['x_ary']
        expected = expected['x_ary']
        CASE22_LOGGER.info(f'res: {res}')
        CASE22_LOGGER.info(f'expected: {expected}')
        np.testing.assert_array_equal(res, expected)

    def test_y_ary(self, case22_setup, CASE22_LOGGER):
        res, expected = case22_setup
        res = res['y_ary']
        expected = expected['y_ary']
        CASE22_LOGGER.info(f'res: {res}')
        CASE22_LOGGER.info(f'expected: {expected}')
        np.testing.assert_array_equal(res, expected)


if __name__ == '__main__':
    pass
