import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_spartan_3_6 import *
from .dev import *


__all__ = ["NumatoMimasPlatform"]


class NumatoMimasPlatform(XilinxSpartan6Platform):
    device      = "xc6slx9"
    package     = "tqg144"
    speed       = "2"
    default_clk = "clk100"
    resources   = [
        Resource("clk100", 0, Pins("P126", dir="i"),
                 Clock(100e6), Attrs(IOSTANDARD="LVCMOS33")),

        Resource("user_led", 0, Pins("P119", dir="o"),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("user_led", 1, Pins("P118", dir="o"),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("user_led", 2, Pins("P117", dir="o"),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("user_led", 3, Pins("P116", dir="o"),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("user_led", 4, Pins("P115", dir="o"),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("user_led", 5, Pins("P114", dir="o"),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("user_led", 6, Pins("P112", dir="o"),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("user_led", 7, Pins("P111", dir="o"),
                 Attrs(IOSTANDARD="LVCMOS33")),

        Resource("user_btn", 0, Pins("P124", dir="i"),
                 Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE")),
        Resource("user_btn", 1, Pins("P123", dir="i"),
                 Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE")),
        Resource("user_btn", 2, Pins("P121", dir="i"),
                 Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE")),
        Resource("user_btn", 3, Pins("P120", dir="i"),
                 Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE")),
    ]
    connectors  = [
        Connector("p", 1,
            "-    -    P35  P34  P33  P32  P30  P29  P27  P26  "
            "P24  P23  P22  P21  P17  P16  P15  P14  P12  P11  "
            "P10  P9   P8   P7   P6   P5   P2   P1   P142 P141 "
            "P140 P139 P138 P137 P134 P133 P132 P131 -    -    "
        ),
        Connector("p", 2,
            "-    -    P43  P44  P45  P46  P47  P48  P50  P51  "
            "P55  P56  P74  P75  P78  P79  P80  P81  -    -    "
            "P82  P83  P84  P85  P87  P88  P92  P93  P94  P95  "
            "P97  P98  P99  P100 P101 P102 P104 P105 -    -    "
        )
    ]

    # Programming this board is not currently supported.


if __name__ == "__main__":
    from ._blinky import Blinky
    NumatoMimasPlatform().build(Blinky())
