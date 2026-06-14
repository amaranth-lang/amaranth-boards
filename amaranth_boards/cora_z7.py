import os
import subprocess
import unittest

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["CoraZ7Platform"]


class CoraZ7Platform(XilinxPlatform):
    device      = "xc7z007s"
    package     = "clg400"
    speed       = "1"
    default_clk = "clk125"

    resources = [
        Resource("clk125", 0,
            Pins("H16", dir="i"), Clock(125e6), Attrs(IOSTANDARD="LVCMOS33")),

        RGBLEDResource(0,
            r="N15", g="G17", b="L15",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),
        RGBLEDResource(1,
            r="M15", g="L14", b="G14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(
            pins="D19 D20",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("crypto_sda", 0,
            Pins("J15", dir="io"),
            Attrs(IOSTANDARD="LVCMOS33")),

        # Pmod connectors JA and JB (full 8‑bit I/O)
        Resource("pmod", 0,
            Subsignal("io", Pins("Y18 Y19 Y16 Y17 U18 U19 W18 W19", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33")),
        Resource("pmod", 1,
            Subsignal("io", Pins("W14 Y14 T11 T10 V16 W16 V12 W13", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33")),
    ]

    connectors = [
        # ChipKit outer digital header (0‑13)
        Connector("ck_io", 0, {
            "io0":  "U14", "io1":  "V13", "io2":  "T14", "io3":  "T15",
            "io4":  "V17", "io5":  "V18", "io6":  "R17", "io7":  "R14",
            "io8":  "N18", "io9":  "M18", "io10": "U15", "io11": "K18",
            "io12": "J18", "io13": "G15",
        }),

        # ChipKit inner digital header (26‑41)
        Connector("ck_io", 1, {
            "io26": "R16", "io27": "U12", "io28": "U13", "io29": "V15",
            "io30": "T16", "io31": "U17", "io32": "T17", "io33": "R18",
            "io34": "P18", "io35": "N17", "io36": "M17", "io37": "L17",
            "io38": "H17", "io39": "H18", "io40": "G18", "io41": "L20",
        }),

        # ChipKit SPI header
        Connector("ck_spi", 0, {
            "cipo": "W15",
            "copi": "T12",
            "sck":  "H15",
            "ss":   "F16",
        }),

        # ChipKit I2C header
        Connector("ck_i2c", 0, {
            "scl": "P16",
            "sda": "P15",
        }),

        # User digital I/O header J1 (1‑12)
        Connector("user_dio", 0, {
            "1":  "L19", "2":  "M19", "3":  "N20", "4":  "P20",
            "5":  "P19", "6":  "R19", "7":  "T20", "8":  "T19",
            "9":  "U20", "10": "V20", "11": "W20", "12": "K19",
        }),

        # Single extra ChipKit signal (ck_ioa)
        Connector("ck_ioa", 0, {"a": "M20"}),

        # XADC analog inputs (optional)
        Connector("xadc", 0, {
            "vaux1_n":  "D18", "vaux1_p":  "E17",
            "vaux9_n":  "E19", "vaux9_p":  "E18",
            "vaux6_n":  "J14", "vaux6_p":  "K14",
            "vaux15_n": "J16", "vaux15_p": "K16",
            "vaux5_n":  "H20", "vaux5_p":  "J20",
            "vaux13_n": "G20", "vaux13_p": "G19",
        }),
    ]

    def toolchain_program(self, products, name, **kwargs):
        xc3sprog = os.environ.get("XC3SPROG", "xc3sprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run(
                [xc3sprog, "-c", "jtaghs1_fast", "-p", "1", bitstream_filename],
                check=True
            )


class TestCase(unittest.TestCase):
    def test_smoke(self):
        from .test.blinky import Blinky
        CoraZ7Platform().build(Blinky(), do_build=False)


if __name__ == "__main__":
    from .test.blinky import Blinky
    CoraZ7Platform().build(Blinky(), do_program=True)
