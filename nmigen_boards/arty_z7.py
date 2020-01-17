import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from .resources import *


__all__ = ["ArtyZ720Platform"]


class ArtyZ720Platform(Xilinx7SeriesPlatform):
    device      = "xc7z020"
    package     = "clg400"
    speed       = "1"
    default_clk = "clk125"
    resources   = [
        Resource("clk125", 0,
            Pins("H16", dir="i"), Clock(125e6), Attrs(IOSTANDARD="LVCMOS33")),

        *SwitchResources(
            pins="M20 M19",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        RGBLEDResource(0,
            r="N15", g="G17", b="L15",                          # LD4
            attrs=Attrs(IOSTANDARD="LVCMOS33")),
        RGBLEDResource(1,                                       # LD5
            r="M15", g="L14", b="G14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(
            pins="R14 P14 N16 M14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(
            pins="D19 D20 L20 L19",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("audio", 0,
            Subsignal("pwm", Pins("R18", dir="o")),
            Subsignal("sd",  PinsN("T17", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")),

        Resource("crypto_sda", 0,                               # ATSHA204A
            Pins("J15", dir="io"),
            Attrs(IOSTANDARD="LVCMOS33")),

        Resource("hdmi_rx", 0,                                  # J10
            Subsignal("cec", Pins("H17", dir="io")),
            Subsignal("clk", DiffPairs("N18", "P19", dir="i"),
                Attrs(IO_TYPE="TMDS_33")),
            Subsignal("d",   DiffPairs("V20 T20 N20", "W20 U20 P20", dir="i"),
                Attrs(IO_TYPE="TMDS_33")),
            Subsignal("hpd", Pins("T19", dir="o")),
            Subsignal("scl", Pins("U14", dir="io")),
            Subsignal("sda", Pins("U15", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33")),

        Resource("hdmi_tx", 0,                                  # J11
            Subsignal("cec", Pins("G15", dir="io")),
            Subsignal("clk", DiffPairs("L16", "L17", dir="o"),
                Attrs(IO_TYPE="TMDS_33")),
            Subsignal("d",   DiffPairs("K17 K19 J18", "K18 J19 H18", dir="o"),
                Attrs(IO_TYPE="TMDS_33")),
            Subsignal("hpd", PinsN("R19", dir="i")),
            Subsignal("scl", Pins("M17", dir="io")),
            Subsignal("sda", Pins("M18", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33"))
    ]
    connectors = [
        Connector("pmod", 0, "Y18 Y19 Y16 Y17 - - U18 U19 W18 W19 - -"),  # JA
        Connector("pmod", 1, "Y14 W14 T10 T11 - - W16 V16 W13 V12 - -"),  # JB

        Connector("ck_io", 0, {
            # Outer Digital Header
            "io0": "T14",
            "io1": "U12",
            "io2": "U13",
            "io3": "V13",
            "io4": "V15",
            "io5": "T15",
            "io6": "R16",
            "io7": "U17",
            "io8": "V17",
            "io9": "V18",
            "io10": "T16",
            "io11": "R17",
            "io12": "P18",
            "io13": "N17",

            # Inner Digital Header
            "io26": "U5",
            "io27": "V5",
            "io28": "V6",
            "io29": "U7",
            "io30": "V7",
            "io31": "U8",
            "io32": "V8",
            "io33": "V10",
            "io34": "W10",
            "io35": "W6",
            "io36": "Y6",
            "io37": "Y7",
            "io38": "W8",
            "io39": "Y8",
            "io40": "W9",
            "io41": "Y9",

            # Outer Analog Header as Digital IO
            "a0": "Y11",
            "a1": "Y12",
            "a2": "W11",
            "a3": "V11",
            "a4": "T5",
            "a5": "U10",

            # Inner Analog Header as Digital IO
            "a6": "F19",
            "a7": "F20",
            "a8": "C20",
            "a9": "B20",
            "a10": "B19",
            "a11": "A20",

            # Misc.
            "a": "Y13"
        }),

        Connector("ck_spi", 0, {
            "miso": "W15",
            "mosi": "T12",
            "sck": "H15",
            "ss": "F16"
        }),

        Connector("ck_i2c", 0, {
            "scl": "P16",
            "sda": "P15"
        }),

        Connector("xadc", 0, {
            # Outer Analog Header
            "vaux1_n": "D18",
            "vaux1_p": "E17",
            "vaux9_n": "E19",
            "vaux9_p": "E18",
            "vaux6_n": "J14",
            "vaux6_p": "K14",
            "vaux15_n": "J16",
            "vaux15_p": "K16",
            "vaux5_n": "H20",
            "vaux5_p": "J20",
            "vaux13_n": "G20",
            "vaux13_p": "G19",

            # Inner Analog Header
            "vaux12_n": "F20",
            "vaux12_p": "F19",
            "vaux0_n": "B20",
            "vaux0_p": "C20",
            "vaux8_n": "A20",
            "vaux8_p": "B19"
        })
    ]

    def toolchain_program(self, products, name, **kwargs):
        xc3sprog = os.environ.get("XC3SPROG", "xc3sprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([xc3sprog, "-c", "jtaghs1_fast", "-p", "1", bitstream_filename], check=True)


if __name__ == "__main__":
    from .test.blinky import *
    ArtyZ720Platform().build(Blinky(), do_program=True)
