import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["DE1SoCPlatform"]


class DE1SoCPlatform(IntelPlatform):
    device      = "5CSEMA5" # Cyclone V 85K LEs
    package     = "F31"     # FBGA-896
    speed       = "C6"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("AF14", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("AA16", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("Y26", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 3, Pins("K14", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="V16 W16 V17 V18 W17 W19 Y19 W20 W21 Y21",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="AA14 AA15 W15 Y16", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *SwitchResources(
            pins="AB12 AC12 AF9 AF10 AD11 AD12 AE11 AC9 AD10 AE12",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(0,
            a="AE26", b="AE27", c="AE28", d="AG27", e="AF28",
            f="AG28", g="AH28", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(1,
            a="AJ29", b="AH29", c="AH30", d="AG30", e="AF29",
            f="AF30", g="AD27", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(2,
            a="AB23", b="AE29", c="AD29", d="AC28", e="AD30",
            f="AC29", g="AC30", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(3,
            a="AD26", b="AC27", c="AD25", d="AC25", e="AB28",
            f="AB25", g="AB22", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(4,
            a="AA24", b="Y23", c="Y24", d="W22", e="W24",
            f="V23", g="W25", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(5,
            a="V25", b="AA28", c="Y27", d="AB27", e="AB26",
            f="AA26", g="AA25", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
    ]
    connectors  = [
        # Located on the right hand side of the board
        Connector("gpio", 0,
            "AC18 Y17  AD17 Y18  AK16 AK18 AK19 AJ19 AJ17 AJ16 "
            " -    -   AH18 AH17 AG16 AE16 AF16 AG17 AA18 AA19 "
            "AE17 AC20 AH19 AJ20 AH20 AK21 AD19 AD20  -    -   "
            "AE18 AE19 AF20 AF21 AF19 AG21 AF18 AG20 AG18 AJ21 "),
        
        Connector("gpio", 1,
            "AB17 AA21 AB21 AC23 AD24 AE23 AE24 AF25 AF26 AG25 "
            "-    -    AG26 AH24 AH27 AJ27 AK29 AK28 AK27 AJ26 "
            "AK26 AH25 AJ25 AJ24 AK24 AG23 AK23 AH23  -    -   "
            "AK22 AJ22 AH22 AG22 AF24 AF23 AE22 AD21 AA20 AC22 "),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            # The @2 selects the second device in the JTAG chain, because this chip
            # puts the ARM cores first.
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename + "@2"])


if __name__ == "__main__":
    from .test.blinky import Blinky
    DE1SoCPlatform().build(Blinky(), do_program=True)
