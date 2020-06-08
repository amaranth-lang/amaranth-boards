import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["ICEStickPlatform"]


class ICEStickPlatform(LatticeICE40Platform):
    device      = "iCE40HX1K"
    package     = "TQ144"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("21", dir="i"),
                 Clock(12e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        *LEDResources(pins="99 98 97 96 95", attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        UARTResource(0,
            rx="9", tx="8", rts="7", cts="4", dtr="3", dsr="2", dcd="1",
            attrs=Attrs(IO_STANDARD="SB_LVTTL", PULLUP=1),
            role="dce"
        ),

        IrDAResource(0,
            rx="106", tx="105", sd="107",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),

        *SPIFlashResources(0,
            cs="71", clk="70", mosi="67", miso="68",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    connectors  = [
        Connector("pmod", 0, "78 79 80 81 - - 87 88 90 91 - -"),  # J2

        Connector("j", 1, "- - 112 113 114 115 116 117 118 119"), # J1
        Connector("j", 3, "- -  62  61  60  56  48  47  45  44"), # J3
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([iceprog, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    ICEStickPlatform().build(Blinky(), do_program=True)
