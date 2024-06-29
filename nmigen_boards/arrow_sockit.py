import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *

__all__ = ["ArrowSoCKitPlatform"]

_device_map = {
    "revb" : ("5CSXFC6D6", "ES"),
    "revc" : ("5CSXFC6D6", "ES"),
    "revd" : ("5CSXFC6D6", ""),
}

class ArrowSoCKitPlatform(IntelPlatform):
    device      = None
    package     = "F31"
    speed       = "C8"
    suffix      = None
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("AF14", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="AF10 AD10 AE11 AD7",
            invert=False,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *ButtonResources(
            pins="AE9 AE12 AD9 AD11",
            invert=False,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *SwitchResources(
            pins="W25 V25 AC28 AC29",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        Resource("ddr3", 0,
            Subsignal("rst",    PinsN("AK21", dir="o")),
            Subsignal("clk",    DiffPairs("AA14", "AA15", dir="o"),
                                Attrs(io_standard="DIFFERENTIAL 1.5-V SSTL CLASS I",
                                    Misc="INPUT_TERMINATION=PARALLEL 50 OHM WITH CALIBRATION "
                                         "OUTPUT_TERMINATION=SERIES 50 OHM WITH CALIBRATION")),
            Subsignal("clk_en", Pins("AJ21", dir="o")),
            Subsignal("cs",     PinsN("AB15", dir="o")),
            Subsignal("we",     PinsN("AJ6", dir="o")),
            Subsignal("ras",    PinsN("AH8", dir="o")),
            Subsignal("cas",    PinsN("AH7", dir="o")),
            Subsignal("a",      Pins("AJ14 AK14 AH12 AJ12 AG15 AH15 AK12 AK13 "
                                     "AH13 AH14 AJ9  AK9  AK7  AK8  AG12", dir="o"),
                                Attrs(io_standard="SSTL15")),
            Subsignal("ba",     Pins("AH10 AJ11 AK11", dir="o")),
            Subsignal("dqs",    DiffPairs("V16 V17 Y17 AC20", "W16 W17 AA18 AD19", dir="io"),
                                Attrs(io_standard="DIFFERENTIAL 1.5-V SSTL CLASS I",
                                      Misc="INPUT_TERMINATION=PARALLEL 50 OHM WITH CALIBRATION "
                                           "OUTPUT_TERMINATION=SERIES 50 OHM WITH CALIBRATION")),
            Subsignal("dq",     Pins("AF18 AE17 AG16 AF16 AH20 AG21 AJ16 AH18 "
                                     "AK18 AJ17 AG18 AK19 AG20 AF19 AJ20 AH24 "
                                     "AE19 AE18 AG22 AK22 AF21 AF20 AH23 AK24 "
                                     "AF24 AF23 AJ24 AK26 AE23 AE22 AG25 AK27", dir="io"),
                                Attrs(io_standard="SSTL-15 CLASS I",
                                      Misc="INPUT_TERMINATION=PARALLEL 50 OHM WITH CALIBRATION "
                                           "OUTPUT_TERMINATION=SERIES 50 OHM WITH CALIBRATION")),
            Subsignal("dm",     Pins("AH17 AG23 AK23 AJ27", dir="o"),
                                Attrs(io_standard="SSTL-15 CLASS I",
                                      Misc="OUTPUT_TERMINATION=SERIES 50 OHM WITH CALIBRATION")),
            Subsignal("odt",    Pins("AE16", dir="o")),
            Attrs(io_standard="SSTL-15 CLASS I")),

        Resource("vga", 0,
            Subsignal("sync",    PinsN("AG2")),
            Subsignal("blank",   PinsN("AH3")),
            Subsignal("clk",     Pins("W20")),
            Subsignal("hsync",   PinsN("AD12")),
            Subsignal("vsync",   PinsN("AC12")),
            Subsignal("r",       Pins("AG5  AA12 AB12 AF6  AG6  AJ2  AH5  AJ1")),
            Subsignal("g",       Pins("Y21  AA25 AB26 AB22 AB23 AA24 AB25 AE27")),
            Subsignal("b",       Pins("AE28 Y23  Y24  AG28 AF28 V23  W24  AF29")),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("irda", 0,
            Subsignal("irda_rxd", Pins("AH2")),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("temperature", 0,
            Subsignal("temp_cs",   PinsN("AF8")),
            Subsignal("temp_din",  Pins("AG7")),
            Subsignal("temp_dout", Pins("AG1")),
            Subsignal("temp_sclk", Pins("AF9")),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("audio", 0,
            Subsignal("aud_adclrck",  Pins("AG30")),
            Subsignal("aud_adcdat",   Pins("AC27")),
            Subsignal("aud_daclrck",  Pins("AH4")),
            Subsignal("aud_dacdat",   Pins("AG3")),
            Subsignal("aud_xck",      Pins("AC9")),
            Subsignal("aud_bclk",     Pins("AE7")),
            Subsignal("aud_i2c_sclk", Pins("AH30")),
            Subsignal("aud_i2c_sdat", Pins("AF30")),
            Subsignal("aud_mute",     Pins("AD26")),
            Attrs(io_standard="3.3-V LVTTL")),
    ]

    connectors  = [ ]

    gpio_daughterboard_connectors = [
        Connector("J", 2, "- G15 F14 H15 F15 A13 G13 B13 H14 B11 E13 - - "
            "C12 F13 B8 B12 C8 C13 A10 D10 A11 D11 B7 D12 C7 E12 A5 D9 - - "
            "A6 E9 A3 B5 A4 B6 B1 C2 B2 D2"),
        # Top to bottom, starting with 57.
        Connector("JP", 2, "- D1 E1 E11 F11"),

        Connector("J", 3, "- AB27 F8 AA26 F9 B3 G8 C3 H8 D4 H7 - - "
            "E4 J7 E2 K8 E3 K7 E6 J9 E7 J10 C4 J12 D5 G10 C5 J12 - - "
            "D6 K12 F6 G11 G7 G12 D7 A8 E8 A9"),
        # Top to bottom, starting with 117.
        Connector("JP", 3, "- C9 C10 H12 H13"),

        Connector("J", 4, "- - - AD3 AE1 AD4 AE2 - - AB3 AC1 - - "
            "AB4 AC2 - - Y3 AA1 Y4 AA2 - - V3 W1 V4 W2 - - - -"
            "T3 U1 T4 R1 - R2 P3 U2 P4 -"),
         # Top to bottom, starting with 169.
        Connector("JP", 4, "- M3 M4 - H3 H4 J14 AD29 - N1 N2 - J1 J2")
    ]

    def __init__(self, *, toolchain="Quartus",
                 revision="revd",
                 with_gpio_daughterboard=False,
                 with_mister_sdram=False):

        self.device, self.suffix = _device_map[revision]
        if with_gpio_daughterboard:
            self.connectors.append(self.gpio_daughterboard_connectors)
            self.resources.append(Resource("gpio_serial", 0,
                                           Subsignal("tx", Pins("J_3:9")),
                                           Subsignal("rx", Pins("J_3:10")),
                                           Attrs(io_standard="3.3-V LVTTL")))

        if with_mister_sdram:
            self.resources.append(SDRAMResource(0,
                clk="D10", cke="B3", cs_n="A3", we_n="A5", ras_n="E9", cas_n="A6",
                ba="B5 A4", a="B1 C2 B2 D2 D9 C7 E12 B7 D12 A11 B6 D11 A10",
                dq="F14 G15 F15 H15 G13 A13 H14 B13 C13 C8 B12 B8 F13 C12 B11 E13",
                dqm="AB27 AA26",
                attrs=Attrs(io_standard="3.3-V LVCMOS")))

        super().__init__(toolchain=toolchain)

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG", "-c", "CV SoCKit",
                                                "--operation", "P;" + bitstream_filename])

if __name__ == "__main__":
    from .test.blinky import Blinky
    ArrowSoCKitPlatform().build(Blinky(), do_program=True)
