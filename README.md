Bitflyer for Micropython for the BBC micro:bit
=================================

https://medium.com/@stestagg/the-first-video-game-on-the-bbc-micro-bit-probably-4175fab44da8

This is the source code and build tools for bitflyer, a simple game for the micro:bit.

It relies on an I2C 0.96" oled display.

Game python code is embedded in a custom micropython build (hence all the build tooling), along with the image data.

There is a Makefile which knows how to build the final file (that can be copied onto the microbit as usual (drag-drop into the root when plugged-in in mass-storage mode)).

```
make build/final.hex 
```
should produce a file called build/final.hex which is the firmware

** NOTE ** - This is highly unlikely to work out-of-the box.  The toolchain is extremely complex, and relies on many components from many vendors.  There are IP/licensing issues that prevent me from making this too much easier.


MicroPython for the BBC micro:bit
=================================

This is the source code for MicroPython running on the BBC micro:bit!

To get involved with the community subscribe to the microbit@python.org
mailing list (https://mail.python.org/mailman/listinfo/microbit). You need to
be a member to post messages.

Various things are in this repository, including:
- Source code in source/ and inc/ directories.
- Example Python programs in the examples/ directory.
- Tools in the tools/ directory.

The source code is a yotta application and needs yotta to build, along
with an ARM compiler toolchain (eg arm-none-eabi-gcc and friends).

Ubuntu users can install the needed packages using:
```
sudo add-apt-repository -y ppa:terry.guo/gcc-arm-embedded
sudo add-apt-repository -y ppa:pmiller-opensource/ppa
sudo apt-get update
sudo apt-get install cmake ninja-build gcc-arm-none-eabi srecord
pip3 install yotta
```

Once all packages are installed, use yotta to build.

- Use target bbc-microbit-classic-gcc-nosd:

  ```
  yt target bbc-microbit-classic-gcc-nosd
  ```

- Run yotta update to fetch remote assets:

  ```
  yt up
  ```

- Start the build:

  ```
  yt build
  ```

The resulting microbit-micropython.hex file to flash onto the device can be
found in the build/bbc-microbit-classic-gcc-nosd/source from the root of the
repository.

There is a Makefile provided that does some extra preprocessing of the source,
which is needed only if you add new interned strings to qstrdefsport.h.  The
Makefile also puts the resulting firmware at build/firmware.hex, and includes
some convenience targets.

How to use
==========

Upon reset you will have a REPL on the USB CDC serial port, with baudrate
115200 (eg picocom /dev/ttyACM0 -b 115200).

Then try:

    >>> import microbit
    >>> microbit.display.scroll('hello!')
    >>> microbit.random(100)

Tab completion works and is very useful!

Read our documentation here:

http://microbit-micropython.readthedocs.org/en/latest/

You can also use the tools/pyboard.py script to run Python scripts directly
from your PC, eg:

    $ ./tools/pyboard.py /dev/ttyACM0 examples/conway.py

Be brave! Break things! Learn and have fun!
