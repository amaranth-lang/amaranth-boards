import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *

__all__ = ["ICEBreakerBitsyPlatform"]

class ICEBreakerBitsyPlatform(LatticeICE40Platform):
    device      = "iCE40UP5K"
    package     = "SG48"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("35", dir="i"),
                 Clock(12e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        DirectUSBResource(0, d_p="42", d_n="38", pullup="37",
                attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        *SPIFlashResources(0,
            cs="16", clk="15", copi="14", cipo="17", wp="18", hold="19",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),

        RGBLEDResource(0, r="39", g="40", b="41", invert=True,
                attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        *LEDResources(pins="25 6", invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_r", 0, PinsN("25", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_g", 0, PinsN("6", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),

        *ButtonResources(pins="2", invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
    ]
    connectors = [
        Connector("edge", 0,  # Pins bottom P0 - P12,
            "47 44 48 45  4  3  9 10 11 12 21 13"
            "20 25 23 27 26 28 31 32 34 36 43 46"
        )
    ]


    def toolchain_program(self, products, name):
        dfu_util = os.environ.get("DFU_UTIL", "dfu-util")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([dfu_util, "-d", "1209:6146", "-a", "0", "-D", bitstream_filename])



if __name__ == "__main__":
    from .test.blinky import *
    ICEBreakerBitsyPlatform().build(Blinky(), do_program=True)
