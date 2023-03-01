import os
import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_nexus import *
from amaranth.back import verilog
from .resources import *


__all__ = ["LIFCLEVNPlatform"]


class LIFCLEVNPlatform(LatticeNexusPlatform):
    device      = "LIFCL-40"
    package     = "BG400"
    speed       = "8"
    default_clk = "clk12"
    default_rst = "rst"

    def __init__(self, *, VCCIO0="3V3", VCCIO1="3V3", VCCIO2="3V3", VCCIO3="1V8", VCCIO4="1V8", VCCIO5="1V8", VCCIO6="3V3", VCCIO7="3V3", **kwargs):
        """
        Table 3.1. CrossLink-NX VCCIO Supply Options
        VCCIO Bank  Selection           V3P3        V1P8
        --------------------------------------------------------------
        VCCIO0      J44 Connector       Default     Selectable
        VCCIO1      —                   Fixed       N/A
        VCCIO2      —                   Fixed       N/A
        VCCIO3      —                   N/A         Fixed
        VCCIO4      —                   N/A         Fixed
        VCCIO5      —                   N/A         Fixed
        VCCIO6      J42 Connector       Default     Selectable
        VCCIO7      —                   Fixed       N/A
        --------------------------------------------------------------
        see page 14 in FPGA-EB-1-4-Crosslink-NX-Evaluation-Board.pdf"
        """
        super().__init__(**kwargs)
        assert VCCIO0 in ("3V3", "1V8")
        assert VCCIO1 in ("3V3",      )
        assert VCCIO2 in ("3V3",      )
        assert VCCIO3 in (       "1V8")
        assert VCCIO4 in (       "1V8")
        assert VCCIO5 in (       "1V8")
        assert VCCIO6 in ("3V3", "1V8")
        assert VCCIO7 in ("3V3",      )
        self._VCCIO0 = VCCIO0
        self._VCCIO1 = VCCIO1
        self._VCCIO2 = VCCIO2
        self._VCCIO3 = VCCIO3
        self._VCCIO4 = VCCIO4
        self._VCCIO5 = VCCIO5
        self._VCCIO6 = VCCIO6
        self._VCCIO7 = VCCIO7

    def _vccio_to_iostandard(self, vccio):
        if vccio == "1V8":
            return "LVCMOS18"
        if vccio == "3V3":
            return "LVCMOS33"
        assert False

    def bank0_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIO0)

    def bank1_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIO1)

    def bank2_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIO2)

    def bank6_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIO6)

    #Clock Frequency  Signal Name        CrossLink-NX Ball Location  Clock Source  Comments
    #12 MHz           12 MHz             L13                         U1            JP2 installed. JP1 removed.
    #200 MHz          200 MHz/200 MHz_n  C12/ C11                    U5            Insert R65 & R66, remove R54 & R56
    #125 MHz          125 MHz/125 MHz_n  C12/ C11                    U4            Insert R54 & R56, remove R65 & R66
    resources   = [
        Resource("rst", 0, Pins("G19", dir="i"), # gsrn
                              Attrs(IO_TYPE=bank1_iostandard)),
        Resource("clk12", 0, Pins("L13", dir="i"),
                 Clock(12e6), Attrs(IO_TYPE=bank1_iostandard)),
        Resource("clk125", 0, Pins("C12", dir="i"),
                 Clock(125e6), Attrs(IO_TYPE="LVDS")),

        Resource("i2c", 0,
            Subsignal("scl", Pins("Y5", dir="io"), Attrs(IO_TYPE="LVCMOS18H")),
            Subsignal("sda", Pins("W5", dir="io"), Attrs(IO_TYPE="LVCMOS18H")),
        ),

        *LEDResources(pins={0: "E17", 1: "F13", 2: "G13", 3: "F14", 4: "L16", 5: "L15", 6: "L20", 7: "L19"}, invert=True,
                              attrs=Attrs(IO_TYPE=bank1_iostandard)),
        *LEDResources(pins={8: "R17", 9: "R18", 10: "U20", 11: "T20", 12: "W20", 13: "V20"}, invert=True,
                              attrs=Attrs(IO_TYPE=bank2_iostandard)),

        #*ButtonResources(pins="G14 G15", invert=True,
        #                 attrs=Attrs(IO_TYPE="LVCMOS33")),
        #*SwitchResources(pins={1: "J1", 2: "H1", 3: "K1"}, invert=True,
        #                 attrs=Attrs(IO_TYPE=bank6_iostandard)),
        #*SwitchResources(pins={4: "E15", 5: "D16", 6: "B16", 7: "C16", 8: "A16"}, invert=True,
        #                 attrs=Attrs(IO_TYPE=bank1_iostandard)),

        # Requires installation of 0-ohm jumpers R15 and R17 to properly route signals
        # Note that it is R15 and R17, not R16 and R17 as stated in the user guide
        UARTResource(0,
            rx="F16", tx="F18",
            attrs=Attrs(IO_TYPE=bank1_iostandard, PULLMODE="UP")
        ),

        *SPIFlashResources(0,
            cs_n="E13", clk="E12", cipo="D15", copi="D13", wp_n="D14", hold_n="W1",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),

        # TODO: add other resources
    ]
    connectors  = [
        ## Expansion connectors
        #Connector("J", 39, "- - - D15 B15 C15 B13 B20 D11 E11 B12 C12 D12 E12 C13 D13 E13 A14 A9 B10 - - - - - - - - E7 - A11 - A19 - - - - - - -"),
        #Connector("J", 40, "K2 - A15 F1 H2 G1 J4 J5 J3 K3 L4 L5 M4 N5 N4 P5 N3 M3 - - K5 - M5 - L3 - N2 M1 L2 - L1 N1 C14 - P1 E14 D14 - K4 -"),
        ## Arduino
        #Connector("J", 6, "K16 J16 H17 J17 H18 H16 - G18 G16 F17"),
        #Connector("J", 3, "F19 F20 E20 E19 D19 D20 C20 K17"),
        #Connector("J", 7, "C18 - D17 - - - - -"),
        #Connector("J", 4, "F18 E17 E18 D18 F16 E16"),
        ## Raspberry Pi
        #Connector("JP", 8, "- - T17 - U16 - U17 P18 - N20 N19 T16 M18 - N17 P17 - M17 U20 - T19 N18 R20 U19 - R18 L18 L17 U18 - T18 T20 P20 - R17 P19 N16 P16 - R16"),
        ## GPIO
        #Connector("J", 5, "- - H20 G19 - - K18 J18 - - K19 J19 - - K20 J20 - - G20 - - -"), # Contains 4 differential pairs
        #Connector("J", 8, "- - L19 M19 L20 M20 L16 -"),
        #Connector("J", 32, "- - - - A5 A4 - - C5 B5 - - B4 C4 - - B3 A3 - - D5 E4 - - D3 C3 - - E3 F4 - - F5 E5 - - B1 A2 - -"), # Contains 9 differential pairs
        #Connector("J", 33, "- - - - C2 B2 - - D1 C1 - - E1 D2 - - G5 H4 - - H3 H5 - - F3 G3 - - E2 F2 - -"), # Contains 7 differential pairs
        ## Mic
        #Connector("J", 30, "- B6 D9 C9 E9 D10 A6 E10 - -"),
        ## PMOD
        #Connector("J", 31, "C6 C7 E8 D8 - - C8 B8 A7 A8 - -"),
        ## JTAG
        #Connector("J", 1, "- V4 R5 - - U5 - T5"),
        ## Parallel configuration
        #Connector("J", 38, "W3 R2 T3 Y3 R1 V3 T1 V2 U1 W2 V1 T2 W1 U2 Y2 R2 U3 R3 - -"), # Connect pin 2 / R2 with jumper when needed
    ]

    @property
    def file_templates(self):
        return {
            **super().file_templates,
            "{{name}}-openocd.cfg": r"""
            interface ftdi
            ftdi_device_desc "Lattice Nexus Evaluation Board"
            ftdi_vid_pid 0x0403 0x6010
            ftdi_channel 0
            ftdi_layout_init 0xfff8 0xfffb
            reset_config none
            adapter_khz 25000

            jtag newtap ecp5 tap -irlen 8 -expected-id 0x81113043
            """
        }

    def toolchain_program(self, products, name):
        ecpprog = os.environ.get("ECPPROG", "ecpprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([ecpprog, "-S", bitstream_filename])

if __name__ == "__main__":
    from .test.blinky import *
    LIFCLEVNPlatform().build(Blinky(), do_program=True)
