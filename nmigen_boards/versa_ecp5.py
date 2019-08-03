import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ecp5 import *
from .dev import *


__all__ = ["VersaECP5Platform"]


class VersaECP5Platform(LatticeECP5Platform):
    device      = "LFE5UM-45F"
    package     = "BG381"
    speed       = "8"
    default_clk = "clk100"
    resources   = [
        Resource("rst", 0, PinsN("T1", dir="i"), Attrs(IO_TYPE="LVCMOS33")),
        Resource("clk100", 0, DiffPairs("P3", "P4", dir="i"),
                 Clock(100e6), Attrs(IO_TYPE="LVDS")),
        Resource("pclk", 0, DiffPairs("A4", "A5", dir="i"),
                 Attrs(IO_TYPE="LVDS")),

        Resource("user_led", 0, PinsN("E16", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_led", 1, PinsN("D17", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_led", 2, PinsN("D18", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_led", 3, PinsN("E18", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_led", 4, PinsN("F17", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_led", 5, PinsN("F18", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_led", 6, PinsN("E17", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_led", 7, PinsN("F16", dir="o"), Attrs(IO_TYPE="LVCMOS25")),

        Resource("alnum_led", 0,
            Subsignal("a", PinsN("M20", dir="o")),
            Subsignal("b", PinsN("L18", dir="o")),
            Subsignal("c", PinsN("M19", dir="o")),
            Subsignal("d", PinsN("L16", dir="o")),
            Subsignal("e", PinsN("L17", dir="o")),
            Subsignal("f", PinsN("M18", dir="o")),
            Subsignal("g", PinsN("N16", dir="o")),
            Subsignal("h", PinsN("M17", dir="o")),
            Subsignal("j", PinsN("N18", dir="o")),
            Subsignal("k", PinsN("P17", dir="o")),
            Subsignal("l", PinsN("N17", dir="o")),
            Subsignal("m", PinsN("P16", dir="o")),
            Subsignal("n", PinsN("R16", dir="o")),
            Subsignal("p", PinsN("R17", dir="o")),
            Subsignal("dp", PinsN("U1", dir="o")),
            Attrs(IO_TYPE="LVCMOS25")
        ),

        Resource("user_sw", 0, PinsN("H2",  dir="i"), Attrs(IO_TYPE="LVCMOS15")),
        Resource("user_sw", 1, PinsN("K3",  dir="i"), Attrs(IO_TYPE="LVCMOS15")),
        Resource("user_sw", 2, PinsN("G3",  dir="i"), Attrs(IO_TYPE="LVCMOS15")),
        Resource("user_sw", 3, PinsN("F2",  dir="i"), Attrs(IO_TYPE="LVCMOS15")),
        Resource("user_sw", 4, PinsN("J18", dir="i"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_sw", 5, PinsN("K18", dir="i"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_sw", 6, PinsN("K19", dir="i"), Attrs(IO_TYPE="LVCMOS25")),
        Resource("user_sw", 7, PinsN("K20", dir="i"), Attrs(IO_TYPE="LVCMOS25")),

        UARTResource(0,
            rx="C11", tx="A11",
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")
        ),

        *SPIFlashResources(0,
            cs="R2", clk="U3", miso="W2", mosi="V2", wp="Y2", hold="W1",
            attrs=Attrs(IO_STANDARD="LVCMOS33")
        ),

        Resource("eth_clk125",     0, Pins("L19", dir="i"),
                 Clock(125e6), Attrs(IO_TYPE="LVCMOS25")),
        Resource("eth_clk125_pll", 0, Pins("U16", dir="i"),
                 Clock(125e6), Attrs(IO_TYPE="LVCMOS25")), # NC by default
        Resource("eth_rgmii", 0,
            Subsignal("rst",     PinsN("U17", dir="o")),
            Subsignal("mdc",     Pins("T18", dir="o")),
            Subsignal("mdio",    Pins("U18", dir="io")),
            Subsignal("tx_clk",  Pins("P19", dir="o")),
            Subsignal("tx_ctl",  Pins("R20", dir="o")),
            Subsignal("tx_data", Pins("N19 N20 P18 P20", dir="o")),
            Subsignal("rx_clk",  Pins("L20", dir="i")),
            Subsignal("rx_ctl",  Pins("U19", dir="i")),
            Subsignal("rx_data", Pins("T20 U20 T19 R18", dir="i")),
            Attrs(IO_TYPE="LVCMOS25")
        ),
        Resource("eth_sgmii", 0,
            Subsignal("rst",     PinsN("U17", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
            Subsignal("mdc",     Pins("T18", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
            Subsignal("mdio",    Pins("U18", dir="io"), Attrs(IO_TYPE="LVCMOS25")),
            Subsignal("tx",      DiffPairs("W13", "W14", dir="o")),
            Subsignal("rx",      DiffPairs("Y14", "Y15", dir="i")),
        ),

        Resource("eth_clk125",     1, Pins("J20", dir="i"),
                 Clock(125e6), Attrs(IO_TYPE="LVCMOS25")),
        Resource("eth_clk125_pll", 1, Pins("C18", dir="i"),
                 Clock(125e6), Attrs(IO_TYPE="LVCMOS25")), # NC by default
        Resource("eth_rgmii", 1,
            Subsignal("rst",     PinsN("F20", dir="o")),
            Subsignal("mdc",     Pins("G19", dir="o")),
            Subsignal("mdio",    Pins("H20", dir="io")),
            Subsignal("tx_clk",  Pins("C20", dir="o")),
            Subsignal("tx_ctrl", Pins("E19", dir="o")),
            Subsignal("tx_data", Pins("J17 J16 D19 D20", dir="o")),
            Subsignal("rx_clk",  Pins("J19", dir="i")),
            Subsignal("rx_ctrl", Pins("F19", dir="i")),
            Subsignal("rx_data", Pins("G18 G16 H18 H17", dir="i")),
            Attrs(IO_TYPE="LVCMOS25")
        ),
        Resource("eth_sgmii", 1,
            Subsignal("rst",     PinsN("F20", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
            Subsignal("mdc",     Pins("G19", dir="o"), Attrs(IO_TYPE="LVCMOS25")),
            Subsignal("mdio",    Pins("H20", dir="io"), Attrs(IO_TYPE="LVCMOS25")),
            Subsignal("tx",      DiffPairs("W17", "W18", dir="o")),
            Subsignal("rx",      DiffPairs("Y16", "Y17", dir="i")),
        ),

        Resource("ddr3", 0,
            Subsignal("rst",     PinsN("N4", dir="o")),
            Subsignal("clk",     DiffPairs("M4", "N5", dir="o"), Attrs(IO_TYPE="LVDS")),
            Subsignal("clk_en",  Pins("N2", dir="o")),
            Subsignal("cs",      PinsN("K1", dir="o")),
            Subsignal("we",      PinsN("M1", dir="o")),
            Subsignal("ras",     PinsN("P1", dir="o")),
            Subsignal("cas",     PinsN("L1", dir="o")),
            Subsignal("a",       Pins("P2 C4 E5 F5 B3 F4 B5 E4 C5 E3 D5 B4 C3", dir="o")),
            Subsignal("ba",      Pins("P5 N3 M3", dir="o")),
            Subsignal("dqs",     DiffPairs("K2 H4", "J1 G5", dir="io"), Attrs(IO_TYPE="LVDS")),
            Subsignal("dq",      Pins("L5 F1 K4 G1 L4 H1 G2 J3 D1 C1 E2 C2 F3 A2 E1 B1",
                                      dir="io")),
            Subsignal("dm",      Pins("J4 H5", dir="o")),
            Subsignal("odt",     Pins("L2", dir="o")),
            Attrs(IO_TYPE="LVCMOS15")
        )
    ]
    connectors = [
        Connector("expcon", 1, """
        -   -   -   B19 B12 B9  E6  D6  E7  D7  B11 B6  E9  D9  B8  C8  D8  E8  C7  C6
        -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        """), # X3
        Connector("expcon", 2, """
        A8  -   A12 A13 B13 C13 D13 E13 A14 C14 D14 E14 D11 C10 A9  B10 D12 E12 -   -
        B15 -   C15 -   D15 -   E15 A16 B16 -   C16 D16 B17 -   C17 A17 B18 A7  A18 -
        """), # X4
    ]

    file_templates = {
        **LatticeECP5Platform.file_templates,
        "{{name}}-openocd.cfg": r"""
        interface ftdi
        {# FTDI descriptors is identical between non-5G and 5G recent Versa boards #}
        ftdi_device_desc "Lattice ECP5_5G VERSA Board"
        ftdi_vid_pid 0x0403 0x6010
        ftdi_channel 0
        ftdi_layout_init 0xfff8 0xfffb
        reset_config none
        adapter_khz 25000

        # ispCLOCK device (unusable with openocd and must be bypassed)
        #jtag newtap ispclock tap -irlen 8 -expected-id 0x00191043
        # ECP5 device
        {% if "5G" in platform.device -%}
        jtag newtap ecp5 tap -irlen 8 -expected-id 0x81112043 ; # LFE5UM5G-45F
        {% else -%}
        jtag newtap ecp5 tap -irlen 8 -expected-id 0x01112043 ; # LFE5UM-45F
        {% endif %}
        """
    }

    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}-openocd.cfg".format(name), "{}.svf".format(name)) \
                as (config_filename, vector_filename):
            subprocess.check_call([openocd,
                "-f", config_filename,
                "-c", "transport select jtag; init; svf -quiet {}; exit".format(vector_filename)
            ])


if __name__ == "__main__":
    from ._blinky import build_and_program
    build_and_program(VersaECP5Platform)
