import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from nmigen_boards.resources import *


__all__ = ["QMTechXC7A35TCorePlatform"]

class QMTechXC7A35TCorePlatform(Xilinx7SeriesPlatform):
    device      = "xc7a35t"
    package     = "ftg256"
    speed       = "1"
    default_clk = "clk50"
    default_rst = "rst"

    def __init__(self, standalone=True):
        if (not standalone):
            # D3 - we do not use LEDResources here, because there are five LEDs
            # on the daughterboard and this will then clash with those
            self.resources[2] = Resource("core_led", 0, PinsN("E6"), Attrs(IOSTANDARD="LVCMOS33"))
        super().__init__()

    resources   = [
        Resource("clk50", 0, Pins("N11", dir="i"),
                 Clock(50e6), Attrs(IOSTANDARD="LVCMOS33")),

        # SW2
        Resource("rst", 0, PinsN("K5", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(
            pins="E6", invert=True,
            attrs=Attrs(io_standard="LVCMOS33")),

        # MT25QL128
        Resource("qspi_flash", 0,
            Subsignal("cs",        PinsN("L12")),
            Subsignal("clk",       Pins("E8")),
            Subsignal("dq",        Pins("J13 J14 K15 K16")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # MT41J128M16JT-125K
        Resource("ddr3", 0,
            Subsignal("rst",    PinsN("E15", dir="o")),
            Subsignal("clk",    DiffPairs("B9", "A10", dir="o"), Attrs(IOSTANDARD="DIFF_SSTL135")),
            Subsignal("clk_en", Pins("D13", dir="o")),
            Subsignal("cs",     PinsN("-", dir="o")),
            Subsignal("we",     PinsN("C12", dir="o")),
            Subsignal("ras",    PinsN("B16", dir="o")),
            Subsignal("cas",    PinsN("C11", dir="o")),
            Subsignal("a",      Pins("B14 C8 A14 C14 C9 B10 D9 A12 D8 A13 B12 A9 A8 B11", dir="o")),
            Subsignal("ba",     Pins("C16 A15 B15", dir="o")),
            Subsignal("dqs",    DiffPairs("D14 D15", "G14 F14", dir="io"),
                                Attrs(IOSTANDARD="DIFF_SSTL135")),
            Subsignal("dq",     Pins("F15 F13 E16 D11 E12 E13 D16 E11 G12 J16 G16 J15 H14 H12 H16 H13", dir="io"),
                                Attrs(IN_TERM="UNTUNED_SPLIT_40")),
            Subsignal("dm",     Pins("F12 H11", dir="o")),
            Subsignal("odt",    Pins("C13", dir="o")),
            Attrs(IOSTANDARD="SSTL135", SLEW="FAST"),
        ),
    ]

    # The connectors are named after the daughterboard, not the core board
    # because on the different core boards the names vary, but on the
    # daughterboard they stay the same, which we need to connect the
    # daughterboard peripherals to the core board.
    # On this board J2 is U7 and J3 is U8
    connectors  = [
        Connector("J", 2, {
             # odd row     even row
             "5": "M12",   "6": "N13",
             "7": "N14",   "8": "N16",
             "9": "P15",  "10": "P16",
            "11": "R15",  "12": "R16",
            "13": "T14",  "14": "T15",
            "15": "P13",  "16": "P14",
            "17": "T13",  "18": "R13",
            "19": "T12",  "20": "R12",
            "21": "L13",  "22": "N12",
            "23": "K12",  "24": "K13",
            "25": "P10",  "26": "P11",
            "27": "N9",   "28": "P9",
            "29": "T10",  "30": "R11",
            "31": "T9",   "32": "R10",
            "33": "T8",   "34": "R8",
            "35": "T7",   "36": "R7",
            "37": "T5",   "38": "R6",
            "39": "P6",   "40": "R5",
            "41": "N6",   "42": "M6",
            "43": "L5",   "44": "P5",
            "45": "T4",   "46": "T3",
            "47": "R3",   "48": "T2",
            "49": "R2",   "50": "R1",
            "51": "M5",   "52": "N4",
            "53": "P4",   "54": "P3",
            "55": "N1",   "56": "P1",
            "57": "M2",   "58": "M1",
        }),

        Connector("J", 3, {
            # odd row     even row
             "5": "B7",   "6": "A7",
             "7": "B6",   "8": "B5",
             "9": "E6",  "10": "K5",
            "11": "J5",  "12": "J4",
            "13": "G5",  "14": "G4",
            "15": "C7",  "16": "C6",
            "17": "D6",  "18": "D5",
            "19": "A5",  "20": "A4",
            "21": "B4",  "22": "A3",
            "23": "D4",  "24": "C4",
            "25": "C3",  "26": "C2",
            "27": "B2",  "28": "A2",
            "29": "C1",  "30": "B1",
            "31": "E2",  "32": "D1",
            "33": "E3",  "34": "D3",
            "35": "F5",  "36": "E5",
            "37": "F2",  "38": "E1",
            "39": "F4",  "40": "F3",
            "41": "G2",  "42": "G1",
            "43": "H2",  "44": "H1",
            "45": "K1",  "46": "J1",
            "47": "L3",  "48": "L2",
            "49": "H5",  "50": "H4",
            "51": "J3",  "52": "H3",
            "53": "K3",  "54": "K2",
            "55": "L4",  "56": "M4",
            "57": "N3",  "58": "N2",
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
                """
                set_property INTERNAL_VREF 0.675 [get_iobanks 34]
                set_property CFGBVS VCCO [current_design]
                set_property CONFIG_VOLTAGE 3.3 [current_design]
                """
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        xc3sprog = os.environ.get("XC3SPROG", "xc3sprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([xc3sprog, "-v", "-c", "ft232h", bitstream_filename], check=True)


if __name__ == "__main__":
    from nmigen_boards.test.blinky import *
    QMTechXC7A35TCorePlatform().build(Blinky(), do_program=True)
