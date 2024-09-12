import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from nmigen_boards.resources import *

__all__ = ["WaveshareEP4CE10Platform"]


class WaveshareEP4CE10Platform(IntelPlatform):
    device      = "EP4CE10"
    package     = "F17"
    speed       = "C8"
    default_clk = "clk50"

    resources   = [
        Resource("clk50", 0, Pins("E16", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        Resource("buzzer", 0, Pins("J1", dir="o"),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("ds18b20", 0, Pins("J2", dir="io"),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("joystick", 0,
            Subsignal("down",  Pins("F1", dir="i")),
            Subsignal("left",  Pins("F2", dir="i")),
            Subsignal("right", Pins("G1", dir="i")),
            Subsignal("up",    Pins("G2", dir="i")),
            Subsignal("press", Pins("D1", dir="i")),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("lcd12864", 0,
            Subsignal("RS",  Pins("G16", dir="o")),
            Subsignal("RW",  Pins("F16", dir="o")),
            Subsignal("E",   Pins("F15", dir="o")),
            Subsignal("D0",  Pins("L10", dir="o")),
            Subsignal("D1",  Pins("M10", dir="o")),
            Subsignal("D2",  Pins("M11", dir="o")),
            Subsignal("D3",  Pins("N13", dir="o")),
            Subsignal("D4",  Pins("P14", dir="o")),
            Subsignal("D5",  Pins("N14", dir="o")),
            Subsignal("D6",  Pins("L13", dir="o")),
            Subsignal("D7",  Pins("M12", dir="o")),
            Subsignal("PSB", Pins("L12", dir="o")),
            Subsignal("RST", Pins("J13", dir="o")),
            Subsignal("A",   Pins("K12", dir="o")),
            Subsignal("K",   Pins("J12", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("lcd1602", 0,
            Subsignal("RS",  Pins("G16", dir="o")),
            Subsignal("RW",  Pins("F16", dir="o")),
            Subsignal("E",   Pins("F15", dir="o")),
            Subsignal("D0",  Pins("L10", dir="o")),
            Subsignal("D1",  Pins("M10", dir="o")),
            Subsignal("D2",  Pins("M11", dir="o")),
            Subsignal("D3",  Pins("N13", dir="o")),
            Subsignal("D4",  Pins("P14", dir="o")),
            Subsignal("D5",  Pins("N14", dir="o")),
            Subsignal("D6",  Pins("L13", dir="o")),
            Subsignal("D7",  Pins("M12", dir="o")),
            Subsignal("A",   Pins("L12", dir="o")),
            Subsignal("K",   Pins("L14", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="D12 C11 B10 B7",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="B16", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="P15", cke="P16", cs_n="P3", we_n="R1", ras_n="L3", cas_n="L4",
            ba="N3 N6", a="P8 P6 L6 N8 R12 T12 R13 T13 R14 T14 N5 R16 T15",
            dq="K2 K1 L2 L1 N2 N1 P2 P1 N15 L16 L15 K16 K15 J16 J15 G15", dqm="T2 N16",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
    ]

    # These are the connectors on the daughterboard DVK600
    connectors = [
        Connector("8IOs", 1, {
              "8": "J13",
              "7": "L11",
              "6": "K12",
              "5": "J12",
              "4": "K11",
              "3": "J11",
              "2": "K10",
              "1": "F11",
        }),

        Connector("8IOs", 2, {
              "8": "G1",
              "7": "G2",
              "6": "J1",
              "5": "J2",
              "4": "K1",
              "3": "K2",
              "2": "L1",
              "1": "L2",
        }),

        Connector("16IOs", 1, {
              "1": "L6",
              "2": "N8",
              "3": "P8",
              "4": "P6",
              "5": "N6",
              "6": "N5",
              "7": "P3",
              "8": "N3",
              "9": "L4",
             "10": "L3",
             "11": "T2",
             "12": "R1",
             "13": "P2",
             "14": "P1",
             "15": "N2",
             "16": "N1",
        }),

        Connector("16IOs", 2, {
              "1": "F2",
              "2": "F1",
              "3": "D1",
              "4": "C2",
              "5": "B1",
              "6": "A2",
              "7": "B3",
              "8": "A3",
              "9": "B4",
             "10": "A4",
             "11": "B5",
             "12": "A5",
             "13": "B6",
             "14": "A6",
             "15": "F3",
             "16": "D3",
        }),

        Connector("32IOs", 1, {
              "1": "L12",
              "2": "L14",
              "3": "L13",
              "4": "M12",
              "5": "P14",
              "6": "N14",
              "7": "M11",
              "8": "N13",
              "9": "L10",
             "10": "M10",
             "11": "F16",
             "12": "F15",
             "13": "G16",
             "14": "G15",
             "15": "J15",
             "16": "J16",
             "17": "K15",
             "18": "K16",
             "19": "L15",
             "20": "L16",
             "21": "N15",
             "22": "N16",
             "23": "P15",
             "24": "P16",
             "25": "T15",
             "26": "R16",
             "27": "T14",
             "28": "R14",
             "29": "T13",
             "30": "R13",
             "31": "T12",
             "32": "R12",
        }),

        Connector("32IOs", 2, {
              "1": "R11",
              "2": "N12",
              "3": "P11",
              "4": "N11",
              "5": "P9",
              "6": "N9",
              "7": "R10",
              "8": "T11",
              "9": "R9",
             "10": "T10",
             "11": "R8",
             "12": "T9",
             "13": "R7",
             "14": "T8",
             "15": "R6",
             "16": "T7",
             "17": "R5",
             "18": "T6",
             "19": "R4",
             "20": "T5",
             "21": "R3",
             "22": "T4",
             "23": "M9",
             "24": "T3",
             "25": "K9",
             "26": "L9",
             "27": "L8",
             "28": "K8",
             "29": "M7",
             "30": "M8",
             "31": "M6",
             "32": "L7",
        }),

        Connector("32IOs", 3, {
              "1": "A7",
              "2": "E6",
              "3": "B8",
              "4": "A8",
              "5": "B9",
              "6": "A9",
              "7": "D5",
              "8": "C6",
              "9": "D6",
             "10": "E7",
             "11": "E8",
             "12": "F8",
             "13": "G11",
             "14": "F9",
             "15": "E9",
             "16": "E10",
             "17": "D8",
             "18": "C8",
             "19": "D9",
             "20": "C9",
             "21": "B11",
             "22": "A10",
             "23": "A12",
             "24": "A11",
             "25": "A13",
             "26": "B12",
             "27": "A14",
             "28": "B13",
             "29": "E11",
             "30": "F10",
             "31": "B14",
             "32": "D11",
        }),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                    "--operation", "P;" + bitstream_filename])

if __name__ == "__main__":
    from nmigen_boards.test.blinky import Blinky
    WaveshareEP4CE10Platform().build(Blinky(), do_program=True)