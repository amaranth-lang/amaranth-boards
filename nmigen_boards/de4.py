import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["DE4Platform"]

#This is for the larger (500k LEs) chip. The DE4 also comes in a configuration with the EP4SGX230C2
class DE4Platform(IntelPlatform):
    device      = "EP4SGX530" # Stratix IV 530k LEs
    package     = "KH40"     # FBGA-1517
    speed       = "C2"
    default_clk = "clk50"
    default_rst = "cpu_reset_n"
    resources   = [
        Resource("clk50", 0, Pins("AC35", dir="i"),
                 Clock(50e6), Attrs(io_standard="2.5-V")),
        Resource("clk50", 1, Pins("AV22", dir="i"),
                 Clock(50e6), Attrs(io_standard="1.8-V")),
        Resource("clk50", 2, Pins("AV19", dir="i"),
                 Clock(50e6), Attrs(io_standard="1.8-V")),
        Resource("clk50", 3, Pins("AC6", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.0-V")),
        Resource("clk50", 4, Pins("AB6", dir="i"),
                 Clock(50e6), Attrs(io_standard="2.5-V")),
        Resource("clk50", 5, Pins("A19", dir="i"),
                 Clock(50e6), Attrs(io_standard="1.8-V")),
        Resource("clk100", 0, Pins("A21", dir="i"),
                 Clock(100e6), Attrs(io_standard="1.8-V")), #100MHz assumes SW7 is set to 00

        Resource("cpu_reset_n", 0, Pins("AH8", dir="i"),
                invert=True, Attrs(io_standard="2.5-V"))
   

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


        Display7SegResource(0, 
            a ="L34", b="M34", c="M33", d="H31", e="J33",
            f="L35", g="K32", dp="AL34", invert=True,
            attrs=Attrs(io_standard="2.5-V")),

        Display7SegResource(1, 
            a = "E31", b="F31", c="G31", d="C34", e="C33",
            f="D33", g="D34", dp="AL35", invert=True,
            attrs=Attrs(io_standard="2.5-V")),


       
    ]
    connectors  = [
        # Located on the right of the board
        Connector("gpio", 0,
            "AF6  AU9  AE5  AR8  AN9  AP9  AV5  AW6  AV7  AW7  "
            " -    -   AT5  AT8  AP5  AP7  AN5  AN10 AM5  AM10 "
            "AL10 AM8  AL8  AK8  AJ11 AK7  AJ5  AH12  -    -   "
            "AG10 AG13 AG9  AF11 AT9  AF10 AD10 AD9  AD12 AD13 ", Attrs(io_standard="3.0V")),
    
        Connector("gpio", 1,
            "AW5  AW8  AW4  AV10 AV8  AW10 AU10 AU8  AP8  AT10 "
            " -    -   AU6  AT6  AU7  AR5  AP6  AT7  AN7  AN6  "
            "AL6  AM6  AL5  AL9  AK9  AJ6  AJ10 AH11  -    -   "
            "AH8  AH9  AG12 AH10 AF13 AE13 AE10 AP10 AE12 AE11 ", Attrs(io_standard="3.0V")),

    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import Blinky
    DE4Platform().build(Blinky(), do_program=True)
