from amaranth.build import *
from amaranth.vendor.xilinx_7series import *
from .resources import *


__all__ = ["TE0714_03_50_2IPlatform"]


class TE0714_03_50_2IPlatform(Xilinx7SeriesPlatform):
    device      = "xc7a50t"
    package     = "csg325"
    speed       = "2"
    default_clk = "clk25"
    resources = [
        Resource("clk25", 0, Pins("T14", dir="i"), Clock(25e6), Attrs(IOSTANDARD="LVCMOS18")),
        *LEDResources(pins="K18", attrs=Attrs(IOSTANDARD="LVCMOS18")),
        *SPIFlashResources(0,
            cs_n="L15", clk="E8", copi="K16", cipo="K17", wp_n="J15", hold_n="J16",
            attrs=Attrs(IOSTANDARD="LVCMOS18")
        )
    ]
    connectors = [
        Connector("JM1", 0,
            "G4  D6  "
            "G3  D5  "
            "-   -   "
            "C4  B2  "
            "C3  B1  "
            "-   -   "
            "A4  D2  "
            "A3  D1  "
            "-   -   "
            "E4  F2  "
            "E3  F1  "
            "-   -   "
            "K10 H2  "
            "L9  H1  "
            "-   -   "
            "J5  L5  "
            "J4  M5  "
            "K6  M2  "
            "K5  M1  "
            "K3  K2  "
            "L2  K1  "
            "L4  N1  "
            "L3  P1  "
            "-   -   "
            "M4  M6  "
            "N4  N6  "
            "N2  R2  "
            "N3  R1  "
            "P3  R3  "
            "P4  T2  "
            "L6  U1  "
            "T3  U2  "
            "T4  -   "
            "R5  V2  "
            "T5  V3  "
            "P5  U4  "
            "P6  V4  "
            "T7  U5  "
            "R7  U6  "
            "V6  V7  "
            "U7  V8  "
            "-   -   "
            "V9  T9  "
            "U9  T8  "
            "V11 F8  "
            "U11 R8  "
            "V12 -   "
            "V13 F12 "
            "-   -   "
            "-   -   "
        ),
        Connector("JM2", 0,
            "A12 B9  "
            "B12 A9  "
            "A13 B10 "
            "A14 A10 "
            "B14 B11 "
            "A15 C11 "
            "C14 C8  "
            "B15 D8  "
            "-   E11 "
            "A17 C9  "
            "B16 D9  "
            "B17 D11 "
            "C16 C12 "
            "C18 D13 "
            "C17 C13 "
            "D18 E13 "
            "E17 D14 "
            "-   -   "
            "E18 D15 "
            "F17 E15 "
            "F18 D16 "
            "G17 E16 "
            "F15 F14 "
            "G15 G14 "
            "H17 G16 "
            "H18 H16 "
            "-   A16 "
            "K17 J14 "
            "L18 K15 "
            "M17 M14 "
            "M16 N14 "
            "R18 N16 "
            "T18 N17 "
            "E8  K16 "
            "L15 J16 "
            "L17 -   "
            "J15 P16 "
            "N18 P15 "
            "P18 R17 "
            "T17 R16 "
            "U17 P14 "
            "-   R15 "
            "V17 T15 "
            "V16 T14 "
            "U16 -   "
            "U15 R13 "
            "U14 T13 "
            "V14 U12 "
            "U10 T12 "
            "L14 R12 "
        )
    ]


if __name__ == "__main__":
    from .test.blinky import Blinky
    TE0714_03_50_2IPlatform().build(Blinky(), do_program=False)
