# importing modules
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import struct
import math
from PIL import Image

# INPUTS FROM USER
# filepath_read = input image full filename. Greyscale or viridis colour scale are supported
# filepath_write = output ZBF full filename
# X_size_mm = Full X size of the beam array in mm
# Wave_mm = Wavelength in mm
# Text_bool = Boolean. Write 1 to create a ZBF text or 0 to creat a a ZBF binary
filepath_read = r'LaserBeam1.png'
filepath_write = r"C:\Users\Documents\Zemax\POP\BEAMFILES\LaserBeam.ZBF"
X_size_mm = 10
Wave_mm = 0.0006328
Text_bool = 1


def next_largest_power_of_2(n):
    """
        Function that returns the next largest power of 2 value
        For example, if n=20, then it will return 32 (2^5)

        Parameters
        ----------
        n value

        Returns
        -------
        integer
            
        """       
    return pow(2, int(math.log(n) / math.log(2))+1)   
    

# Read Images
# img = mpimg.imread(filepath_read)

# Convert to grey scale
im = np.array(Image.open(filepath_read).convert('L'))  # can pass multiple arguments in single line
plt.imshow(im)
plt.colorbar()
plt.show()

size = im.shape
Number_Y_pixels = size[0]
Number_X_pixels = size[1]

# The array size in POP are power of 2, for example 32 (2^5), 64 (2^6), 
# so the array size must be a power of 2 so need to resize
padding_y = next_largest_power_of_2(Number_Y_pixels) - Number_Y_pixels
padding_x = next_largest_power_of_2(Number_X_pixels) - Number_X_pixels

padding_y_left = int(padding_y/2)
padding_y_right = padding_y - padding_y_left
padding_x_left = int(padding_x/2)
padding_x_right = padding_x - padding_x_left

im = np.pad(im, ((padding_y_left, padding_y_right), (padding_x_left, padding_x_right)), 'constant', constant_values=(0))

# Finally flip the array
im = np.flipud(im)

# Now the array size is a power of 2
size = im.shape
Number_Y_pixels = size[0]
Number_X_pixels = size[1]

Y_size_mm = Number_Y_pixels * X_size_mm / Number_X_pixels

# width_byte = width.to_bytes((width.bit_length() + 7) // 8, byteorder='little')
# height_byte = width.to_bytes((height.bit_length() + 7) // 8, byteorder='little')

# what needs to be inside the ZBF File
Version = 1
Nx = Number_X_pixels
Ny = Number_Y_pixels
IsPol = 0  # set to unpolarized - The "is polarized" flag; 0 for unpolarized, 1 for polarized.
Units = 0  # for mm
Unused = 0  # Unused
Xspacing = X_size_mm / Number_X_pixels
Yspacing = Y_size_mm / Number_Y_pixels
X_ZPos = 0
X_ZR = 0
X_W0 = 0
Y_ZPos = 0
Y_ZR = 0
Y_W0 = 0
Wave = Wave_mm
Indx = 1
Rec_Eff = 0
Sys_Eff = 0

# Normalize the max of the image to 1
max = 0
for i in range(0, Number_Y_pixels, 1):
    for j in range(0, Number_X_pixels, 1):
        if (im[i, j]) > max:
            max = im[i, j]

if max == 0:
    # print('Error max of the image = 0')
    sys.exit("Error max of the image = 0")

if (Text_bool):
    file = open(filepath_write, "w")  # Overwrites the file if the file exists
    # Writing the header text lines
    file.write("A" + '\n')
    file.write(str(Version) + '\n')
    file.write(str(Number_X_pixels) + '\n')
    file.write(str(Number_Y_pixels) + '\n')
    file.write(str(IsPol) + '\n')
    file.write(str(Units) + '\n')
    for i in range(1, 5, 1):  # 4 unused integers
        file.write(str(Unused) + '\n')
    file.write(str(Xspacing) + '\n')  # d is for double for 8 bytes
    file.write(str(Yspacing) + '\n')
    file.write(str(X_ZPos) + '\n')
    file.write(str(X_ZR) + '\n')
    file.write(str(X_W0) + '\n')
    file.write(str(Y_ZPos) + '\n')
    file.write(str(Y_ZR) + '\n')
    file.write(str(Y_W0) + '\n')
    file.write(str(Wave) + '\n')
    file.write(str(Indx) + '\n')
    file.write(str(Rec_Eff) + '\n')
    file.write(str(Sys_Eff) + '\n')
    for i in range(1, 9, 1):  # 8 unused doubles
        file.write(str(Unused) + '\n')

    # First write Ex
    for i in range(0, Number_Y_pixels, 1):
        for j in range(0, Number_X_pixels, 1):
            Ex_r = math.sqrt((im[i, j]) / 2 / max)
            Ex_i = 0
            file.write(str(Ex_r) + '\n')
            file.write(str(Ex_i) + '\n')

    # Then write Ey
    # There is no Ey since the beam is not polarized
    # for i in range(0, Number_Y_pixels, 1):
    #    for j in range(0, Number_X_pixels, 1):
    #        Ey_r = math.sqrt((im[i, j]) / 2 / max)
    #        Ey_i = 0
    #        file.write(str(Ey_r) + '\n')
    #        file.write(str(Ey_i) + '\n')

else:
    file = open(filepath_write, "wb")  # Overwrites the file if the file exists
    # Writing the header binary lines
    file.write(Version.to_bytes(4, byteorder='little'))
    file.write(Number_X_pixels.to_bytes(4, byteorder='little'))
    file.write(Number_Y_pixels.to_bytes(4, byteorder='little'))
    file.write(IsPol.to_bytes(4, byteorder='little'))
    file.write(Units.to_bytes(4, byteorder='little'))
    for i in range(1, 5, 1):  # 4 unused integers
        file.write(Unused.to_bytes(4, byteorder='little'))
    file.write(struct.pack('d', Xspacing))  # d is for double for 8 bytes
    file.write(struct.pack('d', Yspacing))
    file.write(struct.pack('d', X_ZPos))
    file.write(struct.pack('d', X_ZR))
    file.write(struct.pack('d', X_W0))
    file.write(struct.pack('d', Y_ZPos))
    file.write(struct.pack('d', Y_ZR))
    file.write(struct.pack('d', Y_W0))
    file.write(struct.pack('d', Wave))
    file.write(struct.pack('d', Indx))
    file.write(struct.pack('d', Rec_Eff))
    file.write(struct.pack('d', Sys_Eff))
    for i in range(1, 9, 1):  # 8 unused doubles
        file.write(struct.pack('d', Unused))

    # First write Ex
    for i in range(0, Number_Y_pixels, 1):
        for j in range(0, Number_X_pixels, 1):
            Ex_r = math.sqrt((im[i, j]) / 2 / max)
            Ex_i = 0
            file.write(struct.pack('d', Ex_r))
            file.write(struct.pack('d', Ex_i))

    # Then write Ey
    # There is no Ey since the beam is not polarized
    # for i in range(0, Number_Y_pixels, 1):
    #    for j in range(0, Number_X_pixels, 1):
    #        Ey_r = math.sqrt((im[i, j]) / 2 / max)
    #        Ey_i = 0
    #        file.write(struct.pack('d', Ey_r))
    #        file.write(struct.pack('d', Ey_i))

file.close()

print('The file %s has been created!' % filepath_write)
