import os
import subprocess

from amaranth.build import *
from amaranth.vendor.intel import *
from amaranth_boards.resources import *
from amaranth_boards.qmtech_daughterboard import QMTechDaughterboard


__all__ = ["QMTechEP4CGX150Platform"]


class QMTechEP4CGX150Platform(IntelPlatform):
    device      = "EP4CGX150"
    package     = "DF27I7"
    speed       = ""
    default_clk = "clk50"

    # at the time of writing EP4CE15 and EP4CE55 are available from QMTech
    # so no_kluts = 15 or 55 for these platforms
    def __init__(self, standalone=True):
        if not standalone:
            # D3 - we do not use LEDResources/ButtonResources here, because there are five LEDs
            # on the daughterboard and this will then clash with those
            self.resources[1] = Resource("core_led",    0, PinsN("A25"),  Attrs(io_standard="3.3-V LVTTL"))
            self.resources[2] = Resource("core_led",    0, PinsN("A24"),  Attrs(io_standard="3.3-V LVTTL"))
            self.resources[3] = Resource("core_button", 0, PinsN("AD23"), Attrs(io_standard="3.3-V LVTTL"))
            self.resources[4] = Resource("core_button", 1, PinsN("AD24"), Attrs(io_standard="3.3-V LVTTL"))
            daughterboard = QMTechDaughterboard(Attrs(io_standard="3.3-V LVTTL"))
            self.connectors += daughterboard.connectors
            self.resources  += daughterboard.resources

        super().__init__()

    resources   = [
        Resource("clk50", 0, Pins("B14", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="A25 A24",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *ButtonResources(
            pins="AD23 AD24", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *SPIFlashResources(0,
            cs_n="D5", clk="F6", copi="E6", cipo="D6",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="J23", cke="K24", cs_n="H26", we_n="G25", ras_n="H25", cas_n="G26",
            ba="J25 J26", a="L25 L26 M25 M26 N22 N23 N24 M22 M24 L23 K26 L24 K23",
            dq="B25 B26 C25 C26 D25 D26 E25 E26 H23 G24 G22 F24 F23 E24 D24 C24", dqm="F26 H24",
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
              "7": "AF24",   "8": "AF25",
              "9": "AC21",  "10": "AD21",
             "11": "AE23",  "12": "AF23",
             "13": "AE22",  "14": "AF22",
             "15": "AD20",  "16": "AE21",
             "17": "AF20",  "18": "AF21",
             "19": "AE19",  "20": "AF19",
             "21": "AC19",  "22": "AD19",
             "23": "AE18",  "24": "AF18",
             "25": "AC18",  "26": "AD18",
             "27": "AE17",  "28": "AF17",
             "29": "AC17",  "30": "AD17",
             "31": "AF15",  "32": "AF16",
             "33": "AC16",  "34": "AD16",
             "35": "AE14",  "36": "AE15",
             "37": "AC15",  "38": "AD15",
             "39": "AC14",  "40": "AD14",
             "41": "AF11",  "42": "AF12",
             "43": "AC10",  "44": "AD10",
             "45": "AE9",   "46": "AF9",
             "47": "AF7",   "48": "AF8",
             "49": "AE7",   "50": "AF6",
             "51": "AE5",   "52": "AE6",
             "53": "AD5",   "54": "AD6",
             "55": "AF4",   "56": "AF5",
             "57": "AD3",   "58": "AE3",
             "59": "AC4",   "60": "AD4",
        }),
        Connector("J", 3, {
            # odd row     even row
             "7": "C21",    "8": "B22",
             "9": "B23",   "10": "A23",
            "11": "B21",   "12": "A22",
            "13": "C19",   "14": "B19",
            "15": "A21",   "16": "A20",
            "17": "A19",   "18": "A18",
            "19": "C17",   "20": "B18",
            "21": "C16",   "22": "B17",
            "23": "A17",   "24": "A16",
            "25": "B15",   "26": "A15",
            "27": "C15",   "28": "C14",
            "29": "C13",   "30": "B13",
            "31": "C12",   "32": "C11",
            "33": "A13",   "34": "A12",
            "35": "B11",   "36": "A11",
            "37": "B10",   "38": "A10",
            "39": "C10",   "40": "B9",
            "41": "A9",    "42": "A8",
            "43": "A7",    "44": "A6",
            "45": "B7",    "46": "B6",
            "47": "B5",    "48": "A5",
            "49": "B4",    "50": "A4",
            "51": "C5",    "52": "C4",
            "53": "A3",    "54": "A2",
            "55": "B2",    "56": "B1",
            "57": "D1",    "58": "C1",
            "59": "E2",    "60": "E1",
        })
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                    "--operation", "P;" + bitstream_filename])

if __name__ == "__main__":
    from amaranth_boards.test.blinky import Blinky
    QMTechEP4CGX150Platform(standalone=True).build(Blinky(), do_program=True)
