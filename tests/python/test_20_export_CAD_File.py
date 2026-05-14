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

import pytest

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_20_export_CAD_File as ex20


@pytest.fixture(scope="module")
def CASE20_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase20_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx20Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case20_setup(CASE20_LOGGER, pytestconfig):
    CASE20_LOGGER.info(f"Test Date: {TODAY}")
    CASE20_LOGGER.info("Start to run the example 20")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex20.main(True, ZOS_PATH)
    CASE20_LOGGER.info("Finish example 20!")
    zos = ex20.PythonStandaloneApplication(ZOS_PATH)
    yield zos
    file = zos.TheApplication.ObjectsDir + '\\CAD Files\\API_CADexport_sample.step'
    Path(file).unlink(missing_ok=True)
    del zos


class TestExportCAD:
    def test_file_exist(self, case20_setup):
        zos = case20_setup
        file = zos.TheApplication.ObjectsDir + '\\CAD Files\\API_CADexport_sample.step'

        assert Path(file).exists(), f"File Path: {file}"


if __name__ == '__main__':
    pass