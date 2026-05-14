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

import numpy as np
import pytest
import pytest_html

from glob_settings import *
from utils import make_subplots_in_horizontal, map_infos

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_02_NSC_ray_trace as ex2


@pytest.fixture(scope="module")
def CASE02_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase02_pytest")
    LOGGER.setLevel(logging.INFO)

    test02_log = log_folder.joinpath(f"ZOSPythonEx02Pytest_{TODAY}.log")
    case02_fh = logging.FileHandler(test02_log, mode="w")
    LOGGER.addHandler(case02_fh)
    return LOGGER


@pytest.mark.api_case02
@pytest.mark.xdist_group(name="pyapi_02")
def test_detector_data(CASE02_LOGGER, pytestconfig, extra):
    image_folder = Path(pytestconfig.getoption("img_folder"))
    image_folder.mkdir(parents=True, exist_ok=True)
    CASE02_LOGGER.info(f"Test Date: {TODAY}")
    CASE02_LOGGER.info("Start to run the example 02")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    CASE02_LOGGER.info(f"ZOS_PATH = {ZOS_PATH}")
    detector_data = ex2.main(True, zos_path = ZOS_PATH)
    CASE02_LOGGER.info("Finish example 02!")

    CASE02_LOGGER.info("Start to check the value in the sample file.")

    data_dict = {"real": None, "expected": None}
    fig_dict = {"real": None, "expected": None}
    with open(CMP_DATA_FOLDER.joinpath("ex02/ex02.json"), 'r') as f:
        expected = np.array(json.load(f))
    data_dict["expected"] = expected
    detector_data = np.asarray(detector_data)
    data_dict["real"] = detector_data
    
    # Plot figure
    # fig_dict["expected"] = go.Contour(
    #     z=expected,
    #     colorscale="jet",
    #     contours_coloring="heatmap",
    #     line_width=0,
    #     coloraxis="coloraxis",
    # )

    # fig_dict["real"] = go.Contour(
    #     z=detector_data,
    #     colorscale="jet",
    #     contours_coloring="heatmap",
    #     line_width=0,
    #     coloraxis="coloraxis",
    # )
    # fig = make_subplots_in_horizontal(fig_dict)
    # fig_folder = image_folder.joinpath("ex2")
    # fig_folder.mkdir(exist_ok=True)
    # fig_path = fig_folder.joinpath("cmp_detector_data.png")
    # fig.write_image(fig_path)
    # extra.append(pytest_html.extras.image(str(fig_path.relative_to(TEST_SCRIPT_FOLDER))))

    CASE02_LOGGER.info(f"\n{map_infos(data_dict)}")
    actual_rms = np.nanmean(data_dict["real"] ** 2) ** 0.5
    expected = np.nanmean(data_dict["expected"] ** 2) ** 0.5
    assert actual_rms == pytest.approx(expected, rel=0.001)


if __name__ == "__main__":
    pass
