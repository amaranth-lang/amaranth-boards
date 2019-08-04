import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .dev import *


__all__ = ["BlackIceIIPlatform"]


class BlackIceIIPlatform(LatticeICE40Platform):
    device      = "iCE40HX4K"
    package     = "TQ144"
    default_clk = "clk100"
    resources   = [
        Resource("clk100", 0, Pins("129", dir="i"),
            Clock(100e6), Attrs(GLOBAL="1", IO_STANDARD="SB_LVCMOS33")
        ),

        Resource("user_led", 0, Pins("71", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_led", 1, Pins("67", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_led", 2, Pins("68", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_led", 3, Pins("70", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        # Color aliases
        Resource("user_ledb", 0, Pins("71", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_ledg", 0, Pins("67", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_ledo", 0, Pins("68", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_ledr", 0, Pins("70", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS33")),

        Resource("user_btn", 0, PinsN("63", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_btn", 1, PinsN("64", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS33")),

        Resource("user_sw", 0, PinsN("37", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_sw", 1, PinsN("38", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_sw", 2, PinsN("39", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS33")),
        Resource("user_sw", 3, PinsN("41", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS33")),

        UARTResource(0,
            rx="88", tx="85", rts="91", cts="94",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS33", PULLUP="1")
        ),

        Resource("sram", 0,
            Subsignal("address", Pins(
                "137 138 139 141 142 42 43 44 73 74 75 76 115 116 117 118 119 78",
                dir="o"
            )),
            Subsignal("data", Pins(
                "136 135 134 130 125 124 122 121 62 61 60 56 55 48 47 45",
                dir="io"
            )),
            Subsignal("oe", PinsN("29", dir="o")),
            Subsignal("we", PinsN("120", dir="o")),
            Subsignal("cs", PinsN("136", dir="o")),
            Subsignal("ub", PinsN("28", dir="o")),
            Subsignal("lb", PinsN("24", dir="o")),
            Attrs(IO_STANDARD="SB_LVCMOS33"),
        ),
    ]
    connectors  = [
        Connector("pmod", 0, " 94  91  88  85 - -  95  93  90  87 - -"),  # PMOD1/2
        Connector("pmod", 1, "105 102  99  97 - - 104 101  98  96 - -"),  # PMOD3/4
        Connector("pmod", 2, "143 114 112 107 - - 144 113 110 106 - -"),  # PMOD5/6
        Connector("pmod", 3, " 10   9   2   1 - -   8   7   4   3 - -"),  # PMOD7/8
        Connector("pmod", 4, " 20  19  16  15 - -  18  17  12  11 - -"),  # PMOD9/10
        Connector("pmod", 5, " 34  33  22  21 - -  32  31  26  25 - -"),  # PMOD11/12
        Connector("pmod", 6, " 37  38  39  41 - -"),  # PMOD13
        Connector("pmod", 7, " 71  67  68  70 - -"),  # PMOD14
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call(["cp", bitstream_filename, "/dev/ttyACM0"])


if __name__ == "__main__":
    from ._blinky import Blinky
    BlackIceIIPlatform().build(Blinky(), do_program=True)
