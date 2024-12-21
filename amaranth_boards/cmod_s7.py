import os
import subprocess

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *

"""
Example Usage:
    platform = CModS7_Platform(toolchain="Symbiflow")
    platform.build(Top(), do_program=True)

Supported programmer:
    openocd
"""

__all__ = ["CmodS7_Platform"]


class CmodS7_Platform(XilinxPlatform):
    device      = "xc7s25"
    package     = "csga225"
    speed       = "1"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("M9", dir="i"),
                 Clock(12e6), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(pins="E2 K1 J1 E1", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        RGBLEDResource(0, r="F2", g="D3", b="F1", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(pins="D2 D1", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        UARTResource(0,
            rx="K15", tx="L12",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        # Clock only via STARTUPE2 primitive
        *SPIFlashResources(0,
            cs_n="L11", clk="F5", copi="H14", cipo="H15", wp_n="J12",
            hold_n="K13",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        # One-wire interface to crypto authentication device
        # May not be populated on the board
        Resource("atsha204a", 0, Pins("D17", dir="io"),
            Attrs(IOSTANDARD="LVCMOS33"))
    ]
    connectors  = [
        Connector("pmod", 0, "J2 H2 H4 F3 - - H3 H1 G1 F4 - -"), # JA

        # Pin 24/25 are VCC and GND
        # Pin 32/33 are analog (XADC)
        # Pin 9-15 and 34-39 do not exist
        Connector("gpio", 0,
            """
            L1  M4  M3  N2  M2  P3  N3  P1  N1  -   -   -
            -   -   -   P14 P15 N13 N15 N14 M15 M14 L15 -
            -   L14 K14 J15 L13 M13 J11 -   -   -   -   -
            -   -   -   C5  A2  B2  B1  C1  B3  B4  A3  A4
            """),

        Connector("xadc", 0, {
            "vaux5_n":   "A13",
            "vaux5_p":   "A14",
            "vaux12_n":  "A11",
            "vaux12_p":  "A12"
        })
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call(["openFPGALoader",
                "-c", "digilent",
                "--fpga-part", "xc7s25",
                "{}".format(bitstream_filename)
            ])


if __name__ == "__main__":
    from .test.blinky import *
    CmodS7_Platform().build(Blinky(), do_program=True)
