import os
import subprocess

from amaranth.build import *
from amaranth.vendor.gowin import *
from .resources import *


__all__ = ["TangNano9kPlatform"]


class TangNano9kPlatform(GowinPlatform):
    device      = "GW1N-9C"
    family      = "GW1NR"
    voltage     = "LV"
    size        = "9"
    package     = "QN88P"
    speed       = "C6/I5"
    default_clk = "clk27"
    board       = "tangnano9k"
    resources   = [
        Resource("clk27", 0, Pins("52", dir="i"),
                 Clock(27e6), Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins="10 11 12 13 14 15 16",
                      attrs=Attrs(IO_TYPE="LVCMOS33")),

        *SPIFlashResources(0,
            cs_n="60", clk="59", copi="61", cipo="62",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),
    ]
    connectors  = [
        Connector("gpio", 0,
                  # When viewed from top (FPGA-side up), from USB to HDMI
                  # top row
                  #                                                   5V
                  "63 86 85 84 83 82 81 80 79 77 76 75 74 73 72 71 70  -"
                  #           GND 3V3
                  "48 49 31 32  -  -"
                  # bottom row
                  "38 37 36 39 25 26 27 28 29 30 33 34 40 35 41 42 51 53"
                  "54 55 56 57 68 69"
        ),
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.fs".format(name)) as bitstream_filename:
            subprocess.check_call(["openFPGALoader",
                                   "-b",
                                   self.board,
                                   bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    TangNano9kPlatform().build(Blinky(), do_program=True)
