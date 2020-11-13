import os
import sys
import subprocess

from nmigen.build import *
from nmigen.vendor.quicklogic import *
from nmigen_boards.resources import *


__all__ = ["QuickfeatherPlatform"]


class QuickfeatherPlatform(QuicklogicPlatform):
    device      = "ql-eos-s3_wlcsp"
    package     = "PU64"
    default_clk = "sys_clk0"
    connectors = [
        Connector("J", 2, "- 28 22 21 37 36 42 40 7 2 4 5"),
        Connector("J", 3, "- 8 9 17 16 20 6 55 31 25 47 - - - - 41"),
        Connector("J", 8, "27 26 33 32 23 57 56 3 64 62 63 61 59 - - -"),
    ]
    resources   = [
        # This is a placeholder resource since the board utilizes
        # default internal SoC clock.
        Resource("sys_clk0", 0, Pins("63", dir="i"), Clock(60e6)),

        *ButtonResources(pins="62"),

        RGBLEDResource(0, r="34", g="39", b="38"),

        UARTResource(0,
            rx="9", tx="8",
        ),

        SPIResource(0,
            cs="11", clk="20", copi="16", cipo="17"
        ),
        SPIResource(1,
            cs="37", clk="40", copi="36", cipo="42",
            role="peripheral"
        ),

        I2CResource(0,
            scl="4", sda="5"
        ),
        I2CResource(1,
            scl="22", sda="21"
        ),

        DirectUSBResource(0, d_p="10", d_n="14"),

        Resource("swd", 0,
            Subsignal("clk", Pins("54", dir="io")),
            Subsignal("io",  Pins("53", dir="io")),
        ),
    ]

    # This programmer requires OpenOCD with support for eos-s3:
    # https://github.com/antmicro/openocd/tree/eos-s3-support
    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}.openocd".format(name),
                              "{}_iomux.openocd".format(name)) as \
                (bitstream_openocd_filename, iomux_openocd_filename):
            subprocess.check_call([
                openocd,
                "-s", "tcl",
                "-f", "interface/ftdi/antmicro-ftdi-adapter.cfg",
                "-f", "interface/ftdi/swd-resistor-hack.cfg",
                "-f", "board/quicklogic_quickfeather.cfg",
                "-f", bitstream_openocd_filename,
                "-c", "init",
                "-c", "reset halt",
                "-c", "load_bitstream",
                "-f", iomux_openocd_filename,
                "-c", "exit"
            ])


if __name__ == "__main__":
    from .test.blinky import *
    QuickfeatherPlatform().build(Blinky())
