#!/usr/bin/env python3

# This scripts calculates CRC32 and SHA512 checksums of a file.
#
# CRC32 checksums are listed in the ".ver" file in the root directory
# of the update package.
#
# SHA512 checksums are listed in the "checksum" file in the "update" directory.
# The SHA512 checksum is equal to SHA512(file_content || version1 || version2)
# where "version1" and "version2" are the first two parts of "ro.build.product"
#
# Example:
#   ro.build.product=OSEV.EUR.0000.V126.220421, version1=OSEV, version2=EUR
#   ro.build.product=TLFL.EUR.0000.V126.220421, version1=TLFL, version2=EUR
#   ro.build.product=CK19.CAN.0000.V133.221006, version1=CK19, version2=CAN
# and so on.
import sys
import struct
import hashlib
import zlib

def crc32_file(in_file):
    prev = 0
    with open(in_file, 'rb') as f:
        while True:
            s = f.read(4096)
            if not s:
                break
            prev = zlib.crc32(s, prev)
    return prev

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <file> [ver1] [ver2]".format(sys.argv[0]))
        sys.exit(1)
    fname = sys.argv[1]
    crc32 = crc32_file(fname)
    # convert crc32 to signed 32bit int
    crc32 = struct.unpack('i', struct.pack('I', crc32))[0]
    print("CRC32 checksum: {}".format(crc32))
    if (len(sys.argv) == 4):
        ver1 = sys.argv[2]
        ver2 = sys.argv[3]
        # create a hash object
        h = hashlib.sha512()
        # open file for reading in binary mode
        with open(fname, "rb") as f:
            h.update(f.read())
        h.update(ver1.encode('ascii'))
        h.update(ver2.encode('ascii'))
        print("SHA512 checksum: {}".format(h.hexdigest().upper()))
