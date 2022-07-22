import os
import subprocess
import errno

from amaranth.build import *
from amaranth.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["MCH2022BadgePlatform"]


class MCH2022BadgePlatform(LatticeICE40Platform):
    device = "iCE40UP5K"
    package = "SG48"
    default_clk = "clk12"
    resources = [
        Resource(
            "clk12",
            0,
            Pins("35", dir="i"),
            Clock(12e6),
            Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS"),
        ),
        # UART (to RP2040)
        UARTResource(0, rx="6", tx="9", attrs=Attrs(IO_STANDARD="SB_LVTTL", PULLUP=1)),
        # IRQ (to ESP32)
        Resource(
            "irq", 0, PinsN("10", dir="oe"), Attrs(IO_STANDARD="SB_LVCMOS", PULLUP=1)
        ),
        # SPI Peripheral (to ESP32)
        SPIResource(
            0,
            copi="17",
            cipo="14",
            clk="15",
            cs_n="16",
            role="peripheral",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS"),
        ),
        # SPI-connected PSRAM.
        Resource(
            "spi_psram_4x",
            0,
            Subsignal("dq", Pins("21 13 12 20")),
            Subsignal("clk", Pins("19")),
            Subsignal("cs", PinsN("18"), Attrs(PULLMODE="UP")),
            Attrs(IO_STANDARD="SB_LVCMOS", SLEWRATE="SLOW"),
        ),
        # LCD
        Resource(
            "lcd",
            0,
            Subsignal(
                "db",
                Pins("26 27 31 32 34 37 38 42"),
            ),
            Subsignal("rs", Pins("11"), Attrs(PULLMODE="UP")),
            Subsignal("wr", PinsN("23"), Attrs(PULLMODE="UP")),
            Subsignal("cs", PinsN("28", dir="oe"), Attrs(PULLMODE="UP")),
            Subsignal("mode", Pins("43")),
            Subsignal("rst", PinsN("36", dir="oe")),
            Subsignal("fmark", Pins("25")),
            Attrs(IO_STANDARD="SB_LVCMOS"),
        ),
        # RGB driver
        *LEDResources(
            pins="39 40 41", invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
        # Semantic aliases
        Resource("led_r", 0, PinsN("39", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_g", 0, PinsN("40", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_b", 0, PinsN("41", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
    ]
    connectors = [
        Connector("pmod", 0, "47 48  4  2 - - 44 45  3 46 - -"),
    ]

    def toolchain_program(self, products, name):
        webusb_fpga = os.environ.get("WEBUSB_FPGA")
        if not webusb_fpga:
            print(
                "Please clone https://github.com/badgeteam/mch2022-tools and set the WEBUSB_FPGA environment variable"
            )
            print("e.g. `export WEBUSB_FPGA=~/mch2022-tools/webusb_fpga.py`")
            exit(errno.ENOENT)
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([webusb_fpga, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *

    p = MCH2022BadgePlatform()
    p.build(Blinky(), do_program=True)
