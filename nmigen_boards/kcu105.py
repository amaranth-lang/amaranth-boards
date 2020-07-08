import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_ultrascale import *
from .resources import *


__all__ = ["KCU105Platform"]


class KCU105Platform(XilinxUltraScalePlatform):
    device      = "xcku040"
    package     = "ffva1156"
    speed       = "2-e"
    default_clk = "clk125"
    resources   = [
        Resource("clk125", 0, DiffPairs("G10", "F10", dir="i"),
                 Clock(125e6), Attrs(IOSTANDARD="LVDS")),

        *LEDResources(pins="AP8 H23 P20 P21 N22 M22 R23 P23",
                      attrs=Attrs(IOSTANDARD="LVCMOS18")),
    ]
    connectors  = []

    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([openocd,
                "-c", "source [find board/kcu105.cfg]; init; pld load 0 {}; exit"
                      .format(bitstream_filename)
            ])


if __name__ == "__main__":
    from .test.blinky import *
    KCU105Platform().build(Blinky(), do_program=True)
