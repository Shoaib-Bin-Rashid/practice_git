#!/usr/bin/env python3
"""
reverse_tools.py
Simple, safe helper tools for learning reverse-engineering:
- hexdump
- extract printable strings
- simple XOR decode + brute-force for short single-byte keys

Usage examples:
  python3 reverse_tools.py hexdump somefile.bin
  python3 reverse_tools.py strings somefile.bin
  python3 reverse_tools.py xor-decode somefile.bin 0x4f  > decoded.bin
  python3 reverse_tools.py xor-bruteforce somefile.bin  # tries single-byte keys
"""

import sys
import os
import argparse
from binascii import hexlify

def hexdump(data, width=16):
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hexpart = ' '.join(f"{b:02x}" for b in chunk)
        text = ''.join((chr(b) if 32 <= b < 127 else '.') for b in chunk)
        print(f"{i:08x}  {hexpart:<{width*3}}  |{text}|")

def extract_strings(data, min_len=4):
    out = []
    cur = []
    for b in data:
        if 32 <= b < 127:
            cur.append(chr(b))
        else:
            if len(cur) >= min_len:
                out.append(''.join(cur))
            cur = []
    if len(cur) >= min_len:
        out.append(''.join(cur))
    return out

def xor_decode(data, key):
    return bytes((b ^ key) for b in data)

def xor_bruteforce_print(data, sample_len=64):
    # Try all single-byte keys, print first printable portion
    for key in range(256):
        dec = xor_decode(data, key)
        strings = extract_strings(dec, min_len=4)
        if strings:
            print(f"key=0x{key:02x} -> possible strings: {strings[:5]}")

def main():
    parser = argparse.ArgumentParser(description="Small reverse-engineering helper tools")
    sub = parser.add_subparsers(dest='cmd')

    p_hd = sub.add_parser('hexdump')
    p_hd.add_argument('file')

    p_str = sub.add_parser('strings')
    p_str.add_argument('file')
    p_str.add_argument('--min', type=int, default=4)

    p_xd = sub.add_parser('xor-decode')
    p_xd.add_argument('file')
    p_xd.add_argument('key', help='single byte key as decimal or 0xNN hex', type=str)
    p_xd.add_argument('-o','--out', help='output file (optional)', default=None)

    p_xb = sub.add_parser('xor-bruteforce')
    p_xb.add_argument('file')

    args = parser.parse_args()
    if args.cmd is None:
        parser.print_help()
        sys.exit(1)

    if not os.path.isfile(args.file):
        print("File not found:", args.file)
        sys.exit(2)

    with open(args.file, 'rb') as f:
        data = f.read()

    if args.cmd == 'hexdump':
        hexdump(data)
    elif args.cmd == 'strings':
        for s in extract_strings(data, min_len=args.min):
            print(s)
    elif args.cmd == 'xor-decode':
        k = args.key
        key = int(k, 0)  # handles '0x..' or decimal
        dec = xor_decode(data, key)
        if args.out:
            with open(args.out, 'wb') as out:
                out.write(dec)
            print("Wrote decoded output to", args.out)
        else:
            # print first few lines (as text) if printable
            try:
                print(dec.decode('utf-8', errors='replace')[:2000])
            except Exception:
                print("Decoded (binary) length:", len(dec))
    elif args.cmd == 'xor-bruteforce':
        xor_bruteforce_print(data)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

