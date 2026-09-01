import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["DE1SoCPlatform"]


class DE1SoCPlatform(IntelPlatform):
    device      = "5CSEMA5" # Cyclone V 85K LEs
    package     = "F31"     # FBGA-896
    speed       = "C6"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("AF14", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("AA16", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("Y26", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 3, Pins("K14", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="V16 W16 V17 V18 W17 W19 Y19 W20 W21 Y21",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="AA14 AA15 W15 Y16", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *SwitchResources(
            pins="AB12 AC12 AF9 AF10 AD11 AD12 AE11 AC9 AD10 AE12",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(0,
            a="AE26", b="AE27", c="AE28", d="AG27", e="AF28",
            f="AG28", g="AH28", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(1,
            a="AJ29", b="AH29", c="AH30", d="AG30", e="AF29",
            f="AF30", g="AD27", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(2,
            a="AB23", b="AE29", c="AD29", d="AC28", e="AD30",
            f="AC29", g="AC30", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(3,
            a="AD26", b="AC27", c="AD25", d="AC25", e="AB28",
            f="AB25", g="AB22", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(4,
            a="AA24", b="Y23", c="Y24", d="W22", e="W24",
            f="V23", g="W25", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(5,
            a="V25", b="AA28", c="Y27", d="AB27", e="AB26",
            f="AA26", g="AA25", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        Resource("audio_codec", 0,      #WM8731 codec. Uses I2C for config
            Subsignal("adclrck", Pins("K8", dir = "i")),
            Subsignal("adcdat",  Pins("K7", dir = "i")),
            Subsignal("daclrck", Pins("H8", dir = "i")),
            Subsignal("dacdat",  Pins("J7", dir = "o")),
            Subsignal("xck",     Pins("G7", dir = "o")),
            Subsignal("bclk",    Pins("H7", dir = "i")),
            Attrs(io_standard="3.3-V LVTTL"),
        ),

        #Have used I2C resource for this but am wondering if it should be named,
        #since it does config for the audio codec and TV decoder
        I2CResource(0,      
            scl="J12", sda="K12", 
            atttrs=Attrs(io_standard="3.3-V LVTTL"),
        ),

        Resource("vga", 0,          #ADV7123 DAC
            Subsignal("r",     Pins("A13  C13  E13  B12  C12  D12  E12  F13", dir="o")),
            Subsignal("g",     Pins("J9   J10  H12  G10  G11  G12  F11  E11", dir="o")),
            Subsignal("b",     Pins("B13  G13  H13  F14  H14  F15  G15  J14", dir="o")),
            Subsignal("clk",   Pins("A11", dir="o")),
            Subsignal("blank", PinsN("F10", dir="o")),
            Subsignal("hs",    Pins("B11", dir="o")),
            Subsignal("vs",    Pins("D11", dir="o")),
            Subsignal("sync",  PinsN("C10", dir="o")),
            Attrs(io_standard="3.3-V LVTTL"),
        ),

        Resource("tv_decoder", 0,   #ADV7180 TV decoder chip. Uses I2C for config
            Subsignal("data",  Pins("D2 B1 E2 B2 D1 E1 C2 B3", dir="i")),
            Subsignal("hs",    Pins("A5", dir="i")),
            Subsignal("vs",    Pins("A3", dir="i")),
            Subsignal("clk27", Pins("H15", dir="i")),
            Subsignal("reset", PinsN("F6", dir="o")),
            Attrs(io_standard="3.3-V LVTTL"),
        ),

        IrDAResource(0,
            rx="AA30", tx="AB30",
            attrs=Attrs(io_standard="3.3-V LVTTL"),
        ),

        SDRAMResource(0,
            clk  = "AH12", cke   = "AK13", cs_n  = "AG11",
            we_n = "AA13", ras_n = "AE13", cas_n = "AF11",
            ba  = "AF13 AJ12",
            a   = "AK14 AH14 AG15 AE14 AB15 AC14 AD14 AF15 AH15 AG13 AG12 AH13 AJ14",
            dq  = "AK6  AJ7  AK7  AK8  AK9  AG10 AK11 AJ11 AH10 AJ10 AJ9  AH9  AH8  AH7  AJ6  AJ5",
            dqm = "AB13 AK12",
            attrs=Attrs(io_standard="3.3-V LVTTL"),
        ),

        Resource("ps2", 0,      #A dual PS2 port. If using one device, just use LSB of the clk/dat signals
            Subsignal("clk", Pins("AD7 AD9", dir="io")),
            Subsignal("dat", Pins("AE7 AE9", dir="io")),
            Attrs(io_standard="3.3-V LVTTL"),
        ),

        Resource("adc", 0,      #LTC2308 ADC with SPI interface. Again wondering if it should be SPIResource
            Subsignal("sclk", Pins("AK2", dir="o")),
            Subsignal("din",  Pins("AK4", dir="o")), #I don't like having an output called DIN but it's ADC_DIN in the manual
            Subsignal("dout", Pins("AK3", dir="i")),
            Subsignal("cs",   PinsN("AJ4", dir="o")),
            Attrs(io_standard="3.3-V LVTTL"),
        ),

    ]
    connectors  = [
        # Located on the right hand side of the board
        Connector("gpio", 0,
            "AC18 Y17  AD17 Y18  AK16 AK18 AK19 AJ19 AJ17 AJ16 "
            " -    -   AH18 AH17 AG16 AE16 AF16 AG17 AA18 AA19 "
            "AE17 AC20 AH19 AJ20 AH20 AK21 AD19 AD20  -    -   "
            "AE18 AE19 AF20 AF21 AF19 AG21 AF18 AG20 AG18 AJ21 "),
        
        Connector("gpio", 1,
            "AB17 AA21 AB21 AC23 AD24 AE23 AE24 AF25 AF26 AG25 "
            "-    -    AG26 AH24 AH27 AJ27 AK29 AK28 AK27 AJ26 "
            "AK26 AH25 AJ25 AJ24 AK24 AG23 AK23 AH23  -    -   "
            "AK22 AJ22 AH22 AG22 AF24 AF23 AE22 AD21 AA20 AC22 "),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            # The @2 selects the second device in the JTAG chain, because this chip
            # puts the ARM cores first.
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename + "@2"])


if __name__ == "__main__":
    from .test.blinky import Blinky
    DE1SoCPlatform().build(Blinky(), do_program=True)
