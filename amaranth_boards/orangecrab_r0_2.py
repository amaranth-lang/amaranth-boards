import os
import subprocess
import shutil

from amaranth.build import *
from amaranth.vendor.lattice_ecp5 import *
from .resources import *

# NOTE: Keep OrangeCrabR0_2Platform for backwards compatibility
# Originally, there was only OrangeCrabR0_2Platform, but the 85F variant
# needs a different device.
__all__ = ["OrangeCrabR0_2Platform", "OrangeCrabR0_2_25FPlatform", "OrangeCrabR0_2_85FPlatform"]

class _OrangeCrabR0_2Platform(LatticeECP5Platform):
    package     = "MG285"
    speed       = "8"
    default_clk = "clk"
    resources   = [
        Resource("clk", 0, Pins("A9", dir="i"),
                 Clock(48e6), Attrs(IO_TYPE="LVCMOS33")),

        # Used to reload FPGA configuration.
        # Can enter USB bootloader by assigning button 0 to program.
        Resource("program", 0, PinsN("V17", dir="o"), Attrs(IO_TYPE="LVCMOS33")),

        RGBLEDResource(0, 
            r="K4", g="M3", b="J3", invert=True,
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        *ButtonResources(
            pins={0: "J17" }, invert=True,
            attrs=Attrs(IO_TYPE="SSTL135_I")),

        *SPIFlashResources(0,
            cs_n="U17", clk="U16", cipo="T18", copi="U18", wp_n="R18", hold_n="N18",
            attrs=Attrs(IO_TYPE="LVCMOS33"),
        ),

        Resource("ddr3", 0,
            Subsignal("rst",     PinsN("L18", dir="o")),
            Subsignal("clk",     DiffPairs("J18", "K18", dir="o"), Attrs(IO_TYPE="SSTL135D_I")),
            Subsignal("clk_en",  Pins("D18", dir="o")),
            Subsignal("cs",      PinsN("A12", dir="o")),
            Subsignal("we",      PinsN("B12", dir="o")),
            Subsignal("ras",     PinsN("C12", dir="o")),
            Subsignal("cas",     PinsN("D13", dir="o")),
            Subsignal("a",       Pins("C4 D2 D3 A3 A4 D4 C3 B2 B1 D1 A7 C2 B6 C1 A2 C7", dir="o")),
            Subsignal("ba",      Pins("P5 N3 M3", dir="o")),
            Subsignal("dqs",     DiffPairs("G18 H17", "B15 A16", dir="io"),
                      Attrs(IO_TYPE="SSTL135D_I", TERMINATION="OFF",
                      DIFFRESISTOR="100")),
            Subsignal("dq",      Pins("C17 D15 B17 C16 A15 B13 A17 A13 F17 F16 G15 F15 J16 C18 H16 F18",
                                      dir="io"), Attrs(TERMINATION="75")),
            Subsignal("dm",      Pins("G16 D16", dir="o")),
            Subsignal("odt",     Pins("C13", dir="o")),
            Attrs(IO_TYPE="SSTL135_I", SLEWRATE="FAST")
        ),

        Resource("ddr3_pseudo_power", 0,
            # pseudo power pins, leave these at their default value
            Subsignal("vcc_virtual", PinsN("K16 D17 K15 K17 B18 C6", dir="o")),
            Subsignal("gnd_virtual", Pins("L15 L16", dir="o")),
            Attrs(IO_TYPE="SSTL135_II", SLEWRATE="FAST")
        ),

        Resource("adc", 0,
            Subsignal("ctrl",     Pins("G1 F1", dir="o")),
            Subsignal("mux",      Pins("F4 F3 F2 H1", dir="o")),
            Subsignal("sense",    DiffPairs("H3", "G3", dir="i"), Attrs(IO_TYPE="LVCMOS33D")),
            Attrs(IO_TYPE="LVCMOS33")
        ),

        *SDCardResources(0,
            dat0="J1", dat1="K3", dat2="L3", dat3="M1", clk="K1", cmd="K2", cd="L1",
            attrs=Attrs(IO_TYPE="LVCMOS33", SLEWRATE="FAST")
        ),

        DirectUSBResource(0, d_p="N1", d_n="M2", pullup="N2", attrs=Attrs(IO_TYPE="LVCMOS33"))
    ]
    connectors = [
        Connector("io", 0, {
            "0":    "N17",
            "1":    "M18",
            "5":    "B10",
            "6":    "B9",
            "9":    "C8",
            "10":   "B8",
            "11":   "A8",
            "12":   "H2",
            "13":   "J2",
            "a0":   "L4",
            "a1":   "N3",
            "a2":   "N4",
            "a3":   "H4",
            "a4":   "G4",
            "cipo": "N15",
            "copi": "N16",
            "sck":  "R17",
            "scl":  "C9",
            "sda":  "C10"
        })
    ]

    @property
    def required_tools(self):
        return super().required_tools + [
            "dfu-suffix"
        ]

    @property
    def command_templates(self):
        return super().command_templates + [
            r"""
            {{invoke_tool("dfu-suffix")}}
                -v 1209 -p 5af0 -a {{name}}.bit
            """
        ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = dict(ecppack_opts="--compress --freq 38.8")
        overrides.update(kwargs)
        return super().toolchain_prepare(fragment, name, **overrides)

    def toolchain_program(self, products, name):
        dfu_util = os.environ.get("DFU_UTIL", "dfu-util")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([dfu_util, "-a 0", "-D", bitstream_filename])

class OrangeCrabR0_2Platform(_OrangeCrabR0_2Platform):
    device      = "LFE5U-25F"

class OrangeCrabR0_2_25FPlatform(_OrangeCrabR0_2Platform):
    device      = "LFE5U-25F"

class OrangeCrabR0_2_85FPlatform(_OrangeCrabR0_2Platform):
    device      = "LFE5U-85F"

if __name__ == "__main__":
    from .test.blinky import *
    OrangeCrabR0_2Platform().build(Blinky(), do_program=True)
