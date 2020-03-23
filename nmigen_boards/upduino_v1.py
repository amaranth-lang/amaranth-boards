from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["UpduinoV1Platform"]


class UpduinoV1Platform(LatticeICE40Platform):
    device      = "iCE40UP5K"
    package     = "SG48"
    default_clk = "SB_HFOSC"
    hfosc_div   = 0
    resources   = [
        *LEDResources(pins="39 40 41", invert=True,
                      attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_g", 0, PinsN("39", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_b", 0, PinsN("40", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_r", 0, PinsN("41", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),

        *SPIFlashResources(0,
            cs="16", clk="15", miso="17", mosi="14",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    connectors  = [
        # "Left" row of header pins (JP5 on the schematic)
        Connector("j", 0, "- - 23 25 26 27 32 35 31 37 34 43 36 42 38 28"),
        # "Right" row of header pins (JP6 on the schematic)
        Connector("j", 1, "12 21 13 19 18 11 9 6 44 4 3 48 45 47 46 2")
    ]

    # This board doesn't have an integrated programmer.
