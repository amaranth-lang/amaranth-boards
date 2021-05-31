import os
import subprocess
import shutil

from nmigen.build import *
from nmigen.vendor.lattice_ecp5 import *
from .resources import *

__all__ = ["ColorLightI5Platform"]

class ColorLightI5Platform(LatticeECP5Platform):
    package                = "BG381"
    speed                  = "6"
    default_clk            = "clk25"
    device                 = "LFE5U-25F"

    resources = [
        Resource("clk25", 0, Pins("P3", dir="i"), Clock(25e6), Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins="U16",
            attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4")),

        *SPIFlashResources(0,
            cs_n="R2", clk="U3", copi="W2", cipo="V2",
            attrs=Attrs(PULLMODE="NONE", DRIVE="4", IO_TYPE="LVCMOS33")
        ),

        RGMIIResource(0,
            txc="U19", txd="U20 T19 T20 R20", tx_ctl="P19",
            rxc="L19", rxd="P20 N19 N20 M19", rx_ctl="M20",
            mdc="N5", mdio="P5",
            attrs=Attrs(PULLMODE="NONE", DRIVE="4", SLEWRATE="FAST", IO_TYPE="LVCMOS33")
        ),

        RGMIIResource(1,
            txc="G1", txd="G2 H1 J1 J3", tx_ctl="K1",
            rxc="H2", rxd="K2 L1 N1 P1", rx_ctl="P2",
            mdc="N5", mdio="P5",
            attrs=Attrs(PULLMODE="NONE", DRIVE="4", SLEWRATE="FAST", IO_TYPE="LVCMOS33")
        ),

        SDRAMResource(0,
            clk="B9", we_n="A10", cas_n="A9", ras_n="B10",
            ba="B11 C8", a="B13 C14 A16 A17 B16 B15 A14 A13 A12 A11 B12",
            dq="B6 A5 A6 A7 C7 B8 B5 A8 D8 D7 E8 D6 C6 D5 E7 C5 C10 D9 E11 D11 C11 D12 E9 C12 E14 C15 E13 D15 E12 B17 D14 D13",
            attrs=Attrs(PULLMODE="NONE", DRIVE="4", SLEWRATE="FAST", IO_TYPE="LVCMOS33")
        ),
    ]

    connectors = [
        Connector("ddr2-sodimm-200p", 0, (
            "-   -   -   -   -   -   -   -   -   -   " #   1- 10
            "-   -   -   -   -   -   -   -   -   -   " #  11- 20
            "-   -   -   -   -   -   -   -   -   -   " #  21- 30
            "-   -   -   -   -   -   -   -   -   -   " #  31- 40
            "U16 R1  -   T1  -   U1  -   Y2  K18 W1  " #  41- 50
            "C18 V1  -   M1  -   -   T18 N2  R18 N3  " #  51- 60
            "R17 T2  P17 M3  M17 T3  T17 R3  U18 N4  " #  61- 70
            "U17 M4  P18 L4  N17 L5  N18 P16 M18 J16 " #  71- 80
            "L20 J18 L18 J17 K20 H18 K19 H17 J20 G18 " #  81- 90
            "J19 H16 H20 F18 G20 G16 G19 E18 F20 F17 " #  91-100
            "F19 F16 E20 E16 -   -   -   -   E19 E17 " # 101-110
            "D20 D18 D19 D17 C20 G5  B20 D16 B19 F5  " # 111-120
            "B18 E6  A19 E5  C17 F4  A18 E4  D3  F1  " # 121-130
            "C4  F3  B4  G3  C3  H3  E3  H4  A3  H5  " # 131-140
            "C2  J4  B1  J5  C1  K3  D2  K4  D1  K5  " # 141-150
            "E2  B3  E1  A2  F2  B2  -   -   -   -   " # 151-160
            "-   -   -   -   -   -   -   -   -   -   " # 161-170
            "-   -   -   -   -   -   -   -   -   -   " # 171-180
            "-   -   -   -   -   -   -   -   -   -   " # 181-190
            "-   -   -   -   -   -   -   -   -   -   " # 191-200
            ))
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
            subprocess.check_call([tool, '-m', bitstream_filename])

if __name__ == "__main__":
    from .test.blinky import *
    ColorLightI5Platform().build(Blinky(), do_program=True)
