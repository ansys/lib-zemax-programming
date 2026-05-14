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

from glob_settings import TEST_SCRIPT_FOLDER, PYTHONNET_VER, TODAY, TEST_ZOS_PATH
import pytest
import sys

def main(argv):
    TURNS = 1
    LOG_FOLDER = TEST_SCRIPT_FOLDER.joinpath(f"reports/logs_PYNET{PYTHONNET_VER}_run{TURNS:02d}_{TODAY}")
    while LOG_FOLDER.exists():
        TURNS += 1
        LOG_FOLDER = TEST_SCRIPT_FOLDER.joinpath(f"reports/logs_PYNET{PYTHONNET_VER}_run{TURNS:02d}_{TODAY}")
    IMAGE_FOLDER = LOG_FOLDER.joinpath("imgs")
    LOG_FOLDER.mkdir(parents=True, exist_ok=True)
    IMAGE_FOLDER.mkdir(parents=True, exist_ok=True)
    HTML_FILE = LOG_FOLDER.joinpath("report.html")
    argv.extend(["--log-folder", str(LOG_FOLDER), "--img-folder", str(IMAGE_FOLDER), "--html", str(HTML_FILE), "--ZOS-PATH", str(TEST_ZOS_PATH)])
    pytest.main(args=argv)


if __name__ == "__main__":
    main(argv=sys.argv[1:])
