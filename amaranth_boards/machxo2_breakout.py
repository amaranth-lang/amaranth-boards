import os
import subprocess

from amaranth.build import *
from amaranth.vendor import LatticeMachXO2Platform
from .resources import *


__all__ = ["MachXO2_7000HE_BreakoutPlatform", "MachXO2_1200ZE_BreakoutPlatform"]


# https://www.latticesemi.com/Products/DevelopmentBoardsAndKits/MachXO2BreakoutBoard
class MachXO2_7000HE_BreakoutPlatform(LatticeMachXO2Platform):
    device         = "LCMXO2-7000HE"
    package        = "TG144"
    default_clk    = "OSCH"
    osch_frequency = 2.08 # documented default; see amaranth.vendor.lattice_machxo_2_3l for more options
    speed          = "4"
    resources      = [
        *LEDResources(pins="97 98 99 100 104 105 106 107", invert=True),
    ]

    # Connectable to the FTDI UART but disconnected by default. Populate R14-R21 to connect.
    # Use `p.add_resource(p.serial)` to add the resource.
    serial = UARTResource(0, rx="73", tx="74", rts="75", cts="76", dtr="81", dsr="77", dcd="78", role="dte")

    connectors     = [
        Connector("j", 2, # J2
                  "- - "
                  "109 - " # 110: INITn
                  "111 112 "
                  "- - "
                  "113 114 "
                  "115 117 "
                  "119 120 "
                  "- - "
                  "121 122 "
                  "125 126 "
                  "127 128 "
                  "- - "
                  "- - " # 130: TMS, 131: TCK
                  "132 133 "
                  "- - " # 136: TDI, 137: TDO
                  "- - "
                  "138 139 "
                  "140 141 "
                  "142 143 "
                  "- - "),
        Connector("j", 3, # J3
                  "- - "
                  "- - "
                  "74 73 "
                  "76 75 "
                  "- - "
                  "78 77 "
                  "82 81 "
                  "- - "
                  "84 83 "
                  "86 85 "
                  "- - "
                  "92 91 "
                  "94 93 "
                  "- - "
                  "96 95 "
                  "98 97 "
                  "- - "
                  "100 99 "
                  "105 104 "
                  "107 106 "),
        Connector("j", 4, # J4
                  "- - "
                  "- - "
                  "1 2 "
                  "3 4 "
                  "5 6 "
                  "9 10 "
                  "- - "
                  "11 12 "
                  "13 14 "
                  "- - "
                  "19 20 "
                  "21 22 "
                  "- - "
                  "23 24 "
                  "25 26 "
                  "- - "
                  "27 28 "
                  "- - "
                  "32 33 "
                  "34 35 "),
        Connector("j", 5, # J5
                  "- - "
                  "71 69 "
                  "70 68 "
                  "67 62 "
                  "65 61 "
                  "- - "
                  "60 58 "
                  "59 57 "
                  "- - "
                  "56 54 "
                  "55 52 "
                  "- - "
                  "50 48 "
                  "49 47 "
                  "- - "
                  "45 43 "
                  "44 42 "
                  "- - "
                  "41 39 "
                  "40 38 "),
    ]

    def toolchain_program(self, products, name):
        tool = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([tool, "-b", "machXO2EVN", "-m", bitstream_filename])


# This is an older version of the board, that has an FPGA with less logic
# resources. It is otherwise the same.
class MachXO2_1200ZE_BreakoutPlatform(MachXO2_7000HE_BreakoutPlatform):
    device         = "LCMXO2-1200ZE"
    speed          = "1"


if __name__ == "__main__":
    from .test.blinky import *
    MachXO2_7000HE_BreakoutPlatform().build(Blinky(), do_program=True)
