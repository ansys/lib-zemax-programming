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
import pandas as pd

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_05_Read_ZRD_File as ex5


@pytest.fixture(scope="module")
def CASE05_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase05_pytest")
    LOGGER.setLevel(logging.INFO)

    test05_log = log_folder.joinpath(f"ZOSPythonEx05Pytest_{TODAY}.log")
    case05_fh = logging.FileHandler(test05_log, mode="w")
    LOGGER.addHandler(case05_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case05_setup(CASE05_LOGGER, pytestconfig):
    image_folder = Path(pytestconfig.getoption("img_folder"))
    image_folder.mkdir(parents=True, exist_ok=True)
    CASE05_LOGGER.info(f"Test Date: {TODAY}")
    CASE05_LOGGER.info("Start to run the example 05")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    res = ex5.main(True, ZOS_PATH)
    CASE05_LOGGER.info("Finish example 05!")
    
    with open(CMP_DATA_FOLDER.joinpath("ex05/ex05.json"), 'r') as f:
        expected = json.load(f)

    return res, expected

@pytest.mark.api_case05
@pytest.mark.xdist_group(name="pyapi_05")
def test_zrd_data(case05_setup):
    res, expected = case05_setup
    res = pd.DataFrame(res)
    expected = pd.DataFrame(expected)
    pd.testing.assert_frame_equal(res, expected)
    

if __name__ == "__main__":
    pass
