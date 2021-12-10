import os
import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["ICESugarNanoPlatform"]


class ICESugarNanoPlatform(LatticeICE40Platform):
    device      = "iCE40LP1K"
    package     = "CM36"
    default_clk = "clk12"

    resources   = [
        Resource("clk12", 0, Pins("D1", dir="i"),
                 Clock(12e6), Attrs(GLOBAL=True, IO_STANDARD="LVCMOS33")),

        *LEDResources(pins="B6", invert=False, attrs=Attrs(IO_STANDARD="LVCMOS33")),

        UARTResource(0,
            tx="B3", rx="A3",
            attrs=Attrs(IO_STANDARD="LVTTL33", PULLUP=1)
        ),

        *SPIFlashResources(0,
            cs_n="D5", clk="E5", copi="E4", cipo="F5",
            attrs=Attrs(IO_STANDARD="LVCMOS33")
        ),
    ]

    connectors = [
        Connector("pmod", 0, "E2 D1 B1 A1 - -"),                    # PMOD1
        Connector("pmod", 1, "B3 A3 B6 C5 - -"),                    # PMOD2
        Connector("pmod", 2, "B4 B5 E1 B1 - - C6 E3 C2 A1 - -"),    # PMOD3
    ]

    def toolchain_program(self, products, name):
        icesprog = os.environ.get("ICESPROG", "icesprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([icesprog, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    ICESugarNanoPlatform().build(Blinky(), do_program=True)
