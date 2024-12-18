import struct


def pack(arraylist):
    buf = struct.pack('%sf' % len(arraylist), *arraylist)

    return buf


def unpack(buf):
    arraylist = list(struct.unpack('%sf' % int(len(buf)/4), buf));

    return arraylist
