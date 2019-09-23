import subprocess
import textwrap

from nmigen.build import *
from nmigen.vendor.xilinx_spartan_3_6 import *
from .dev import *


__all__ = ["AtlysPlatform"]


class AtlysPlatform(XilinxSpartan6Platform):
    """Platform file for Digilent Atlys Spartan 6 board.
    https://reference.digilentinc.com/reference/programmable-logic/atlys/start"""

    device  = "xc6slx45"
    package = "csg324"
    speed   = "3"

    def __init__(self, *, JP12="2V5", **kwargs):
        super().__init__(**kwargs)

        assert JP12 in ["2V5", "3V3"]
        self._JP12 = JP12

    def bank2_iostandard(self):
        return "LVCMOS25" if self._JP12 == "2V5" else "LVCMOS33"

    default_clk = "clk100"
    resources   = [
        Resource("clk100", 0, Pins("L15",  dir="i"),
                 Clock(100e6), Attrs(IOSTANDARD="LVCMOS33")), # GCLK

        Resource("led",    0, Pins("U18",  dir="o"), Attrs(IOSTANDARD="LVCMOS33")),       # LD0
        Resource("led",    1, Pins("M14",  dir="o"), Attrs(IOSTANDARD="LVCMOS33")),       # LD1
        Resource("led",    2, Pins("N14",  dir="o"), Attrs(IOSTANDARD="LVCMOS33")),       # LD2
        Resource("led",    3, Pins("L14",  dir="o"), Attrs(IOSTANDARD="LVCMOS33")),       # LD3
        Resource("led",    4, Pins("M13",  dir="o"), Attrs(IOSTANDARD="LVCMOS33")),       # LD4
        Resource("led",    5, Pins("D4",   dir="o"), Attrs(IOSTANDARD="LVCMOS33")),       # LD5
        Resource("led",    6, Pins("P16",  dir="o"), Attrs(IOSTANDARD="LVCMOS33")),       # LD6
        Resource("led",    7, Pins("N12",  dir="o"), Attrs(IOSTANDARD=bank2_iostandard)), # LD7

        Resource("button", 0, PinsN("T15", dir="i"), Attrs(IOSTANDARD=bank2_iostandard)), # RESET
        Resource("reset",  0, PinsN("T15", dir="i"), Attrs(IOSTANDARD=bank2_iostandard)), # RESET
        Resource("button", 1, Pins("N4",   dir="i"), Attrs(IOSTANDARD="LVCMOS18")),       # BTNU
        Resource("button", 2, Pins("P4",   dir="i"), Attrs(IOSTANDARD="LVCMOS18")),       # BTNL
        Resource("button", 3, Pins("P3",   dir="i"), Attrs(IOSTANDARD="LVCMOS18")),       # BTND
        Resource("button", 4, Pins("F6",   dir="i"), Attrs(IOSTANDARD="LVCMOS18")),       # BTNR
        Resource("button", 5, Pins("F5",   dir="i"), Attrs(IOSTANDARD="LVCMOS18")),       # BTNC

        Resource("switch", 0, Pins("A10",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),       # SW0
        Resource("switch", 1, Pins("D14",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),       # SW1
        Resource("switch", 2, Pins("C14",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),       # SW2
        Resource("switch", 3, Pins("P15",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),       # SW3
        Resource("switch", 4, Pins("P12",  dir="i"), Attrs(IOSTANDARD=bank2_iostandard)), # SW4
        Resource("switch", 5, Pins("R5",   dir="i"), Attrs(IOSTANDARD=bank2_iostandard)), # SW5
        Resource("switch", 6, Pins("T5",   dir="i"), Attrs(IOSTANDARD=bank2_iostandard)), # SW6
        Resource("switch", 7, Pins("E4",   dir="i"), Attrs(IOSTANDARD="LVCMOS18")),       # SW7

        UARTResource(0, rx="A16", tx="B16", attrs=Attrs(IOSTANDARD="LVCMOS33")), # J17/UART

        Resource("ps2", 0, # PS/2 keyboard interface converted from J13 "HOST" USB connector
            Subsignal("clk",    Pins("P17", dir="i")),
            Subsignal("dat",    Pins("N15", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33"),
        ),
        Resource("ps2", 1, # PS/2 mouse interface converted from J13 "HOST" USB connector
            Subsignal("clk",    Pins("N18", dir="i")),
            Subsignal("dat",    Pins("P18", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33"),
        ),

        *SPIFlashResources(0,
            cs="AE14", clk="AH18", mosi="AF14", miso="AF20", wp="AG21", hold="AG17",
            attrs=Attrs(IOSTANDARD="LVCMOS25", SLEW="FAST"),
        ),

        Resource("ddr2", 0,
            Subsignal("clk",    DiffPairs("G3", "G1", dir="o"),
                                Attrs(IOSTANDARD="DIFF_SSTL18_II", IN_TERM="NONE")),
            Subsignal("clk_en", Pins("H7", dir="o")),
            Subsignal("we",     PinsN("E3", dir="o")),
            Subsignal("ras",    PinsN("L5", dir="o")),
            Subsignal("cas",    PinsN("K5", dir="o")),
            Subsignal("a",      Pins("J7 J6 H5 L7 F3 H4 H3 H6 D2 D1 F4 D3 G6", dir="o")),
            Subsignal("ba",     Pins("F2 F1 E1", dir="o")),
            Subsignal("dqs",    DiffPairs("P2 L4", "P1 L3", dir="o"),
                                Attrs(IOSTANDARD="DIFF_SSTL18_II")),
            Subsignal("dq",     Pins("L2 L1 K2 K1 H2 H1 J3 J1 M3 M1 N2 N1 T2 T1 U2 U1", dir="io")),
            Subsignal("dm",     Pins("K4 K3", dir="o")),
            Subsignal("odt",    Pins("K6", dir="o")),
            Attrs(IOSTANDARD="SSTL18_II", SLEW="FAST"),
        ),

        Resource("eth_gmii", 0,
            Subsignal("rst",     PinsN("G13", dir="o")),
            Subsignal("int",     PinsN("L16", dir="o")),
            Subsignal("mdio",    Pins("N17", dir="io")),
            Subsignal("mdc",     Pins("F16", dir="o")), # Max 8.3MHz
            Subsignal("gtx_clk", Pins("L12", dir="o")),
            Subsignal("tx_clk",  Pins("K16", dir="i")),
            Subsignal("tx_en",   Pins("H15", dir="o")),
            Subsignal("tx_er",   Pins("G18", dir="o")),
            Subsignal("tx_data", Pins("H16 H13 K14 K13 J13 G14 H12 K12", dir="o")),
            Subsignal("rx_clk",  Pins("K15", dir="i")),
            Subsignal("rx_dv",   Pins("F17", dir="i"), Attrs(PULLDOWN="TRUE")),
            Subsignal("rx_er",   Pins("F18", dir="i")),
            Subsignal("rx_data", Pins("G16 H14 E16 F15 F14 E18 D16 D17", dir="i")),
            Subsignal("col",     Pins("C17", dir="i")),
            Subsignal("crs",     Pins("C18", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),
        Resource("eth_rgmii", 0,
            Subsignal("rst",     PinsN("G13", dir="o")),
            Subsignal("int",     PinsN("L16", dir="o")),
            Subsignal("mdio",    Pins("N17", dir="io")),
            Subsignal("mdc",     Pins("F16", dir="o")), # Max 8.3MHz
            Subsignal("tx_clk",  Pins("L12", dir="o")),
            Subsignal("tx_ctl",  Pins("H15", dir="o")),
            Subsignal("tx_data", Pins("H16 H13 K14 K13", dir="o")),
            Subsignal("rx_clk",  Pins("K15", dir="i")),
            Subsignal("rx_ctl",  Pins("F17", dir="i"), Attrs(PULLDOWN="TRUE")),
            Subsignal("rx_data", Pins("G16 H14 E16 F15", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),
        Resource("eth_mii", 0,
            Subsignal("rst",     PinsN("G13", dir="o")),
            Subsignal("int",     PinsN("L16", dir="o")),
            Subsignal("mdio",    Pins("N17", dir="io")),
            Subsignal("mdc",     Pins("F16", dir="o")), # Max 8.3MHz
            Subsignal("tx_clk",  Pins("K16", dir="i")),
            Subsignal("tx_en",   Pins("H15", dir="o")),
            Subsignal("tx_er",   Pins("G18", dir="o")),
            Subsignal("tx_data", Pins("H16 H13 K14 K13", dir="o")),
            Subsignal("rx_clk",  Pins("K15", dir="i")),
            Subsignal("rx_dv",   Pins("F17", dir="i"), Attrs(PULLDOWN="TRUE")),
            Subsignal("rx_er",   Pins("F18", dir="i")),
            Subsignal("rx_data", Pins("G16 H14 E16 F15", dir="i")),
            Subsignal("col",     Pins("C17", dir="i")),
            Subsignal("crs",     Pins("C18", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),
        # Device does not support RMII
        Resource("eth_tbi", 0,
            Subsignal("rst",     PinsN("G13", dir="o")),
            Subsignal("int",     PinsN("L16", dir="o")),
            Subsignal("mdio",    Pins("N17", dir="io")),
            Subsignal("mdc",     Pins("F16", dir="o")), # Max 8.3MHz
            Subsignal("tx_clk",  Pins("L12", dir="o")),
            Subsignal("tx_data", Pins("H16 H13 K14 K13 J13 G14 H12 K12 H15 G18", dir="o")),
            Subsignal("rx_clk",  Pins("K15 L12", dir="i")),
            Subsignal("rx_data", Pins("G16 H14 E16 F15 F14 E18 D16 D17 F17 F18", dir="i")),
            Subsignal("lpbk",    Pins("C17", dir="o"), Attrs(PULLDOWN="TRUE")),
            Subsignal("comma",   Pins("C18", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),
        Resource("eth_rtbi", 0,
            Subsignal("rst",     PinsN("G13", dir="o")),
            Subsignal("int",     PinsN("L16", dir="o")),
            Subsignal("mdio",    Pins("N17", dir="io")),
            Subsignal("mdc",     Pins("F16", dir="o")), # Max 8.3MHz
            Subsignal("tx_clk",  Pins("L12", dir="o")),
            Subsignal("tx_data", Pins("H16 H13 K14 K13 H15", dir="o")),
            Subsignal("rx_clk",  Pins("K15", dir="i")),
            Subsignal("rx_data", Pins("G16 H14 E16 F15 F17", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        Resource("hdmi", 0, # J1, input only due to on board buffer, HDMI A connector
            Subsignal("scl",     Pins("C13"), Attrs(IOSTANDARD="I2C")),
            Subsignal("sda",     Pins("A13"), Attrs(IOSTANDARD="I2C")),
            Subsignal("clk",     DiffPairs("D11", "C11", dir="i")),
            Subsignal("d",       DiffPairs("G9 B11 B12", "F9 A11 A12", dir="i")),
            Attrs(IOSTANDARD="TMDS_33"),
        ),
        Resource("hdmi", 1, # J2, output only due to on board buffer, HDMI A connector
            Subsignal("scl",     Pins("D9"), Attrs(IOSTANDARD="I2C")),
            Subsignal("sda",     Pins("C9"), Attrs(IOSTANDARD="I2C")),
            Subsignal("clk",     DiffPairs("B6", "A6", dir="o")),
            Subsignal("d",       DiffPairs("D8 C7 B8", "C8 A7 A8", dir="o")),
            Attrs(IOSTANDARD="TMDS_33"),
        ),
        Resource("hdmi", 2, # J3, input only due to on board buffer, HDMI A connector
            Subsignal("scl",     Pins("M16"), Attrs(IOSTANDARD="I2C")),
            Subsignal("sda",     Pins("M18"), Attrs(IOSTANDARD="I2C")),
            Subsignal("clk",     DiffPairs("H17", "H18", dir="i")),
            Subsignal("d",       DiffPairs("K17 L17 J16", "K18 L18 J18", dir="i")),
            Attrs(IOSTANDARD="TMDS_33"),
        ),
        Resource("hdmi", 3, # JA, input/output as it is unbuffered, HDMI D connector
            Subsignal("scl",     Pins("C13"), Attrs(IOSTANDARD="I2C")),
            Subsignal("sda",     Pins("A13"), Attrs(IOSTANDARD="I2C")),
            Subsignal("clk",     DiffPairs("T9", "V9")),
            Subsignal("d",       DiffPairs("R3 T4 N5", "T3 V4 P6")),
            Attrs(IOSTANDARD="TMDS_33"),
        ),

        Resource("ac97", 0,
            Subsignal("clk",     Pins("L13", dir="o")),
            Subsignal("sync",    Pins("U17", dir="o")),
            Subsignal("reset",   Pins("T17", dir="o")),
            Subsignal("sdo",     Pins("N18", dir="o")),
            Subsignal("sdi",     Pins("T18", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),
    ]
    connectors  = [
        Connector("pmod", 0, "T3 R3 P6 N5 - - V9 T9 V4 T4 - -"), # JB

        Connector("vhdci", 0, # JC
            "U16 - U15 U13 - M11 R11 - T12 N10 - M10 U11 - R10 - - - - U10 - R8  M8  - U8  U7  - N7  T6  - R7  N6  - U5 "
            "V16 - V15 V13 - N11 T11 - V12 P11 - N9  V11 - T10 - - - - V10 - T8  N8  - V8  V7  - P8  V6  - T7  P7  - V5 "
        ),
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.bit".format(name)) as bitfile:
            cmd = textwrap.dedent("""
                setMode -bscan
                setCable -port auto
                addDevice -p 1 -file "{}"
                program -p 1
                exit
            """).format(bitfile).encode('utf-8')
            subprocess.run(["impact", "-batch"], input=cmd, check=True)


if __name__ == "__main__":
    from .test.blinky import *
    AtlysPlatform().build(Blinky(), do_program=True)
