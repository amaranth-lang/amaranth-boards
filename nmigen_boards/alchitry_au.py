import os
import subprocess
import shutil

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from .resources import *


__all__ = ["AlchitryAuPlatform"]


def find_loader():
    loader_prgm = os.environ.get("ALCHITRY_LOADER", shutil.which("loader"))
    if loader_prgm is None:
        raise EnvironmentError("Could not find Alchrity Loader. Place "
            "it directly in PATH or specify path explicitly via the "
            "ALCHITRY_LOADER environment variable")
    bridge_bin = os.environ.get("ALCHITRY_BRIDGE_BIN", os.path.join(os.path.dirname(loader_prgm), "au_loader.bin"))
    return (loader_prgm, bridge_bin)


class AlchitryAuPlatform(Xilinx7SeriesPlatform):
    device      = "XC7A35T" # Artix 7 33K LEs
    package     = "FTG256"
    speed       = "1"
    default_clk = "clk100"
    resources   = [
        Resource("clk100", 0, Pins("N14", dir="i"),
                 Clock(10e7), Attrs(IOSTANDARD="LVCMOS33")),

        # On-Board LED Array
        *LEDResources(
            pins="K13 K12 L14 L13 M16 M14 M12 N16",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("usb", 0,
            Subsignal("usb_tx", Pins("P16", dir="o")),
            Subsignal("usb_rx", Pins("P15", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # TODO: This is untested
        Resource("ddr3", 0,
            Subsignal("rst",     PinsN("D13", dir="o")),
            Subsignal("clk",     DiffPairs("G14", "F14", dir="o"), Attrs(IOSTANDARD="LVDS")),
            Subsignal("clk_en",  Pins("D15", dir="o")),
            Subsignal("cs",      PinsN("D16", dir="o")),
            Subsignal("we",      PinsN("E11", dir="o")),
            Subsignal("ras",     PinsN("D11", dir="o")),
            Subsignal("cas",     PinsN("D14", dir="o")),
            Subsignal("a",       Pins("F12 G16 G15 E16 H11 G12 H16 H12 H16 H13 E12 H14 F13 J15", dir="o")),
            Subsignal("ba",      Pins("E13 F15 E15", dir="o")),
            Subsignal("dqs",     DiffPairs("B15 A15", "B9 A10", dir="io"), Attrs(IOSTANDARD="LVDS")),
            Subsignal("dq",      Pins("A13 B16 B14 C11 C13 C16 C12 C14 D8 B11 C8 B10 A12 A8 B12 A9",
                                      dir="io")),
            Subsignal("dm",      Pins("A14 C9", dir="o")),
            Subsignal("odt",     Pins("G11", dir="o")),
            Attrs(IOSTANDARD="LVCMOS15")
        )

    ]

    connectors  = [
        Connector("bank", 0, "T8  T7  T5  R5  R8  P8  L2  L3  J1  K1  H1  H2  G1  G2  K5  E6 "
                             "T10 T9  R6  R7  P9  N9  K2  K3  J4  J5  H3  J3  H4  H5  N6  M6 "),
        Connector("bank", 1, "D1  E2  A2  B2  E1  F2  F3  F4  A3  B4  A4  A5  B5  B6  A7  B7 "
                             "B1  C1  C2  C3  D3  E3  C4  D4  G4  G5  E5  F5  D5  D6  C6  C7 "),
        Connector("bank", 2, "T13 R13 T12 R12 R11 R10 N2  N3  P3  P4  M4  L4  N4  M5  L5  P5 "
                             "P11 P10 N12 N11 P13 N13 M1  M2  P1  N1  R1  R2  T2  R3  T3  T4 "),
        Connector("bank", 3, "L14 L13 M12 N16 R16 R15 P14 M15 P16 P15  -   -   -   -   -   - "
                             "K13 K12 M16 M14 T16 T14 N14   -   -   -  -   -   -   -   -   - ")
    ]

    def toolchain_program(self, products, name):
        (loader, bridge_bin) = find_loader()
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([loader, "-e", "-f", bitstream_filename,
                "-p", bridge_bin
            ])


if __name__ == "__main__":
    from .test.blinky import Blinky
    AlchitryAuPlatform().build(Blinky(), do_program=True)
