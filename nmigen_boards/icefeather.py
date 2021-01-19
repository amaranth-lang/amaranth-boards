import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["ICEFeatherPlatform"]


class ICEFeatherPlatform(LatticeICE40Platform):
    device      = "iCE40UP5K"
    package     = "SG48"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("35", dir="i"),
                 Clock(12e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        RGBLEDResource(0,
            r="47", g="41", b="39",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        *LEDResources(pins="47", invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        # Semantic aliases
        Resource("led_r", 0, PinsN("47", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),

        UARTResource(0,
            rx="23", tx="21",
            attrs=Attrs(IO_STANDARD="SB_LVTTL", PULLUP=1)
        ),

        *SPIFlashResources(0,
            cs_n="16", clk="15", copi="14", cipo="17",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    connectors = [
        Connector("wing", 0,
        # IO  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
            "25 26 27 28 36 31 32 37 38 43 44 48  2  3  4  6  9 10 11 12"
        )
    ]
    led_wing = [
        # Buttons present on the "led wing" attachment
        *ButtonResources(pins={0: "9", 1: "10", 2: "12", 3: "11"}, invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        # Semantic aliases
        Resource("button_sw1", 0, Pins("9", dir="i", conn=("wing", 0)), Attrs(IO_TYPE="LVCMOS33")),
        Resource("button_sw2", 0, Pins("10", dir="i", conn=("wing", 0)), Attrs(IO_TYPE="LVCMOS33")),
        Resource("button_sw3", 0, Pins("12",  dir="i", conn=("wing", 0)), Attrs(IO_TYPE="LVCMOS33")),
        Resource("button_sw4", 0, Pins("11",  dir="i", conn=("wing", 0)), Attrs(IO_TYPE="LVCMOS33")),

        RGBLEDResource(1,
            r="15", g="14", b="13",
            conn = ("wing", 0),
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([iceprog, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    p = ICEFeatherPlatform()
    p.add_resources(p.led_wing)
    p.build(Blinky(), do_program=True)
