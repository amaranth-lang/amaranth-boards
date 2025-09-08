import textwrap
import subprocess

from nmigen.vendor.xilinx_7series import *
from nmigen_boards.resources import *
from nmigen.build import *

__all__ = ["Basys3Platform"]

class Basys3Platform(Xilinx7SeriesPlatform):
    """
    Platform module for Digilent Basys 3

    Based on:
    https://reference.digilentinc.com/reference/programmable-logic/basys-3/
    https://github.com/Digilent/digilent-xdc/blob/master/Basys-3-Master.xdc
    """

    device = "xc7a35t"
    package = "cpg236"
    speed = "1"
    default_clk = "clk100"

    resources = [
        Resource("clk100", 0, Pins("W5", dir="i"), Clock(100e6), Attrs(IOSTANDARD="LVCMOS33")),

        *SwitchResources(pins="V17 V16 W16 W17 W15 V15 W14 W13 V2 T3 T2 R3 W2 U1 T1 R2",
                attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(pins="U16 E19 U19 V19 W18 U15 U14 V14 V13 V3 W3 U3 P3 N3 P1 L1",
                attrs=Attrs(IOSTANDARD="LVCMOS33")),

        UARTResource(0, rx="B18", tx="A18", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("vga", 0,
            Subsignal("r", Pins("G19 H19 J19 N19", dir="o")),
            Subsignal("g", Pins("J17 H17 G17 D17", dir="o")),
            Subsignal("b", Pins("N18 L18 K18 J18", dir="o")),
            Subsignal("hs", Pins("P19", dir="o")),
            Subsignal("vs", Pins("R19", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33"),
        ),

        Resource("ps2", 0,
            Subsignal("clk", Pins("C17", dir="o")),
            Subsignal("dat", Pins("B17", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33", PULLUP="true"),
        ),

        *SPIFlashResources(0,
            cs_n="K19", clk="C11", copi="D18", cipo="D19",
            wp_n="G18", hold_n="F18",
            attrs=Attrs(IOSTANDARD="LVCMOS33"),
        ),

        Display7SegResource(0,
            a="W7", b="W6", c="U8", d="V8",
            e="U5", f="V5", g="U7", dp="V7",
            attrs=Attrs(IOSTANDARD="LVCMOS33"),
        ),
        Resource("display_anode", Pins("U2 U4 V4 W4"), Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(pins={
            "C": "U18",
            "U": "T18",
            "L": "W19",
            "R": "T17",
            "D": "U17"},
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
    ]

    connectors = [
        Connector("pmod", 0, "J1 L2 J2 G2 - - H1 K2 H2 G3 - -"), # JA
        Connector("pmod", 1, "A14 A16 B15 B16 - - A15 A17 C15 C16 - -"), # JB
        Connector("pmod", 2, "K17 M18 N17 P18 - - L17 M19 P17 R18 - -"), # JC

        Connector("xadc", 0, "J3 L3 M2 N2 - - K3 M3 M1 N1 - -"), # JXADC
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "add_constraints":
                """
                set_property CFGBVS VCCO [current_design]
                set_property CONFIG_VOLTAGE 3.3 [current_design]
                """
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, product, name):
        with product.extract(f"{name}.bin") as bit_filename:
            script = textwrap.dedent(f"""
            open_hw_manager
            connect_hw_server
            open_hw_target

            current_hw_device [lindex [get_hw_devices] 0]
            set_property PROGRAM.FILE {{{bit_filename}}} [current_hw_device]
            program_hw_devices [current_hw_device]

            close_hw_target
            disconnect_hw_server
            close_hw_manager
            """
            ).encode()
            subprocess.run(["vivado", "-nolog", "-nojournal", "-mode", "tcl"],
                    input=script, check=True)

if __name__ == "__main__":
    from .test.blinky import *
    Basys3Platform().build(Blinky(), do_program=True)
