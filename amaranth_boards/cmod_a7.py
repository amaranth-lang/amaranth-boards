import os
import subprocess

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *

"""
Example Usage:
    platform = CModA7_35Platform(toolchain="Symbiflow")
    platform.build(Top(), do_program=True)

Supported programmer:
    openocd
"""

__all__ = ["CmodA7_15Platform", "CmodA7_35Platform"]


class _CmodA7Platform(XilinxPlatform):
    package     = "cpg236"
    speed       = "1"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("L17", dir="i"),
                 Clock(12e6), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(pins="A17 C16", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        RGBLEDResource(0, r="C17", g="B16", b="B17", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(pins="A18 B18", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        UARTResource(0,
            rx="J17", tx="J18",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        *SPIFlashResources(0,
            cs_n="K19", clk="E19", copi="D19", cipo="D18", wp_n="G18",
            hold_n="F18",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        SRAMResource(0,
            cs_n="N19", oe_n="P19", we_n="R19",
            a="M18 M19 K17 N17 P17 P18 R18 W19 U19 V19 W18 T17 T18 U17 U18 V16 W16 W17 V15",
            d="W15 W13 W14 U15 U16 V13 V14 U14"),

        # One-wire interface to crypto authentication device
        # May not be populated on the board
        Resource("atsha204a", 0, Pins("D17", dir="io"),
            Attrs(IOSTANDARD="LVCMOS33"))
    ]
    connectors  = [
        Connector("pmod", 0, "G17 G19 N18 L18 - - H17 H19 J19 K18 - -"), # JA

        # Pin 24/25 are VCC and GND
        # Pin 15/16 are analog (XADC)
        Connector("gpio", 0,
            """
            M3  L3 A16  K3 C15  H1 A15 B15 A14  J3  J1  K2
            L1  L2   -   -  M1  N3  P3  M2  N1  N2  P1   -
             -  R3  T3  R2  T1  T2  U1  W2  V2  W3  V3  W5
            V4  U4  V5  W4  U5  U2  W6  U3  U7  W7  U8  V8
            """),

        Connector("xadc", 0, {
            "vaux4_n":   "G2",
            "vaux4_p":   "G3",
            "vaux12_n":  "J2",
            "vaux12_p":  "H2"
        })
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call(["openFPGALoader",
                "-b", "cmoda7_35t",
                "{}".format(bitstream_filename)
            ])


class CmodA7_15Platform(_CmodA7Platform):
    device      = "xc7a15t"

class CmodA7_35Platform(_CmodA7Platform):
    device      = "xc7a35t"

if __name__ == "__main__":
    from .test.blinky import *
    CmodA7_35Platform().build(Blinky(), do_program=True)
