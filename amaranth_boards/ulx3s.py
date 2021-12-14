import os
import argparse
import subprocess
import shutil

from amaranth.build import *
from amaranth.vendor.lattice_ecp5 import *
from .resources import *


__all__ = [
    "ULX3S_12F_Platform", "ULX3S_25F_Platform",
    "ULX3S_45F_Platform", "ULX3S_85F_Platform"
]


class _ULX3SPlatform(LatticeECP5Platform):
    package                = "BG381"
    speed                  = "6"
    default_clk            = "clk25"

    resources = [
        Resource("clk25", 0, Pins("G2", dir="i"), Clock(25e6), Attrs(IO_TYPE="LVCMOS33")),

        # Used to reload FPGA configuration.
        Resource("program", 0, PinsN("M4", dir="o"), Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")),

        *LEDResources(pins="B2 C2 C1 D2 D1 E2 E1 H3",
            attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4")),
        *ButtonResources(pins="R1 T1 R18 V1 U1 H16",
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="DOWN")
        ),
        *ButtonResources("switch", pins="E8 D8 D7 E7",
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="DOWN")
        ),

        # Semantic aliases by button label.
        Resource("button_pwr",   0, PinsN("D6", dir="i"), Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")),
        Resource("button_fire",  0, Pins("R1",  dir="i"), Attrs(IO_TYPE="LVCMOS33", PULLMODE="DOWN")),
        Resource("button_fire",  1, Pins("T1",  dir="i"), Attrs(IO_TYPE="LVCMOS33", PULLMODE="DOWN")),
        Resource("button_up",    0, Pins("R18", dir="i"), Attrs(IO_TYPE="LVCMOS33", PULLMODE="DOWN")),
        Resource("button_down",  0, Pins("V1",  dir="i"), Attrs(IO_TYPE="LVCMOS33", PULLMODE="DOWN")),
        Resource("button_left",  0, Pins("U1",  dir="i"), Attrs(IO_TYPE="LVCMOS33", PULLMODE="DOWN")),
        Resource("button_right", 0, Pins("H16", dir="i"), Attrs(IO_TYPE="LVCMOS33", PULLMODE="DOWN")),

        # FTDI connection.
        UARTResource(0, 
            rx="M1", tx="L4", rts="M3", dtr="N1", role="dce",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),
        Resource("uart_tx_enable", 0, Pins("L3", dir="o"), Attrs(IO_TYPE="LVCMOS33")),

        *SDCardResources(0,
            clk="J1", cmd="J3", dat0="K2", dat1="K1", dat2="H2", dat3="H1",
            attrs=Attrs(IO_TYPE="LVCMOS33", SLEW="FAST")
        ),

        # SPI Flash clock is accessed via USR_MCLK instance.
        Resource("spi_flash", 0,
            Subsignal("cs",   PinsN("R2", dir="o")),
            Subsignal("copi", Pins("W2", dir="o")),
            Subsignal("cipo", Pins("V2", dir="i")),
            Subsignal("hold", PinsN("W1", dir="o")),
            Subsignal("wp",   PinsN("Y2", dir="o")),
            Attrs(PULLMODE="NONE", DRIVE="4", IO_TYPE="LVCMOS33")
        ),

        SDRAMResource(0,
            clk="F19", cke="F20", cs_n="P20", we_n="T20", cas_n="T19", ras_n="R20", dqm="U19 E20",
            ba="P19 N20", a="M20 M19 L20 L19 K20 K19 K18 J20 J19 H20 N19 G20 G19",
            dq="J16 L18 M18 N18 P18 T18 T17 U20 E19 D20 D19 C20 E18 F18 J18 J17",
            attrs=Attrs(PULLMODE="NONE", DRIVE="4", SLEWRATE="FAST", IO_TYPE="LVCMOS33")
        ),

        # SPI bus for ADC.
        SPIResource("adc", 0, cs_n="R17", copi="R16", cipo="U16", clk="P17",
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")),

        # TRRS audio jack
        Resource("audio", 0,
            Subsignal("l", Pins("E4 D3 C3 B3", dir="o")),
            Subsignal("r", Pins("A3 B5 D5 C5", dir="o")),
            Subsignal("ring2", Pins("H5 F2 F5 E5", dir="o")), # extra ring out for video adapters
        ),

        # ESP-32 connections
        Resource("esp32", 0,
            Subsignal("en",     Pins("F1", dir="o"), Attrs(PULLMODE="UP")),
            Subsignal("tx",     Pins("K3", dir="o"), Attrs(PULLMODE="UP")),
            Subsignal("rx",     Pins("K4", dir="i"), Attrs(PULLMODE="UP")),
            Subsignal("gpio0",  Pins("L2"),          Attrs(PULLMODE="UP")),
            Subsignal("gpio5",  Pins("N4")),
            Subsignal("gpio16", Pins("L1"),          Attrs(PULLMODE="UP")),
            Subsignal("gpio17", Pins("N3"),          Attrs(PULLMODE="UP")),
            Attrs(IO_TYPE="LVCMOS33", DRIVE="4")
        ),

        # PCB antenna, tuned to 433MHz
        Resource("ant", 0, Pins("G1", dir="o"), Attrs(IO_TYPE="LVCMOS33")),

        # Differential versions of our connector I/O.
        Resource("diff_gpio", 0, DiffPairs("B11", "C11"), Attrs(IO_TYPE="LVCMOS33")),
        Resource("diff_gpio", 1, DiffPairs("A10", "A11"), Attrs(IO_TYPE="LVCMOS33")),
        Resource("diff_gpio", 2, DiffPairs("A9", "B10"), Attrs(IO_TYPE="LVCMOS33")),
        Resource("diff_gpio", 3, DiffPairs("B9", "C10"),  Attrs(IO_TYPE="LVCMOS33")),
        
        # HDMI (only TX, due to the top bank of ECP5 only supporting diff. outputs)
        Resource("hdmi", 0,
            Subsignal("cec", Pins("A18", dir="io"),
                Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP")),
            Subsignal("clk", DiffPairs("A17", "B18", dir="o"),
                Attrs(IO_TYPE="LVCMOS33D", DRIVE="4")),
            Subsignal("d",   DiffPairs("A16 A14 A12", "B16 C14 A13", dir="o"),
                Attrs(IO_TYPE="LVCMOS33D", DRIVE="4")),
            Subsignal("eth", DiffPairs("A19", "B20", dir="o"),
                Attrs(IO_TYPE="LVCMOS33D", DRIVE="4")),
            Subsignal("scl", Pins("E12", dir="io"),
                Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP")),
            Subsignal("sda", Pins("B19", dir="io"),
                Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="UP"))),

        DirectUSBResource(0,
            d_p="D15", d_n="E15", pullup="B12",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        )
    ]

    connectors = [
        Connector("gpio", 0, {
            "0+": "B11",  "0-":  "C11", "1+":  "A10", "1-":  "A11",
            "2+": "A9",   "2-":  "B10", "3+":  "B9",  "3-":  "C10",
            "4+": "A7",   "4-":  "A8",  "5+":  "C8",  "5-":  "B8",
            "6+": "C6",   "6-":  "C7",  "7+":  "A6",  "7-":  "B6",
            "8+": "A4",   "8-":  "A5",  "9+":  "A2",  "9-":  "B1",
            "10+": "C4",  "10-": "B4",  "11+": "F4",  "11-": "E3",
            "12+": "G3",  "12-": "F3",  "13+": "H4",  "13-": "G5",
            "14+": "U18", "14-": "U17", "15+": "N17", "15-": "P16",
            "16+": "N16", "16-": "M17", "17+": "L16", "17-": "L17",
            "18+": "H18", "18-": "H17", "19+": "F17", "19-": "G18",
            "20+": "D18", "20-": "E17", "21+": "C18", "21-": "D17",
            "22+": "B15", "22-": "C15", "23+": "B17", "23-": "C17",
            "24+": "C16", "24-": "D16", "25+": "D14", "25-": "E14",
            "26+": "B13", "26-": "C13", "27+": "D13", "27-": "E13",
        })
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
            subprocess.check_call([tool, "-b", "ulx3s", '-m', bitstream_filename])


class ULX3S_12F_Platform(_ULX3SPlatform):
    device                 = "LFE5U-12F"


class ULX3S_25F_Platform(_ULX3SPlatform):
    device                 = "LFE5U-25F"


class ULX3S_45F_Platform(_ULX3SPlatform):
    device                 = "LFE5U-45F"


class ULX3S_85F_Platform(_ULX3SPlatform):
    device                 = "LFE5U-85F"


if __name__ == "__main__":
    from .test.blinky import *
    
    variants = {
        '12F': ULX3S_12F_Platform,
        '25F': ULX3S_25F_Platform,
        '45F': ULX3S_45F_Platform,
        '85F': ULX3S_85F_Platform
    }
    
    # Figure out which FPGA variant we want to target...
    parser = argparse.ArgumentParser()
    parser.add_argument('variant', choices=variants.keys())
    args = parser.parse_args()

    # ... and run Blinky on it.
    platform = variants[args.variant]
    platform().build(Blinky(), do_program=True)
