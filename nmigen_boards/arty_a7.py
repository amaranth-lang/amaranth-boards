import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from .dev import *


__all__ = ["ArtyA7Platform"]


class ArtyA7Platform(Xilinx7SeriesPlatform):
    device      = "xc7a35ti"
    package     = "csg324"
    speed       = "1L"
    default_clk = "clk100"
    resources   = [
        Resource("clk100", 0, Pins("E3", dir="i"),
                 Clock(100e6), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(pins="H5 J5 T9 T10", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        RGBLEDResource(0, r="G6", g="F6", b="E1", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        RGBLEDResource(1, r="G3", g="J4", b="G4", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        RGBLEDResource(2, r="J3", g="J2", b="H4", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        RGBLEDResource(3, r="K1", g="H6", b="K2", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(pins="D9  C9  B9  B8 ", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        *SwitchResources(pins="A8  C11 C10 A10", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        UARTResource(0,
            rx="A9", tx="D10",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        Resource("cpu_reset", 0, Pins("C2", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),

        SPIResource(0,
            cs="C1", clk="F1", mosi="H1", miso="G1",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        Resource("i2c", 0,
            Subsignal("scl",        Pins("L18", dir="io")),
            Subsignal("sda",        Pins("M18", dir="io")),
            Subsignal("scl_pullup", Pins("A14", dir="o")),
            Subsignal("sda_pullup", Pins("A13", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        *SPIFlashResources(0,
            cs="L13", clk="L16", mosi="K17", miso="K18", wp="L14", hold="M14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        Resource("ddr3", 0,
            Subsignal("rst",    PinsN("K6", dir="o")),
            Subsignal("clk",    DiffPairs("U9", "V9", dir="o"), Attrs(IOSTANDARD="DIFF_SSTL135")),
            Subsignal("clk_en", Pins("N5", dir="o")),
            Subsignal("cs",     PinsN("U8", dir="o")),
            Subsignal("we",     PinsN("P5", dir="o")),
            Subsignal("ras",    PinsN("P3", dir="o")),
            Subsignal("cas",    PinsN("M4", dir="o")),
            Subsignal("a",      Pins("R2 M6 N4 T1 N6 R7 V6 U7 R8 V7 R6 U6 T6 T8", dir="o")),
            Subsignal("ba",     Pins("R1 P4 P2", dir="o")),
            Subsignal("dqs",    DiffPairs("N2 U2", "N1 V2", dir="io"),
                                Attrs(IOSTANDARD="DIFF_SSTL135")),
            Subsignal("dq",     Pins("K5 L3 K3 L6 M3 M1 L4 M2 V4 T5 U4 V5 V1 T3 U3 R3", dir="io"),
                                Attrs(IN_TERM="UNTUNED_SPLIT_40")),
            Subsignal("dm",     Pins("L1 U1", dir="o")),
            Subsignal("odt",    Pins("R5", dir="o")),
            Attrs(IOSTANDARD="SSTL135", SLEW="FAST"),
        ),

        Resource("eth_clk25", 0, Pins("G18", dir="o"),
                 Clock(25e6), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("eth_clk50", 0, Pins("G18", dir="o"),
                 Clock(50e6), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("eth_mii", 0,
            Subsignal("rst",     PinsN("C16", dir="o")),
            Subsignal("mdio",    Pins("K13", dir="io")),
            Subsignal("mdc",     Pins("F16", dir="o")),
            Subsignal("tx_clk",  Pins("H16", dir="i")),
            Subsignal("tx_en",   Pins("H15", dir="o")),
            Subsignal("tx_data", Pins("H14 J14 J13 H17", dir="o")),
            Subsignal("rx_clk",  Pins("F15", dir="i")),
            Subsignal("rx_dv",   Pins("G16", dir="i"), Attrs(PULLDOWN="TRUE")), # strap to select MII
            Subsignal("rx_er",   Pins("C17", dir="i")),
            Subsignal("rx_data", Pins("D18 E17 E18 G17", dir="i")),
            Subsignal("col",     Pins("D17", dir="i")),
            Subsignal("crs",     Pins("G14", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),
        Resource("eth_rmii", 0,
            Subsignal("rst",       PinsN("C16", dir="o")),
            Subsignal("mdio",      Pins("K13", dir="io")),
            Subsignal("mdc",       Pins("F16", dir="o")),
            Subsignal("tx_en",     Pins("H15", dir="o")),
            Subsignal("tx_data",   Pins("H14 J14", dir="o")),
            Subsignal("rx_crs_dv", Pins("G14", dir="i")),
            Subsignal("rx_dv",     Pins("G16", dir="i"), Attrs(PULLUP="TRUE")), # strap to select RMII
            Subsignal("rx_er",     Pins("C17", dir="i")),
            Subsignal("rx_data",   Pins("D18 E17", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        )
    ]
    connectors  = [
        Connector("pmod", 0, "G13 B11 A11 D12 - - D13 B18 A18 K16 - -"), # JA
        Connector("pmod", 1, "E15 E16 D15 C15 - - J17 J18 K15 J15 - -"), # JB
        Connector("pmod", 2, "U12 V12 V10 V11 - - U14 V14 T13 U13 - -"), # JC
        Connector("pmod", 3, " D4  D3  F4  F3 - -  E2  D2  H2  G2 - -"), # JD

        Connector("ck_io", 0, {
            # Outer Digital Header
            "io0":  "V15",
            "io1":  "U16",
            "io2":  "P14",
            "io3":  "T11",
            "io4":  "R12",
            "io5":  "T14",
            "io6":  "T15",
            "io7":  "T16",
            "io8":  "N15",
            "io9":  "M16",
            "io10": "V17",
            "io11": "U18",
            "io12": "R17",
            "io13": "P17",

            # Inner Digital Header
            "io26": "U11",
            "io27": "V16",
            "io28": "M13",
            "io29": "R10",
            "io30": "R11",
            "io31": "R13",
            "io32": "R15",
            "io33": "P15",
            "io34": "R16",
            "io35": "N16",
            "io36": "N14",
            "io37": "U17",
            "io38": "T18",
            "io39": "R18",
            "io40": "P18",
            "io41": "N17",

            # Outer Analog Header as Digital IO
            "a0": "F5",
            "a1": "D8",
            "a2": "C7",
            "a3": "E7",
            "a4": "D7",
            "a5": "D5",

            # Inner Analog Header as Digital IO
            "io20": "B7",
            "io21": "B6",
            "io22": "E6",
            "io23": "E5",
            "io24": "A4",
            "io25": "A3"
        }),
        Connector("xadc", 0, {
            # Outer Analog Header
            "vaux4_n":   "C5",
            "vaux4_p":   "C6",
            "vaux5_n":   "A5",
            "vaux5_p":   "A6",
            "vaux6_n":   "B4",
            "vaux6_p":   "C4",
            "vaux7_n":   "A1",
            "vaux7_p":   "B1",
            "vaux15_n":  "B2",
            "vaux15_p":  "B3",
            "vaux0_n":  "C14",
            "vaux0_p":  "D14",

            # Inner Analog Header
            "vaux12_n": "B7",
            "vaux12_p": "B6",
            "vaux13_n": "E6",
            "vaux13_p": "E5",
            "vaux14_n": "A4",
            "vaux14_p": "A3",

            # Power Measurements
            "vsnsuv_n":   "B17",
            "vsnsuv_p":   "B16",
            "vsns5v0_n":  "B12",
            "vsns5v0_p":  "C12",
            "isns5v0_n":  "F14",
            "isns5v0_n":  "F13",
            "isns0v95_n": "A16",
            "isns0v95_n": "A15",
        })
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_before_bitstream":
                "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "script_after_bitstream":
                "write_cfgmem -force -format bin -interface spix4 -size 16 "
                "-loadbit \"up 0x0 {name}.bit\" -file {name}.bin".format(name=name),
            "add_constraints":
                "set_property INTERNAL_VREF 0.675 [get_iobanks 34]"
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        xc3sprog = os.environ.get("XC3SPROG", "xc3sprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([xc3sprog, "-c", "nexys4", bitstream_filename], check=True)


if __name__ == "__main__":
    from .test.blinky import *
    ArtyA7Platform().build(Blinky(), do_program=True)
