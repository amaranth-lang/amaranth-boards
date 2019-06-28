import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .dev import *


__all__ = ["ICEBreakerPlatform"]


class ICEBreakerPlatform(LatticeICE40Platform):
    device     = "iCE40UP5K"
    package    = "SG48"
    resources  = [
        Resource("clk12", 0, Pins("35", dir="i"),
                 Clock(12e6), Attrs(GLOBAL="1", IO_STANDARD="SB_LVCMOS33")),

        Resource("user_led",  0, PinsN("11", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_led",  1, PinsN("37", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        # Color-specific aliases
        Resource("user_ledr", 0, PinsN("11", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_ledg", 0, PinsN("37", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),

        Resource("user_btn",  0, PinsN("10", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS33")),

        Resource("serial", 0,
            Subsignal("rx",  Pins("6", dir="i")),
            Subsignal("tx",  Pins("9", dir="o"), Attrs(PULLUP="1")),
            Attrs(IO_STANDARD="SB_LVTTL")
        ),

        *SPIFlashResources(0,
            cs="16", clk="15", mosi="14", miso="17", wp="12", hold="13",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS33")
        ),
    ]
    connectors = [
        Connector("pmod", 0, "4 2 47 45 - -  3 48 46 44 - -"),  # PMOD1A
        Connector("pmod", 1, "43 38 34 31 - - 42 36 32 28 - -"), # PMOD1B
        Connector("pmod", 2, "27 25 21 19 - -  26 23 20 18 - -"), # PMOD2
    ]
    # The attached LED/button section can be either used standalone or as a PMOD.
    # Attach to platform using:
    # p.add_resources(p.break_off_pmod)
    # pmod_btn = plat.request("user_btn")
    break_off_pmod = [
         Resource("user_btn", 1, Pins("9", dir="i", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_btn", 2, Pins("4", dir="i", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_btn", 3, Pins("10", dir="i", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),

         Resource("user_led", 2, Pins("7", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_led", 3, Pins("1", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_led", 4, Pins("2", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_led", 5, Pins("8", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_led", 6, Pins("3", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),

         # Color-specific aliases
         Resource("user_ledr", 1, Pins("7", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_ledg", 1, Pins("1", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_ledg", 2, Pins("2", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_ledg", 3, Pins("8", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33")),
         Resource("user_ledg", 4, Pins("3", dir="o", conn=("pmod", 2)),
                  Attrs(IO_STANDARD="SB_LVCMOS33"))
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.run([iceprog, bitstream_filename], check=True)


if __name__ == "__main__":
    from ._blinky import Blinky
    p = ICEBreakerPlatform()
    p.add_resources(p.break_off_pmod)
    p.build(Blinky("clk12"), do_program=True)
