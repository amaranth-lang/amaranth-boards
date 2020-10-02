import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["DE4Platform"]

#This is for the larger (500k LEs) chip. The DE4 also comes in a configuration with the EP4SGX230C2
class DE4Platform(IntelPlatform):
    device      = "EP4SGX530" # Stratix IV 530k LEs
    package     = "U23"     # UBGA-484
    speed       = "C2"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("V11", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("Y13", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("E11", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        #from 0 to n
        *LEDResources(
            pins="V28 W28 R29 P29 N29 M29 M30 N30", invert=True,
            attrs=Attrs(io_standard="2.5-V")),
        *ButtonResources(
            pins="AH5 AG5 AG7 AH8", invert=True,
            attrs=Attrs(io_standard="3.0-V")),
        *SwitchResources( 
            pins="J7 K7 AK6 L7",
            attrs=Attrs(io_standard="2.5-V")),


       
    ]
    connectors  = [
        # Located on the right of the board
        Connector("gpio", 0,
            "V12  E8   W12  D11  D8   AH13 AF7  AH14 AF4  AH3  "
            "-    -    AD5  AG14 AE23 AE6  AD23 AE24 D12  AD20 "
            "C12  AD17 AC23 AC22 Y19  AB23 AA19 W11  -    -    "
            "AA18 W14  Y18  Y17  AB25 AB26 Y11  AA26 AA13 AA11 "),
    
        Connector("gpio", 1,
            "Y15  AC24 AA15 AD26 AG28 AF28 AE25 AF27 AG26 AH27 "
            "-    -    AG25 AH26 AH24 AF25 AG23 AF23 AG24 AH22 "
            "AH21 AG21 AH23 AA20 AF22 AE22 AG20 AF21 -    -    "
            "AG19 AH19 AG18 AH18 AF18 AF20 AG15 AE20 AE19 AE17 "),

    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import Blinky
    DE4Platform().build(Blinky(), do_program=True)
