import os
import subprocess

from amaranth.build import *
from amaranth.vendor import GowinPlatform

from .resources import *

__all__ = ["TangPrimer25kPlatform", "TangPrimer25kDockPlatform"]

# Specification: https://api.dl.sipeed.com/file/download?verify_code=6xhl&file_url=TANG/Primer_25K/01_Specification/Tang_Primer_25K_Specification_V1.0_en.pdf
# Board schematic: https://dl.sipeed.com/fileList/TANG/Primer_25K/02_Schematic/Tang_Primer_25K_Dock_60033_Schematic.pdf


class TangPrimer25kPlatform(GowinPlatform):
    part = "GW5A-LV25MG121NC1/I0"
    family = "GW5A-25A"
    default_clk = "clk27"
    resources = [
        Resource(
            "clk27", 0, Pins("E2", dir="i"), Clock(27e6), Attrs(IO_TYPE="LVCMOS33")
        ),
        UARTResource(
            0, rx="B3", tx="C3", attrs=Attrs(PULLMODE="UP", IO_TYPE="LVCMOS33")
        ),
        *SPIFlashResources(
            0,
            cs_n="E6",
            clk="E7",
            cipo="D6",
            copi="E5",
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP"),
        ),
    ]
    connectors = [
        Connector(
            "J1",
            0,
            # GND GND
            " -   -   L9  H5  K9  J5  J8  L5  K8  K5"  # ( 1 - 10)
            #                 GND
            " F7  H8  F6  H7  -   G7  E8  G8  B3  F5"  # (11 - 20)
            #             VCCIO0/1    GND GND VCCIO6/7
            " C3  G5  E3  -   D7  -   -   -   -   L6"  # (21 - 30)
            " -   K6  J11 K7  J10 J7  H11 L7  H10 L8"  # (31 - 40)
            #                 GND                 GND
            " G11 L10 G10 K10 -   K11 D11 L11 D10 -"  #  (41 - 50)
            #                                 GND GND
            " C11 E11 C10 E10 B11 A11 B10 A10 -   -",  #    (51 - 59)
        ),
        Connector(
            "J2",
            0,
            # GND VCCIO2/3
            " -   -   B2  -   C2  L2  F2  L1  F1  K1"  # ( 1 - 10)
            #                                 GND
            " A1  K2  D8  J4  E1  K4  D1  G2  -   G1"  # (11 - 20)
            #                                 GND
            " C1  L4  B1  L3  A2  J1  A3  J2  -   G4"  # (21 - 30)
            #                 GND                 GND
            " D3P H4  D3N H1  -   H2  D2P -   D2N -"  #  (31 - 40)
            #                     GND
            " -   -   CKP -   CKN -   -   -   D1P -"  #  (41 - 50)
            #     GND                         GND 5V
            " D1N -   -   -   D0P -   -   D0N -   -",  # (51 - 59)
        ),
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "nextpnr_opts": "--vopt sspi_as_gpio",
            "gowin_pack_opts": "--sspi_as_gpio --mspi_as_gpio --ready_as_gpio --done_as_gpio --cpu_as_gpio",
        }

        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        with products.extract("{}.fs".format(name)) as bitstream_filename:
            subprocess.check_call(
                ["openFPGALoader", "-b", "tangprimer25k", "-m", bitstream_filename]
            )


class TangPrimer25kDockPlatform(TangPrimer25kPlatform):
    resources = TangPrimer25kPlatform.resources + [
        *ButtonResources(
            pins={0: "37", 1: "39"},
            invert=True,
            conn=("J1", 0),
            attrs=Attrs(
                IO_TYPE="LVCMOS33", PULLMODE="DOWN", DRIVE="OFF", BANK_VCCIO="3.3"
            ),
        ),
        *LEDResources(
            pins={0: "17", 1: "25"},
            invert=False,
            conn=("J1", 0),
            attrs=Attrs(IO_TYPE="LVCMOS33"),
        ),
        Resource(
            "usb",
            0,
            Subsignal("d_p", Pins("30", conn=("J1", 1), dir="io")),
            Subsignal("d_n", Pins("32", conn=("J1", 1), dir="io")),
            Subsignal("pullup", Pins("17", conn=("J1", 0), dir="o")),
            Attrs(IO_TYPE="LVCMOS33", DRIVE="4", PULLMODE="NONE"),
        ),
    ]
    connectors = TangPrimer25kPlatform.connectors + [
        #                     3V3 3V3 GND GND
        Connector("pmod", 0, "-   -   -   -   C11 C10 B11 B10 D11 D10 G11 G10"),
        Connector("pmod", 1, "-   -   -   -   L5  K5  K11 L11 E11 E10 A11 A10 "),
        Connector("pmod", 2, "-   -   -   -   H5  J5  H8  H7  G7  G8  F5  G5"),
        Connector(
            "gpio",
            0,
            " K2  K1  L1  L2  K4  J4  G1  G2  L3  L4"  #   ( 1 - 10)
            # 5V  GND -   -   -   -   -   -   -   -        (11 - 20)
            " -   -   C2  B2  F1  F2  A1  E1  D1  E3"
            " J2  J1  H4  G4  H2  H1  J7  K7  L8  L7"  #   (21 - 30)
            " K10 L10 K9  L9  K8  J8  F6  F7  J10 J11",  # (31 - 40)
        ),
    ]


if __name__ == "__main__":
    from .test.blinky import *

    TangPrimer25kDockPlatform().build(Blinky(), do_program=True)
