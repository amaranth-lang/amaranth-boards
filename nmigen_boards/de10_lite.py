import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["DE10LitePlatform"]


class DE10LitePlatform(IntelPlatform):
    device      = "10M50DAF484" # MAX10
    package     = "F23"     # FBGA-484
    speed       = "I7"
    default_clk = "clk50"
    resources   = [
        Resource("clk10", 0, Pins("N5", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("P11", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("N14", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="A8 A9 A10 B10 D13 C13 E14 D14 A11 B11",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="B8 A7", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *SwitchResources(
            pins="C10 C11 D12 C12 A12 B12 A13 A14 B14 F15",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(0,
            a="C14", b="E15", c="C15", d="C16", e="E16", f="D17", g="C17", dp="D15", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(1,
            a="C18", b="D18", c="E18", d="B16", e="A17", f="A18", g="B17", dp="A16", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(2,
            a="B20", b="A20", c="B19", d="A21", e="B21", f="C22", g="B22", dp="A19", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(3,
            a="F21", b="E22", c="E21", d="C19", e="C20", f="D19", g="E17", dp="D22", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(4,
            a="F18", b="E20", c="E19", d="J18", e="H19", f="F19", g="F20", dp="F17", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(5,
            a="J20", b="K20", c="L18", d="N18", e="M20", f="N19", g="N20", dp="L19", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        # Arduino header
        UARTResource(0,
            rx="V10", tx="W10",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="L14", cs_n="U20", we_n="V20", ras_n="U22", cas_n="U21",
            ba="T21 T22", a="U17 W19 V18 U18 U19 T18 T19 R18 P18 P19 T20 P20 R20",
            dq="Y21 Y20 AA22 AA21 Y22 W22 W20 V21 P21 J22 H21 H22 G22 G20 G19 F22",
            dqm="V22 J21", attrs=Attrs(io_standard="3.3-V LVCMOS")),

        Resource("vga", 0,
            Subsignal("r", Pins("AA1 V1 Y2 Y1", dir="o")),
            Subsignal("g", Pins("W1 T2 R2 R1", dir="o")),
            Subsignal("b", Pins("P1 T1 P4 N2", dir="o")),
            Subsignal("hs", Pins("N3", dir="o")),
            Subsignal("vs", Pins("N1", dir="o")),
            Attrs(io_standard="3.3-V LVTTL"))
    ]
    connectors  = [
        Connector("gpio", 0,
            "V10 W10 V9 W9 V8 W8 V7 W7 W6 V5 W5 AA15 AA14 W13 W12 AB13 AB12 Y11 AB11 W11 AB10 "
            "AA10 AA9 Y8 AA8 Y7 AA7 Y6 AA6 Y5 AA5 Y4 AB3 Y3 AB2 AA2"),
        Connector("gpio", 5,
            "AB5 AB6 AB7 AB8 AB9 Y10 AA11 AA12 AB17 AA17 AB19 AA19 Y19 AB20 AB21 AA20 F16"),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import Blinky
    DE10LitePlatform().build(Blinky(), do_program=True)
