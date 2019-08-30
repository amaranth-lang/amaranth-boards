import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .dev import *


__all__ = ["FomuHackerPlatform"]


class FomuHackerPlatform(LatticeICE40Platform):
    device      = "iCE40UP5K"
    package     = "UWG30"
    default_clk = "clk48"
    resources   = [
        Resource("clk48", 0, Pins("F5", dir="i"),
                 Clock(48e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS33")),

        Resource("user_led", 0, PinsN("A5", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("rgb_led", 0,
            Subsignal("r", PinsN("C5")),
            Subsignal("g", PinsN("B5")),
            Subsignal("b", PinsN("A5")),
            Attrs(IO_STANDARD="SB_LVCMOS33"),
        ),

        Resource("usb", 0,
            Subsignal("d_p", Pins("A4")),
            Subsignal("d_n", Pins("A2")),
            Subsignal("pullup", Pins("D5")),
            Attrs(IO_STANDARD="SB_LVCMOS33"),
        ),

        *SPIFlashResources(0,
            cs="C1", clk="D1", mosi="F1", miso="E1",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS33"),
        ),
    ]

    connectors = [
        Connector("pin", 0, "F4"),
        Connector("pin", 1, "E5"),
        Connector("pin", 2, "E4"),
        Connector("pin", 3, "F2"),
    ]

    def toolchain_program(self, products, name):
        dfu_util = os.environ.get("DFU_UTIL", "dfu-util")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([dfu_util, "-D", bitstream_filename])


if __name__ == "__main__":
    from ._blinky import Blinky
    FomuHackerPlatform().build(Blinky(), do_program=True)
