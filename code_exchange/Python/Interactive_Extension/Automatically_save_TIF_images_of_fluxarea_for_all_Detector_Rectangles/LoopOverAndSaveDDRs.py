from PIL import Image  #pip install pillow
import numpy as np
from itertools import islice

def LoopOverAndSaveDDRs(TheSystem):


    TheNCE = TheSystem.NCE
    input_file = TheSystem.SystemFile
    object_count = TheNCE.NumberOfObjects  # Determine iteration count for loop over all objects
    for i in range(object_count):
        obj = TheSystem.NCE.GetObjectAt(i + 1)
        if obj.RowTypeName == 'Detector Rectangle':
            # This is code copied directly from a sample file:
            # ! [e08s08_py]
            # To retrieve the entire data array (flux, flux/area, etc.) for all pixel data,
            # can use GetAllDetectorDataSafe(), or GetAllDetectorData().
            # The 'Data' inputs for these functions (parameter 2) can be found in the API syntax help,
            # under the listing for GetDetectorData().
            # DetRectangleData_Flux = TheSystem.NCE.GetAllDetectorDataSafe(i + 1, 0)  # total flux on each pixel
            DetRectangleData_FluxArea = TheNCE.GetAllDetectorDataSafe(i + 1, 1)    # flux/area on each pixel
            # DetRectangleDimensions = TheSystem.NCE.GetAllDetectorSize(i + 1)
            # DetRectangleData_FluxArea = TheSystem.NCE.GetAllDetectorDataSafe(i + 1, 1)  # flux/area on each pixel
            dims_bool_return, X_detectorDims, Y_detectorDims = TheNCE.GetDetectorDimensions(i + 1, 0, 0)  # get number of
            # pixels in X, Y
            # DetRectangleData_FluxSAP = TheSystem.NCE.GetAllDetectorDataSafe(i + 1, 2)  # flux/solid angle pixel on each pixel
            # ! [e08s08_py]
            flux_area_data = np.flipud(np.asarray(reshape(DetRectangleData_FluxArea, X_detectorDims, Y_detectorDims)))
            if obj.Comment:
                my_detector_string = ', ' + obj.Comment + ', D{0}'.format(i + 1)
            else:
                my_detector_string = ', D{0}'.format(i + 1)
            my_tiff = input_file[:-4] + my_detector_string + '.tif'
            Image.fromarray(flux_area_data).save(my_tiff)  # , tiffinfo=tiff_info
            print('Saved {}.'.format(my_tiff))


def reshape(data, x, y, transpose=False):
    """Converts a System.Double[,] to a 2D list for plotting or post processing

    Parameters
    ----------
    data      : System.Double[,] data directly from ZOS-API
    x         : x width of new 2D list [use var.GetLength(0) for dimension]
    y         : y width of new 2D list [use var.GetLength(1) for dimension]
    transpose : transposes data; needed for some multi-dimensional line series data

    Returns
    -------
    res       : 2D list; can be directly used with Matplotlib or converted to
                a numpy array using numpy.asarray(res)
    """
    if type(data) is not list:
        data = list(data)
    var_lst = [y] * x
    it = iter(data)
    res = [list(islice(it, i)) for i in var_lst]
    if transpose:
        return self.transpose(res)
    return res


def transpose(data):
    """Transposes a 2D list (Python3.x or greater).

    Useful for converting mutli-dimensional line series (i.e. FFT PSF)

    Parameters
    ----------
    data      : Python native list (if using System.Data[,] object reshape first)

    Returns
    -------
    res       : transposed 2D list
    """
    if type(data) is not list:
        data = list(data)
    return list(map(list, zip(*data)))