import os
import subprocess
import unittest

from amaranth.build import *
from amaranth.vendor import IntelPlatform
from .resources import *


__all__ = ["DE10StandardPlatform"]


class DE10StandardPlatform(IntelPlatform):
    device      = "5CSXFC6D6" # Cyclone V SX SoC, 110K LEs
    package     = "F31"       # FBGA-896
    speed       = "C6"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("AF14", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("AA16", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("Y26", dir="i"),
                 Clock(50e6), Attrs(io_standard="2.5 V")),
        Resource("clk50", 3, Pins("K14", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="AA24 AB23 AC23 AD24 AG25 AF25 AE24 AF24 AB22 AC22",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="AJ4 AK4 AA14 AA15", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *SwitchResources(
            pins="AB30 Y27 AB28 AC30 W25 V25 AC28 AD30 AC29 AA30",
            attrs=Attrs(io_standard="2.5 V")),

        Display7SegResource(0,
            a="W17",  b="V18",  c="AG17", d="AG16", e="AH17",
            f="AG18", g="AH18", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(1,
            a="AF16", b="V16",  c="AE16", d="AD17", e="AE18",
            f="AE17", g="V17",  invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(2,
            a="AA21", b="AB17", c="AA18", d="Y17",  e="Y18",
            f="AF18", g="W16",  invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(3,
            a="Y19",  b="W19",  c="AD19", d="AA20", e="AC20",
            f="AA19", g="AD20", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(4,
            a="AD21", b="AG22", c="AE22", d="AE23", e="AG23",
            f="AF23", g="AH22", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(5,
            a="AF21", b="AG21", c="AF20", d="AG20", e="AE19",
            f="AF19", g="AB21", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="AH12", cke="AK13", cs_n="AG11", we_n="AA13",
            ras_n="AE13", cas_n="AF11",
            ba="AF13 AJ12",
            a="AK14 AH14 AG15 AE14 AB15 AC14 AD14 AF15 AH15 AG13 AG12 AH13 AJ14",
            dq="AK6 AJ7 AK7 AK8 AK9 AG10 AK11 AJ11 "
               "AH10 AJ10 AJ9 AH9 AH8 AH7 AJ6 AJ5",
            dqm="AB13 AK12",
            attrs=Attrs(io_standard="3.3-V LVCMOS")),

        Resource("vga", 0,
            Subsignal("r",       Pins("AK29 AK28 AK27 AJ27 AH27 AF26 AG26 AJ26", dir="o")),
            Subsignal("g",       Pins("AK26 AJ25 AH25 AK24 AJ24 AH24 AK23 AH23", dir="o")),
            Subsignal("b",       Pins("AJ21 AJ20 AH20 AJ19 AH19 AJ17 AJ16 AK16", dir="o")),
            Subsignal("hs",      Pins("AK19", dir="o")),
            Subsignal("vs",      Pins("AK18", dir="o")),
            Subsignal("clk",     Pins("AK21", dir="o")),
            Subsignal("blank_n", PinsN("AK22", dir="o")),
            Subsignal("sync_n",  PinsN("AJ22", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("adv7180", 0,
            Subsignal("clk27",   Pins("AC18", dir="i")),
            Subsignal("hs",      Pins("AH28", dir="i")),
            Subsignal("vs",      Pins("AG28", dir="i")),
            Subsignal("data",    Pins("AG27 AF28 AE28 AE27 AE26 AD27 AD26 AD25", dir="i")),
            Subsignal("reset_n", PinsN("AC27", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("audio", 0,
            Subsignal("xck",     Pins("AH30", dir="o")),
            Subsignal("bclk",    Pins("AF30", dir="io")),
            Subsignal("adclrck", Pins("AH29", dir="io")),
            Subsignal("adcdat",  Pins("AJ29", dir="i")),
            Subsignal("daclrck", Pins("AG30", dir="io")),
            Subsignal("dacdat",  Pins("AF29", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        I2CResource(0, scl="Y24", sda="Y23",
                    attrs=Attrs(io_standard="3.3-V LVTTL")),

        SPIResource("adc", 0,
            cs_n="Y21", clk="W24", copi="W22", cipo="V23",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        Resource("ir", 0,
            Subsignal("rx", Pins("W20", dir="i")),
            Subsignal("tx", Pins("W21", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        PS2Resource(0,
            clk="AB25", dat="AA25",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        PS2Resource(1,
            clk="AC25", dat="AB26",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
    ]
    connectors  = [
        Connector("gpio", 0,
            "W15  AK2  Y16  AK3  AJ1  AJ2  AH2  AH3  AH4  AH5  "
            "-    -    AG1  AG2  AG3  AG5  AG6  AG7  AG8  AF4  "
            "AF5  AF6  AF8  AF9  AF10 AE7  AE9  AE11 -    -    "
            "AE12 AD7  AD9  AD10 AD11 AD12 AC9  AC12 AB12 AA12 "),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            # The @2 selects the second device in the JTAG chain, because this chip
            # puts the ARM cores first.
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename + "@2"])


class TestCase(unittest.TestCase):
    def test_smoke(self):
        from .test.blinky import Blinky
        DE10StandardPlatform().build(Blinky(), do_build=False)


if __name__ == "__main__":
    from .test.blinky import Blinky
    DE10StandardPlatform().build(Blinky(), do_program=True)
