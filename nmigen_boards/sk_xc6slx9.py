import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_spartan_3_6 import *
from .dev import *


__all__ = ["SK_XC6SLX9Platform"]


class SK_XC6SLX9Platform(XilinxSpartan6Platform):
    device      = "xc6slx9"
    package     = "tqg144"
    speed       = "2"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("P134", dir="i"),
            Clock(50e6), Attrs(IOSTANDARD="LVCMOS33")
        ),

        *SPIFlashResources(0,
            cs="P38", clk="P70", mosi="P64", miso="65",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        SRAMResource(0,
            cs="P97", oe="P45", we="P51",
            a="P39 P40 P41 P43 P44 P55 P56 P57 P58 P59 P82 P81 P80 P79 P78 P66 P62 P61 P60",
            d="P46 P47 P48 P50 P75 P74 P69 P67",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
    ]
    connectors  = [
        Connector("x", 7,
            "-    -    P34  -    P33  P32  P30  P29  P27  P26  "
            "P24  P23  P22  P21  P17  P16  P15  P14  P12  P11  "
            "P10  P9   P8   P7   P6   P5   P2   P1   P143 P144 "
            "P141 P142 P139 P140 P137 P138 P132 P133 P127 P131 "
        ),
        Connector("x", 9,
            "-    -    P93  -    P92  P88  P87  P85  P84  P83  "
            "P74  P75  P78  P79  P81  P80  P69  P82  P66  P67  "
            "P61  P62  P59  P60  P58  P57  P55  P56  P50  P51  "
            "P47  P48  P44  P46  P45  P43  P40  P41  P35  P39  "
        ),
        Connector("x", 8,
            "-    -    P126 -    P123 P124 P120 P121 P118 P119 "
            "P116 P117 P114 P115 P111 P112 P104 P105 P101 P102 "
            "P99  P100 P97  P98  P94  P95  -    -    -    -    "
            "-    -    -    -    -    -    -    -    -    -    "
        ),
    ]

    # This board doesn't have an integrated programmer.
