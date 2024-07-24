import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from nmigen_boards.resources import *
from nmigen_boards.qmtech_daughterboard import QMTechDaughterboard


__all__ = ["QMTechEP4CEPlatform"]


class QMTechEP4CEPlatform(IntelPlatform):
    device      = "EP4CE"
    package     = "F23"
    speed       = "C8"
    default_clk = "clk50"

    # at the time of writing EP4CE15 and EP4CE55 are available from QMTech
    # so no_kluts = 15 or 55 for these platforms
    def __init__(self, no_kluts=15, standalone=True):
        self.device += str(no_kluts)

        if not standalone:
            # D3 - we do not use LEDResources/ButtonResources here, because there are five LEDs
            # on the daughterboard and this will then clash with those
            self.resources[1] = Resource("core_led",    0, PinsN("E4"),  Attrs(io_standard="3.3-V LVTTL"))
            self.resources[2] = Resource("core_button", 0, PinsN("Y13"), Attrs(io_standard="3.3-V LVTTL"))
            self.resources[3] = Resource("core_button", 1, PinsN("W13"), Attrs(io_standard="3.3-V LVTTL"))
            daughterboard = QMTechDaughterboard(Attrs(io_standard="3.3-V LVTTL"))
            self.connectors += daughterboard.connectors
            self.resources  += daughterboard.resources

        super().__init__()

    resources   = [
        Resource("clk50", 0, Pins("T2", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="E4",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *ButtonResources(
            pins="Y13 W13", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *SPIFlashResources(0,
            cs_n="E2", clk="K2", copi="D1", cipo="K1",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="Y6", cke="W6", cs_n="AA3", we_n="AB4", ras_n="AB3", cas_n="AA4",
            ba="Y1 W2", a="V2 V1 U2 U1 V3 V4 Y2 AA1 Y3 V5 W1 Y4 V6",
            dq="AA10 AB9 AA9 AB8 AA8 AB7 AA7 AB5 Y7 W8 Y8 V9 V10 Y10 W10 V11", dqm="AA5 W7",
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
              "7": "R1",   "8": "R2",
              "9": "P1",  "10": "P2",
             "11": "N1",  "12": "N2",
             "13": "M1",  "14": "M2",
             "15": "J1",  "16": "J2",
             "17": "H1",  "18": "H2",
             "19": "F1",  "20": "F2",
             "21": "E1",  "22": "D2",
             "23": "C1",  "24": "C2",
             "25": "B1",  "26": "B2",
             "27": "B3",  "28": "A3",
             "29": "B4",  "30": "A4",
             "31": "C4",  "32": "C3",
             "33": "B5",  "34": "A5",
             "35": "B6",  "36": "A6",
             "37": "B7",  "38": "A7",
             "39": "B8",  "40": "A8",
             "41": "B9",  "42": "A9",
             "43": "B10", "44": "A10",
             "45": "B13", "46": "A13",
             "47": "B14", "48": "A14",
             "49": "B15", "50": "A15",
             "51": "B16", "52": "A16",
             "53": "B17", "54": "A17",
             "55": "B18", "56": "A18",
             "57": "B19", "58": "A19",
             "59": "B20", "60": "A20",
        }),
        Connector("J", 3, {
            # odd row     even row
             "7": "AA13",   "8": "AB13",
             "9": "AA14",  "10": "AB14",
            "11": "AA15",  "12": "AB15",
            "13": "AA16",  "14": "AB16",
            "15": "AA17",  "16": "AB17",
            "17": "AA18",  "18": "AB18",
            "19": "AA19",  "20": "AB19",
            "21": "AA20",  "22": "AB20",
            "23": "Y22",   "24": "Y21",
            "25": "W22",   "26": "W21",
            "27": "V22",   "28": "V21",
            "29": "U22",   "30": "U21",
            "31": "R22",   "32": "R21",
            "33": "P22",   "34": "P21",
            "35": "N22",   "36": "N21",
            "37": "M22",   "38": "M21",
            "39": "L22",   "40": "L21",
            "41": "K22",   "42": "K21",
            "43": "J22",   "44": "J21",
            "45": "H22",   "46": "H21",
            "47": "F22",   "48": "F21",
            "49": "E22",   "50": "E21",
            "51": "D22",   "52": "D21",
            "53": "C22",   "54": "C21",
            "55": "B22",   "56": "B21",
            "57": "N20",   "58": "N19",
            "59": "M20",   "60": "M19",
        })
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                    "--operation", "P;" + bitstream_filename])

if __name__ == "__main__":
    from nmigen_boards.test.blinky import Blinky
    QMTechEP4CEPlatform(standalone=True).build(Blinky(), do_program=True)