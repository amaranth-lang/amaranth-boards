import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ecp5 import *
from .resources import *


__all__ = ["ECP55GEVNPlatform"]


class ECP55GEVNPlatform(LatticeECP5Platform):
    device      = "LFE5UM5G-85F"
    package     = "BG381"
    speed       = "8"
    default_clk = "clk12"
    default_rst = "rst"

    def __init__(self, *, VCCIO1="2V5", VCCIO6="3V3", **kwargs):
        """
        VCCIO1 is connected by default to 2.5 V via R100 (can be set to 3.3 V by disconnecting
        R100 and connecting R105)
        VCCIO6 is connected to 3.3 V by default via R99 (can be switched to 2.5 V with R104,
        see page 51 in the ECP5-5G-EVN datasheet)
        """
        super().__init__(**kwargs)
        assert VCCIO1 in ("3V3", "2V5")
        assert VCCIO6 in ("3V3", "2V5")
        self._VCCIO1 = VCCIO1
        self._VCCIO6 = VCCIO6

    def _vccio_to_iostandard(self, vccio):
        if vccio == "2V5":
            return "LVCMOS25"
        if vccio == "3V3":
            return "LVCMOS33"
        assert False

    def bank1_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIO1)

    def bank6_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIO6)

    resources   = [
        Resource("rst", 0, PinsN("G2", dir="i"), Attrs(IO_TYPE="LVCMOS33")),
        Resource("clk12", 0, Pins("A10", dir="i"),
                 Clock(12e6), Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins="A13 A12 B19 A18 B18 C17 A17 B17", invert=True,
                      attrs=Attrs(IO_TYPE=bank1_iostandard)),
        *ButtonResources(pins="P4", invert=True,
                         attrs=Attrs(IO_TYPE=bank6_iostandard)),
        *SwitchResources(pins={1: "J1", 2: "H1", 3: "K1"}, invert=True,
                         attrs=Attrs(IO_TYPE=bank6_iostandard)),
        *SwitchResources(pins={4: "E15", 5: "D16", 6: "B16", 7: "C16", 8: "A16"}, invert=True,
                         attrs=Attrs(IO_TYPE=bank1_iostandard)),

        Resource("serdes", 0,
            Subsignal("tx", DiffPairs("W4", "W5", dir="o")),
            Subsignal("rx", DiffPairs("Y5", "Y6", dir="i")),
        ),
        Resource("serdes", 1,
            Subsignal("tx", DiffPairs("W8", "W9", dir="o")),
            Subsignal("rx", DiffPairs("Y7", "Y8", dir="i")),
        ),
        Resource("serdes", 2,
            Subsignal("tx", DiffPairs("W13", "W14", dir="o")),
            Subsignal("rx", DiffPairs("Y14", "Y15", dir="i")),
        ),
        Resource("serdes", 3,
            Subsignal("tx", DiffPairs("W17", "W18", dir="o")),
            Subsignal("rx", DiffPairs("Y16", "Y17", dir="i")),
        ),

        Resource("serdes_clk", 0, DiffPairs("Y11", "Y12", dir="i")),
        Resource("serdes_clk", 1, DiffPairs("Y19", "W20", dir="i")), # 200 MHz

        # TODO: add other resources
    ]
    connectors  = [
        # Expansion connectors
        Connector("J", 39, "- - - D15 B15 C15 B13 B20 D11 E11 B12 C12 D12 E12 C13 D13 E13 A14 A9 B10 - - - - - - - - E7 - A11 - A19 - - - - - - -"),
        Connector("J", 40, "K2 - A15 F1 H2 G1 J4 J5 J3 K3 L4 L5 M4 N5 N4 P5 N3 M3 - - K5 - M5 - L3 - N2 M1 L2 - L1 N1 C14 - P1 E14 D14 - K4 -"),
        # Arduino
        Connector("J", 6, "K16 J16 H17 J17 H18 H16 - G18 G16 F17"),
        Connector("J", 3, "F19 F20 E20 E19 D19 D20 C20 K17"),
        Connector("J", 7, "C18 - D17 - - - - -"),
        Connector("J", 4, "F18 E17 E18 D18 F16 E16"),
        # Raspberry Pi
        Connector("JP", 8, "- - T17 - U16 - U17 P18 - N20 N19 T16 M18 - N17 P17 - M17 U20 - T19 N18 R20 U19 - R18 L18 L17 U18 - T18 T20 P20 - R17 P19 N16 P16 - R16"),
        # GPIO
        Connector("J", 5, "- - H20 G19 - - K18 J18 - - K19 J19 - - K20 J20 - - G20 - - -"), # Contains 4 differential pairs
        Connector("J", 8, "- - L19 M19 L20 M20 L16 -"),
        Connector("J", 32, "- - - - A5 A4 - - C5 B5 - - B4 C4 - - B3 A3 - - D5 E4 - - D3 C3 - - E3 F4 - - F5 E5 - - B1 A2 - -"), # Contains 9 differential pairs
        Connector("J", 33, "- - - - C2 B2 - - D1 C1 - - E1 D2 - - G5 H4 - - H3 H5 - - F3 G3 - - E2 F2 - -"), # Contains 7 differential pairs
        # Mic
        Connector("J", 30, "- B6 D9 C9 E9 D10 A6 E10 - -"),
        # PMOD
        Connector("J", 31, "C6 C7 E8 D8 - - C8 B8 A7 A8 - -"),
        # JTAG
        Connector("J", 1, "- V4 R5 - - U5 - T5"),
        # Parallel configuration
        Connector("J", 38, "W3 R2 T3 Y3 R1 V3 T1 V2 U1 W2 V1 T2 W1 U2 Y2 R2 U3 R3 - -"), # Connect pin 2 / R2 with jumper when needed
    ]

    @property
    def file_templates(self):
        return {
            **super().file_templates,
            "{{name}}-openocd.cfg": r"""
            interface ftdi
            ftdi_device_desc "Lattice ECP5 Evaluation Board"
            ftdi_vid_pid 0x0403 0x6010
            ftdi_channel 0
            ftdi_layout_init 0xfff8 0xfffb
            reset_config none
            adapter_khz 25000

            jtag newtap ecp5 tap -irlen 8 -expected-id 0x81113043
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
    from .test.blinky import *
    ECP55GEVNPlatform().build(Blinky(), do_program=True)
