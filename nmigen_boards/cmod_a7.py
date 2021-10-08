import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from .resources import *

"""
Example Usage:
    platform = CModA7_35Platform(toolchain="Symbiflow")
    platform.build(Top(), do_program=True)

Supported programmer:
    openocd
"""

__all__ = ["CmodA7_15Platform", "CmodA7_35Platform"]


class _CmodA7Platform(Xilinx7SeriesPlatform):
    package     = "cpg236"
    speed       = "1"
    default_clk = "clk12"
    default_rst = None
    resources   = [
        Resource("clk12", 0, Pins("L17", dir="i"),
                 Clock(12e6), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(pins="A17 C16", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        RGBLEDResource(0, r="C17", g="B16", b="B17", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(pins="A18 B18", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        UARTResource(0,
            rx="J18", tx="J17",
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
            d="W15 W13 W14 U15 U16 V13 V14 U14")
    ]
    connectors  = [
        Connector("pmod", 0, "G17 G19 N18 L18 - - H17 H19 J19 K18 - -"), # JA

        Connector("gpio", 0, {
            "io1":  "M3",
            "io2":  "L3",
            "io3":  "A16",
            "io4":  "K3",
            "io5":  "C15",
            "io6":  "H1",
            "io7":  "A15",
            "io8":  "B15",
            "io9":  "A14",
            "io10":  "J3",
            "io11": "J1",
            "io12": "K2",
            "io13": "L1",
            "io14": "L2",
            # IO 15/16 are analog
            "io17": "M1",
            "io18": "M3",
            "io19": "P3",
            "io20": "M2",
            "io21": "N1",
            "io22": "N2",
            "io23": "P1",
            # IO 24/25 are VCC and GND
            "io26": "R3",
            "io27": "T3",
            "io28": "R2",
            "io29": "T1",
            "io30": "T2",
            "io31": "U1",
            "io32": "W2",
            "io33": "V2",
            "io34": "W3",
            "io35": "V3",
            "io36": "W5",
            "io37": "V4",
            "io38": "U4",
            "io39": "V5",
            "io40": "W4",
            "io41": "U5",
            "io42": "U2",
            "io43": "W6",
            "io44": "U3",
            "io45": "U7",
            "io46": "W7",
            "io47": "U8",
            "io48": "V8"
        }),
        Connector("xadc", 0, {
            "vaux4_n":   "G2",
            "vaux4_p":   "G3",
            "vaux12_n":  "J2",
            "vaux12_p":  "H2"
        })
    ]

    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([openocd,
                # Use for debug output
                #"-d",
                "-c",
                "source [find board/digilent_cmod_a7.cfg]; init; pld load 0 {}; exit"
                    .format(bitstream_filename)
            ])


class CmodA7_15Platform(_CmodA7Platform):
    device      = "xc7a15t"

class CmodA7_35Platform(_CmodA7Platform):
    device      = "xc7a35t"

if __name__ == "__main__":
    from .test.blinky import *
    CmodA7_35Platform().build(Blinky(), do_program=True)
