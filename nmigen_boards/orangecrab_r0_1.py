import os
import subprocess
import shutil

from nmigen.build import *
from nmigen.vendor.lattice_ecp5 import *
from .resources import *


__all__ = ["OrangeCrabR0_1Platform"]


class OrangeCrabR0_1Platform(LatticeECP5Platform):
    device      = "LFE5U-25F"
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
            r="V17", g="T17", b="J3", invert=True,
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        *SPIFlashResources(0,
            cs="U17", clk="U16", miso="T18", mosi="U18", wp="R18", hold="N18",
            attrs=Attrs(IO_TYPE="LVCMOS33"),
        ),

        Resource("ddr3", 0,
            Subsignal("rst",     PinsN("B1", dir="o")),
            Subsignal("clk",     DiffPairs("J18", "K18", dir="o"), Attrs(IO_TYPE="SSTL135D_I")),
            Subsignal("clk_en",  Pins("D6", dir="o")),
            Subsignal("cs",      PinsN("A12", dir="o")),
            Subsignal("we",      PinsN("B12", dir="o")),
            Subsignal("ras",     PinsN("C12", dir="o")),
            Subsignal("cas",     PinsN("D13", dir="o")),
            Subsignal("a",       Pins("A4 D2 C3 C7 D3 D4 D1 B2 C1 A2 A7 C2 C4", dir="o")),
            Subsignal("ba",      Pins("B6 B7 A6", dir="o")),
            Subsignal("dqs",     DiffPairs("G18 H17", "B15 A16", dir="io"),
                      Attrs(IO_TYPE="SSTL135D_I", TERMINATION="OFF",
                      DIFFRESISTOR="100")),
            Subsignal("dq",      Pins("F17 F16 G15 F15 J16 C18 H16 F18 C17 D15 B17 C16 A15 B13 A17 A13", dir="io"),
                      Attrs(TERMINATION="75")),
            Subsignal("dm",      Pins("G16 D16", dir="o")),
            Subsignal("odt",     Pins("C13", dir="o")),
            Attrs(IO_TYPE="SSTL135_I", SLEWRATE="FAST")
        ),

        Resource("ddr3_pseudo_power", 0,
            # pseudo power pins, leave these at their default value
            Subsignal("vcc_virtual", PinsN("A3 B18 C6 C15 D17 D18 K15 K16 K17", dir="o")),
            Subsignal("gnd_virtual", Pins("L15 L16 L18", dir="o")),
            Attrs(IO_TYPE="SSTL135_II", SLEWRATE="FAST")
        ),

        *SDCardResources(0,
            dat0="J1", dat1="K3", dat2="L3", dat3="M1", clk="K1", cmd="K2", cd="L1",
            attrs=Attrs(IO_TYPE="LVCMOS33", SLEWRATE="FAST")
        ),

        Resource("usb", 0,
            Subsignal("d_p",    Pins("N1", dir="io")),
            Subsignal("d_m",    Pins("M2", dir="io")),
            Subsignal("pullup", Pins("N2", dir="o")),
            Attrs(IO_TYPE="LVCMOS33")
        ),
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
            "miso": "N15",
            "mosi": "N16",
            "sck":  "R17",
            "scl":  "C9",
            "sda":  "C10"
        }),
        Connector("mcu", 0, {
            "0":    "A10",
            "1":    "C11",
            "2":    "A11",
            "3":    "B11",
        }),
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
            subprocess.check_call([dfu_util, "-D", bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    OrangeCrabR0_1Platform().build(Blinky(), do_program=True)
