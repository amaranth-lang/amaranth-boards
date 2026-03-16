import os
import subprocess

from amaranth.build import *
from amaranth.vendor import GowinPlatform

from .resources import *


__all__ = ["TangMega138kProDockPlatform"]


class TangMega138kProDockPlatform(GowinPlatform):
    part          = "GW5AST-LV138FPG676AC1/I0"
    family        = "GW5AST-138B"
    default_clk   = "clk50"
    resources     = [
        Resource("clk50", 0, Pins("P16", dir="i"),
                 Clock(50e6), Attrs(IO_TYPE="LVCMOS33")),

        *ButtonResources(pins={0: "K16", 1: "G15", 2: "F15", 3: "G16"},
                         invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins={0: "R26", 1: "J14", 2: "L20",
                            3: "M25", 4: "N21", 5: "N23"},
                      invert=True,
                      attrs=Attrs(IO_TYPE="LVCMOS33")),

        Resource("ws2812", 0, Pins("H16", dir="o"),
                 Attrs(IO_TYPE="LVCMOS33")),

        UARTResource(0, rx="P15", tx="N16",
            attrs=Attrs(PULL_MODE="UP", IO_TYPE="LVCMOS33")),
    ]

    connectors = [
        Connector("pmod", 0,
                  "T24 R17 L24 R16 - - N17 N26 M26 N18 - -"),
        Connector("pmod", 1,
                  "H15 H14 L18 L17 - - D25 E25 B24 C24 - -"),
        Connector("pmod", 2,
                  "A18 A17 A19 B19 - - A20 B20 B21 C21 - -"),
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.fs".format(name)) as bitstream_filename:
            subprocess.check_call(["openFPGALoader", "-b", "tangmega138k",
                                   bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    TangMega138kProDockPlatform().build(Blinky(), do_program=True)
