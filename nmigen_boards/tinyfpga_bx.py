import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["TinyFPGABXPlatform"]


class TinyFPGABXPlatform(LatticeICE40Platform):
    device      = "iCE40LP8K"
    package     = "CM81"
    default_clk = "clk16"
    resources   = [
        Resource("clk16", 0, Pins("B2", dir="i"),
                 Clock(16e6), Attrs(IO_STANDARD="SB_LVCMOS")),

        *LEDResources(pins="B3", attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        DirectUSBResource(0, d_p="B4", d_n="A4", pullup="A3",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),

        *SPIFlashResources(0,
            cs="F7", clk="G7", copi="G6", cipo="H7", wp="H4", hold="J8",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    connectors  = [
        Connector("gpio", 0,
            # Left side of the board
            #     1  2  3  4  5  6  7  8  9 10 11 12 13
             "   A2 A1 B1 C2 C1 D2 D1 E2 E1 G2 H1 J1 H2 "
            # Right side of the board
            #          14 15 16 17 18 19 20 21 22 23 24
             "         H9 D9 D8 C9 A9 B8 A8 B7 A7 B6 A6 "
            # Bottom of the board
            # 25 26 27 28 29 30 31
             "G1 J3 J4 G9 J9 E8 J2"
        ),
    ]

    def toolchain_program(self, products, name):
        tinyprog = os.environ.get("TINYPROG", "tinyprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([tinyprog, "-p", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    TinyFPGABXPlatform().build(Blinky(), do_program=True)
