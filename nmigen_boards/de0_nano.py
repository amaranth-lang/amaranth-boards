import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from nmigen_boards.resources import *


__all__ = ["DE0NanoPlatform"]


class DE0NanoPlatform(IntelPlatform):
    device      = "EP4CE22"
    package     = "F17"
    speed       = "C6"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("R8", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="A15 A13 B13 A11 D1 F3 B1 L3",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="J15 E1", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *SwitchResources(
            pins="M1 T8 B9 M15",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        UARTResource(0,
            # GND on JP1 Pin 12.
            rx="JP_1:8", tx="JP_1:10",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="R4", cke="L7", cs_n="P6", we_n="C2", ras_n="L2", cas_n="L1",
            ba="M7 M6", a="P2 N5 N6 M8 P8 T7 N8 T6 R1 P1 N2 N1 L4",
            dq="G2 G1 L8 K5 K2 J2 J1 R7 T4 T2 T3 R3 R5 P3 N3 K1", dqm="R6 T5",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        # Accelerometer
        Resource("acc", 0,
            Subsignal("cs_n", Pins("G5", dir="o")),
            Subsignal("int",  Pins("M2", dir="i")),
            Attrs(io_standard="3.3-V LVTTL")),
        # I2C is part of the Accelerometer
        I2CResource(0,
            scl="F2", sda="F1",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        # ADC
        Resource("adc", 0,
            Subsignal("cs_n",  Pins("A10")),
            Subsignal("saddr", Pins("B10")),
            Subsignal("sclk",  Pins("B14")),
            Subsignal("sdat",  Pins("A9")),
            Attrs(io_standard="3.3-V LVTTL")),

        # ECPS
        Resource("epcs", 0,
            Subsignal("data0", Pins("H2")),
            Subsignal("dclk",  Pins("H1")),
            Subsignal("ncs0",  Pins("D2")),
            Subsignal("asd0",  Pins("C1")),
            Attrs(io_standard="3.3-V LVTTL")),
    ]
    connectors  = [
        # PIN               1  2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18 19 20  21  22  23  24  25  26  27  28 29 30 31  32  33  34  35  36  37  38  39  40
        Connector("JP", 1, "A8 D3  B8  C3  A2  A3  B3  B4  A4  B5  -   -   A5  D5  B6  A6  B7  D6 A7 C6  C8  E6  E7  D8  E8  F8  F9  E9  - -  C9  D9  E11 E10 C11 B11 A12 D11 D12 B12"),
        Connector("JP", 2, "T9 F13 R9  T15 T14 T13 R13 T12 R12 T11 -   -   T10 R11 P11 R10 N12 P9 N9 N11 L16 K16 R16 L15 P15 P16 R14 N16 - -  N15 P14 L14 N14 M10 L13 J16 K15 J13 J14"),
        Connector("JP", 3, "-  E15 E16 M16 A14 B16 C14 C16 C15 D16 D15 D14 F15 F16 F14 G16 G15 -  -  -   -   -   -   -   -   -")
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                    "--operation", "P;" + bitstream_filename])

if __name__ == "__main__":
    from nmigen_boards.test.blinky import Blinky
    DE0NanoPlatform().build(Blinky(), do_program=True)