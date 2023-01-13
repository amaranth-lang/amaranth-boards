# iCESugar-pro Platform
# See: https://github.com/wuxx/icesugar-pro

import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_ecp5 import *
from amaranth_boards.resources import *

__all__ = ["ICESugarProPlatform"]


class ICESugarProPlatform(LatticeECP5Platform):
    name = "IceSugar Pro v1.3"
    device  = "LFE5U-25F"
    package = "BG256"
    speed   = "6"
    default_clk = "clk25"

    resources = [
        Resource("clk25", 0, Pins("P6", dir="i"), 
                 Clock(25e6), Attrs(IO_TYPE="LVCMOS33")),
        
        RGBLEDResource(0, r="B11", g="A11", b="A12", attrs=Attrs(IO_TYPE="LVCMOS33")),

        UARTResource(0, rx="A9", tx="N4",
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLUP=1)
        ),
    ]

    # https://github.com/wuxx/icesugar-pro/tree/master/schematic
    connectors = [
        Connector("io", 0, {
            "41:": "A8",
            "42:": "P11",
            "44:": "P12",
            "46:": "N12",
            "48:": "P13",
            "49:": "B8",
            "50:": "N13",
            "51:": "A7",
            "52:": "P14",
            "54:": "M12",
            "57:": "B7",
            "58:": "M13",
            "59:": "A6",
            "60:": "L14",
            "61:": "B6",
            "62:": "L13",
            "63:": "A5",
            "64:": "K14",
            "65:": "B5",
            "66:": "K13",
            "67:": "A4",
            "68:": "J14",
            "69:": "B4",
            "70:": "J13",
            "71:": "A3",
            "72:": "H14",
            "73:": "B3",
            "74:": "H13",
            "75:": "A2",
            "76:": "G14",
            "77:": "B1",
            "78:": "G13",
            "79:": "B2",
            "80:": "F14",
            "81:": "C1",
            "82:": "F13",
            "83:": "C2",
            "84:": "E14",
            "85:": "D1",
            "86:": "E13",
            "87:": "D3",
            "88:": "E12",
            "89:": "E1",
            "90:": "C13",
            "91:": "E2",
            "92:": "D13",
            "93:": "F1",
            "94:": "C12",
            "95:": "F2",
            "96:": "D12",
            "97:": "G1",
            "98:": "C11",
            "99:": "G2",
            "100:": "D11",
            "101:": "H2",
            "102:": "C10",
            "103:": "J1",
            "104:": "D10",
            "109:": "J2",
            "110:": "C9",
            "111:": "K1",
            "112:": "D9",
            "113:": "K2",
            "114:": "C8",
            "115:": "L1",
            "116:": "D8",
            "117:": "L2",
            "118:": "C7",
            "119:": "M1",
            "120:": "D7",
            "121:": "M2",
            "122:": "C6",
            "123:": "N1",
            "124:": "D6",
            "125:": "N3",
            "126:": "C5",
            "127:": "P1",
            "128:": "D5",
            "129:": "P2",
            "130:": "C4",
            "131:": "R1",
            "132:": "D4",
            "133:": "R2",
            "134:": "C3",
            "135:": "T2",
            "136:": "E4",
            "137:": "R3",
            "138:": "E3",
            "139:": "T3",
            "140:": "F4",
            "141:": "R4",
            "142:": "F3",
            "143:": "T4",
            "144:": "G4",
            "145:": "R5",
            "146:": "G3",
            "147:": "R6",
            "148:": "H3",
            "149:": "T6",
            "150:": "J4",
            "151:": "P7",
            "152:": "J3",
            "153:": "R7",
            "154:": "K4",
            "155:": "R8",
            "156:": "K3",
        })
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call(["icesprog", bitstream_filename])


if __name__ == "__main__":
    from amaranth_boards.test.blinky import *
    ICESugarProPlatform().build(Blinky(), do_program=True)
