import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .dev import *


__all__ = ["ICE40HX1KBlinkEVNPlatform"]


class ICE40HX1KBlinkEVNPlatform(LatticeICE40Platform):
    device      = "iCE40HX1K"
    package     = "VQ100"
    default_clk = "clk3p3"
    resources   = [
        Resource("clk3p3", 0, Pins("13", dir="i"), Clock(3.3e6),
                 Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        *LEDResources(pins="59 56 53 51", attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        Resource("touch", 0, Pins("60"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("touch", 1, Pins("57"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("touch", 2, Pins("54"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("touch", 3, Pins("52"), Attrs(IO_STANDARD="SB_LVCMOS")),

        *SPIFlashResources(0,
            cs="49", clk="48", mosi="45", miso="46",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    connectors  = [
        Connector("pmod",  1, "10  9  8  7 - -  4  3  2  1 - -"), # J1
        Connector("pmod",  5, "40 42 62 64 - - 37 41 63 45 - -"), # J5
        Connector("pmod",  6, "25 24 21 20 - - 26 27 28 33 - -"), # J6
        Connector("pmod", 11, "49 45 46 48 - -"), # J11
        Connector("pmod", 12, "59 56 53 51 - -"), # J12
    ]

    def toolchain_program(self, products, name):
        iceburn = os.environ.get("ICEBURN", "iCEburn")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([iceburn, "-evw", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    ICE40HX1KBlinkEVNPlatform().build(Blinky(), do_program=True)
