import os
import subprocess

from amaranth.build import *
from amaranth.vendor import LatticeECP5Platform
from .resources import *


__all__ = ["IcepiZero1_3Platform"]


class IcepiZero1_3Platform(LatticeECP5Platform):
    device      = "LFE5U-25F"
    package     = "BG256"
    speed       = "6"
    default_clk = "clk50"

    resources   = [
        Resource("clk50", 0, Pins("M1", dir="i"), Clock(50e6), Attrs(IO_TYPE="LVCMOS33", PULLMODE="NONE")),

        *LEDResources(pins="E13 D14 E12 C13 D13",
                      attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4")),
        
        *ButtonResources(pins="C4 C5", invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP")),

        UARTResource(0,
            rx="K16", tx="K15", rts="L16", dtr="L15", role="dce",
            attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP")    
        ),

        *SDCardResources(0,
            clk="P15", cmd="N16", cd="M16", dat0="P14", dat1="R14", dat2="M15", dat3="M14",
            attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP", SLEWRATE="FAST")
        ),

        *SPIFlashResources(0,
            cs_n="N8", clk="N9", cipo="T7", copi="T8", wp_n="M7", hold_n="N7",
            attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP"),
        ),

        SDRAMResource(0,
            clk="A3", cke="B4", cs_n="B12", we_n="A13", cas_n="B13", ras_n="A12", dqm="B14 B3",
            ba="A11 B11", a="B10 A9 B9 A8 B8 A7 B7 A6 B6 A5 A10 B5 A4",
            dq="B16 C14 C16 C15 D16 A15 B15 A14 A2 B2 E2 D1 C2 C1 C3 B1",
            attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="NONE", SLEWRATE="FAST")
        ),

        Resource("hdmi", 0,
                 Subsignal("d",     DiffPairs(p="R13 R15 P16", n="T14 T15 R16", dir="o"),
                           Attrs(IO_TYPE="LVCMOS33D", DRIVE="4")),
                 Subsignal("clk",   DiffPairs(p="R12", n="T13", dir="o"),
                           Attrs(IO_TYPE="LVCMOS33D", DRIVE="4")),
                 Subsignal("cec",   Pins("R5", dir="io"),
                           Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP")),
                 Subsignal("scl",   Pins("T3", dir="io"),
                           Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP")),
                 Subsignal("sda",   Pins("T4", dir="io"),
                           Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP")),
                 # Named utility in schematics.
                 Subsignal("hec",   Pins("P5", dir="io"),
                           Attrs(IO_TYPE="LVCMOS33", PULLMODE="NONE")),
                 Subsignal("hpd",   Pins("L14", dir="i"),
                           Attrs(IO_TYPE="LVCMOS33", PULLMODE="NONE"))),

        Resource("usb", 0, 
                 Subsignal("d_p",       Pins("F15", dir="io")),
                 Subsignal("d_n",       Pins("E16", dir="io")),
                 Subsignal("pullup",    Pins("H14 G15", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="NONE")),

        Resource("usb", 1, 
                 Subsignal("d_p",       Pins("J16", dir="io")),
                 Subsignal("d_n",       Pins("J15", dir="io")),
                 Subsignal("pullup",    Pins("E11 E14", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="NONE")),

        Resource("test", 0, Pins("C7 C8", dir="o"), Attrs(IO_TYPE="LVCMOS33"))
    ]

    connectors  = [
        Connector("gpio", 0, {
            "0":    "G3",
            "1":    "K3",
            "2":    "T2",
            "3":    "R2",
            "4":    "R1",
            "5":    "E1",
            "6":    "F3",
            "7":    "G1",
            "8":    "H2",
            "9":    "J1",
            "10":   "L2",
            "11":   "G2",
            "12":   "J3",
            "13":   "E3",
            "14":   "P1",
            "15":   "N1",
            "16":   "H3",
            "17":   "R3",
            "18":   "N4",
            "19":   "E4",
            "20":   "F1",
            "21":   "F2",
            "22":   "P2",
            "23":   "M2",
            "24":   "L1",
            "25":   "J2",
            "26":   "D4",
            "27":   "P3"
        })
    ]
    
    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = dict(ecppack_opts="--compress")
        overrides.update(kwargs)
        return super().toolchain_prepare(fragment, name, **overrides)

    def toolchain_program(self, products, name):
        tool = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([tool, "-b", "icepi-zero", bitstream_filename, "--write-flash"])


if __name__ == "__main__":
    from .test.blinky import *
    IcepiZero1_3Platform().build(Blinky(), do_program=True)