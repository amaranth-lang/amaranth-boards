import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from .resources import *


__all__ = ["EBAZ4205Platform"]


class EBAZ4205Platform(Xilinx7SeriesPlatform):
    device      = "xc7z010"
    package     = "clg400"
    speed       = "1"
    default_clk = "clk33_333"
    resources   = [
        Resource("clk33_333", 0,
            Pins("N18", dir="i"), Clock(33.333e6), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(
            pins="W14 W13",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        UARTResource(0,
            rx="B19", tx="B20",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),
    ]
    connectors = [
    ]

    def toolchain_program(self, products, name, **kwargs):
        xc3sprog = os.environ.get("XC3SPROG", "xc3sprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([xc3sprog, "-c", "jtaghs1_fast", "-p", "1", bitstream_filename], check=True)


if __name__ == "__main__":
    from .test.blinky import *
    EBAZ4205Platform().build(Blinky(), do_program=True)
