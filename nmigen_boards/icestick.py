import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .dev import *


__all__ = ["ICEStickPlatform"]


class ICEStickPlatform(LatticeICE40Platform):
    device     = "iCE40HX1K"
    package    = "TQ144"
    resources  = [
        Resource("clk12", 0, Pins("21", dir="i"),
                 Clock(12e6), Attrs(GLOBAL="1", IO_STANDARD="SB_LVCMOS33")),

        Resource("user_led", 0, Pins("99", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_led", 1, Pins("98", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_led", 2, Pins("97", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_led", 3, Pins("96", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_led", 4, Pins("95", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),

        Resource("serial", 0,
            Subsignal("rx",  Pins("9", dir="i")),
            Subsignal("tx",  Pins("8", dir="o")),
            Subsignal("rts", Pins("7", dir="o")),
            Subsignal("cts", Pins("4", dir="i")),
            Subsignal("dtr", Pins("3", dir="o")),
            Subsignal("dsr", Pins("2", dir="i")),
            Subsignal("dcd", Pins("1", dir="i")),
            Attrs(IO_STANDARD="SB_LVTTL", PULLUP="1")
        ),

        Resource("irda", 0,
            Subsignal("rx", Pins("106", dir="i")),
            Subsignal("tx", Pins("105", dir="o")),
            Subsignal("sd", Pins("107", dir="o")),
            Attrs(IO_STANDARD="SB_LVCMOS33")
        ),

        *SPIFlashResources(0,
            cs="71", clk="70", mosi="67", miso="68",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS33")
        ),
    ]
    connectors = [
        Connector("pmod", 0, "78 79 80 81 - - 87 88 90 91 - -"),  # J2

        Connector("j", 1, "- - 112 113 114 115 116 117 118 119"), # J1
        Connector("j", 3, "- -  62  61  60  56  48  47  45  44"), # J3
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.run([iceprog, bitstream_filename], check=True)


if __name__ == "__main__":
    from ._blinky import build_and_program
    build_and_program(ICEStickPlatform, "clk12")
