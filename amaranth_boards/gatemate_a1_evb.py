import os
import argparse
import subprocess
import shutil
import unittest

from amaranth.build import *
from amaranth.vendor import GateMatePlatform
from .resources import *


__all__ = [
    "GateMate_A1_EVB"
]

class GateMate_A1_EVB(GateMatePlatform):
    device                 = "GateMate_A1_EVB"
    package                = "CCGM1A1"
    default_clk            = "clk0"

    resources = [
        Resource("clk0", 0, Pins("IO_SB_A8", dir = "i"), Clock(10e6), Attrs(SCHMITT_TRIGGER="true")),
        Resource("clk1", 0, Pins("IO_SB_A7", dir = "i"), Clock(10e6)), # GPIO23
        Resource("clk2", 0, Pins("IO_SB_A6", dir = "i"), Clock(10e6)), # GPIO24
        Resource("clk3", 0, Pins("IO_SB_A5", dir = "i"), Clock(10e6)),

        *LEDResources(pins = "IO_SB_B6", attrs=Attrs()),
        *ButtonResources("fpga_but", pins="IO_SB_B7", attrs=Attrs()),

    
        # Note: The documentation flipped the rx and tx pins
        UARTResource(0,
            rx="IO_SA_A6", tx="IO_SA_B6", role="dce" , attrs=Attrs()
        ),

        # TODO: Check what is copi and cipo? 
        # TODO: Check where to place SPI_D0, SPI_D1, SPI_D2, SPI_D3 and FPGA_SPI_FWD?
        #SPIResource(0,
        #    cs_n="IO_WA_A8", clk="IO_WA_B8"
        #),

        PS2Resource(0,
            clk="IO_WB_A0", dat="IO_WB_B0"
        ),

        Resource("psram", 0,
            Subsignal("cs",   Pins("IO_WC_A4", dir="o")),
            Subsignal("sclk", Pins("IO_WC_B4", dir="o")),
            Subsignal("data", Pins("IO_WC_A5 IO_WC_B5 IO_WC_A6 IO_WC_B6 "
                                         "IO_WC_A7 IO_WC_B7 IO_WC_A8 IO_WC_B8", 
                                          dir="io"))
        ),
        
        VGAResource("vga", 0, 
            r="IO_WB_B3 IO_WB_A3 IO_WB_B2 IO_WB_A2",
            g="IO_WB_B5 IO_WB_A5 IO_WB_B4 IO_WB_A4",
            b="IO_WB_B7 IO_WB_A7 IO_WB_B6 IO_WB_A6",
            vs= "IO_WB_B1",
            hs="IO_WB_A1"
        ),

        Resource("jtag", 0,
            Subsignal("led", Pins("IO_SB_B5", dir="o")),
            Subsignal("tck", Pins("IO_WA_A5", dir="i")),
            Subsignal("tms", Pins("IO_WA_B4", dir="i")),
            Subsignal("tdi", Pins("IO_WA_A4", dir="i")),
            Subsignal("tdo", Pins("IO_WA_B3", dir="o"))
        ),

        Resource("spi", 0,
            Subsignal("clk", Pins("IO_WA_B8", dir="o")),
            Subsignal("csn", Pins("IO_WA_A8", dir="o")),
            Subsignal("d", Pins("IO_WA_B7 IO_WA_A7 IO_WA_B6 IO_WA_A6" , dir="io")),
            Subsignal("fwd", Pins("IO_WA_B5", dir="o")),
        ),

        Resource("serdes", 0,
            Subsignal("clk", DiffPairs("IO_SER_CLK_N", "IO_SER_CLK_P")),
            Subsignal("tx",  DiffPairs("IO_SER_TX_P",  "IO_SER_TX_N")),
            Subsignal("rx",  DiffPairs("IO_SER_RX_N",  "IO_SER_RX_P")),
        ),

        # Mostly used for RP2040
        Resource("gpio", 0,
            Subsignal("0",  Pins("IO_SA_A0", dir ="io")),
            Subsignal("1",  Pins("IO_SA_B0", dir ="io")),
            Subsignal("2",  Pins("IO_SA_A1", dir ="io")),
            Subsignal("3",  Pins("IO_SA_B1", dir ="io")),
            Subsignal("4",  Pins("IO_SA_A2", dir ="io")),
            Subsignal("5",  Pins("IO_SA_B2", dir ="io")),
            Subsignal("6",  Pins("IO_SA_A3", dir ="io")),
            Subsignal("7",  Pins("IO_SA_B3", dir ="io")),
            Subsignal("8",  Pins("IO_SA_A4", dir ="io")),
            Subsignal("9",  Pins("IO_SA_B4", dir ="io")),
            Subsignal("10", Pins("IO_SA_A5", dir ="io")),
            Subsignal("11", Pins("IO_SA_B5", dir ="io")),
            Subsignal("14", Pins("IO_SA_A7", dir ="io")),
            Subsignal("15", Pins("IO_SA_B7", dir ="io")),
            Subsignal("21", Pins("IO_SB_B8", dir ="io")), # GPIN1
            Subsignal("26", Pins("IO_SB_B4", dir ="io")),
            Subsignal("27", Pins("IO_SB_A4", dir ="io")),
            Subsignal("28", Pins("IO_SB_A8", dir ="io")),
            Subsignal("29", Pins("IO_SB_B8", dir ="io")),
        ),
    ]


    connectors = [
        Connector("bank_na1", 0, {        
            # Lower Row (BOTTOM LEFT PIN IS VDD)
            #"1" : "VDD"
            "3": "IO_NA_A0",
            "5": "IO_NA_A1",
            "7": "IO_NA_A2",
            "9": "IO_NA_A3",
            "11": "IO_NA_A4",
            "13": "IO_NA_A5",
            "15": "IO_NA_A6",
            "17": "IO_NA_A7",
            "19": "IO_NA_A8",
            # Upper Row (TOP LEFT PIN IS GND)
            #"2" : "GND"
            "4": "IO_NA_B0",
            "6": "IO_NA_B1",
            "8": "IO_NA_B2",
            "10": "IO_NA_B3",
            "12": "IO_NA_B4",
            "14": "IO_NA_B5",
            "16": "IO_NA_B6",
            "18": "IO_NA_B7",
            "20": "IO_NA_B8",
        }),
        
        Connector("bank_nb1", 0, {
            # Lower Row (BOTTOM LEFT PIN IS VDD)
            #"1" : "VDD"
            "3": "IO_NB_A0",
            "5": "IO_NB_A1",
            "7": "IO_NB_A2",
            "9": "IO_NB_A3",
            "11": "IO_NB_A4",
            "13": "IO_NB_A5",
            "15": "IO_NB_A6",
            "17": "IO_NB_A7",
            "19": "IO_NB_A8",
            # Upper Row (TOP LEFT PIN IS GND)
            #"2" : "GND"
            "4": "IO_NB_B0",
            "6": "IO_NB_B1",
            "8": "IO_NB_B2",
            "10": "IO_NB_B3",
            "12": "IO_NB_B4",
            "14": "IO_NB_B5",
            "16": "IO_NB_B6",
            "18": "IO_NB_B7",
            "20": "IO_NB_B8",
        }),
        
        Connector("bank_eb1", 0, {        
            # Lower Row (BOTTOM LEFT PIN IS VDD)
            #"1" : "VDD"
            "3": "IO_EB_A0",
            "5": "IO_EB_A1",
            "7": "IO_EB_A2",
            "9": "IO_EB_A3",
            "11": "IO_EB_A4",
            "13": "IO_EB_A5",
            "15": "IO_EB_A6",
            "17": "IO_EB_A7",
            "19": "IO_EB_A8",
            # Upper Row (TOP LEFT PIN IS GND)
            #"2" : "GND"
            "4": "IO_EB_B0",
            "6": "IO_EB_B1",
            "8": "IO_EB_B2",
            "10": "IO_EB_B3",
            "12": "IO_EB_B4",
            "14": "IO_EB_B5",
            "16": "IO_EB_B6",
            "18": "IO_EB_B7",
            "20": "IO_EB_B8",
        }),

        Connector("bank_misc1", 0, {
            # Left Row (TOP LEFT PIN IS 2.5V)
            #"1" : "2.5V"
            "fpga_spi_fwd": "IO_WA_B5", # 3
            "5":  "IO_EA_A8",
            "7":  "IO_EA_B8",
            "9":  "IO_WB_A8",
            "11": "IO_WB_B8",
            "13": "IO_SB_B3",
            "15": "IO_SB_A3",
            "17": "IO_SB_B2",
            "19": "IO_SB_A2",
            "21": "IO_SB_B1",
            "23": "IO_SB_A1",
            "25": "IO_SB_B0",
            "27": "IO_SB_A0",
            "fpga_reset_in": "RST_N",
            # Right Row (TOP RIGHT PIN IS 1.8V)
            #"2" : "1.8V"
            "4":  "IO_WC_B3",
            "6":  "IO_WC_A3",
            "8":  "IO_WC_B2",
            "10": "IO_WC_A2",
            "12": "IO_WC_B1",
            "14": "IO_WC_A1",
            "16": "IO_WC_B0",
            "18": "IO_WC_A0",
            # SerDes
            "18": "IO_SER_CLK_N",
            "20": "IO_SER_CLK_P",
            "22": "IO_SER_TX_P",
            "24": "IO_SER_TX_N",
            "26": "IO_SER_RX_N",
            "28": "IO_SER_RX_P"
        }),

        Connector("pmod", 0, {
            "1":  "IO_EA_A4",
            "7":  "IO_EA_B4",
            "2":  "IO_EA_A5",
            "8":  "IO_EA_B5",
            "3":  "IO_EA_A6",
            "9":  "IO_EA_B6",
            "4":  "IO_EA_A7",
            "10": "IO_EA_B7"
        }),

        Connector("uext", 0, {
            "txd":  "IO_EA_A0",
            "rxd":  "IO_EA_B0",
            "scl":  "IO_EA_A1",
            "sda":  "IO_EA_B1",
            "miso": "IO_EA_A2",
            "mosi": "IO_EA_B2",
            "sck":  "IO_EA_A3",
            "cs":   "IO_EA_B3"
        })
    ]

    def toolchain_program(self, products, name):
        tool = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}_00.cfg.bit".format(name)) as bitstream_filename:
            subprocess.check_call([tool, "-b", "gatemate_evb_jtag", "--cable", "dirtyJtag", bitstream_filename])


class TestCase(unittest.TestCase):
    def test_smoke(self):
        from .test.blinky import Blinky
        GateMate_A1_EVB().build(Blinky(), do_build= False)



if __name__ == "__main__":
    from .test.blinky import *

    platform = GateMate_A1_EVB()
    platform.build(Blinky(), do_program=True)


