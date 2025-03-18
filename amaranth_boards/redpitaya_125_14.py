import os
import subprocess

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["RedPitaya14Platform"]


class RedPitaya14Platform(XilinxPlatform):
    device      = "xc7z010"
    package     = "clg400"
    speed       = "1"
    default_clk = "clk125"
    resources   = [
        Resource("clk125", 0,
            DiffPairs("U18", "U19", dir="i"), Clock(125e6), Attrs(IOSTANDARD="TMDS_33")),

        *LEDResources(
            pins="F16 F17 G15 H15 K14 G14 J15 J14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("daisy_io", 0,
            DiffPairs("T12", "U12", dir="i"), Attrs(IOSTANDARD="TMDS_33")),
        Resource("daisy_io", 1,
            DiffPairs("U14", "U15", dir="i"), Attrs(IOSTANDARD="TMDS_33")),
        Resource("daisy_io", 2,
            DiffPairs("P14", "R14", dir="i"), Attrs(IOSTANDARD="TMDS_33")),
        Resource("daisy_io", 3,
            DiffPairs("N18", "P19", dir="i"), Attrs(IOSTANDARD="TMDS_33")),
    ]
    connectors = [
            Connector("E1", 0, {
            # Outer Analog Header
            "dio0_p": "G17",
            "dio0_n": "G18",
            "dio1_p": "H16",
            "dio1_n": "H17",
            "dio2_p": "J18",
            "dio2_n": "H18",
            "dio3_p": "K17",
            "dio3_n": "K18",
            "dio4_p": "L14",
            "dio4_n": "L15",
            "dio5_p": "L16",
            "dio5_n": "L17",
            "dio6_p": "K16",
            "dio6_n": "J16",
            "dio7_p": "M14",
            "dio7_n": "M15",
        })
    ]

    def toolchain_program(self, products, name, **kwargs):
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call(["openFPGALoader", "-c", "digilent_hs2", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    RedPitaya14Platform().build(Blinky(), do_program=True)
