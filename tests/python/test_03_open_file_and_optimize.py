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
import plotly.graph_objs as go
import json

import pandas as pd
import pytest
import pytest_html
import json

from glob_settings import *
from utils import convert_mf_to_list

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_03_open_file_and_optimise as ex03


@pytest.fixture(scope="module")
def CASE03_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase03_pytest")
    LOGGER.setLevel(logging.INFO)

    test03_log = log_folder.joinpath(f"ZOSPythonEx03Pytest_{TODAY}.log")
    case03_fh = logging.FileHandler(test03_log, mode="w")
    LOGGER.addHandler(case03_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case03_setup(CASE03_LOGGER, pytestconfig):
    CASE03_LOGGER.info(f"Test Date: {TODAY}")
    CASE03_LOGGER.info("Start to run the example 03")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex03.main(True, zos_path = ZOS_PATH)
    CASE03_LOGGER.info("Finish example 03!")

    CASE03_LOGGER.info("Start to check the value in the sample file.")
    zos = ex03.PythonStandaloneApplication()
    ZOSAPI = zos.ZOSAPI

    TheSystem = zos.TheSystem

    yield TheSystem, zos, ZOSAPI

    del zos


@pytest.fixture(scope="class")
def merit_setup(case03_setup):
    TheSystem, zos, ZOSAPI = case03_setup
    TheApplication = zos.TheApplication
    sampleDir = TheApplication.SamplesDir
    mf_file = sampleDir + "\\API\\Python\\Example_3_MF.mf"
    result = convert_mf_to_list(mf_file)

    with open(CMP_DATA_FOLDER.joinpath('ex03/ex03.json'), 'r') as f:
        expected = json.load(f)

    return pd.DataFrame(result),  pd.DataFrame(expected)


@pytest.mark.MFE
class TestMeritfunction:
    def test_merit_function(self, merit_setup, CASE03_LOGGER):
        res, expected = merit_setup
        CASE03_LOGGER.info(f'results:\n {res}\n')
        CASE03_LOGGER.info(f'expected:\n {expected}\n')

        pd.testing.assert_frame_equal(res, expected)

if __name__ == "__main__":
    pass
