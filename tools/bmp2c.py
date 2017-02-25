#!/usr/bin/env python3
import os
import sys

from PIL import Image

def to_c(img):
    out = []
    for row in range(img.height // 8):
        for col in range(img.width):
            val = 0
            for i in range(8):
                pixel = img.getpixel((col, (8*row) + i))
                val |= pixel << i
            out.append(hex(val))
    return out


def main(filename, name):
    img = Image.open(filename)
    assert img.height % 8 == 0
    parts = to_c(img)
    print("unsigned char %s[] = {%s}" % (name, ",".join(parts)))
    print


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
