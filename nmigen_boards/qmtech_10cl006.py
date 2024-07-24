import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from nmigen_boards.resources import *
from nmigen_boards.qmtech_daughterboard import QMTechDaughterboard


__all__ = ["QMTech10CL006Platform"]


class QMTech10CL006Platform(IntelPlatform):
    device      = "10CL006"
    package     = "YU256"
    speed       = "C8G"
    default_clk = "clk50"

    def __init__(self, standalone=True):
        if not standalone:
            # D3 - we do not use LEDResources/ButtonResources here, because there are five LEDs
            # on the daughterboard and this will then clash with those
            self.resources[1] = Resource("core_led",    0, PinsN("L9"), Attrs(io_standard="3.3-V LVTTL"))
            self.resources[2] = Resource("core_button", 0, PinsN("F3"), Attrs(io_standard="3.3-V LVTTL"))
            self.resources[3] = Resource("core_button", 1, PinsN("J6"), Attrs(io_standard="3.3-V LVTTL"))
            daughterboard = QMTechDaughterboard(Attrs(io_standard="3.3-V LVTTL"))
            self.connectors += daughterboard.connectors
            self.resources  += daughterboard.resources

        super().__init__()

    resources   = [
        Resource("clk50", 0, Pins("E1", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="L9",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *ButtonResources(
            pins="F3 J6", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *SPIFlashResources(0,
            cs_n="D2", clk="H1", copi="C1", cipo="H2",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="P2", cke="R1", cs_n="P8", we_n="P6", ras_n="M8", cas_n="M7",
            ba="N8 L8", a="R7 T7 R8 T8 R6 T5 R5 T4 R4 T3 T6 R3 T2",
            dq="K5 L3 L4 K6 N3 M6 P3 N5 N2 N1 L1 L2 K1 K2 J1 J2", dqm="N6 P1",
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
              "7": "G1",   "8": "G2",
              "9": "D1",  "10": "C2",
             "11": "B1",  "12": "F5",
             "13": "D3",  "14": "C3",
             "15": "B3",  "16": "A3",
             "17": "B4",  "18": "A4",
             "19": "E5",  "20": "A2",
             "21": "D4",  "22": "E6",
             "23": "C6",  "24": "D6",
             "25": "B5",  "26": "A5",
             "27": "B6",  "28": "A6",
             "29": "B7",  "30": "A7",
             "31": "D8",  "32": "C8",
             "33": "D9",  "34": "C9",
             "35": "B8",  "36": "A8",
             "37": "B9",  "38": "A9",
             "39": "E9",  "40": "E8",
             "41": "E11", "42": "E10",
             "43": "A10", "44": "B10",
             "45": "D12", "46": "D11",
             "47": "B11", "48": "A11",
             "49": "B12", "50": "A12",
             "51": "B13", "52": "A13",
             "53": "B14", "54": "A14",
             "55": "D14", "56": "C14",
             "57": "B16", "58": "A15",
             "59": "C16", "60": "C15",
        }),
        Connector("J", 3, {
            # odd row     even row
             "7": "R9",    "8":  "T9",
             "9": "R10",   "10": "T10",
            "11": "R11",   "12": "T11",
            "13": "R12",   "14": "T12",
            "15": "N9",    "16": "M9",
            "17": "M10",   "18": "P9",
            "19": "P11",   "20": "N11",
            "21": "R13",   "22": "T13",
            "23": "T15",   "24": "T14",
            "25": "N12",   "26": "M11",
            "27": "R14",   "28": "N13",
            "29": "N14",   "30": "P14",
            "31": "P16",   "32": "R16",
            "33": "N16",   "34": "N15",
            "35": "M16",   "36": "M15",
            "37": "L16",   "38": "L15",
            "39": "P15",   "40": "M12",
            "41": "L14",   "42": "L13",
            "43": "K16",   "44": "K15",
            "45": "K12",   "46": "J12",
            "47": "J14",   "48": "J13",
            "49": "K11",   "50": "J11",
            "51": "G11",   "52": "F11",
            "53": "F13",   "54": "F14",
            "55": "F10",   "56": "F9",
            "57": "E16",   "58": "E15",
            "59": "D16",   "60": "D15",
        })
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                    "--operation", "P;" + bitstream_filename])

if __name__ == "__main__":
    from nmigen_boards.test.blinky import Blinky
    QMTech10CL006Platform(standalone=True).build(Blinky(), do_program=True)