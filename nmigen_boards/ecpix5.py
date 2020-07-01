import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ecp5 import *
from .resources import *


__all__ = ["ECPIX585Platform", "ECPIX545Platform"]


class _ECPIX5Platform(LatticeECP5Platform):
    package     = "BG554"
    speed       = "8"
    default_clk = "clk100"
    default_rst = "rst"

    resources   = [
        Resource("rst", 0, PinsN("AB1", dir="i"), Attrs(IO_TYPE="LVCMOS33")),
        Resource("clk100", 0, Pins("K23", dir="i"), Clock(100e6), Attrs(IO_TYPE="LVCMOS33")),

        RGBLEDResource(0,
            r="T23", g="R21", b="T22", invert=True,
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")
        ),
        RGBLEDResource(1,
            r="U21", g="W21", b="T24", invert=True,
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")
        ),
        RGBLEDResource(2,
            r="K21", g="K24", b="M21", invert=True,
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")
        ),
        RGBLEDResource(3,
            r="P21", g="R23", b="P22", invert=True,
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")
        ),

        UARTResource(0,
            rx="R26", tx="R24",
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")
        ),

        *SPIFlashResources(0,
            cs="AA2", clk="AE3", miso="AE2", mosi="AD2", wp="AF2", hold="AE1",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),

        Resource("eth_rgmii", 0,
            Subsignal("rst",     PinsN("C13", dir="o")),
            Subsignal("mdio",    Pins("A13", dir="io")),
            Subsignal("mdc",     Pins("C11", dir="o")),
            Subsignal("tx_clk",  Pins("A12", dir="o")),
            Subsignal("tx_ctrl", Pins("C9", dir="o")),
            Subsignal("tx_data", Pins("D8 C8 B8 A8", dir="o")),
            Subsignal("rx_clk",  Pins("E11", dir="i")),
            Subsignal("rx_ctrl", Pins("A11", dir="i")),
            Subsignal("rx_data", Pins("B11 A10 B10 A9", dir="i")),
            Attrs(IO_TYPE="LVCMOS33")
        ),
        Resource("eth_int", 0, PinsN("B13", dir="i"), Attrs(IO_TYPE="LVCMOS33")),

        Resource("ddr3", 0,
            Subsignal("clk",    DiffPairs("H3", "J3", dir="o"), Attrs(IO_TYPE="SSTL135D_I")),
            Subsignal("clk_en", Pins("P1", dir="o")),
            Subsignal("we",     PinsN("R3", dir="o")),
            Subsignal("ras",    PinsN("T3", dir="o")),
            Subsignal("cas",    PinsN("P2", dir="o")),
            Subsignal("a",      Pins("T5 M3 L3 V6 K2 W6 K3 L1 H2 L2 N1 J1 M1 K1", dir="o")),
            Subsignal("ba",     Pins("U6 N3 N4", dir="o")),
            Subsignal("dqs",    DiffPairs("V4 V1", "U5 U2", dir="io"), Attrs(IO_TYPE="SSTL135D_I")),
            Subsignal("dq",     Pins("T4 W4 R4 W5 R6 P6 P5 P4 R1 W3 T2 V3 U3 W1 T1 W2", dir="io")),
            Subsignal("dm",     Pins("U4 U1", dir="o")),
            Subsignal("odt",    Pins("P3", dir="o")),
            Attrs(IO_TYPE="SSTL135_I")
        ),

        Resource("sata", 0,
            Subsignal("tx", DiffPairs("AD16", "AD17", dir="o")),
            Subsignal("rx", DiffPairs("AF15", "AF16", dir="i")),
            Attrs(IO_TYPE="LVDS")
        ),

        Resource("ulpi", 0,
            Subsignal("rst",  Pins("E23", dir="o")),
            Subsignal("clk",  Pins("H24", dir="i")),
            Subsignal("dir",  Pins("F22", dir="i")),
            Subsignal("nxt",  Pins("F23", dir="i")),
            Subsignal("stp",  Pins("H23", dir="o")),
            Subsignal("data", Pins("M26 L25 L26 K25 K26 J23 P25 H25", dir="io")),
            Attrs(IO_TYPE="LVCMOS33")
        ),

        Resource("usbc_cfg", 0,
            Subsignal("scl", Pins("D24", dir="io")),
            Subsignal("sda", Pins("C24", dir="io")),
            Subsignal("dir", Pins("B23", dir="i")),
            Subsignal("id",  Pins("D23", dir="i")),
            Subsignal("int", PinsN("B24", dir="i")),
            Attrs(IO_TYPE="LVCMOS33")
        ),
        Resource("usbc_mux", 0,
            Subsignal("en",    Pins("C23", dir="oe")),
            Subsignal("amsel", Pins("B26", dir="oe")),
            Subsignal("pol",   Pins("D26", dir="o")),
            Subsignal("lna",   DiffPairs( "AF9", "AF10", dir="i"), Attrs(IO_TYPE="LVCMOS18D")),
            Subsignal("lnb",   DiffPairs("AD10", "AD11", dir="o"), Attrs(IO_TYPE="LVCMOS18D")),
            Subsignal("lnc",   DiffPairs( "AD7",  "AD8", dir="o"), Attrs(IO_TYPE="LVCMOS18D")),
            Subsignal("lnd",   DiffPairs( "AF6",  "AF7", dir="i"), Attrs(IO_TYPE="LVCMOS18D")),
            Attrs(IO_TYPE="LVCMOS33")
        ),
    ]

    connectors  = [
        Connector("pmod", 0, "T25 U25 U24 V24 - - T26 U26 V26 W26 - -"),
        Connector("pmod", 1, "U23 V23 U22 V21 - - W25 W24 W23 W22 - -"),
        Connector("pmod", 2, "J24 H22 E21 D18 - - K22 J21 H21 D22 - -"),
        Connector("pmod", 3, " E4  F4  E6  H4 - -  F3  D4  D5  F5 - -"),
        Connector("pmod", 4, "E26 D25 F26 F25 - - A25 A24 C26 C25 - -"),
        Connector("pmod", 5, "D19 C21 B21 C22 - - D21 A21 A22 A23 - -"),
        Connector("pmod", 6, "C16 B17 C18 B19 - - A17 A18 A19 C19 - -"),
        Connector("pmod", 7, "D14 B14 E14 B16 - - C14 A14 A15 A16 - -"),
    ]

    @property
    def file_templates(self):
        return {
            **super().file_templates,
            "{{name}}-openocd.cfg": r"""
            interface ftdi
            ftdi_vid_pid 0x0403 0x6010
            ftdi_channel 0
            ftdi_layout_init 0xfff8 0xfffb
            reset_config none
            adapter_khz 25000

            {% if "85F" in platform.device -%}
            jtag newtap ecp5 tap -irlen 8 -expected-id 0x81113043 ; # LF5UM5G-85F
            {% else -%}
            jtag newtap ecp5 tap -irlen 8 -expected-id 0x81112043 ; # LF5UM5G-45F
            {% endif %}
            """
        }

    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}-openocd.cfg".format(name), "{}.svf".format(name)) \
                as (config_filename, vector_filename):
            subprocess.check_call([openocd,
                "-f", config_filename,
                "-c", "transport select jtag; init; svf -quiet {}; exit".format(vector_filename)
            ])


class ECPIX545Platform(_ECPIX5Platform):
    device      = "LFE5UM5G-45F"

    resources   = [
        *_ECPIX5Platform.resources,

        # The IT6613E HDMI transmitter has access to 8 bits per color channel.
        Resource("it6613e", 0,
            Subsignal("rst",   PinsN("N6", dir="o")),
            Subsignal("scl",   Pins("C17", dir="io")),
            Subsignal("sda",   Pins("E17", dir="io")),
            Subsignal("pclk",  Pins("C1", dir="o")),
            Subsignal("vsync", Pins("A4", dir="o")),
            Subsignal("hsync", Pins("B4", dir="o")),
            Subsignal("de",    Pins("A3", dir="o")),
            Subsignal("d",
                Subsignal("b", Pins(" B3  C3  D3  B1  C2  D2 D1 E3", dir="o")),
                Subsignal("g", Pins(" E1  F2  F1 D17 D16 E16 J6 H6", dir="o")),
                Subsignal("r", Pins("E10 D11 D10 C10  D9  E8 H5 J4", dir="o")),
            ),
            Subsignal("mclk",  Pins("E19", dir="o")),
            Subsignal("sck",   Pins("D6", dir="o")),
            Subsignal("ws",    Pins("C6", dir="o")),
            Subsignal("i2s",   Pins("A6 B6 A5 C5", dir="o")),
            Subsignal("int",   PinsN("C4", dir="i")),
            Attrs(IO_TYPE="LVTTL33")
        ),
    ]


class ECPIX585Platform(_ECPIX5Platform):
    device      = "LFE5UM5G-85F"

    resources   = [
        *_ECPIX5Platform.resources,

        # The IT6613E HDMI transmitter has access to 12 bits per color channel. The LFE5UM5G-85F
        # has an additional I/O bank which is used to provide the lower 4 bits of each channel.
        Resource("it6613e", 0,
            Subsignal("rst",   PinsN("N6", dir="o")),
            Subsignal("scl",   Pins("C17", dir="io")),
            Subsignal("sda",   Pins("E17", dir="io")),
            Subsignal("pclk",  Pins("C1", dir="o")),
            Subsignal("vsync", Pins("A4", dir="o")),
            Subsignal("hsync", Pins("B4", dir="o")),
            Subsignal("de",    Pins("A3", dir="o")),
            Subsignal("d",
                Subsignal("b", Pins("AD25 AC26 AB24 AB25  B3  C3  D3  B1  C2  D2 D1 E3", dir="o")),
                Subsignal("g", Pins("AA23 AA22 AA24 AA25  E1  F2  F1 D17 D16 E16 J6 H6", dir="o")),
                Subsignal("r", Pins("AD26 AE25 AF25 AE26 E10 D11 D10 C10  D9  E8 H5 J4", dir="o")),
            ),
            Subsignal("mclk",  Pins("E19", dir="o")),
            Subsignal("sck",   Pins("D6", dir="o")),
            Subsignal("ws",    Pins("C6", dir="o")),
            Subsignal("i2s",   Pins("A6 B6 A5 C5", dir="o")),
            Subsignal("int",   PinsN("C4", dir="i")),
            Attrs(IO_TYPE="LVTTL33")
        ),
    ]


if __name__ == "__main__":
    import argparse
    from .test.blinky import Blinky

    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("85", "45"), default="85",
        help="platform variant (default: %(default)s)")

    args = parser.parse_args()
    if args.variant == "85":
        platform = ECPIX585Platform()
    else:
        platform = ECPIX545Platform()

    platform.build(Blinky(), do_program=True)
