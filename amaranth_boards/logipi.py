import os
import subprocess

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["LogiPiPlatform"]


class LogiPiPlatform(XilinxPlatform):
    device      = "xc6slx9"
    package     = "tqg144"
    speed       = "2"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("P85", dir="i"),
            Clock(50e6), Attrs(IOSTANDARD="LVTTL")
        ),

        *LEDResources(pins="P105 P104",
                      attrs=Attrs(IOSTANDARD="LVTTL")),

        *ButtonResources(pins="P102 P101",
                         attrs=Attrs(IOSTANDARD="LVTTL")),

        *SwitchResources(
            pins="P99 P100",
            attrs=Attrs(IOSTANDARD="LVTTL")),

        *SPIFlashResources(0,
            cs_n="P38", clk="P70", copi="P64", cipo="P65",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        SDRAMResource(0,
            clk="P50", cke="P48", we_n="P8", ras_n="P6", cas_n="P7",
            ba="P26 P27", a="P30 P32 P33 P34 P35 P40 P41 P43 P44 P45 P29 P46 P47 ",
            dq="P24 P23 P22 P21 P17 P12 P11 P10 P66 P62 P61 P59 P58 P57 P56 P55", dqm="R6 T5",
            attrs=Attrs(io_standard="3.3-V LVCMOS")
        ),



    ]
    connectors  = [
        Connector("pmod", 0, # PMOD1
            "P5 P2 P1 P16 - - P88 P92 P93 P94 - -"
        ),
        Connector("pmod", 1, # PMOD2
            "P142 P141 P15 P14 - - P144 P143 P140 P139 - -"
        ),
        Connector("pmod", 2, # PMOD3
            "P138 P137  P124 P123 - - P119 P118 P117 P116 - -"
        ),
        Connector("pmod", 3, # PMOD4
            "P112 P111 P132 P131 - - P115 P114 P134 P133 - -"
        ),
    ]

    # This board doesn't have an integrated programmer.
