import os
import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_ecp5 import *
from amaranth_boards.resources import *


__all__ = ["Colorlight_5A75B_R80Platform"]


class Colorlight_5A75B_R80Platform(LatticeECP5Platform):
    device                 = "LFE5U-25F"
    package                = "BG256"
    speed                  = "6"
    default_clk            = "clk25"

    # Pins according to https://github.com/q3k/chubby75/blob/master/5a-75b/hardware_V8.0.md
    # Some of these still need verifying.

    resources = [
        Resource("clk25", 0, Pins("P6", dir="i"), Clock(25e6), Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins="T6", invert = True,
                      attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4")),

        *ButtonResources(pins="R7", invert = True,
                         attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")),

        UARTResource(0,
            tx="T6", # led (J19 DATA_LED-)
            rx="R7", # btn (J19 KEY+)
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),

        # SPIFlash (25Q32JVSIQ) 32-Mbits
        Resource("spi_flash", 0,
            Subsignal("cs",   PinsN("N8", dir="o")),
            # Subsignal("clk", Pins("", dir="i")),              # driven through USRMCLK
            Subsignal("cipo", Pins("T8", dir="i")),             # Chip: DI/IO0
            Subsignal("copi", Pins("T7", dir="o")),             #       DO/IO1
            # Subsignal("wp", PinsN("unknown", dir="o")),     #          IO2 Todo
            # Subsignal("hold", PinsN("unknown", dir="o")),   #          IO3 Todo
            Attrs(IO_TYPE="LVCMOS33")
        ),

        # 1x ESMT M12L64322A 2M 200MHz SDRAM (organized as 4 x 512k x 32bit)
        SDRAMResource(0,
            clk="C8", we_n="B5", cas_n="A6", ras_n="B6",
            ba="B7 A8", a="A9 B9 B10 C10 D9 C9 E9 D8 E8 C7 B8",
            dq="B2 A2 C3 A3 B3 A4 B4 A5 E7 C6 D7 D6 E6 D5 C5 E5 "
            "A11 B11 B12 A13 B13 A14 D14 D13 E11 C13 D11 C12 E10 C11 D10",
            attrs=Attrs(PULLMODE="NONE", DRIVE="4", SLEWRATE="FAST", IO_TYPE="LVCMOS33")
        ),

        # 2x Realtek RTL8211FD Gigabit Ethernet PHYs
        Resource("eth_rgmii", 0,
            Subsignal("rst",     PinsN("R6", dir="o")),
            Subsignal("mdc",     Pins("R5", dir="o")),
            Subsignal("mdio",    Pins("T4", dir="io")),
            Subsignal("tx_clk",  Pins("L1", dir="o")),
            Subsignal("tx_ctl",  Pins("L2", dir="o")),
            Subsignal("tx_data", Pins("M2 M1 P1 R1", dir="o")),
            Subsignal("rx_clk",  Pins("J1", dir="i")),
            Subsignal("rx_ctl",  Pins("J2", dir="i")),
            Subsignal("rx_data", Pins("K2 J3 K1 K3", dir="i")),
            Attrs(IO_TYPE="LVCMOS33")
        ),

        Resource("eth_rgmii", 1,
            Subsignal("rst",     PinsN("R6", dir="o")),
            Subsignal("mdc",     Pins("R5", dir="o")),
            Subsignal("mdio",    Pins("T4", dir="io")),
            Subsignal("tx_clk",  Pins("J16", dir="o")),
            Subsignal("tx_ctl",  Pins("K14", dir="o")),
            Subsignal("tx_data", Pins("K16 J15 J14 K15", dir="o")),
            Subsignal("rx_clk",  Pins("M16", dir="i")),
            Subsignal("rx_ctl",  Pins("P16", dir="i")),
            Subsignal("rx_data", Pins("M15 R16 L15 L16", dir="i")),
            Attrs(IO_TYPE="LVCMOS33")
        ),

    ]
    connectors = [
        Connector("j",  1, "C4  D4  E4  - D3  F5  E3  N4 N5 N3 P3 P4 M3 N1 M4 -"),
        Connector("j",  2, "F1  F2  G2  - G1  H2  H3  N4 N5 N3 P3 P4 M3 N1 M4 -"),
        Connector("j",  3, "B1  C2  C1  - D1  E2  E1  N4 N5 N3 P3 P4 M3 N1 M4 -"),
        Connector("j",  4, "P5  R3  P2  - R2  T2  N6  N4 N5 N3 P3 P4 M3 N1 M4 -"),
        Connector("j",  5, "T13 R12 R13 - R14 T14 P12 N4 N5 N3 P3 P4 M3 N1 M4 -"),
        Connector("j",  6, "R15 T15 P13 - P14 N14 H15 N4 N5 N3 P3 P4 M3 N1 M4 -"),
        Connector("j",  7, "G16 H14 G15 - F15 F16 E16 N4 N5 N3 P3 P4 M3 N1 M4 -"),
        Connector("j",  8, "D16 E15 C16 - B16 C15 B15 N4 N5 N3 P3 P4 M3 N1 M4 -"),
        #Connector("j", 19, " -  M13  -  - P11"),
    ]

    @property
    def required_tools(self):
        return super().required_tools + [
            "openFPGALoader"
        ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = dict(ecppack_opts="--compress")
        overrides.update(kwargs)
        return super().toolchain_prepare(fragment, name, **overrides)

    def toolchain_program(self, products, name):
        tool = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([tool, "-c", "ft232", "-m", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    Colorlight_5A75B_R80Platform().build(Blinky(), do_program=True)
