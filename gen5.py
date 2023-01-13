#!/usr/bin/env python3
import os
import sys
import zlib
import argparse
from Cryptodome.Cipher import AES

AES_KEY = b')1Zorxo^fAhGlh$#'
AES_IV = b'aoAkfwk+#1.6G{dE'

FW_FILES = [('lk.rom', 0x00),
            ('boot.img', 0x4000),
            ('system.img', 0x1004000),
            ('recovery.img', 0x3f00c000),
            ('splash.img', 0x40010000)]

# The structure of the encrypted files is as follows:
# 4 bytes: decrypted file size
# 8 bytes: offset
# remaining bytes: AES-128-CBC encrypted data split into 4KB chunks
FW_ENC_FILES = ['encrypt_lk.rom', 'encrypt_boot.img', 'encrypt_system.img', 'encrypt_recovery.img', 'encrypt_splash.img', 'encrypt_partition.dat']

def read_exactly(f, num_bytes):
    ret = b''
    while len(ret) < num_bytes:
        data = f.read(num_bytes - len(ret))
        if not data:
            raise Exception('Unexpected end of file')
        ret += data
    return ret

def encrypt_file(in_file, offset, out_file):
    file_size = os.path.getsize(in_file)
    num_chunks = file_size // 0x1000
    inf = open(in_file, 'rb')
    outf = open(out_file, 'wb')
    outf.write(file_size.to_bytes(4, byteorder='little'))
    outf.write(offset.to_bytes(8, byteorder='little'))
    for i in range(num_chunks):
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        data = read_exactly(inf, 0x1000)
        outf.write(cipher.encrypt(data))
    remainder = file_size % 0x1000
    if remainder > 0:
        data = read_exactly(inf, remainder)
        if remainder % 16 != 0:
            # pad with zeroes to make it a multiple of 16
            data += b'\x00' * (16 - remainder % 16)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        outf.write(cipher.encrypt(data))
    outf.close()
    inf.close()

def crc32_file(in_file):
    prev = 0
    with open(in_file, 'rb') as f:
        while True:
            s = f.read(4096)
            if not s:
                break
            prev = zlib.crc32(s, prev)
    return prev

def create_file_info(out_basepath):
    out_file = os.path.join(out_basepath, 'file_info')
    outf = open(out_file, 'wb')
    for f in FW_ENC_FILES:
        outf.write(f.encode('ascii'))
        outf.write((32 - len(f)) * b'\x00')
        curr_file = os.path.join(out_basepath, f)
        file_size = os.path.getsize(curr_file)
        outf.write(file_size.to_bytes(4, byteorder='little'))
        crc32 = crc32_file(curr_file)
        outf.write(crc32.to_bytes(4, byteorder='little'))
    outf.close()

def encrypt(in_basepath, out_basepath):
    print('Encrypting files in {}'.format(in_basepath))
    for f, offset in FW_FILES:
        curr_in_file = os.path.join(in_basepath, f)
        if not os.path.exists(curr_in_file):
            print('File ' + curr_in_file + ' does not exist, skipping')
            continue
        out_file = 'encrypt_' + f
        curr_out_file = os.path.join(out_basepath, out_file)
        if os.path.exists(curr_out_file):
            print('File ' + curr_out_file + ' already exists. Overwrite? (y/n)')
            if input() != 'y':
                continue
        print('Encrypting ' + curr_in_file + ' to ' + curr_out_file)
        encrypt_file(curr_in_file, offset, curr_out_file)
    script_base = os.path.dirname(os.path.abspath(__file__))
    partition_dat = os.path.join(script_base, 'partition.dat')
    curr_out_file = os.path.join(out_basepath, 'encrypt_partition.dat')
    print('Encrypting ' + partition_dat + ' to ' + curr_out_file)
    encrypt_file(partition_dat, 0, curr_out_file)
    print('Creating file_info')
    create_file_info(out_basepath)

def decrypt_file(in_file, out_file):
    enc_file_size = os.path.getsize(in_file)
    inf = open(in_file, 'rb')
    dec_file_size = inf.read(4)
    dec_file_size = int.from_bytes(dec_file_size, byteorder='little')
    # Skip 8 bytes
    _ = inf.read(8)
    pad_size = 0
    if dec_file_size % 16 != 0:
        pad_size = 16 - dec_file_size % 16
    if enc_file_size != dec_file_size + pad_size + 12:
        raise Exception('File size mismatch')
    outf = open(out_file, 'wb')
    num_chunks = (enc_file_size - 12) // 0x1000
    for i in range(num_chunks):
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        data = inf.read(0x1000)
        outf.write(cipher.decrypt(data))
    remainder = (enc_file_size - 12) % 0x1000
    if remainder > 0:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        data = read_exactly(inf, remainder)
        outf.write(cipher.decrypt(data))
    inf.close()
    # truncate to strip the padding bytes if any
    outf.truncate(dec_file_size)
    outf.close()

def decrypt(in_basepath, out_basepath):
    print('Decrypting files in {}'.format(in_basepath))
    for f in FW_ENC_FILES:
        curr_in_file = os.path.join(in_basepath, f)
        if not os.path.exists(curr_in_file):
            print('File ' + curr_in_file + ' does not exist, skipping')
            continue
        out_file = f.split('_')[1]
        curr_out_file = os.path.join(out_basepath, out_file)
        if os.path.exists(curr_out_file):
            print('File ' + curr_out_file + ' already exists. Overwrite? (y/n)')
            if input() != 'y':
                continue
        print('Decrypting ' + curr_in_file + ' to ' + curr_out_file)
        decrypt_file(curr_in_file, curr_out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')
    parser_enc = subparsers.add_parser('encrypt', help='encrypt files')
    parser_enc.add_argument('in_dir',type=str, help='input directory with files to encrypt')
    parser_enc.add_argument('out_dir',type=str, help='output directory')

    parser_dec = subparsers.add_parser('decrypt', help='decrypt files')
    parser_dec.add_argument('in_dir', type=str, help='input directory with files to decrypt')
    parser_dec.add_argument('out_dir', type=str, help='output directory')
    args = parser.parse_args()

    if not os.path.exists(args.in_dir):
        print('Input directory does not exist')
        sys.exit(1)
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    if (args.cmd == 'encrypt'):
        encrypt(args.in_dir, args.out_dir)
    elif (args.cmd == 'decrypt'):
        decrypt(args.in_dir, args.out_dir)
