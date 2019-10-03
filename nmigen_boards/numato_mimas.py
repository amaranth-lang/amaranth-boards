import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_spartan_3_6 import *
from .resources import *


__all__ = ["NumatoMimasPlatform"]


class NumatoMimasPlatform(XilinxSpartan6Platform):
    device      = "xc6slx9"
    package     = "tqg144"
    speed       = "2"
    default_clk = "clk100"
    resources   = [
        Resource("clk100", 0, Pins("P126", dir="i"),
                 Clock(100e6), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(pins="P119 P118 P117 P116 P115 P114 P112 P111",
                      attrs=Attrs(IOSTANDARD="LVCMOS33")),
        *ButtonResources(pins="P124 P123 P121 P120",
                         attrs=Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE")),

        *SPIFlashResources(0,
            cs="P38", clk="P70", mosi="P64", miso="65",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
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
    from .test.blinky import *
    NumatoMimasPlatform().build(Blinky())
