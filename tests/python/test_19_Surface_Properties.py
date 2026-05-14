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
import os

import pytest

from glob_settings import *

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "..", 'examples\\python\\')))
print(sys.path)
import PythonStandalone_19_Surface_Properties as ex19


@pytest.fixture(scope="module")
def CASE19_LOGGER(pytestconfig):
    log_folder = Path(pytestconfig.getoption("log_folder"))
    log_folder.mkdir(parents=True, exist_ok=True)
    LOGGER = logging.getLogger("ZOSPythonExampleCase19_pytest")
    LOGGER.setLevel(logging.INFO)

    test_log = log_folder.joinpath(f"ZOSPythonEx19Pytest_{TODAY}.log")
    case_fh = logging.FileHandler(test_log, mode="w")
    LOGGER.addHandler(case_fh)
    return LOGGER


@pytest.fixture(scope="module")
def case19_setup(CASE19_LOGGER, pytestconfig):
    CASE19_LOGGER.info(f"Test Date: {TODAY}")
    CASE19_LOGGER.info("Start to run the example 19")
    if pytestconfig.getoption("ZOS_PATH") == "":
        ZOS_PATH = None
    else: 
        ZOS_PATH = pytestconfig.getoption("ZOS_PATH")
    ex19.main(True, ZOS_PATH)
    CASE19_LOGGER.info("Finish example 19!")
    zos = ex19.PythonStandaloneApplication(ZOS_PATH)
    yield zos
    del zos


@pytest.fixture(scope="class")
def case19_prism_chain(case19_setup, CASE19_LOGGER):
    CASE19_LOGGER.info("Start to check the value in the sample file.")
    zos = case19_setup
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = TheApplication.CreateNewSystem(ZOSAPI.SystemType.Sequential)

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(os.sep, sampleDir, r"API\Python\e19_Sample_Prism_Chain.zmx")

    CASE19_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    return TheSystem, zos, ZOSAPI


@pytest.fixture(scope="class")
def case19_prism_chain_global(case19_setup, CASE19_LOGGER):
    CASE19_LOGGER.info("Start to check the value in the sample file.")
    zos = case19_setup
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = TheApplication.CreateNewSystem(ZOSAPI.SystemType.Sequential)

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep, sampleDir, r"API\Python\e19_Sample_Prism_Chain_GlobalCoordinate.zmx"
    )

    CASE19_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    return TheSystem, zos, ZOSAPI


@pytest.fixture(scope="class")
def case19_back_to_local(case19_setup, CASE19_LOGGER):
    CASE19_LOGGER.info("Start to check the value in the sample file.")
    zos = case19_setup
    ZOSAPI = zos.ZOSAPI

    TheApplication = zos.TheApplication
    TheSystem = TheApplication.CreateNewSystem(ZOSAPI.SystemType.Sequential)

    sampleDir = TheApplication.SamplesDir
    testFile = os.path.join(
        os.sep,
        sampleDir,
        r"API\Python\e19_Sample_Prism_Chain_BackTo_LocalCoordinate.zmx",
    )

    CASE19_LOGGER.info(f"Load test file: {testFile}")
    TheSystem.LoadFile(testFile, False)

    return TheSystem, zos, ZOSAPI


@pytest.mark.LDE
class TestPrismChain:
    @pytest.mark.surface_property
    def test_lens_aperture(self, case19_prism_chain, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_prism_chain

        res = []
        for i in range(10):
            surf_id = i * 3 + 2
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            aperture_type = surf.ApertureData.CurrentType
            x_width = (
                surf.ApertureData.CurrentTypeSettings._S_RectangularAperture.XHalfWidth
            )
            y_width = (
                surf.ApertureData.CurrentTypeSettings._S_RectangularAperture.YHalfWidth
            )

            data = (aperture_type, x_width, y_width)
            res.append(data)

        res_cmp = [
            data
            == (ZOSAPI.Editors.LDE.SurfaceApertureTypes.RectangularAperture, 10, 10)
        ]
        assert all(res_cmp), f"results: {res}"

    @pytest.mark.surface_property
    def test_lens_tilt(self, case19_prism_chain, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_prism_chain

        res = []
        for i in range(10):
            surf_id = i * 3 + 2
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            tile_order = surf.TiltDecenterData.BeforeSurfaceOrder
            before_surface = surf.TiltDecenterData.BeforeSurfaceTiltX
            after_surface = surf.TiltDecenterData.AfterSurfaceTiltX

            data = (tile_order, before_surface, after_surface)
            res.append(data)

        res_cmp = [
            data == (ZOSAPI.Editors.LDE.TiltDecenterOrderType.Decenter_Tilt, 15, -15)
        ]
        assert all(res_cmp), f"results: {res}"

        res = []
        for i in range(10):
            surf_id = i * 3 + 3
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            tile_order = surf.TiltDecenterData.BeforeSurfaceOrder
            before_surface = surf.TiltDecenterData.BeforeSurfaceTiltX
            after_surface = surf.TiltDecenterData.AfterSurfaceTiltX

            data = (tile_order, before_surface, after_surface)
            res.append(data)

        res_cmp = [
            data == (ZOSAPI.Editors.LDE.TiltDecenterOrderType.Decenter_Tilt, -15, 15)
            for data in res
        ]
        assert all(res_cmp), f"results: {res}"


    def test_coordinate_break_solve(self, case19_prism_chain, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_prism_chain

        res = []
        for i in range(10):
            surf_id = i * 3 + 4
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            thickness = TheSystem.LDE.GetSurfaceAt(surf_id).Thickness
            surface_data = ZOSAPI.Editors.LDE.ISurfaceCoordinateBreak(surf.SurfaceData)
            dec_x = surface_data.Decenter_X_Cell.Solve
            dec_y = surface_data.Decenter_Y_Cell.Solve
            tilt_x = surface_data.TiltAbout_X_Cell.Solve
            tilt_y = surface_data.TiltAbout_Y_Cell.Solve
            tilt_z = surface_data.TiltAbout_Z_Cell.Solve

            data = (thickness, dec_x, dec_y, tilt_x, tilt_y, tilt_z)
            res.append(data)

        editor_solve_type = ZOSAPI.Editors.SolveType
        PICKUP = editor_solve_type.PickupChiefRay
        FIXED = editor_solve_type.Fixed
        res_cmp = [data == (30, PICKUP, PICKUP, PICKUP, PICKUP, FIXED) for data in res]

        assert all(res_cmp), f"results: {res}"

    def test_material(self, case19_prism_chain, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_prism_chain

        res = []
        for i in range(10):
            surf_id = i * 3 + 2
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            data = surf.Material
            res.append(data)

        res_cmp = [data == "N-BK7" for data in res]

        assert all(res_cmp), f"results: {res}"

@pytest.mark.ConvertCoordinate
class TestPrismChainGlobal:
    @pytest.mark.surface_property
    def test_coordinate_break_return(self, case19_prism_chain_global, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_prism_chain_global

        res = []
        for i in range(10):
            surf_id = i * 5 + 4
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            coor_return = surf.TiltDecenterData.CoordinateReturn
            surf_return = surf.TiltDecenterData.CoordinateReturnToSurface
            data = (coor_return, surf_return)
            res.append(data)

        res_cmp = [data == (ZOSAPI.Editors.LDE.CoordinateReturnType.OrientationXYZ, 1) for data in res]
        assert all(res_cmp), f"results: {res}"


class TestPrismChainBackToLocal:
    @pytest.mark.surface_property
    def test_lens_aperture(self, case19_back_to_local, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_back_to_local

        res = []
        for i in range(10):
            surf_id = i * 3 + 2
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            aperture_type = surf.ApertureData.CurrentType
            x_width = (
                surf.ApertureData.CurrentTypeSettings._S_RectangularAperture.XHalfWidth
            )
            y_width = (
                surf.ApertureData.CurrentTypeSettings._S_RectangularAperture.YHalfWidth
            )

            data = (aperture_type, x_width, y_width)
            res.append(data)

        res_cmp = [
            data
            == (ZOSAPI.Editors.LDE.SurfaceApertureTypes.RectangularAperture, 10, 10)
        ]
        assert all(res_cmp), f"results: {res}"

    @pytest.mark.surface_property
    def test_lens_tilt(self, case19_back_to_local, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_back_to_local

        res = []
        for i in range(10):
            surf_id = i * 3 + 2
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            tile_order = surf.TiltDecenterData.BeforeSurfaceOrder
            before_surface = surf.TiltDecenterData.BeforeSurfaceTiltX
            after_surface = surf.TiltDecenterData.AfterSurfaceTiltX

            data = (tile_order, before_surface, after_surface)
            res.append(data)

        res_cmp = [
            data == (ZOSAPI.Editors.LDE.TiltDecenterOrderType.Decenter_Tilt, 15, -15)
        ]
        assert all(res_cmp), f"results: {res}"

        res = []
        for i in range(10):
            surf_id = i * 3 + 3
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            tile_order = surf.TiltDecenterData.BeforeSurfaceOrder
            before_surface = surf.TiltDecenterData.BeforeSurfaceTiltX
            after_surface = surf.TiltDecenterData.AfterSurfaceTiltX

            data = (tile_order, before_surface, after_surface)
            res.append(data)

        res_cmp = [
            data == (ZOSAPI.Editors.LDE.TiltDecenterOrderType.Decenter_Tilt, -15, 15)
            for data in res
        ]
        assert all(res_cmp), f"results: {res}"


    def test_coordinate_break_solve(self, case19_back_to_local, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_back_to_local

        res = []
        for i in range(10):
            surf_id = i * 3 + 4
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            surface_data = ZOSAPI.Editors.LDE.ISurfaceCoordinateBreak(surf.SurfaceData)
            dec_x = surface_data.Decenter_X_Cell.Solve
            dec_y = surface_data.Decenter_Y_Cell.Solve
            tilt_x = surface_data.TiltAbout_X_Cell.Solve
            tilt_y = surface_data.TiltAbout_Y_Cell.Solve
            tilt_z = surface_data.TiltAbout_Z_Cell.Solve

            data = (dec_x, dec_y, tilt_x, tilt_y, tilt_z)
            res.append(data)

        editor_solve_type = ZOSAPI.Editors.SolveType
        FIXED = editor_solve_type.Fixed
        res_cmp = [data == (FIXED, FIXED, FIXED, FIXED, FIXED) for data in res]

        assert all(res_cmp), f"results: {res}"

    def test_material(self, case19_back_to_local, CASE19_LOGGER):
        TheSystem, zos, ZOSAPI = case19_back_to_local

        res = []
        for i in range(10):
            surf_id = i * 3 + 2
            surf = TheSystem.LDE.GetSurfaceAt(surf_id)
            data = surf.Material
            res.append(data)

        res_cmp = [data == "N-BK7" for data in res]

        assert all(res_cmp), f"results: {res}" 