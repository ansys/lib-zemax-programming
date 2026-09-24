# write a zemax binary source file
# original author: David Nguyen
#https://github.com/Omnistic/BinarySource_OpticStudio/blob/main/write_source_TEMPLATE.py

# Imports
import struct
import numpy as np

def write_binary_source_file(ray_data, file_name, dimension_flag):
    # Create, and open a new binary file
    file = open(file_name, 'wb')

    # Variable header data
    number_rays = np.size(ray_data, 0)      # The number of rays in the file.
    description = 'Source from ZBB'         # A text description of the source (maximum 100 characters).
    source_flux = np.sum(ray_data[:,6])     # The total flux in watts of this source.
    ray_set_flux = np.sum(ray_data[:,6])    # The flux in watts represented by this Ray Set.
    wavelength = 0                          # The wavelength in micrometers, 0 if a composite.
    inclination = (0, 0)                    # Angular range for ray set (Degrees).
    azimuth = (0, 0)                        # Angular range for ray set (Degrees).
    dimension_units = dimension_flag        # METERS=0, IN=1, CM=2, FEET=3, MM=4
    loc = (0, 0, 0)                    # Coordinate Translation of the source.
    rot = (0, 0, 0)                         # Source rotation (Radians).
    ray_format = 2                          # The ray_format_type must be either 0
                                            # for flux only format, or 2 for the
                                            # spectral color format.
    flux_type = 0                           # If and only if the ray_format_type is
                                            # 0, then the flux_type is 0 for watts,
                                            # and 1 for lumens. For the spectral
                                            # color format, the flux must be in
                                            # watts, and the wavelength in micrometers.

    # Fixed header data
    format_version = 1010                   # Format version ID, current value is 1010.

    # Unused header data
    scale = (0, 0, 0)                       # Currently unused.

    # Write header data
    file.write(struct.pack('i', format_version))
    file.write(struct.pack('i', number_rays))
    if len(description) < 100:
        description.ljust(100, '\0')
    else:
        description = description[0:99]
    file.write(struct.pack('100s', description.encode('utf-8')))
    file.write(struct.pack('f', source_flux))
    file.write(struct.pack('f', ray_set_flux))
    file.write(struct.pack('f', wavelength))
    file.write(struct.pack('2f', inclination[0], inclination[1]))
    file.write(struct.pack('2f', azimuth[0], azimuth[1]))
    file.write(struct.pack('l', dimension_units))
    file.write(struct.pack('3f', loc[0], loc[1], loc[2]))
    file.write(struct.pack('3f', rot[0], rot[1], rot[2]))
    file.write(struct.pack('3f', scale[0], scale[1], scale[2]))
    file.write(struct.pack('4f', 0, 0, 0, 0)) # Unused bytes
    file.write(struct.pack('2i', ray_format, flux_type))
    file.write(struct.pack('2i', 0, 0)) # Reserved bytes

    for i in range(0, np.size(ray_data, 0)):
        # Ray data
        x = ray_data[i,0]
        y = ray_data[i,1]
        z = ray_data[i,2]
        l = ray_data[i,3]
        m = ray_data[i,4]
        n = ray_data[i,5]
        flux = ray_data[i,6]
        wavelength = ray_data[i,7]

        # Write spectral data
        file.write(struct.pack('8f', x, y, z, l, m, n, flux, wavelength))

    # Close the binary file
    file.close()