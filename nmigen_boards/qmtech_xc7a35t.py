import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from nmigen_boards.resources import *
from nmigen_boards.qmtech_daughterboard import QMTechDaughterboard

__all__ = ["QMTechXC7A35TCorePlatform"]

class QMTechXC7A35TPlatform(Xilinx7SeriesPlatform):
    device      = "xc7a35t"
    package     = "ftg256"
    speed       = "1"
    default_clk = "clk50"
    default_rst = "rst"

    def __init__(self, standalone=True, toolchain="Vivado"):
        if not standalone:
            # D3 - we do not use LEDResources here, because there are five LEDs
            # on the daughterboard and this will then clash with those
            self.resources[2] = Resource("core_led", 0, PinsN("E6"), Attrs(IOSTANDARD="LVCMOS33"))
            daughterboard = QMTechDaughterboard(Attrs(IOSTANDARD="LVCMOS33"))
            self.connectors += daughterboard.connectors
            self.resources  += daughterboard.resources

        super().__init__(toolchain=toolchain)

    resources   = [
        Resource("clk50", 0, Pins("N11", dir="i"),
                 Clock(50e6), Attrs(IOSTANDARD="LVCMOS33")),

        # SW2
        Resource("rst", 0, PinsN("K5", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(
            pins="E6", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

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
             "7": "M12",   "8": "N13",
             "9": "N14",  "10": "N16",
            "11": "P15",  "12": "P16",
            "13": "R15",  "14": "R16",
            "15": "T14",  "16": "T15",
            "17": "P13",  "18": "P14",
            "19": "T13",  "20": "R13",
            "21": "T12",  "22": "R12",
            "23": "L13",  "24": "N12",
            "25": "K12",  "26": "K13",
            "27": "P10",  "28": "P11",
            "29": "N9",   "30": "P9",
            "31": "T10",  "32": "R11",
            "33": "T9",   "34": "R10",
            "35": "T8",   "36": "R8",
            "37": "T7",   "38": "R7",
            "39": "T5",   "40": "R6",
            "41": "P6",   "42": "R5",
            "43": "N6",   "44": "M6",
            "45": "L5",   "46": "P5",
            "47": "T4",   "48": "T3",
            "49": "R3",   "50": "T2",
            "51": "R2",   "52": "R1",
            "53": "M5",   "54": "N4",
            "55": "P4",   "56": "P3",
            "57": "N1",   "58": "P1",
            "59": "M2",   "60": "M1",
        }),

        Connector("J", 3, {
            # odd row     even row
             "7": "B7",   "8": "A7",
             "9": "B6",  "10": "B5",
            "11": "E6",  "12": "K5",
            "13": "J5",  "14": "J4",
            "15": "G5",  "16": "G4",
            "17": "C7",  "18": "C6",
            "19": "D6",  "20": "D5",
            "21": "A5",  "22": "A4",
            "23": "B4",  "24": "A3",
            "25": "D4",  "26": "C4",
            "27": "C3",  "28": "C2",
            "29": "B2",  "30": "A2",
            "31": "C1",  "32": "B1",
            "33": "E2",  "34": "D1",
            "35": "E3",  "36": "D3",
            "37": "F5",  "38": "E5",
            "39": "F2",  "40": "E1",
            "41": "F4",  "42": "F3",
            "43": "G2",  "44": "G1",
            "45": "H2",  "46": "H1",
            "47": "K1",  "48": "J1",
            "49": "L3",  "50": "L2",
            "51": "H5",  "52": "H4",
            "53": "J3",  "54": "H3",
            "55": "K3",  "56": "K2",
            "57": "L4",  "58": "M4",
            "59": "N3",  "60": "N2",
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
                set_property INTERNAL_VREF 0.675 [get_iobanks 15]
                set_property CFGBVS VCCO [current_design]
                set_property CONFIG_VOLTAGE 3.3 [current_design]
                """
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        loader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([loader, "-v", "-c", "ft232", bitstream_filename], check=True)


if __name__ == "__main__":
    from nmigen_boards.test.blinky import *
    QMTechXC7A35TPlatform(standalone=True).build(Blinky(), do_program=True)
