import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["FomuPVTPlatform"]


class FomuPVTPlatform(LatticeICE40Platform):
    device      = "iCE40UP5K"
    package     = "UWG30"
    default_clk = "clk48"
    resources   = [
        Resource("clk48", 0, Pins("F4", dir="i"),
                 Clock(48e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        *LEDResources(pins="A5", invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        RGBLEDResource(0,
            r="B5", g="A5", b="C5", invert=True,
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),

        Resource("usb", 0,
            Subsignal("d_p", Pins("A1")),
            Subsignal("d_n", Pins("A2")),
            Subsignal("pullup", Pins("A4")),
            Attrs(IO_STANDARD="SB_LVCMOS"),
        ),

        *SPIFlashResources(0,
            cs="C1", clk="D1", mosi="F1", miso="E1",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS"),
        ),

        Resource("touch", 0, Pins("E4")),
        Resource("touch", 1, Pins("D5")),
        Resource("touch", 2, Pins("E5")),
        Resource("touch", 3, Pins("F5")),
    ]

    connectors = []

    def toolchain_program(self, products, name):
        dfu_util = os.environ.get("DFU_UTIL", "dfu-util")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([dfu_util, "-D", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    FomuPVTPlatform().build(Blinky(), do_program=True)
