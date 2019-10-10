import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["DE10NanoPlatform"]


class DE10NanoPlatform(IntelPlatform):
    device      = "5CSEBA6" # Cyclone V 110K LEs
    package     = "U23"     # UBGA-484
    speed       = "I7"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("V11", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("Y13", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("E11", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="W15 AA24 V16 V15 AF26 AE26 Y16 AA23",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="AH17 AH16", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *SwitchResources(
            pins="Y24 W24 W21 W20",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        # Arduino header
        UARTResource(0,
            rx="AG13", tx="AF13",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        # LTC2308 analogue-to-digital converter
        SPIResource(0,
            cs="U9", clk="V10", mosi="AC4", miso="AD4",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        # ADV7513 HDMI transmitter
        # Note this has a lot of input formats for tx_d, but this defaults to RGB24
        Resource("adv7513", 0,
            Subsignal("tx_d_r", Pins("AD12 AE12 W8   Y8   AD11 AD10 AE11 Y5", dir="o")),
            Subsignal("tx_d_g", Pins("AF10 Y4   AE9  AB4  AE7  AF6  AF8  AF5", dir="o")),
            Subsignal("tx_d_b", Pins("AE4  AH2  AH4  AH5  AH6  AG6  AF9  AE8", dir="o")),
            Subsignal("tx_clk", Pins("AG5", dir="o")),
            Subsignal("tx_de", Pins("AD19", dir="o")),
            Subsignal("tx_hs", Pins("T8", dir="o")),
            Subsignal("tx_vs", Pins("V13", dir="o")),
            Subsignal("tx_int", Pins("AF11", dir="i")),
            Subsignal("i2s0", Pins("T13", dir="o")),
            Subsignal("mclk", Pins("U11", dir="o")),
            Subsignal("lrclk", Pins("T11", dir="o")),
            Subsignal("sclk", Pins("T12", dir="o")),
            Subsignal("scl", Pins("U10", dir="o")),
            Subsignal("sda", Pins("AA4", dir="io")),
            Attrs(io_standard="3.3-V LVTTL")),
    ]
    connectors  = [
        Connector("gpio", 0,
            "V12  E8   W12  D11  D8   AH13 AF7  AH14 AF4  AH3  "
            "-    -    AD5  AG14 AE23 AE6  AD23 AE24 D12  AD20 "
            "C12  AD17 AC23 AC22 Y19  AB23 AA19 W11  -    -    "
            "AA18 W14  Y18  Y17  AB25 AB26 Y11  AA26 AA13 AA11 "),
        Connector("gpio", 1,
            "Y15  AC24 AA15 AD26 AG28 AF28 AE25 AF27 AG26 AH27 "
            "-    -    AG25 AH26 AH24 AF25 AG23 AF23 AG24 AH22 "
            "AH21 AG21 AH23 AA20 AF22 AE22 AG20 AF21 -    -    "
            "AG19 AH19 AG18 AH18 AF18 AF20 AG15 AE20 AE19 AE17 "),
        Connector("arduino", 0,
            "AG13 AF13 AG10 AG9  U14  U13  AG8  AH8  "
            "AF17 AE15 AF15 AG16 AH11 AH12 AH9  AG11 "
            "AH7"),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename + "@2"])


if __name__ == "__main__":
    from .test.blinky import Blinky
    DE10NanoPlatform().build(Blinky(), do_program=True)
