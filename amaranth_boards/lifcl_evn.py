import os
import subprocess

from amaranth.build import *
from amaranth.vendor import LatticeNexusPlatform
from amaranth.back import verilog
from .resources import *
import pdb

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
        VCCIO1      -                   Fixed       N/A
        VCCIO2      -                   Fixed       N/A
        VCCIO3      -                   N/A         Fixed
        VCCIO4      -                   N/A         Fixed
        VCCIO5      -                   N/A         Fixed
        VCCIO6      J42 Connector       Default     Selectable
        VCCIO7      -                   Fixed       N/A
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

        # Raspberry Pi Board GPIO Header
        Connector("raspberry_pi", 0, {
            "P0": "-",      #  0 (no pin 0)
            "P1": "-",      #  1 3.3V
            "P2": "-",      #  2 5V
            "P3": "L6",     #  3 RASP_IO02
            "P4": "-",      #  4 5V
            "P5": "L5",     #  5 RASP_IO03
            "P6": "-",      #  6 GND
            "P7": "M3",     #  7 RASP_IO04
            "P8": "M2",     #  8 RASP_IO14
            "P9": "-",      #  9 GND
            "P10": "L1",    # 10 RASP_IO15
            "P11": "L2",    # 11 RASP_IO17
            "P12": "R2",    # 12 RASP_IO18
            "P13": "R1",    # 13 RASP_IO27
            "P14": "-",     # 14 GND
            "P15": "P2",    # 15 RASP_IO22
            "P16": "P1",    # 16 RASP_IO23
            "P17": "-",     # 17 3.3V
            "P18": "K7",    # 18 RASP_IO24
            "P19": "N4",    # 19 RASP_IO10
            "P20": "-",     # 20 GND
            "P21": "K6",    # 21 RASP_IO09
            "P22": "K5",    # 22 RASP_IO25
            "P23": "N7",    # 23 RASP_IO11
            "P24": "P6",    # 24 RASP_IO08
            "P25": "-",     # 25 GND
            "P26": "N5",    # 26 RASP_IO07
            "P27": "M7",    # 27 RASP_ID_SD
            "P28": "M4",    # 28 RASP_ID_SC
            "P29": "K8",    # 29 RASP_IO05
            "P30": "-",     # 30 GND
            "P31": "L7",    # 31 RASP_IO06
            "P32": "L8",    # 32 RASP_IO12
            "P33": "M5",    # 33 RASP_IO13
            "P34": "-",     # 34 GND
            "P35": "M6",    # 35 RASP_IO19
            "P36": "N6",    # 36 RASP_IO16
            "P37": "P5",    # 37 RASP_IO26
            "P38": "R3",    # 38 RASP_IO20
            "P39": "-",     # 39 GND
            "P40": "R4",    # 40 RASP_IO21
        }),

        Connector("fmc", 0, {
            "C1" : "-",    # GND
            "C2" : "-",    # TXDP_FMC
            "C3" : "-",    # TXDN_FMC
            "C4" : "-",    # GND
            "C5" : "-",    # GND
            "C6" : "-",    # RXDP_FMC
            "C7" : "-",    # RXDN_FMC
            "C8" : "-",    # GND
            "C9" : "-",    # GND
            "C10" : "W9",  # FMC_LA06_P
            "C11" : "Y9",  # FMC_LA06_N
            "C12" : "-",   # GND
            "C13" : "-",   # GND
            "C14" : "W10", # FMC_LA10_P
            "C15" : "Y10", # FMC_LA10_N
            "C16" : "-",   # GND
            "C17" : "-",   # GND
            "C18" : "W11", # FMC_LA14_P
            "C19" : "Y11", # FMC_LA14_N
            "C20" : "-",   # GND
            "C21" : "-",   # GND
            "C22" : "R8",  # FMC_LA18_CC_P
            "C23" : "T8",  # FMC_LA18_CC_N
            "C24" : "-",   # GND
            "C25" : "-",   # GND
            "C26" : "Y13", # FMC_LA27_P
            "C27" : "Y14", # FMC_LA27_N
            "C28" : "-",   # GND
            "C29" : "-",   # GND
            "C30" : "-",   # FMC_SCL
            "C31" : "-",   # FMC_SDA
            "C32" : "-",   # GND
            "C33" : "-",   # GND
            "C34" : "-",   # GND
            "C35" : "-",   # 12V
            "C36" : "-",   # GND
            "C37" : "-",   # 12V
            "C38" : "-",   # GND
            "C39" : "-",   # V3P3
            "C40" : "-",   # GND
            "D1" : "-",    # PS_POR_B
            "D2" : "-",    # GND
            "D3" : "-",    # GND
            "D4" : "-",    # REFCLKP_FMC
            "D5" : "-",    # REFCLKN_FMC
            "D6" : "-",    # GND
            "D7" : "-",    # GND
            "D8" : "W13",  # FMC_LA01_CC_P
            "D9" : "V12",  # FMC_LA01_CC_N
            "D10" : "-",   # GND
            "D11" : "R5",  # FMC_LA05_P
            "D12" : "R6",  # FMC_LA05_N
            "D13" : "-",   # GND
            "D14" : "V6",  # FMC_LA09_P
            "D15" : "U7",  # FMC_LA09_N
            "D16" : "-",   # GND
            "D17" : "R9",  # FMC_LA13_P
            "D18" : "P9",  # FMC_LA13_N
            "D19" : "-",   # GND
            "D20" : "U10", # FMC_LA17_P
            "D21" : "V10", # FMC_LA17_N
            "D22" : "-",   # GND
            "D23" : "P11", # FMC_LA23_P
            "D24" : "R11", # FMC_LA23_N
            "D25" : "-",   # GND
            "D26" : "T13", # FMC_LA26_P
            "D27" : "T14", # FMC_LA26_N
            "D28" : "-",   # GND
            "D29" : "-",   # FMC_TCK
            "D30" : "-",   # FMC_TDI
            "D31" : "-",   # FMC_TDO
            "D32" : "-",   # V3P3
            "D33" : "-",   # FMC_TMS
            "D34" : "-",   # No Connect
            "D35" : "-",   # GND
            "D36" : "-",   # V3P3
            "D37" : "-",   # GND
            "D38" : "-",   # V3P3
            "D39" : "-",   # GND
            "D40" : "-",   # V3P3
            "G1" : "-",    # GND
            "G2" : "R7",   # FMC_CLK1_P
            "G3" : "T7",   # FMC_CLK1_N
            "G4" : "-",    # GND
            "G5" : "-",    # GND
            "G6" : "V11",  # FMC_LA00_CC_P
            "G7" : "U11",  # FMC_LA00_CC_N
            "G8" : "-",    # GND
            "G9" : "W6",   # FMC_LA03_P
            "G10" : "Y6",  # FMC_LA03_N
            "G11" : "-",   # GND
            "G12" : "Y7",  # FMC_LA08_P
            "G13" : "Y8",  # FMC_LA08_N
            "G14" : "-",   # GND
            "G15" : "U1",  # FMC_LA12_P
            "G16" : "T1",  # FMC_LA12_N
            "G17" : "-",   # GND
            "G18" : "P7",  # FMC_LA16_P
            "G19" : "P8",  # FMC_LA16_N
            "G20" : "-",   # GND
            "G21" : "T10", # FMC_LA20_P
            "G22" : "T11", # FMC_LA20_N
            "G23" : "-",   # GND
            "G24" : "V14", # FMC_LA22_P
            "G25" : "U14", # FMC_LA22_N
            "G26" : "-",   # GND
            "G27" : "R12", # FMC_LA25_P
            "G28" : "P12", # FMC_LA25_N
            "G29" : "-",   # GND
            "G30" : "Y15", # FMC_LA29_P
            "G31" : "Y16", # FMC_LA29_N
            "G32" : "-",   # GND
            "G33" : "Y17", # FMC_LA31_P
            "G34" : "W17", # FMC_LA31_N
            "G35" : "-",   # GND
            "G36" : "-",   # ADC_IN1P
            "G37" : "-",   # ADC_IN1N
            "G38" : "-",   # GND
            "G39" : "-",   # VADJ
            "G40" : "-",   # GND
            "H1" : "T6",   # FMC_VREF (ALSO Y18)
            "H2" : "-",    # FMC_PRSNT
            "H3" : "-",    # GND
            "H4" : "Y12",  # FMC_CLK0_P
            "H5" : "W12",  # FMC_CLK0_N
            "H6" : "-",    # GND
            "H7" : "Y2",   # FMC_LA02_P
            "H8" : "Y3",   # FMC_LA02_N
            "H9" : "-",    # GND
            "H10" : "V1",  # FMC_LA04_P
            "H11" : "W1",  # FMC_LA04_N
            "H12" : "-",   # GND
            "H13" : "W7",  # FMC_LA07_P
            "H14" : "V7",  # FMC_LA07_N
            "H15" : "-",   # GND
            "H16" : "P10", # FMC_LA11_P
            "H17" : "R10", # FMC_LA11_N
            "H18" : "-",   # GND
            "H19" : "W8",  # FMC_LA15_P
            "H20" : "V9",  # FMC_LA15_N
            "H21" : "-",   # GND
            "H22" : "U12", # FMC_LA19_P
            "H23" : "T12", # FMC_LA19_N
            "H24" : "-",   # GND
            "H25" : "P13", # FMC_LA21_P
            "H26" : "R13", # FMC_LA21_N
            "H27" : "-",   # GND
            "H28" : "W14", # FMC_LA24_P
            "H29" : "W15", # FMC_LA24_N
            "H30" : "-",   # GND
            "H31" : "U15", # FMC_LA28_P
            "H32" : "V16", # FMC_LA28_N
            "H33" : "-",   # GND
            "H34" : "V17", # FMC_LA30_P
            "H35" : "U16", # FMC_LA30_N
            "H36" : "-",   # GND
            "H37" : "-",   # VREF2_CON
            "H38" : "-",   # No Connect
            "H39" : "-",   # GND
            "H40" : "-",   # VADJ
            }), 
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
