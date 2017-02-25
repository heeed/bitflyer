#!/usr/bin/env python3
import os
import sys

from PIL import Image

def to_row_col(img):
    out = b''
    for row in range(8):
        for col in range(128):
            val = 0
            for i in range(8):
                pixel = img.getpixel((col, (8*row) + i))
                val |= pixel << i
            out += chr(val).encode('latin-1')
    return out

def compress(row):
    out = b''
    cur_char = None
    group_count = 0
    def end_group():
        nonlocal group_count, out, cur_char
        if group_count == -1:
            out += b'\x81' + cur_char
        else:
            out += chr(group_count).encode('latin-1')
            out += cur_char
        cur_char = None
        group_count = 0

    for char in row:
        char = chr(char).encode('latin-1')
        if cur_char is None:
            cur_char = char
        if char == cur_char:
            group_count += 1
            if group_count >= 255:
                die
                end_group()
        else:
            end_group()
            cur_char = char
            group_count = 1
    end_group()
    return out


def main(dirname):
    for name in os.listdir(dirname):
        basename, _ = os.path.splitext(name)
        path = os.path.join(dirname, name)
        img = Image.open(path)
        assert img.width == 128
        assert img.height == 64
        out = compress(to_row_col(img))
        print("%s = %r" % (basename, out))
        print


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
