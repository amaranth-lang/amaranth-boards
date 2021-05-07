import os
import textwrap
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_spartan_3_6 import *
from .resources import *

__all__ = ["PanologicG2PlatformRevB", "PanologicG2PlatformRevC"]


class _PanologicG2Platform(XilinxSpartan6Platform):
    package = "fgg484"

    default_clk = "sysclk"
    default_rst = "sysrst"

    resources = [
        # 25/125 MHz System Clock
        Resource("sysclk", 0,                 Pins("Y13",  dir="i"), Attrs(IOSTANDARD="LVCMOS33"), Clock(125e6)),
        Resource("gmii_rst_as_clk_toggle", 0, PinsN("R11", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),

        # Reset Signals
        Resource("sysrst",    0, PinsN("AB14", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("reset_out", 0, PinsN("AA6",  dir="o"), Attrs(IOSTANDARD="LVCMOS33")),

        # Power Management
        Resource("sleep_req",   0, Pins("C13", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("power_sleep", 0, Pins("C10", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),

        # Pano Button LED Output, Active High
        *LEDResources(
            pins="E12",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
        Resource.family(1, default_name="led", ios=[Pins("B13", dir="o", conn=("AB", 0)), Attrs(IOSTANDARD="LVCMOS33")]),
        Resource.family(2, default_name="led", ios=[Pins("B12", dir="o", conn=("AB", 0)), Attrs(IOSTANDARD="LVCMOS33")]),

        # Pano Button Input, Active Low
        *ButtonResources(pins="B11", conn=("AB", 0), invert=True, attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # DVI Common
        I2CResource("ch7301c_i2c", 0,
            scl="E8", sda="D9",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        # DVI Interface 1 (DVI)
        Resource("ch7301c", 0,
            Subsignal("data",   Pins("B3 A3 B4 A4 B5 A5 B7 A7 B8 A8 B9 A9", conn=("AB", 0), dir="o")),
            Subsignal("xclk_p", Pins("A11",  conn=("AB", 0), dir="o")),
            Subsignal("xclk_n", Pins("A12",  conn=("AB", 0), dir="o")),
            Subsignal("hsync",  Pins("A20",  conn=("AB", 0), dir="o")),
            Subsignal("vsync",  Pins("A21",  conn=("AB", 0), dir="o")),
            Subsignal("de",     Pins("A21",  conn=("AB", 0), dir="o")),
            Subsignal("reset",  PinsN("A24", conn=("AB", 0), dir="o")),
            Subsignal("hpint",  Pins("A25",  conn=("AB", 0), dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        I2CResource("dcc", 0,
            scl="B20", sda="B21", conn=("AB", 0),
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        # DVI DCC as UART
        UARTResource(0, rx="B21", tx="B20", conn=("AB", 0), attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # DVI Interface 2 (micro-HDMI)
        Resource("ch7301c", 1,
            Subsignal("data",   Pins("T18 U16 V17 V19 V18 W17 Y17 Y15 Y18 Y19 AB21 T17", dir="o")),
            Subsignal("xclk_p", Pins("T15",  dir="o")),
            Subsignal("hsync",  Pins("AB15", dir="o")),
            Subsignal("vsync",  Pins("T16",  dir="o")),
            Subsignal("de",     Pins("AB16", dir="o")),
            Subsignal("reset",  PinsN("W18", dir="o")),
            Subsignal("hpint",  Pins("AB18", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        I2CResource("dcc", 1,
            scl="AA21", sda="AB19",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        # Micro-HDMI DCC as UART
        UARTResource(1, rx="AB19", tx="AB21", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # USB PHY
        Resource("ulpi", 0,
            Subsignal("rst",  Pins("C9",  dir="o")),
            Subsignal("clk",  Pins("C12", dir="i")),
            Subsignal("dir",  Pins("C7",  dir="i")),
            Subsignal("nxt",  Pins("C5",  dir="i")),
            Subsignal("stp",  Pins("A5",  dir="o")),
            Subsignal("data", Pins("A7 B8 A8 D6 C6 B6 A6 A4", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # Audio interface
        Resource("wm8750bg", 0,
            Subsignal("bclk",   Pins("AB13", dir="o")),
            Subsignal("adclrc", Pins("W9",   dir="o")),
            Subsignal("adcdat", Pins("R13",  dir="i")),
            Subsignal("daclrc", Pins("U6",   dir="o")),
            Subsignal("dacdat", Pins("Y14",  dir="o")),
            Subsignal("mclk",   Pins("W14",  dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        I2CResource("wm8750bg_i2c", 0,
            scl="U17", sda="AB17",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        # Ethernet PHY
        Resource("gmii", 0,
            Subsignal("rst",     PinsN("R11", dir="o")),
            Subsignal("int",     PinsN("AA4", dir="o")),
            Subsignal("mdio",    Pins("AA2",  dir="io")),
            Subsignal("mdc",     Pins("AB6",  dir="o")),
            Subsignal("gtx_clk", Pins("AA12", dir="o")),
            Subsignal("tx_clk",  Pins("Y11",  dir="i")),
            Subsignal("tx_en",   Pins("AA8",  dir="o")),
            Subsignal("tx_er",   Pins("AB8",  dir="o")),
            Subsignal("tx_data", Pins("AB2 AB3 AB4 AB7 AB9 AB10 T7 Y10", dir="o")),
            Subsignal("rx_clk",  Pins("AB11", dir="i")),
            Subsignal("rx_dv",   Pins("Y7",   dir="i")),
            Subsignal("rx_er",   Pins("Y8",   dir="i")),
            Subsignal("rx_data", Pins("Y3 Y4 R9 R7 V9 R8 U9 Y9", dir="i")),
            Subsignal("col",     Pins("V7",   dir="i")),
            Subsignal("crs",     Pins("W4",   dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # DDR2 SDRAM Interface A
        Resource("ddr2", 0,
            Subsignal("clk", DiffPairs("H20", "J19", dir="o"),
                        Attrs(IOSTANDARD="DIFF_SSTL18_II", IN_TERM="NONE")),
            Subsignal("clk_en", Pins("D21",  dir="o")),
            Subsignal("we",     PinsN("H19", dir="o")),
            Subsignal("ras",    PinsN("H21", dir="o")),
            Subsignal("cas",    PinsN("H22", dir="o")),
            Subsignal("a",      Pins("F21 F22 E22 G20 F20 K20 K19 E20 C20 C22 G19 F19 D22", dir="o")),
            Subsignal("ba",     Pins("J17 K17 H18", dir="o")),
            Subsignal("dqs",    DiffPairs("T21 L20", "T22 L22", dir="o"),
                        Attrs(IOSTANDARD="DIFF_SSTL18_II")),
            Subsignal("dq",     Pins("N20 N22 M21 M22 J20 J22 K21 K22 P21 P22 R20 R22 U20 U22 V21 V22", dir="io")),
            Subsignal("dm",     Pins("M20 L19", dir="o")),
            Subsignal("odt",    Pins("G22",  dir="o")),
            Attrs(IOSTANDARD="SSTL18_II", SLEW="FAST"),
        ),

        # DDR2 SDRAM Interface B
        Resource("ddr2", 1,
            Subsignal("clk", DiffPairs("H4", "H3", dir="o"),
                        Attrs(IOSTANDARD="DIFF_SSTL18_II", IN_TERM="NONE")),
            Subsignal("clk_en", Pins("D2",  dir="o")),
            Subsignal("we",     PinsN("F2", dir="o")),
            Subsignal("ras",    PinsN("K5", dir="o")),
            Subsignal("cas",    PinsN("K4", dir="o")),
            Subsignal("a",      Pins("H2 H1 H5 K6 F3 K3 J4 H6 E3 E1 G4 C1 D1", dir="o")),
            Subsignal("ba",     Pins("G3 G1 F1", dir="o")),
            Subsignal("dqs",    DiffPairs("T2 L3", "T1 L1", dir="o"),
                        Attrs(IOSTANDARD="DIFF_SSTL18_II")),
            Subsignal("dq",     Pins("N3 N1 M2 M1 J3 J1 K2 K1 P2 P1 R3 R1 U3 U1 V2 V1", dir="io")),
            Subsignal("dm",     Pins("M3 L4", dir="o")),
            Subsignal("odt",    Pins("J6",  dir="o")),
            Attrs(IOSTANDARD="SSTL18_II", SLEW="FAST"),
        ),

        # SPI Flash
        *SPIFlashResources(0,
            cs_n="T5", clk="Y21", copi="AB20", cipo="AA20",
            attrs=Attrs(IOSTANDARD="LVCMOS33"),
        )
    ]

    connectors  = [
        Connector("AB", 0, {
            "B3":  "D17", "A3":  "A14",
            "B4":  "A15", "A4":  "A16",
            "B5":  "A17", "A5":  "A18",
            "B7":  "D14", "A7":  "B14",
            "B8":  "B16", "A8":  "B18",
            "B9":  "E16", "A9":  "D15",
            "B11": "H12", "A11": "E14",
            "B12": "F13", "A12": "F15",
            "B13": "H13",
                          "A15": "D9",
            "B20": "C14", "A20": "F12",
            "B21": "C17", "A21": "C16",
                          "A23": "F14",
                          "A24": "C15",
                          "A25": "D13"
        })
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "add_constraints": """
            CONFIG VCCAUX = "2.5";
            """}
        return super().toolchain_prepare(
            fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name, *, programmer="urjtag", cable=None):
        assert programmer in ("impact", "openocd", "urjtag", "xc3sprog")

        if programmer == "impact":
            cable=cable or "-port auto"
            impact = os.environ.get("IMPACT", "impact")
            with products.extract("{}.bit".format(name)) as bitfile:
                cmd = textwrap.dedent("""
                    setMode -bscan
                    setCable {}
                    addDevice -p 1 -file "{}"
                    program -p 1
                    exit
                """).format(cable, bitfile).encode('utf-8')
                subprocess.run([impact, "-batch"], input=cmd, check=True)

        elif programmer == "openocd":
            cable = cable or "interface/altera-usb-blaster.cfg"
            openocd = os.environ.get("OPENOCD", "openocd")
            with products.extract("{}.bit".format(name)) as bitfile:
                cmd = textwrap.dedent("""
                    source [find {}];
                    source [find cpld/xilinx-xc6s.cfg];
                    init;
                    xc6s_program xc6s.tap;
                    pld load 0 {};
                    exit
                """).format(cable, bitfile).encode('utf-8')
                subprocess.check_call([openocd, "-c", cmd])

        elif programmer == "urjtag":
            cable = cable or "usbblaster"
            urjtag = os.environ.get("URJTAG", "jtag")
            with products.extract("{}.bit".format(name)) as bitfile:
                cmd = textwrap.dedent("""
                    cable {}
                    detect

                    register BYPASS 1
                    instruction LENGTH 6

                    instruction CFG_IN 000010 BYPASS
                    instruction JPROGRAM 001011 BYPASS
                    instruction JSTART 001100 BYPASS

                    pld load {}
                """).format(cable, bitfile).encode('utf-8')
                subprocess.run([urjtag], input=cmd, check=True)

        else:
            cable = cable or "ft232h"
            xc3sprog = os.environ.get("XC3SPROG", "xc3sprog")
            with products.extract("{}.bit".format(name)) as bitfile:
                subprocess.check_call([xc3sprog, "-c", cable, bitfile])


class PanologicG2PlatformRevB(_PanologicG2Platform):
    device  = "xc6slx150"
    speed   = "2"


class PanologicG2PlatformRevC(_PanologicG2Platform):
    device  = "xc6slx100"
    speed   = "3"


if __name__ == "__main__":
    import argparse
    from .test.blinky import *

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--rev", choices=("B", "C"), default="B",
        help="Panologic G2 revision (default: %(default)s)")

    parser.add_argument("--programmer", choices=("impact", "openocd", "urjtag", "xc3sprog"),
        help="Programmer (default: %(default)s)")

    parser.add_argument("--cable", type=str,
        help=textwrap.dedent("""Cable or interface for the selected programmer.
        impact example:  "-target \"xilinx_xvc host=10.42.0.118:2542 disableversioncheck=true\""
        openocd example: "interface/altera-usb-blaster.cfg"
        urjtag example:  "usbblaster"
        x3sprog example: "ft232h"
        """)
        )

    args = parser.parse_args()

    if args.programmer is None and args.cable:
        parser.error("--programmer must be provide for a --cable")

    platform = {"B": PanologicG2PlatformRevB, "C": PanologicG2PlatformRevC}[args.rev]

    platform().build(Blinky(), do_program=args.programmer is not None, program_opts={"programmer": args.programmer, "cable": args.cable})
