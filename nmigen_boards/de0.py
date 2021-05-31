import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["DE0Platform"]


class DE0Platform(IntelPlatform):
    device      = "EP3C16" # Cyclone III 15K LEs
    package     = "F484"   # FBGA-484
    speed       = "C6"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("G21", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("B12", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="J1 J2 J3 H1 F2 E1 C1 C2 B2 B1",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="H2 G3 F1", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *SwitchResources(
            pins="J6 H5 H6 G4 G5 J7 H7 E3 E4 D2",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(0,
            a="E11", b="F11", c="H12", d="H13", e="G12", f="F12", g="F13", dp="D13", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(1,
            a="A13", b="B13", c="C13", d="A14", e="B14", f="E14", g="A15", dp="B15", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(2,
            a="D15", b="A16", c="B16", d="E15", e="A17", f="B17", g="F14", dp="A18", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        Display7SegResource(3,
            a="B18", b="F15", c="A19", d="B19", e="C19", f="D19", g="G15", dp="G16", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        UARTResource(0,
            rx="U22", tx="U21", rts="V22", cts="V21",
            attrs=Attrs(io_standard="3.3-V LVTTL"),
            role="dce"),

        Resource("display_hd44780", 0,
            Subsignal("e", Pins("E21", dir="o")),
            Subsignal("d", Pins("D22 D21 C22 C21 B22 B21 D20 C20", dir="io")),
            Subsignal("rw", Pins("E22", dir="o")),
            Subsignal("rs", Pins("F22", dir="o")),
            # Backlight
            Subsignal("bl", Pins("F21", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")
        ),

        VGAResource(0,
            r="H19 H17 H20 H21",
            g="H22 J17 K17 J21",
            b="K22 K21 J22 K18",
            hs="L21", vs="L22",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        Resource("ps2_host", 0, # Keyboard
            Subsignal("clk", Pins("P22", dir="i")),
            Subsignal("dat", Pins("P21", dir="io")),
            Attrs(io_standard="3.3-V LVTTL")
        ),
        Resource("ps2_host", 1, # Mouse
            Subsignal("clk", Pins("R21", dir="i")),
            Subsignal("dat", Pins("R22", dir="io")),
            Attrs(io_standard="3.3-V LVTTL")
        ),

        *SDCardResources(0,
            clk="Y21", cmd="Y22", dat0="AA22", dat3="W21", wp_n="W20",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        SDRAMResource(0,
            clk="E5", cke="E6", cs_n="G7", we_n="D6", ras_n="F7", cas_n="G8",
            ba="B5 A4", a="C4 A3 B3 C3 A5 C6 B6 A6 C7 B7 B4 A7 C8",
            dq="D10 G10 H10 E9 F9 G9 H9 F8 A8 B9 A9 C10 B10 A10 E10 F10", dqm="E7 B8",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        *NORFlashResources(0,
            rst="R1", byte_n="AA1",
            cs_n="N8", oe_n="R6", we_n="P4", wp_n="T3", by="M7",
            a="P7 P5 P6 N7 N5 N6 M8 M4 P2 N2 N1 M3 M2 M1 L7 L6 AA2 M5 M6 P1 P3 R2",
            dq="R7 P8 R8 U1 V2 V3 W1 Y1 T5 T7 T4 U2 V1 V4 W2 Y2",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
    ]
    connectors  = [
        Connector("j", 4,
            "AB12 AB16 AA12 AA16 AA15 AB15 AA14 AB14 AB13 AA13 -    -    "
            "AB10 AA10 AB8  AA8  AB5  AA5  AB3  AB4  AA3  AA4  V14  U14  "
            "Y13  W13  U13  V12  -    -    R10  V11  Y10  W10  T8   V8   "
            "W7   W6   V5   U7  "),
        Connector("j", 5,
            "AB11 AA20 AA11 AB20 AA19 AB19 AB18 AA18 AA17 AB17 -    -    "
            "Y17  W17  U15  T15  W15  V15  R16  AB9  T16  AA9  AA7  AB7  "
            "T14  R14  U12  T12  -    -    R11  R12  U10  T10  U9   T9   "
            "Y7   U8   V6   V7  "),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import Blinky
    DE0Platform().build(Blinky(), do_program=True)
