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

import pytest


def pytest_addoption(parser):
    parser.addoption("--log-folder", action="store", default="reports/logs")
    parser.addoption("--img-folder", action="store", default="reports/logs/imgs")
    parser.addoption("--ZOS-PATH", action="store", default="")


@pytest.fixture(scope="session")
def log_folder(request):
    """Path to the folder where test logs and HTML reports are written."""
    return request.config.getoption("--log-folder")


@pytest.fixture(scope="session")
def img_folder(request):
    """Path to the folder where test images are saved."""
    return request.config.getoption("--img-folder")


@pytest.fixture(scope="session")
def zos_path(request):
    """Path to the OpticStudio installation directory."""
    return request.config.getoption("--ZOS-PATH")
