import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from nmigen_boards.resources import *
from nmigen_boards.qmtech_daughterboard import QMTechDaughterboard


__all__ = ["QMTech5CEFA2Platform"]


class QMTech5CEFA2Platform(IntelPlatform):
    device      = "5CEFA2"
    package     = "F23"
    speed       = "C8"
    default_clk = "clk50"

    def __init__(self, standalone=True):
        if not standalone:
            # D3 - we do not use LEDResources/ButtonResources here, because there are five LEDs
            # on the daughterboard and this will then clash with those
            self.resources[1] = Resource("core_led",    0, PinsN("D17"), Attrs(io_standard="3.3-V LVTTL"))
            self.resources[2] = Resource("core_button", 0, PinsN("AB13"), Attrs(io_standard="3.3-V LVTTL"))
            self.resources[3] = Resource("core_button", 1, PinsN("V18"), Attrs(io_standard="3.3-V LVTTL"))
            daughterboard = QMTechDaughterboard(Attrs(io_standard="3.3-V LVTTL"))
            self.connectors += daughterboard.connectors
            self.resources  += daughterboard.resources

        super().__init__()

    resources   = [
        Resource("clk50", 0, Pins("M9", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="D17",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *ButtonResources(
            pins="AB13 V18", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *SPIFlashResources(0,
            cs_n="R4", clk="V3", copi="AB4", cipo="AB3",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="AB11", cke="V9", cs_n="AB5", we_n="W9", ras_n="AB6", cas_n="AA7",
            ba="T7 P9", a="P8 P7 N8 N6 U6 U7 V6 U8 T8 W8 R6 T9 Y9",
            dq="AA12 Y11 AA10 AB10 Y10 AA9 AB8 AA8 U10 T10 U11 R12 U12 P12 R10 R11", dqm="AB7 V10",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
    ]

    # The connectors are named after the daughterboard, not the core board
    # because on the different core boards the names vary, but on the
    # daughterboard they stay the same, which we need to connect the
    # daughterboard peripherals to the core board.
    # On this board J2 is U7 and J3 is U8
    connectors = [
        Connector("J", 2, {
             # odd row     even row
              "7": "AA2",  "8": "AA1",
              "9": "Y3",  "10": "W2",
             "11": "U1",  "12": "U2",
             "13": "N1",  "14": "N2",
             "15": "L1",  "16": "L2",
             "17": "G1",  "18": "G2",
             "19": "E2",  "20": "D3",
             "21": "C1",  "22": "C2",
             "23": "G6",  "24": "H6",
             "25": "G8",  "26": "H8",
             "27": "F7",  "28": "E7",
             "29": "D6",  "30": "C6",
             "31": "E9",  "32": "D9",
             "33": "B5",  "34": "A5",
             "35": "B6",  "36": "B7",
             "37": "A7",  "38": "A8",
             "39": "A9",  "40": "A10",
             "41": "B10", "42": "C9",
             "43": "G10", "44": "F10",
             "45": "C11", "46": "B11",
             "47": "B12", "48": "A12",
             "49": "E12", "50": "D12",
             "51": "D13", "52": "C13",
             "53": "B13", "54": "A13",
             "55": "A15", "56": "A14",
             "57": "B15", "58": "C15",
             "59": "C16", "60": "B16",
        }),
        Connector("J", 3, {
            # odd row     even row
             "7": "AA14",   "8": "AA13",
             "9": "AA15",  "10": "AB15",
            "11": "Y15",   "12": "Y14",
            "13": "AB18",  "14": "AB17",
            "15": "Y17",   "16": "Y16",
            "17": "AA18",  "18": "AA17",
            "19": "AA20",  "20": "AA19",
            "21": "Y20",   "22": "Y19",
            "23": "AB21",  "24": "AB20",
            "25": "AA22",  "26": "AB22",
            "27": "W22",   "28": "Y22",
            "29": "Y21",   "30": "W21",
            "31": "U22",   "32": "V21",
            "33": "V20",   "34": "W19",
            "35": "U21",   "36": "U20",
            "37": "R22",   "38": "T22",
            "39": "P22",   "40": "R21",
            "41": "T20",   "42": "T19",
            "43": "P16",   "44": "P17",
            "45": "N20",   "46": "N21",
            "47": "M21",   "48": "M20",
            "49": "M18",   "50": "N19",
            "51": "L18",   "52": "L19",
            "53": "M22",   "54": "L22",
            "55": "L17",   "56": "K17",
            "57": "K22",   "58": "K21",
            "59": "M16",   "60": "N16",
        })
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                    "--operation", "P;" + bitstream_filename])

if __name__ == "__main__":
    from nmigen_boards.test.blinky import Blinky
    QMTech5CEFA2Platform(standalone=True).build(Blinky(), do_program=True)