from amaranth.build import *
from amaranth.vendor.xilinx import XilinxPlatform
from .resources import *

__all__ = ["ElbertV2NumatoPlatform"]

class ElbertV2NumatoPlatform(XilinxPlatform):
    device = "xc3s50an"
    package = "tqg144"
    speed = "4"
    default_clk = "clk12"

    resources = [
        Resource("clk12", 0, Pins("P129", dir="i"), Clock(12e6), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(pins="P55 P54 P51 P50 P49 P48 P47 P46",
                      attrs=Attrs(IOSTANDARD="LVCMOS33", SLEW="SLOW", DRIVE="12")),
        Display7SegResource(0, a="P114", b="P110", c="P111", d="P112", e="P113", f="P115", g="P116", dp="P117",
                            invert=True, attrs=Attrs(IOSTANDARD="LVCMOS33", SLEW="SLOW", DRIVE="12")),
        Resource("display_7seg_ctrl", 0,
            Subsignal("en", Pins("P120 P121 P124", invert=True, dir="o"),
                      Attrs(IOSTANDARD="LVCMOS33", SLEW="SLOW", DRIVE="12"))
        ),
        VGAResource(0, r="P105 P104 P103", g="P102 P101 P99", b="P98 P96", hs="P93", vs="P92",
                    attrs=Attrs(IOSTANDARD="LVCMOS33", SLEW="SLOW", DRIVE="12")),
        *SDCardResources(0, dat0="P83", dat1="P82", dat2="P90", dat3="P85", cmd="P84", clk="P57",
                         attrs=Attrs(IOSTANDARD="LVCMOS33", SLEW="SLOW", DRIVE="12")),
        Resource("audiojack", 0,
            Subsignal("audio", Pins("P88 P87", dir="o"), Attrs(IOSTANDARD="LVCMOS33", SLEW="SLOW", DRIVE="12"))
        ),
        *ButtonResources(pins="P80 P79 P78 P77 P76 P75",
                         attrs=Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE", DRIVE="12",
                                     SLEW="SLOW")),
        *SwitchResources(pins="P70 P69 P68 P64 P63 P60 P59 P58",
                         attrs=Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE", DRIVE="12",
                                     SLEW="SLOW"))
    ]

    connectors = [
        Connector("p", 1,
            "- - - - P25 P24 P29 P27 P30 P28 P32 P31"
        ),
        Connector("p", 6,
            "- - - - P13 P12 P16 P15 P20 P18 P21 P19"
        ),
        Connector("p", 2,
            "- - - - P6 P4 P5 P3 P8 P7 P11 P10"
        ),
        Connector("p", 4,
            "- - - - P132 P130 P135 P134 P139 P138 P143 P141"
        ),
        Connector("p", 5,
            "- - P140 P142 P91 P131 P126 P127 P123 P125"
        )
    ]

if __name__ == "__main__":
    from .test.blinky import *
    ElbertV2NumatoPlatform().build(Blinky())
