#!/usr/bin/env python3

# This scripts calculates the checksum of a file.
# All checksums are listed in the "checksum" file in the "update" directory.
# The checksum is equal to SHA512(file_content || version1 || version2)
# where "version1" and "version2" are the first two parts of "ro.build.product"
#
# Example:
#   ro.build.product=OSEV.EUR.0000.V126.220421, version1=OSEV, version2=EUR
#   ro.build.product=TLFL.EUR.0000.V126.220421, version1=TLFL, version2=EUR
#   ro.build.product=CK19.CAN.0000.V133.221006, version1=CK19, version2=CAN
# and so on.
import sys
import hashlib

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: {} <ver1> <ver2> <file>".format(sys.argv[0]))
        sys.exit(1)
    ver1 = sys.argv[1]
    ver2 = sys.argv[2]
    fname = sys.argv[3]
    # create a hash object
    h = hashlib.sha512()
    # open file for reading in binary mode
    with open(fname, "rb") as f:
        h.update(f.read())
    h.update(ver1.encode('ascii'))
    h.update(ver2.encode('ascii'))
    print(h.hexdigest().upper())
