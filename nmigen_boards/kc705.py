import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from .dev import *


__all__ = ["KC705Platform"]


class KC705Platform(Xilinx7SeriesPlatform):
    device      = "xc7k325t"
    package     = "ffg900"
    speed       = "2"
    default_clk = "clk156"
    resources   = [
        Resource("clk156", 0, DiffPairs("K28", "K29", dir="i"),
                 Clock(156e6), Attrs(IOSTANDARD="LVDS_25")),

        Resource("user_led", 0, Pins("AB8", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
        Resource("user_led", 1, Pins("AA8", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
        Resource("user_led", 2, Pins("AC9", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
        Resource("user_led", 3, Pins("AB9", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
        Resource("user_led", 4, Pins("AE26", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
        Resource("user_led", 5, Pins("G19", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
        Resource("user_led", 6, Pins("E18", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
        Resource("user_led", 7, Pins("F16", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),

        UARTResource(0,
            rx="M19", tx="K24",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
    ]
    connectors  = []

    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([openocd,
                "-c", "source [find board/kc705.cfg]; init; pld load 0 {}; exit"
                      .format(bitstream_filename)
            ])


if __name__ == "__main__":
    from ._blinky import build_and_program
    build_and_program(KC705Platform)
