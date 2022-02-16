import os
import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_ecp5 import *
from .resources import *


__all__ = ["LogicbonePlatform", "Logicbone85FPlatform"]


class LogicbonePlatform(LatticeECP5Platform):
    name        = "Logicbone"
    device      = "LFE5UM5G-45F"
    package     = "BG381"
    speed       = "8"

    default_clk = "refclk"

    resources   = [
        Resource("refclk", 0, Pins("M19", dir="i"),
                 Clock(25e6), Attrs(IO_TYPE="LVCMOS18")),

        # SerDes connections.
        Resource("serdes", 0,
            Subsignal("rx", DiffPairs("Y5", "Y6")),
            Subsignal("tx", DiffPairs("W4", "W5")),
        ),
        Resource("serdes", 1,
            Subsignal("rx", DiffPairs("Y8", "Y7")),
            Subsignal("tx", DiffPairs("W8", "W9")),
        ),

        # VBUS Detection is on the USB-C PD controller for both ports.
        DirectUSBResource("usb", 0,
            d_p="B12", d_n="C12", pullup="C16",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),
        DirectUSBResource("usb", 1,
            d_p="R1",  d_n="T1",  pullup="T2",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),

        *LEDResources(pins="D16 C15 C13 B13", attrs=Attrs(IO_TYPE="LVCMOS33"), invert=True),

        *ButtonResources(pins="U2", attrs=Attrs(IO_TYPE="LVCMOS33"), invert=True),

        *SPIFlashResources(0,
            cs_n="R2", clk="U3", cipo="V2", copi="W2", wp_n="Y2", hold_n="W1",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),

        *SDCardResources(0,
            clk="E11", cmd="D15", cd="D14",
            dat0="D13", dat1="E13", dat2="E15", dat3="E13",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),

        Resource("eth_clk125", 0, Pins("A19", dir="i"),
                 Clock(125e6), Attrs(IO_TYPE="LVCMOS33")),
        Resource("eth_rgmii", 0,
            # Stolen for sys_reset usage on prototypes.
            # Subsignal("rst",     PinsN("U17", dir="o")),
            Subsignal("int",     Pins("B20", dir="i")),
            Subsignal("mdc",     Pins("D12", dir="o")),
            Subsignal("mdio",    Pins("B19", dir="io")),
            Subsignal("tx_clk",  Pins("A15", dir="o")),
            Subsignal("tx_ctl",  Pins("B15", dir="o")),
            Subsignal("tx_data", Pins("A12 A13 C14 A14", dir="o")),
            Subsignal("rx_clk",  Pins("B18", dir="i")),
            Subsignal("rx_ctl",  Pins("A18", dir="i")),
            Subsignal("rx_data", Pins("B17 A17 B16 A16", dir="i")),
            Attrs(IO_TYPE="LVCMOS33")
        ),

        Resource("ddr3", 0,
            Subsignal("rst",     PinsN("P1", dir="o")),
            Subsignal("clk",     DiffPairs("M4", "N5", dir="o"), Attrs(IO_TYPE="LVDS")),
            Subsignal("clk_en",  Pins("K4", dir="o")),
            Subsignal("cs",      PinsN("M3", dir="o")),
            Subsignal("we",      PinsN("E4", dir="o")),
            Subsignal("ras",     PinsN("L1", dir="o")),
            Subsignal("cas",     PinsN("M1", dir="o")),
            Subsignal("a",       Pins("D5 F4 B3 F3 E5 C3 C4 A5 A3 B5 G3 F5 D2 A4 D3 E3", dir="o")),
            Subsignal("ba",      Pins("B4 H5 N2", dir="o")),
            Subsignal("dqs",     DiffPairs("K2 H4", "J1 G5", dir="io"), Attrs(IO_TYPE="LVDS")),
            Subsignal("dq",      Pins("G2 K1 F1 K3 H2 J3 G1 H1 B1 E1 A2 F2 C1 E2 C2 D1", dir="io")),
            Subsignal("dm",      Pins("L4 J5", dir="o")),
            Subsignal("odt",     Pins("C5", dir="o")),
            Attrs(IO_TYPE="SSTL135_I")
        )
    ]
    connectors = [
        Connector("P8", 0, """
        -   -   C20 D19 D20 E19 E20 F19 F20 G20 -   -   -   -   -   -
        -   -   -   -   -   -   G19 H20 J20 K20 C18 D17 D18 E17 E18 F18
        F17 G18 E16 F16 G16 H16 J17 J16 H18 H17 J19 K19 J18 K18
        """),
        Connector("P9", 0, """
        -   -   -   -   -   -   -   -   -   -   -   A11 B11 A10 C10 A9
        B9  C11 A8  -   -   D9  C8  B8  A7  A6  B6  D8  C7  D7  C6  D6
        -   -   -   -   -   -   -   -   -   B10 E10 -   -   -
        """),
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = dict(ecppack_opts="--compress --spimode qspi --freq 38.8")
        overrides.update(kwargs)
        return super().toolchain_prepare(fragment, name, **overrides)

    def toolchain_program(self, products, name):
        dfu_util = os.environ.get("DFU_UTIL", "dfu-util")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([
                dfu_util, "-d", "1d50:615d", "-a", "0", "-R",
                "-D", bitstream_filename
            ])


class Logicbone85FPlatform(LogicbonePlatform):
    name        = "Logicbone (85F Variant)"
    device      = "LFE5UM5G-85F"


if __name__ == "__main__":
    import argparse
    from .test.blinky import Blinky

    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("85", "45"), default="45",
        help="platform variant (default: %(default)s)")

    args = parser.parse_args()
    if args.variant == "45":
        platform = LogicbonePlatform()
    if args.variant == "85":
        platform = Logicbone85FPlatform()
    platform.build(Blinky(), do_program=True)
