import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_machxo_2_3l import *
from .resources import *


__all__ = ["MachXO3SKPlatform"]


class MachXO3SKPlatform(LatticeMachXO3LPlatform):
    device      = "LCMXO3LF-6900C"
    package     = "BG256"
    speed       = "5"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("C8", dir="i"),
            Clock(12e6), Attrs(IO_TYPE="LVCMOS33")
        ),

        UARTResource(0,
            rx="A11", tx="C11", rts="F10", cts="D11", dtr="B11", dsr="A12", dcd="B13", ri="A14",
            attrs=Attrs(IO_TYPE="LVCMOS33"), role="dce"
        ), # need to solder R14-R18, R20-R22

        *LEDResources(
            pins="H11 J13 J11 L12 K11 L13 N15 P16",
            invert=True, attrs=Attrs(IO_TYPE="LVCMOS33")
        ), # D9..D2

        *ButtonResources(pins="B3", invert=True, attrs=Attrs(IO_TYPE="LVCMOS33")),

        *SwitchResources(pins="N2 P1 M3 N1",
            invert=True, attrs=Attrs(IO_TYPE="LVCMOS33")
        ), # SW2

        *SPIFlashResources(0,
            cs="R5", clk="P6", mosi="T13", miso="T6",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),
    ]
    connectors  = [
        Connector("j", 3, # J3
             "-  -  A13 C13 F8  B12 C12 E11 E10 D10 "
             "-  -  F9  C10 E8  E9  E7  D8  D7  C7  "
             "-  -  C5  D6  E6  C4  A10 F7  D9  B9  "
             "-  -  B6  B7  B5  A5  B4  A4  -   A3  "),
        Connector("j", 4, # J4
             "-  -  K12 K13 M14 N14 L14 N16 M15 M16 "
             "-  -  L15 L16 K14 K16 K15 J14 H14 J15 "
             "-  -  J16 H15 H16 G15 G16 F15 F16 E15 "
             "-  -  E16 E14 D16 C15 D14 F14 G14 B16 "),
        Connector("j", 6, # J6
             "-  -  T12 T14 R11 R13 T11 M11 P11 N10 "
             "-  -  T10 P10 R9  R10 T9  N9  P9  M8  "
             "-  -  T8  L8  P8  M6  R7  R8  P7  T7  "
             "-  -  L7  R6  N6  T5  R4  P4  T3  T4  "),
        Connector("j", 8, # J8
             "-  -  H6  N3  M2  M1  L2  L1  L3  L5  "
             "-  -  K4  J1  K1  J2  J3  H3  H2  H1  "
             "-  -  G2  G1  F2  F1  E2  E1  D2  D1  "
             "-  -  C2  C1  G3  B1  D3  E3  F3  F5  "),
    ]

    def toolchain_program(self, products, name):
        openFPGALoader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([openFPGALoader, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    MachXO3SKPlatform().build(Blinky(), do_program=True)
