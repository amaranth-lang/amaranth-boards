import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["ICE40HX8KBEVNPlatform"]


class ICE40HX8KBEVNPlatform(LatticeICE40Platform):
    device      = "iCE40HX8K"
    package     = "CT256"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("J3", dir="i"),
                 Clock(12e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        *LEDResources(
            pins="C3 B3 C4 C5 A1 A2 B4 B5",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ), # D2..D9

        UARTResource(0,
            rx="B10", tx="B12", rts="A15", cts="B13", dtr="A16", dsr="B14", dcd="B15",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS", PULLUP=1)
        ),

        *SPIFlashResources(0,
            cs="R12", clk="R11", mosi="P12", miso="P11",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    connectors  = [
        Connector("j", 1, # J1
            "A16 -   A15 B15 B13 B14 -   -   B12 B11 "
            "A11 B10 A10 C9  -   -   A9  B9  B8  A7  "
            "B7  C7  -   -   A6  C6  B6  C5  A5  C4  "
            "-   -   B5  C3  B4  B3  A2  A1  -   -   "),
        Connector("j", 2, # J2
            "-   -   -   R15 P16 P15 -   -   N16 M15 "
            "M16 L16 K15 K16 -   -   K14 J14 G14 F14 "
            "J15 H14 -   -   H16 G15 G16 F15 F16 E14 "
            "-   -   E16 D15 D16 D14 C16 B16 -   -   "),
        Connector("j", 3, # J3
            "R16 -   T15 T16 T13 T14 -   -   N12 P13 "
            "N10 M11 T11 P10 -   -   T10 R10 P8  P9  "
            "T9  R9  -   -   T7  T8  T6  R6  T5  R5  "
            "-   -   R3  R4  R2  T3  T1  T2  -   -   "),
        Connector("j", 4, # J4
            "-   -   -   R1  P1  P2  -   -   N3  N2  "
            "M2  M1  L3  L1  -   -   K3  K1  J2  J1  "
            "H2  J3  -   -   G2  H1  F2  G1  E2  F1  "
            "-   -   D1  D2  C1  C2  B1  B2  -   -   "),
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            # TODO: this should be factored out and made customizable
            subprocess.check_call([iceprog, "-S", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    ICE40HX8KBEVNPlatform().build(Blinky(), do_program=True)
