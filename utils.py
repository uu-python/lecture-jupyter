import numpy
import struct

def read_mrc(filename):
    numbytes1=56           # 56 long ints
    numbytes2=80*10        # 10 header lines of 80 chars each
    input_image=open(filename,'rb')
    header1=input_image.read(numbytes1*4)
    header2=input_image.read(numbytes2)
    byte_pattern='=' + 'l'*numbytes1   #'=' required to get machine independent standard size
    dim=struct.unpack(byte_pattern, header1)[:3]   #(dimx,dimy,dimz)
    imagetype=struct.unpack(byte_pattern, header1)[3]  #0: 8-bit signed, 1:16-bit signed, 2: 32-bit float, 6: unsigned 16-bit (non-std)
    if (imagetype == 0):
        imtype='b'
    elif (imagetype ==1):
        imtype='h'
    elif (imagetype ==2):
        imtype='f4'
    elif (imagetype ==6):
        imtype='H'
    else:
        print "ERROR: Unknown data type! Cannot read MRC file."
        return
    input_image_dimension=(dim[1],dim[0])  #2D images assumed
    image_data=numpy.fromfile(file=input_image,dtype=imtype,count=dim[0]*dim[1]).reshape(input_image_dimension)
    input_image.close()
    return image_data
