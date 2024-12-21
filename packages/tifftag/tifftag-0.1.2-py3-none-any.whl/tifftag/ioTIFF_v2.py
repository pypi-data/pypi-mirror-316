# -*- coding: utf-8 -*-

from fractions import Fraction
import struct
import numpy as np
import sys
from _io import TextIOWrapper

__doc__ = """

This library contains two main classes for handling TIFF files :

 * TIFFReader
 * TIFFWriter

It also contains simple functions for generic uses :

 * readTIFF(fname) 
    return a Numpy array in 2 or 3 dimensions
    
 * writeTIFF(fname, vol, metadata={}, **kwargs)
    write a TIFF file from a Numpy array in 2 or 3 dimensions
    
 * readTIFF_metadata(fname)
    return only the metadata of the TIFF File without loading the image(s)

 * readZeissMD(fname)
    return only the Zeiss metadata of the TIFF File without loading the image(s)

"""

def as_little(array):
    return array.astype(np.dtype('<%s%d' % (array.dtype.kind, array.dtype.itemsize)))

if sys.byteorder == 'little':
    le = ['<', '=']
    be = ['>']
else:
    le = ['<']
    be = ['>', '=']

def change_byte_order(array, new_byteorder):
    return array.astype('%s%s%d' % (new_byteorder, array.dtype.kind, array.dtype.itemsize))

LITTLE_ENDIAN = b'\x49\x49'
BIG_ENDIAN = b'\x4d\x4d'

THE_SOLUTION = 42

def reverse_dico(dico):
    r_dico = {}
    for item in dico.items():
        r_dico[item[1]] = item[0]
    return r_dico

TIFF_TAGS = """NewSubfileType,254,FE,LONG,1
SubfileType,255,FF,SHORT,1
ImageWidth,256,100,SHORT or LONG,1
ImageLength,257,101,SHORT or LONG,1
BitsPerSample,258,102,SHORT,SamplesPerPixel
Compression,259,103,SHORT,1
PhotometricInterpretation,262,106,SHORT,1
Threshholding,263,107,SHORT,1
CellWidth,264,108,SHORT,1
CellLength,265,109,SHORT,1
FillOrder,266,10A,SHORT,1
DocumentName,269,10D,ASCII
ImageDescription,270,10E,ASCII
Make,271,10F,ASCII
Model,272,110,ASCII
StripOffsets,273,111,SHORT or LONG,StripsPerImage
Orientation,274,112,SHORT,1
SamplesPerPixel,277,115,SHORT,1
RowsPerStrip,278,116,SHORT or LONG,1
StripByteCounts,279,117,LONG or SHORT,StripsPerImage
MinSampleValue,280,118,SHORT,SamplesPerPixel
MaxSampleValue,281,119,SHORT,SamplesPerPixel
XResolution,282,11A,RATIONAL,1
YResolution,283,11B,RATIONAL,1
PlanarConfiguration,284,11C,SHORT,1
PageName,285,11D,ASCII
XPosition,286,11E,RATIONAL
YPosition,287,11F,RATIONAL
FreeOffsets,288,120,LONG
FreeByteCounts,289,121,LONG
GrayResponseUnit,290,122,SHORT,1
GrayResponseCurve,291,123,SHORT,2**BitsPerSample
T4Options,292,124,LONG,1
T6Options,293,125,LONG,1
ResolutionUnit,296,128,SHORT,1
PageNumber,297,129,SHORT,2
TransferFunction,301,12D,SHORT,{1 or SamplesPerPixel}*2** BitsPerSample
Software,305,131,ASCII
DateTime,306,132,ASCII,20
Artist,315,13B,ASCII
HostComputer,316,13C,ASCII
Predictor,317,13D,SHORT,1
WhitePoint,318,13E,RATIONAL,2
PrimaryChromaticities,319,13F,RATIONAL,6
ColorMap,320,140,SHORT,3 * (2**BitsPerSample)
HalftoneHints,321,141,SHORT,2
TileWidth,322,142,SHORT or LONG,1
TileLength,323,143,SHORT or LONG,1
TileOffsets,324,144,LONG,TilesPerImage
TileByteCounts,325,145,SHORT or LONG,TilesPerImage
InkSet,332,14C,SHORT,1
InkNames,333,14D,ASCII,total number of characters in all ink name strings, including zeros
NumberOfInks,334,14E,SHORT,1
DotRange,336,150,BYTE or SHORT,2, or 2*NumberOfInks
TargetPrinter,337,151,ASCII,any
ExtraSamples,338,152,BYTE,number of extra components per pixel
SampleFormat,339,153,SHORT,SamplesPerPixel
SMinSampleValue,340,154,Any,SamplesPerPixel
SMaxSampleValue,341,155,Any,SamplesPerPixel
TransferRange,342,156,SHORT,6
JPEGProc,512,200,SHORT,1
JPEGInterchangeFormat,513,201,LONG,1
JPEGInterchangeFormatLngth,514,202,LONG,1
JPEGRestartInterval,515,203,SHORT,1
JPEGLosslessPredictors,517,205,SHORT,SamplesPerPixel
JPEGPointTransforms,518,206,SHORT,SamplesPerPixel
JPEGQTables,519,207,LONG,SamplesPerPixel
JPEGDCTables,520,208,LONG,SamplesPerPixel
JPEGACTables,521,209,LONG,SamplesPerPixel
YCbCrCoefficients,529,211,RATIONAL,3
YCbCrSubSampling,530,212,SHORT,2
YCbCrPositioning,531,213,SHORT,1
ReferenceBlackWhite,532,214,LONG,2*SamplesPerPixel
Copyright,33432,8298,ASCII,Any"""

BYTE_ORDERS = {LITTLE_ENDIAN:'<', BIG_ENDIAN:'>'}
R_BYTE_ORDERS = reverse_dico(BYTE_ORDERS)

class clsTags(object):
    def __init__(self):
        
        from os import path
        
        self.key2value = dict([(int(x.split(',')[1]), x.split(',')[0]) for x in TIFF_TAGS.split('\n')])
        self.value2key = dict([(x.split(',')[0], int(x.split(',')[1])) for x in TIFF_TAGS.split('\n')])
    
    def __getitem__(self, key):
        try:
            return self.key2value[key]
        except:
            return struct.pack('>H', key)
    
    def key(self, value):
        try:
            return self.value2key[value]
        except:
            return struct.unpack('>H', value)[0]

TAGS = clsTags()

TYPES = {1: 'B', 2: 'c', 3: 'H', 4: 'L', 5: 'R', 11: 'f', 12: 'd'}
R_TYPES = reverse_dico(TYPES)

TYPE_SIZE = {}
TYPE_SIZE['B'] = 1
TYPE_SIZE['c'] = 1
TYPE_SIZE['H'] = 2
TYPE_SIZE['L'] = 4
TYPE_SIZE['f'] = 4
TYPE_SIZE['d'] = 8
TYPE_SIZE['R'] = 8
R_TYPE_SIZE = {}
R_TYPE_SIZE[1] = 'B'
R_TYPE_SIZE[2] = 'H'
R_TYPE_SIZE[4] = 'L'
R_TYPE_SIZE[8] = 'R'

DTYPE = {8: 'u1', 16: 'u2', 32: 'f4'}

FD_OPEN_CLOSE = 0
FD_STAY_OPEN = 1


V_FUNCTIONS = {
    0: 'linear',
    1: 'poly2',
    2: 'poly3',
    3: 'poly4',
    4: 'exp',
    5: 'pow',
    6: 'log',
}

R_V_FUNCTIONS = reverse_dico(V_FUNCTIONS)


class FD:
    ""
    def __init__(self, parent, mode='rb'):
        self.parent = parent
        self.mode = mode
    
    def __enter__(self):
        if self.parent.mode == FD_STAY_OPEN:
            if self.parent._fd == None:
                self.parent._fd = open(self.parent.fname, self.mode)
            elif self.parent._fd.mode != self.mode:
                self.parent._fd.close()
                self.parent._fd = open(self.parent.fname, self.mode)
            self.fd = self.parent._fd
        else:
            self.fd = open(self.parent.fname, self.mode)
        return self.fd
    
    def __exit__(self, type, value, traceback):
        if self.parent.mode == FD_OPEN_CLOSE:
            self.fd.close()


def read_bytes(fd, byteorder, ctype, count=0, as_array=False):
    if count == 0:
        count = 1
        single = True
    else:
        single = False
    ctype2dtype = {'B': 'u1', 'H': 'u2', 'L': 'u4', 'd': 'f8'}
    if ctype == 'c':
        return fd.read(count)
    elif ctype == 'R':
        dtype = np.dtype(byteorder + ctype2dtype['L'])
        denominator, numerator = np.fromfile(fd, dtype, 2).tolist()
        return Fraction(numerator, denominator)
    else:
        dtype = np.dtype(byteorder + ctype2dtype[ctype])
        if single:
            return np.fromfile(fd, dtype, count).tolist()[0]
        else:
            if as_array:
                return np.fromfile(fd, dtype, count)
            else:
                return np.fromfile(fd, dtype, count).tolist()

def write_bytes(fd, byteorder, data):
    ctype2dtype = {'B': 'u1', 'H': 'u2', 'L': 'u4', 'd': 'f8'}
    if type(data) == tuple:
        if data[1] == 'c':
            fd.write(data[0])
        elif data[1] == 'R':
            dtype = np.dtype(byteorder + ctype2dtype['L'])
            np.array([data[0].denominator, data[0].numerator], dtype=dtype).tofile(fd)
        else:
            dtype = np.dtype(byteorder + ctype2dtype[data[1]])
            if type(data[0]) == list:
                np.array(data[0], dtype=dtype).tofile(fd)
            else:
                np.array([data[0]], dtype=dtype).tofile(fd)
    elif type(data) == np.ndarray:
        change_byte_order(data, byteorder).tofile(fd)

def _overwrite(src, i, sub):
    j = i+len(sub)
    return src[:i] + sub + src[j:]

class TIFFError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


class TIFFReader:
    """
    
    Class for opening a tiff file.
    
    :Exemple:
    
    >>> test = readTIFF('test.tif')
    >>> plt.imshow(test.frame(10))
    >>> plt.show()    
    
    """
    
    def __init__(self, fname, mode=FD_STAY_OPEN, rewriteable=False):
        """
        open the tiff file named "fname" and load the metadata for each frames.
        """
        
        self.fname = fname
        self.iscontigus = False
        self.ishuge = False
        self.mode = mode
        self.rewriteable = rewriteable
        self.metadata = {}
        
        self._fd = None
        self._ifds = []
        
        with FD(self) as fd:
            
            self.byteorder = BYTE_ORDERS[fd.read(2)]
            
            if read_bytes(fd, self.byteorder, 'H') != THE_SOLUTION:
                raise TIFFError('This is not a TIFF file.')
            
            while True:
                offset = read_bytes(fd, self.byteorder, 'L')
                if offset == 0:
                    break
                self._ifds.append(self._readIFD(fd, offset))
            
            ifd0 = self._ifds[0]
            
            # dictionnary with all information stored in the description field according ImageJ standard.
            if 'ImageDescription' in ifd0:
                self.description =  dict([tuple(x.split(b'='))  for x in ifd0['ImageDescription'][0][:-2].split(b'\n')])
            else:
                self.description = {}
            
            if len(self._ifds) == 1:
                self.iscontigus = True
                if 'slices' in self.description and int(self.description['slices']) > 1:
                    self.ishuge = True
            
            if not self.iscontigus:
                self.iscontigus = True
                offset_prediction = -1
                
                for ifd in self._ifds:
                    if offset_prediction > 0 and offset_prediction != ifd['StripOffsets'][0]:
                        self.iscontigus = False
                        break
                    offset_prediction = ifd['StripOffsets'][0] + ifd['StripByteCounts'][0]
            
            self.dim_x = ifd0['ImageWidth'][0]
            self.dim_y = ifd0['ImageLength'][0]
            
            if self.ishuge:
                self.dim_z = int(self.description['slices'])
            else:
                self.dim_z = len(self._ifds)
            
            self.shape = (self.dim_z, self.dim_y, self.dim_x)
            
            if 'XResolution' in ifd0 and 'YResolution' in ifd0 and 'spacing' in self.description:
                self.metadata['unit_size'] = (float(ifd0['XResolution'][0]), float(ifd0['YResolution'][0]), float(self.description['spacing'][0]))
            
            if 'unit' in self.description:
                self.metadata['unit'] = self.description['unit']
            
            if 'vunit' in self.description and 'cf' in self.description:
                self.metadata['vunit'] = self.description['vunit']
                self.metadata['vunit_function'] = V_FUNCTIONS[int(self.description['cf'])]
                self.metadata['vunit_coefs'] = []
                c = 0
                while 'c{:d}'.format(c) in self.description:
                    self.metadata['vunit_coefs'].append(float(self.description['c{:d}'.format(c)]))
                    c += 1
            
            if 'min' in self.description and 'max' in self.description:
                self.metadata['display_settings'] = (float(self.description['min']), float(self.description['max']))
            
            if 'xorigin' in self.description and 'yorigin' in self.description:
                if 'zorigin' in self.description:
                    zorigin = float(self.description['zorigin'])
                else:
                    zorigin = 0
                self.metadata['origin'] = (float(self.description['xorigin']), 
                                           float(self.description['yorigin']), zorigin)
            
            if type(ifd0['StripOffsets'][0]) == list:
                self.offset0 = ifd0['StripOffsets'][0][0]
            else:
                self.offset0 = ifd0['StripOffsets'][0]
            _bps = ifd0['BitsPerSample'][0]
            if type(_bps) == int:
                self.dtype = np.dtype(self.byteorder+DTYPE[ifd0['BitsPerSample'][0]])
                self.channels = 1
            else:
                self.dtype = np.dtype(self.byteorder+DTYPE[ifd0['BitsPerSample'][0][0]])
                self.channels = 3
    
    def _readIFD(self, fd, ifd_offset):
        ""
        fd.seek(ifd_offset)
        n_dir_entries = read_bytes(fd, self.byteorder, 'H')
        ifd = {}
        
        for i in range(n_dir_entries):
            
            tag = TAGS[read_bytes(fd, self.byteorder, 'H')]
            ctype = TYPES[read_bytes(fd, self.byteorder, 'H')]
            nvalues = read_bytes(fd, self.byteorder, 'L')
            
            if nvalues == 1 and TYPE_SIZE[ctype] <= 4:
                current_offset = fd.tell()
                values = read_bytes(fd, self.byteorder, ctype)
                fd.seek(current_offset+4)
            else:
                offset = read_bytes(fd, self.byteorder, 'L')
                current_offset = fd.tell()
                fd.seek(offset)
                values = read_bytes(fd, self.byteorder, ctype, nvalues)
                fd.seek(current_offset)
            
            if type(values) == list and len(values) == 1:
                values = values[0]
            ifd[tag] = (values, ctype)
            
        return ifd
    
    def frame(self, n, channels=False):
        """
        get the n-th frame (or the n-th slice in the z direction) from the stack as a numpy array of shape (dim_y, dim_x).
        """
        with FD(self) as fd:
            
            if self.iscontigus:
                offset = self.offset0 + self.dim_y*self.dim_x*self.dtype.itemsize*self.channels*n
            else:
                offset = self._ifds[n]['StripOffsets'][0]
            fd.seek(offset)
            a = np.fromfile(fd, self.dtype, self.dim_y*self.dim_x*self.channels)
            
            if self.channels > 1 or channels:
                return a.reshape(self.dim_y, self.dim_x, self.channels)
            else:
                return a.reshape(self.dim_y, self.dim_x)
    
    slice_z = frame
    
    def slice_y(self, n):
        """
        get the n-th slice in the y direction from the stack as a numpy array of shape (dim_z, dim_x).
        """
        with FD(self) as fd:
            
            a = np.zeros((self.dim_z, self.dim_x, self.channels), dtype=self.dtype)
            
            if self.iscontigus:
                for z in range(self.dim_z):
                    fd.seek(self.offset0+(self.dim_y * self.dim_x * z + self.dim_x * n) * self.dtype.itemsize * self.channels)
                    a[z,:,:].flat = np.fromfile(fd, self.dtype, self.dim_x * self.channels)
            else:
                for z in range(self.dim_z):
                    for x in range(self.dim_x):
                        a[z,x,:] = self.frame(z, True)[n,x,:]
            
            if self.channels > 1:
                return a
            else:
                return a[:,:,0]
    
    def slice_x(self, n):
        """
        get the n-th slice in the x direction from the stack as a numpy array of shape (dim_z, dim_y).
        """
        with FD(self) as fd:
            
            a = np.zeros((self.dim_z, self.dim_y), dtype=self.dtype)
            
            if self.iscontigus:
                for z in range(self.dim_z):
                    for y in range(self.dim_y):
                        fd.seek(self.offset0+(self.dim_y*self.dim_x*z+self.dim_x*y+n)*self.dtype.itemsize*self.channels)
                        a[z,y,:] = np.fromfile(fd, self.dtype, self.channels)
            else:
                for z in range(self.dim_z):
                    for y in range(self.dim_y):
                        a[z,y,:] = self.frame(z, True)[y,n,:]
            
            if self.channels > 1:
                return a
            else:
                return a[:,:,0]
    
    def get_pixel(self, x, y, z):
        """
        return the pixel value at the (x, y, z) coordinate.
        """
        with FD(self) as fd:
            
            if self.iscontigus:
                fd.seek(self.offset0+(self.dim_y*self.dim_x*z+self.dim_x*y+x)*self.dtype.itemsize*self.channels)
                a = np.fromfile(fd, self.dtype, self.channels).tolist()[0]
            else:
                a = self.frame(z, True)[y,x,:]
            
            if self.channels > 1:
                return a
            else:
                return a[0]

    def set_pixel(self, x, y, z, value):
        """
        set the pixel value at the (x, y, z) coordinate.
        TODO: value cannot be RGB
        """
        if self.rewriteable:
            with FD(self, 'rb+') as fd:
                if self.iscontigus:
                    fd.seek(self.offset0+(self.dim_y*self.dim_x*z+self.dim_x*y+x)*self.dtype.itemsize*self.channels)
                else:
                    offset = self._ifds[z]['StripOffsets']
                    fd.seek(offset+(self.dim_x*y+x)*self.dtype.itemsize*self.channels)
                write_bytes(fd, self.byteorder, np.array(value).astype(self.dtype))
    
    def writeFrame(self, n, frame):
        """
        Write the frame at the n position in the z direction.
        n = 0 correspond to the first frame.
        TODO: frame cannot be RGB
        """
        if self.rewriteable:
            with FD(self, 'rb+') as fd:
                if self.iscontigus:
                    fd.seek(self.offset0 + self.dim_y*self.dim_x*self.dtype.itemsize*self.channels*n)
                else:
                    fd.seek(self._ifds[n]['StripOffsets'])
                write_bytes(fd, self.byteorder, frame.astype(self.dtype))
    
    def writeStack(self, stack):
        """
        TODO: stack cannot be RGB
        """
        if self.rewriteable:
            if self.iscontigus and self.dtype.byteorder == '>':
                with FD(self, 'rb+') as fd:
                    fd.seek(self.offset0)
                    write_bytes(fd, self.byteorder, stack.astype(self.dtype))
            else:
                for z in range(stack.shape[0]):
                    self.writeFrame(z, stack[z,:,:])
    
    def get_stack(self):
        """
        get the whole stack as a numpy array of shape (dim_z, dim_y, dim_x)
        """
        with FD(self) as fd:
            
            if self.iscontigus:
                fd.seek(self._ifds[0]['StripOffsets'][0])
                a = np.fromfile(fd, self.dtype, self.dim_x*self.dim_y*self.dim_z*self.channels)
            else:
                a = ''
                for ifd in self._ifds:
                    fd.seek(ifd['StripOffsets'][0])
                    a += fd.read(ifd['StripByteCounts'][0])
                a = np.fromstring(a, self.dtype)
            
            if self.channels > 1:
                return a.reshape(self.shape + (self.channels,))
            else:
                return a.reshape(self.shape)
    
    def close(self):
        """
        close the file descriptor of THE file named "fname".
        """
        if self.mode == FD_STAY_OPEN:
            self._fd.close()

        
class TIFFWriter:
    ""
    def __init__(self, fname, shape, dtype, metadata={}, mode=FD_STAY_OPEN, ifd0=None):
        """
        
        Class for writing 3D tiff file (even huge file with more than 4 GB)
        =================================================
        
        Open a file in writing mode.
        :param fname: filename of the tiff file
        :param shape: shape of the 3D array
        :param dtype: dtype of the array. The data will be cast to this dtype if necessary
        :param mode: use FD_STAY_OPEN if you to close the file once you wrote everything,
        otherwise use FD_OPEN_CLOSE
        
        :Example:
        
        >>> h = TIFFWriter('test.tif', (1000,1000,1000), np.dtype('>u2'), mode=FD_OPEN_CLOSE)
        >>> h.writeFrame(500, np.random.random((1000,1000)).astype('>f4')*100)
        >>> h.writeFrame(750, np.random.random((1000,1000)).astype('>f4')*300)
        >>> h.close()
        
        """
        
        self.mode = mode
        self.fname = fname
        self._fd = None
        self.dtype = np.dtype(dtype)
        if self.dtype.byteorder in le:
            self.byteorder = '<'
        elif self.dtype.byteorder in be:
            self.byteorder = '>'
        else:
            if self.dtype.itemsize == 1:
                self.byteorder = '>'
            else:
                raise
        self.shape = shape
        self.dim_z, self.dim_y, self.dim_x = shape
        self.metadata = metadata
        
        self.ifd_metadata = {
            'BitsPerSample': (self.dtype.itemsize*8, 'H'),
            'ImageLength': (self.dim_y, 'L'),
            'ImageWidth': (self.dim_x, 'L'),
            'NewSubfileType': (0, 'L'),
            'PhotometricInterpretation': (1, 'H'),
            'SampleFormat': ({'u':1, 'f':3}[self.dtype.kind], 'H'),
            'RowsPerStrip': (self.dim_y, 'H'),
            'SamplesPerPixel': (1, 'H'),
            'StripByteCounts': (self.dim_x*self.dim_y*self.dtype.itemsize, 'L')}
        
        ImageDescription = b'ImageJ=1.49h\n'
        ImageDescription += b'images=%d\nslices=%d\nloop=false\n' % (self.dim_z, self.dim_z)
        
        if 'display_settings' in self.metadata:
            ImageDescription += b'min={:f}\nmax={:f}\n'.format(*self.metadata['display_settings'])
        
        if 'unit_size' in self.metadata:
            self.ifd_metadata['XResolution'] = (Fraction(int(self.metadata['unit_size'][0]*10**4), 10**4), 'R')
            self.ifd_metadata['YResolution'] = (Fraction(int(self.metadata['unit_size'][1]*10**4), 10**4), 'R')
            ImageDescription += b'spacing={:f}\n'.format(self.metadata['unit_size'][2])
        
        if 'unit' in self.metadata:
            ImageDescription += b'unit={}\n'.format(self.metadata['unit'])
        
        if 'vunit_function' in self.metadata:
            ImageDescription += b'vunit={}\n'.format(self.metadata['vunit'])
            ImageDescription += b'cf={:d}\n'.format(R_V_FUNCTIONS[self.metadata['vunit_function']])
            for (i, v) in enumerate(self.metadata['vunit_coefs']):
                ImageDescription += b'c{:d}={:f}\n'.format(i, v)
        
        if 'origin' in self.metadata:
            ImageDescription += b'xorigin={}\nyorigin={}\nzorigin={}\n'.format(*self.metadata['origin'])
        
        self.ifd_metadata['ImageDescription'] = (ImageDescription + b'\x00', 'c')
        
        if ifd0 != None:
            for key in ifd0:
                if key not in ['RowsPerStrip', 'StripOffsets', 'StripByteCounts']:
                    self.ifd_metadata[key] = ifd0[key]
        
        n_metadata = len(self.ifd_metadata)+1
        
        len_head = 4
        len_offset = 4
        len_ifd = 2 + n_metadata*12 + 4
        len_ifd_strips = [0]
        len_frame = self.dim_y*self.dim_x*self.dtype.itemsize
        
        with FD(self, 'wb') as fd:
            
            fd.write(R_BYTE_ORDERS[self.byteorder])
            fd.write(struct.pack(self.byteorder+'H', THE_SOLUTION))
            fd.write(struct.pack(self.byteorder+'L', len_head+len_offset)) # premier offset
            
            ifd = b''
            ifd_strips = []
            ifd += struct.pack(self.byteorder+'H', n_metadata)
            
            for key in self.ifd_metadata:
                
                ifd += struct.pack(self.byteorder+'H', TAGS.key(key))
                values, ctype = self.ifd_metadata[key]
                if ctype == 'c' or type(values) == list:
                    nvalues = len(values)
                else:
                    nvalues = 1
                ifd += struct.pack(self.byteorder+'H', R_TYPES[ctype])
                
                if nvalues == 1 and ctype != 'R':
                    ifd += struct.pack(self.byteorder+'L'+ctype, nvalues, values)
                    if ctype == 'B':
                        ifd += b'\x00\x00\x00'
                    elif ctype == 'H':
                        ifd += b'\x00\x00'
                else:
                    ifd += struct.pack(self.byteorder+'L', nvalues)
                    ifd += b'\x00\x00\x00\x00'
                    if ctype == 'c':
                        v = values
                    elif ctype == 'R':
                        v = struct.pack(self.byteorder+'LL', values.denominator, values.numerator)
                    else:
                        v = struct.pack(self.byteorder+ctype*nvalues, *values)
                    i, j = len(ifd)-4, len(ifd)
                    len_ifd_strips.append(len(v))
                    ifd_strips.append((i,v))
            
            ifd_f = ifd + struct.pack(self.byteorder+'H', TAGS.key('StripOffsets')) + \
                struct.pack(self.byteorder+'H', R_TYPES['L']) + b'\x00\x00\x00\x01' + \
                struct.pack(self.byteorder+'L', len_head+len_offset+len_ifd+sum(len_ifd_strips))
            
            len_ifd_tot = len(ifd_f) + 4 + sum(len_ifd_strips)
            
            self.ishuge = 8 + self.dim_z*(self.dim_y*self.dim_x*self.dtype.itemsize + len_ifd_tot) > 2**32-1
            
            if self.dim_z == 1 or self.ishuge:
                next_frame_offset = b'\x00\x00\x00\x00'
            else:
                next_frame_offset = struct.pack(self.byteorder+'L', 
                                            len_head+len_offset+len_ifd+sum(len_ifd_strips)+len_frame*self.dim_z)
            
            ifd_f += next_frame_offset + b''.join([x[1] for x in ifd_strips])
            
            for n, strip in enumerate(ifd_strips):
                i, v = strip
                ifd_f = _overwrite(ifd_f, i, struct.pack(self.byteorder+'L', 
                                len_head+len_offset+len_ifd+sum(len_ifd_strips[:n+1])))
            
            fd.write(ifd_f)
            
            self.offset0 = fd.tell()
            
            fd.seek(self.offset0 + self.dim_z*self.dim_y*self.dim_x*self.dtype.itemsize)
            
            if not self.ishuge:
                for f in range(1, self.dim_z):
                    ifd_f = ifd + struct.pack(self.byteorder+'H', TAGS.key('StripOffsets')) + \
                        struct.pack(self.byteorder+'H', R_TYPES['L']) + b'\x00\x00\x00\x01' + \
                        struct.pack(self.byteorder+'L', len_head+len_offset+len_ifd+sum(len_ifd_strips)+len_frame*f)
                    
                    o = len_head+len_offset+len_frame*self.dim_z+(len_ifd)*(f+1)+sum(len_ifd_strips)*f
                    
                    if f < self.dim_z-1:
                        next_frame_offset = struct.pack(self.byteorder+'L', \
                            len_head+len_offset+len_frame*self.dim_z+(len_ifd+sum(len_ifd_strips))*(f+1))
                    else:
                        next_frame_offset = b'\x00\x00\x00\x00'
                    
                    ifd_f += next_frame_offset + b''.join([x[1] for x in ifd_strips])
                    
                    for n, strip in enumerate(ifd_strips):
                        i, v = strip
                        ifd_f = _overwrite(ifd_f, i, struct.pack(self.byteorder+'L', o+len_ifd_strips[n]))
                    
                    fd.write(ifd_f)
            else:
                fd.seek(fd.tell()-1)
                fd.write('\x00')
            
            fd.flush()
        
    def writeFrame(self, n, frame):
        """
        Write the frame at the n position in the z direction.
        n = 0 correspond to the first frame.
        """
        with FD(self, 'rb+') as fd:
            fd.seek(self.offset0 + self.dim_y*self.dim_x*self.dtype.itemsize*n)
            frame.astype(self.dtype).tofile(fd)
        
    def writeStack(self, stack):
        """
        
        """
        with FD(self, 'rb+') as fd:
            fd.seek(self.offset0)
            stack.astype(self.dtype).tofile(fd)

    def set_pixel(self, x, y, z, value):
        """
        set the pixel value at the (x, y, z) coordinate.
        """
        with FD(self, 'rb+') as fd:
            fd.seek(self.offset0+(self.dim_y*self.dim_x*z+self.dim_x*y+x)*self.dtype.itemsize)
            np.array(value).astype(self.dtype).tofile(fd)
        
    def close(self):
        """
        Close the tiff file.
        """
        if self.mode == FD_STAY_OPEN:
            self._fd.close()

class ZeissItem:
    
    def __init__(self, c, v, u):
        self.comment = c
        self.unit = u
        self.value = v
    
    def __repr__(self):
        if self.unit is not None:
            return "%s %s (%s)" % (self.value, self.unit, self.comment)
        elif self.value is not None:
            return "%s (%s)" % (self.value, self.comment)
        else:
            return "[None] (%s)" % (self.comment)
    
    def __call__(self):
        return self.value

class Zeiss:
    
    def __init__(self, fname):
        
        tf = TIFFReader(fname)
        
        md = tf._ifds[0][b'\x85F'][0].split(b'\x00')[0].decode('latin1').strip()
        
        mdt = md.split('\r\n')[35:]
        
        self._md = [
            ('WIDTH', 'largeur en pixels', tf.shape[-1], 'px'), 
            ('HEIGHT', 'hauteur en pixels', tf.shape[-2], 'px'),
            ('COLOR_DEPTH', 'niveaux de gris', 256**tf.dtype.itemsize, None),
        ]
        
        for i in range(len(mdt)//2):
            try:
                c, v = mdt[i*2+1].split(' = ')
            except:
                c = mdt[i*2+1]
                v = None
                u = None
            else:
                v = v.strip().split()
                if len(v) <= 1:
                    try:
                        v = v[0]
                    except:
                        v = None
                    u = None
                else:
                    u = v[-1]
                    v = ' '.join(v[:-1])
                if u not in ['mm', 'nm', '°', 'mbar', 'Pa', 'X', 'V', '%', 'µm', 'kV', 'A', '°C', None]:
                    v = v + u
                    u = None
                try:
                    v = int(v)
                except:
                    try:
                        v = float(v)
                    except:
                        pass
            
            self._md.append((mdt[i*2], c, v, u))
        
        for k, c, v, u in self._md:
            self.__dict__[k] = ZeissItem(c, v, u)
    
    def __repr__(self):
        return '\n'.join(["%s: %s" % (k, repr(self.__dict__[k])) for k, _, _, _ in self._md])

def big_dtype(d):
    d = np.dtype(d)
    return '>%s%d' % (d.kind, d.itemsize)

def little_dtype(d):
    d = np.dtype(d)
    return '<%s%d' % (d.kind, d.itemsize)

def big(a):
    if np.dtype(a.dtype).byteorder in be:
        return a
    else:
        return a.astype(big_dtype(a.dtype))

def little(a):
    if np.dtype(a.dtype).byteorder in le:
        return a
    else:
        return a.astype(little_dtype(a.dtype))

def writeTIFF(fname, vol, metadata={}, **kwargs):
    ""
    if vol.ndim == 2:
        vol = np.array([vol])
    
    writer = TIFFWriter(fname, vol.shape, big_dtype(vol.dtype), metadata, **kwargs)
    writer.writeStack(little(vol))
    writer.close()

def readTIFF(fname):
    ""
    reader = TIFFReader(fname)
    if reader.dim_z > 1:
        return as_little(reader.get_stack())
    else:
        return as_little(reader.frame(0))

def readTIFF_metadata(fname):
    ""
    reader = TIFFReader(fname)
    return reader.metadata

def readZeissMD(fname):
    """
    >>> zmd = readZeissMD(fname)
    >>> zmd
    WIDTH: 2048 px (largeur en pixels)
    HEIGHT: 1536 px (hauteur en pixels)
    COLOR_DEPTH: 256 (niveaux de gris)
    DP_ZOOM: Off (Zoom)
    DP_OUT_DEV: Ecran 19/21pouces (Périphérique)
    AP_TILT_ANGLE: 70.0 ° (Angle d'inclinaison)
    AP_STAGE_AT_X: 56.1915 mm (Platine: position X)
    ...
    >>> zmd.AP_PIXEL_SIZE
    223.4 nm (Dimension Pixel)
    >>> zmd.AP_PIXEL_SIZE()
    223.4
    >>> zmd.AP_PIXEL_SIZE.unit
    'nm'
    """
    return Zeiss(fname)
        
