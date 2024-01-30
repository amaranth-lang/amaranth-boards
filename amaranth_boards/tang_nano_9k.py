import os
import subprocess

from amaranth.build import *
from amaranth.vendor import GowinPlatform

from .resources import *


__all__ = ["TangNano9kPlatform"]


class TangNano9kPlatform(GowinPlatform):
    part          = "GW1NR-LV9QN88PC6/I5"
    family        = "GW1NR-9C"
    default_clk   = "clk27"
    resources     = [
        Resource("clk27", 0, Pins("52", dir="i"),
                 Clock(27e6), Attrs(IO_TYPE="LVCMOS33")),

        *ButtonResources(pins="3 4", invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins="10 11 13 14 15 16", invert=True,
                      attrs=Attrs(IO_TYPE="LVCMOS33")),

        UARTResource(0, rx="18", tx="17",
            attrs=Attrs(PULL_MODE="UP", IO_TYPE="LVCMOS33")),

        *SPIFlashResources(0,
            cs_n="60", clk="59", copi="61", cipo="62",
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        *SDCardResources(0,
            clk="36", cmd="37", dat0="39", dat3="38", wp_n="-",
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        Resource("lcd", 0,
            Subsignal("clk", Pins("35", dir="o")),
            Subsignal("hs", Pins("40", dir="o")),
            Subsignal("vs", Pins("34", dir="o")),
            Subsignal("de", Pins("33", dir="o")),
            Subsignal("r", Pins("75 74 73 72 71", dir="o")),
            Subsignal("g", Pins("70 69 68 57 56 55", dir="o")),
            Subsignal("b", Pins("54 53 51 42 41", dir="o")),
            Attrs(IO_TYPE="LVCMOS33", DRIVE=24)),

        Resource("lcd_backlight", 0, Pins("86", dir="o"),
                 Attrs(IO_TYPE="LVCMOS33")),

        Resource("hdmi", 0,
             Subsignal("clk", DiffPairs(p="69", n="68", dir="o")),
             Subsignal("d", DiffPairs(p="71 73 75", n="70 72 74", dir="o")),
             Attrs(IO_TYPE="LVCMOS33")),
    ]
    connectors = []

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "add_options":
                "set_option -use_mspi_as_gpio 1 -use_sspi_as_gpio 1",
            "gowin_pack_opts":
                "--sspi_as_gpio --mspi_as_gpio"
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        with products.extract("{}.fs".format(name)) as bitstream_filename:
            subprocess.check_call(["openFPGALoader", "-b", "tangnano9k", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    TangNano9kPlatform().build(Blinky(), do_program=True)
