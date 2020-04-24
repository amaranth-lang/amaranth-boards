import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["ICE40UP5KBEVNPlatform"]


class ICE40UP5KBEVNPlatform(LatticeICE40Platform):
    device      = "iCE40UP5K"
    package     = "SG48"
    default_clk = "clk12"
    resources   = [
        # J51 must be connected to use clk12 (it is by default)
        Resource("clk12", 0, Pins("35", dir="i"),
                 Clock(12e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        # 3 LEDs are present in an RGB common-anode package.
        *LEDResources(
            pins="39 40 41", invert=True,
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
        Resource("led_b", 0, PinsN("39", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_g", 0, PinsN("40", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_r", 0, PinsN("41", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),

        # 4 DIP switches are available, requiring internal pull-ups.
        # The switches' "ON" label points to the position which
        # connects them to ground, so invert the inputs.
        *SwitchResources(pins="23 25 34 43", invert=True,
                         attrs=Attrs(IO_STANDARD="SB_LVCMOS", PULLUP=1)
        ),

        *SPIFlashResources(0,
            cs="16", clk="15", mosi="14", miso="17",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    connectors  = [
        Connector("aardvark", 0, # J1
            "- - - - 14 - 15 17 16 -"),
        Connector("pmod", 0, # U6 (board), U11 (schematic)
            "16 14 17 15 - - 27 26 32 31 - -"),
        Connector("j", 0, # 'Header A' (J52)
            "- - 39 14 40 17 - 15 41 16 - -"),
        Connector("j", 1, # 'Header B' (J2)
            "- - 23 - 25 - 26 36 27 42 32 38 31 28 37 15 34 - 43 -"),
        Connector("j", 2, # 'Header C' (J3)
            "- 12 3 21 3 13 48 20 45 19 47 18 44 11 46 10 2 9 - 6"),
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_fn:
            subprocess.check_call([iceprog, bitstream_fn])


if __name__ == "__main__":
    from .test.blinky import *
    ICE40UP5KBEVNPlatform().build(Blinky(), do_program=True)
