import os
import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["ICEBreakerBitsyPlatform"]


class ICEBreakerBitsyPlatform(LatticeICE40Platform):
    device      = "iCE40UP5K"
    package     = "SG48"
    default_clk = "clk12"
    resources   = [
        Resource("clk12", 0, Pins("35", dir="i"),
                 Clock(12e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        DirectUSBResource(0, d_p="42", d_n="38", pullup="37",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        *SPIFlashResources(0,
            cs_n="16", clk="15", copi="14", cipo="17", wp_n="18", hold_n="19",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),

        RGBLEDResource(0, r="39", g="40", b="41", invert=True,
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        *LEDResources(pins="25 6", invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_r", 0, PinsN("25", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_g", 0, PinsN("6", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),

        *ButtonResources(pins="2", invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
    ]
    connectors = [
        Connector("edge", 0,  # Pins bottom P0 - P12,
            {"0":"47",  "1":"44",  "2":"48",  "3":"45",  "4": "4",  "5": "3",
             "6": "9",  "7":"10",  "8":"11",  "9":"12", "10":"21", "11":"13",
            "12":"20", "13":"25", "14":"23", "15":"27", "16":"26", "17":"28",
            "18":"31", "19":"32", "20":"34", "21":"36", "22":"43", "23":"46"}
        ),
        Connector("pmod", 1, " 0  2  4  6 - -  1  3  5  7 - -", conn=("edge", "0")), # PMOD 1
        Connector("pmod", 2, "22 19 16 17 - - 21 18 15 20 - -", conn=("edge", "0")), # PMOD 2
        Connector("pmod", 3, "14  9 11  8 - - 13 10 12 23 - -", conn=("edge", "0"))  # PMOD 3
    ]

    def toolchain_program(self, products, name, run_vid=None, run_pid=None, dfu_vid="1d50", dfu_pid="6146", reset=True):
        dfu_util = os.environ.get("DFU_UTIL", "dfu-util")

        # Construct the device runtime and DFU vid pid string
        dev_str = ""
        if run_vid or run_pid:
            dev_str = "{}:{}".format(run_vid or "", run_pid or "")
        dev_str += ",{}:{}".format(dfu_vid or "", dfu_pid or "")

        # Construct the argument list for dfu-util
        args = [dfu_util, "-d", dev_str, "-a", "0"]
        if reset: args.append("-R")
        args.append("-D")

        # Run dfu-util
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            args.append(bitstream_filename)
            subprocess.check_call(args)


if __name__ == "__main__":
    from .test.blinky import *
    ICEBreakerBitsyPlatform().build(Blinky(), do_program=True)
