import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from nmigen_boards.resources import *


__all__ = ["DE1SoCPlatform"]


# The MiSTer platform is built around the DE10-Nano; if you update one you should update the other.
class DE10NanoPlatform(IntelPlatform):
    device      = "5CSEMA5" # Cyclone V 85K LEs
    package     = "U23"     # UBGA-484
    speed       = "I7"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("V11", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("Y13", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("E11", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="W15 AA24 V16 V15 AF26 AE26 Y16 AA23",
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *ButtonResources(
            pins="AH17 AH16", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        *SwitchResources(
            pins="Y24 W24 W21 W20",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        
    ]
    connectors  = [
        # Located on the top of the board, above the chip.
        Connector("gpio", 0,
            "V12  E8   W12  D11  D8   AH13 AF7  AH14 AF4  AH3  "
            "-    -    AD5  AG14 AE23 AE6  AD23 AE24 D12  AD20 "
            "C12  AD17 AC23 AC22 Y19  AB23 AA19 W11  -    -    "
            "AA18 W14  Y18  Y17  AB25 AB26 Y11  AA26 AA13 AA11 "),
        # Located on the bottom of the board.
        Connector("gpio", 1,
            "Y15  AC24 AA15 AD26 AG28 AF28 AE25 AF27 AG26 AH27 "
            "-    -    AG25 AH26 AH24 AF25 AG23 AF23 AG24 AH22 "
            "AH21 AG21 AH23 AA20 AF22 AE22 AG20 AF21 -    -    "
            "AG19 AH19 AG18 AH18 AF18 AF20 AG15 AE20 AE19 AE17 "),
        
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            # The @2 selects the second device in the JTAG chain, because this chip
            # puts the ARM cores first.
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename + "@2"])


if __name__ == "__main__":
    from nmigen_boards.test.blinky import Blinky
    DE10NanoPlatform().build(Blinky(), do_program=True)
