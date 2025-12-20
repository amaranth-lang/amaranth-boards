import os
import subprocess

from amaranth.build import *
from amaranth.vendor import LatticeECP5Platform
from .resources import *


__all__ = ["Colorlight_5A75B_R70Platform"]


class Colorlight_5A75B_R70Platform(LatticeECP5Platform):
    device                 = "LFE5U-25F"
    package                = "BG256"
    speed                  = "6"
    default_clk            = "clk25"

    resources = [
        Resource("clk25", 0, Pins("P6", dir="i"), Clock(25e6), Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins="P11", invert = True,
                      attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4")),

        *ButtonResources(pins="M13", invert = True,
                         attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")),

        UARTResource(0,
            tx="P11", # led (J19 DATA_LED-)
            rx="M13", # btn (J19 KEY+)
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),

        # SPIFlash (W25Q32JV)   1x/2x/4x speed
        Resource("spi_flash", 0,
            Subsignal("cs",   PinsN("N8", dir="o")),
            # Subsignal("clk", Pins("", dir="i")),              # driven through USRMCLK
            Subsignal("cipo", Pins("T8", dir="i")),             # Chip: DI/IO0
            Subsignal("copi", Pins("T7", dir="o")),             #       DO/IO1
            # Subsignal("wp", PinsN("unknown", dir="o")),     #          IO2 Todo
            # Subsignal("hold", PinsN("unknown", dir="o")),   #          IO3 Todo
            Attrs(IO_TYPE="LVCMOS33")
        ),

        # 2x ESMT M12L16161A-5T 1M x 16bit 200MHz SDRAMs (organized as 1M x 32bit)
        # 2x WinBond W9816G6JH-6 1M x 16bit 166MHz SDRAMs (organized as 1M x 32bit) are lso reported 
        SDRAMResource(0,
            clk="C6", we_n="C7", cas_n="E7", ras_n="D7",
            ba="A7", a="A9 E10 B12 D13 C12 D11 D10 E9 D9 B7 C8",
            dq="B13 C11 C10 A11 C9 E8  B6  B9  A6  B5  A5  B4  B3 C3  A2  B2 "
               "E2  D3  A4  E4  D4 C4  E5  D5  E6  D6  D8  A8  B8 B10 B11 E11",
            attrs=Attrs(PULLMODE="NONE", DRIVE="4", SLEWRATE="FAST", IO_TYPE="LVCMOS33")
        ),

        # Broadcom B50612D Gigabit Ethernet Transceiver
        Resource("eth_rgmii", 0,
            Subsignal("rst",     PinsN("P5", dir="o")),
            Subsignal("mdc",     Pins("P3", dir="o")),
            Subsignal("mdio",    Pins("T2", dir="io")),
            Subsignal("tx_clk",  Pins("M2", dir="o")),
            Subsignal("tx_ctl",  Pins("M3", dir="o")),
            Subsignal("tx_data", Pins("L1 L3 P2 L4", dir="o")),
            Subsignal("rx_clk",  Pins("M1", dir="i")),
            Subsignal("rx_ctl",  Pins("N6", dir="i")),
            Subsignal("rx_data", Pins("N1 M5 N5 M6", dir="i")),
            Attrs(IO_TYPE="LVCMOS33")
        ),

        # Broadcom B50612D Gigabit Ethernet Transceiver
        Resource("eth_rgmii", 1,
            Subsignal("rst",     PinsN("P5", dir="o")),
            Subsignal("mdc",     Pins("P3", dir="o")),
            Subsignal("mdio",    Pins("T2", dir="io")),
            Subsignal("tx_clk",  Pins("M12", dir="o")),
            Subsignal("tx_ctl",  Pins("R15", dir="o")),
            Subsignal("tx_data", Pins("T14 R12 R13 R14", dir="o")),
            Subsignal("rx_clk",  Pins("M16", dir="i")),
            Subsignal("rx_ctl",  Pins("L15", dir="i")),
            Subsignal("rx_data", Pins("P13 N13 P14 M15", dir="i")),
            Attrs(IO_TYPE="LVCMOS33")
        ),

    ]
    connectors = [
        Connector("j",  1, "F3  F1  G3  - G2  H3  H5  F15 L2 K1 J5 K2 B16 J14 F12 -"),
        Connector("j",  2, "J4  K3  G1  - K4  C2  E3  F15 L2 K1 J5 K2 B16 J14 F12 -"),
        Connector("j",  3, "H4  K5  P1  - R1  L5  F2  F15 L2 K1 J5 K2 B16 J14 F12 -"),
        Connector("j",  4, "P4  R2  M8  - M9  T6  R6  F15 L2 K1 J5 K2 B16 J14 F12 -"),
        Connector("j",  5, "M11 N11 P12 - K15 N12 L16 F15 L2 K1 J5 K2 B16 J14 F12 -"),
        Connector("j",  6, "K16 J15 J16 - J12 H15 G16 F15 L2 K1 J5 K2 B16 J14 F12 -"),
        Connector("j",  7, "H13 J13 H12 - G14 H14 G15 F15 L2 K1 J5 K2 B16 J14 F12 -"),
        Connector("j",  8, "A15 F16 A14 - E13 B14 A13 F15 L2 K1 J5 K2 B16 J14 F12 -"),
        Connector("j", 19, " -  M13  -  - P11"),
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
    Colorlight_5A75B_R70Platform().build(Blinky(), do_program=True)
