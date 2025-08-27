import os
import subprocess

from amaranth.build import *
from amaranth.vendor import GowinPlatform

from .resources import *


__all__ = [
    "TangPrimer20kPlatform",
    "TangPrimer20kLitePlatform",
    "TangPrimer20kDockPlatform",
]


class TangPrimer20kPlatform(GowinPlatform):
    part          = "GW2A-LV18PG256C8/I7"
    family        = "GW2A-18C"
    default_clk   = "clk27"
    resources     = [
        Resource("clk27", 0, Pins("H11", dir="i"),
                 Clock(27e6), Attrs(IO_TYPE="LVCMOS33")),

        UARTResource(0, rx="T13", tx="M11",
                     attrs=Attrs(PULL_MODE="UP", IO_TYPE="LVCMOS33")),

        *SPIFlashResources(0, cs_n="M9", clk="L10", cipo="P10", copi="R10",
                           attrs=Attrs(IO_TYPE="LVCMOS33")),

        *SDCardResources(0, clk="N10", cmd="R14", cd="D15",
                         dat0="M8", dat1="M7", dat2="M10", dat3="N11",
                         attrs=Attrs(IO_TYPE="LVCMOS33")),

        DDR3Resource(0, rst_n="B9", clk_p="J1", clk_n="J3", clk_en="J2",
                     cs_n="P5", we_n="L2", ras_n="R4", cas_n="R6",
                     a="F7 A4 D6 F8 C4 E6 B1 D8 A5 F9 K3 B7 A3 C8",
                     ba="H4 D3 H5", dqs_p="G2 J5", dqs_n="G3 K6",
                     dq="G5 F5 F4 F3 E2 C1 E1 B3 M3 K4 N2 L1 P4 H3 R1 M2",
                     dm="G1 K5", odt="R3",
                     attrs=Attrs(IO_TYPE="SSTL15"),
                     diff_attrs=Attrs(IO_TYPE="SSTL15D")),

        # ZIF connector on core board
        Resource("spi_lcd", 0,
                 Subsignal("bl",   PinsN("P12", dir="o")),
                 Subsignal("rst",  PinsN("G13", dir="o")),
                 Subsignal("rs",   Pins("J13", dir="o")),
                 Subsignal("cs",   PinsN("C16", dir="o")),
                 Subsignal("clk",  Pins("F12", dir="o")),
                 Subsignal("copi", Pins("L15", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33")),
    ]

    connectors = [
        # GND, 5V, 3V3 are power pins
        # V01 and V7 are IO bank voltages, tied to 3V3 by R5 and R9 (resp.)
        Connector("sodimm", 0,
                  #     GND GND 5V  5V  5V  5V  GND GND NC  (  1- 10)
                  " T13  -   -   -   -   -   -   -   -   - "
                  #     NC  GND GND     NC  NC  NC  GND GND ( 11- 20)
                  " M11  -   -   -  T10  -   -   -   -   - "
                  # NC  3V3 NC  3V3 GND GND                 ( 21- 30)
                  "  -   -   -   -   -   -  T6  R16 P6  P16"
                  # GND GND                 GND GND         ( 31- 40)
                  "  -   -  T7  P16 R8  N15  -   -  T8  N16"
                  #         GND                 GND GND     ( 41- 50)
                  " P8  N14  -  L16 T9  L14 P9   -   -  K15"
                  #             GND GND                 GND ( 51- 60)
                  " P11 K14 T11  -   -  K16 R11 J15 T12  - "
                  # GND                 GND                 ( 61- 70)
                  "  -  H16 R12 H14 P13  -  R13 G16 T14 H15"
                  # GND GND                                 ( 71- 80)
                  "  -   -  M15 L13 M14 K11 F13 K12 G12 K13"
                  #     NC                  NC  NC          ( 81- 90)
                  " T15  -  J16 H13 J14 J12  -   -  G14 H12"
                  #         NC  NC                  NC  NC  ( 91-100)
                  " G15 G11  -   -  F14 B10 F16 A13  -   - "
                  #     NC      NC  NC  NC      NC      NC  (101-110)
                  "E15  -   D14  -   -   -  A15  -  B14  - "
                  # NC  NC      NC      NC  NC  NC      NC  (111-120)
                  "  -   -  A14  -  B13  -   -   -  C12  - "
                  #     NC      NC      NC  GND GND         (121-130)
                  " B12  -  A12  -  C11  -   -   -  B11 E16"
                  #         GND GND         NC  GND GND     (131-140)
                  " A11 F15  -   -  C10 C13  -   -   -  D16"
                  # NC          GND GND                 GND (141-150)
                  "  -  E14 B8   -   -  C9  C6  A9  A7   - "
                  # GND             GND GND                 (151-160)
                  "  -  L12 A6  J11  -   -  C7  E9  D7  E8 "
                  # GND GND     V01     V01 GND GND     V7  (161-170)
                  "  -   -  T2   -  T3   -   -   -  T4   - "
                  #     GND GND V7              GND GND     (171-180)
                  " T5   -   -   -  N6  F10 N7   -   -  D11"
                  #             GND GND     NC  NC  GND GND (181-190)
                  " N9  D10 R9   -   -  E10  -   -   -   - "
                  #                 GND GND NC      NC      (191-200)
                  " N8  R7  L9  P7   -   -   -  M6   -  L8 "
                  # NC  NC  NC  NC                          (201-204)
                  "  -   -   -   - "
                  )
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "add_options":
                "set_option -use_mspi_as_gpio 1 -use_sspi_as_gpio 1"
                " -use_ready_as_gpio 1 -use_done_as_gpio 1",
            "gowin_pack_opts":
                "--mspi_as_gpio --sspi_as_gpio --ready_as_gpio --done_as_gpio",
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        with products.extract("{}.fs".format(name)) as bitstream_filename:
            subprocess.check_call(
                ["openFPGALoader", "-b", "tangprimer20k", bitstream_filename])


class TangPrimer20kLitePlatform(TangPrimer20kPlatform):
    resources = TangPrimer20kPlatform.resources + [
        *ButtonResources(pins={0: "T10"}, invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS33")),
        *ButtonResources(pins={1: "T2"}, invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS15")),

        *SwitchResources(pins="D7 C7",
                         attrs=Attrs(PULL_MODE="NONE", IO_TYPE="LVCMOS15")),
    ]

    connectors = TangPrimer20kPlatform.connectors + [
        # top left, top right, bottom left, bottom right
        Connector("pmod", 0, "L8  P7  E10 D11 - - M6  R7  D10 F10 - -"),
        Connector("pmod", 1, "T6  T7  T8  T9  - - P6  R8  P8  P9  - -"),
        Connector("pmod", 2, "F15 D16 C9  L12 - - E16 E14 A9  J11 - -"),
        Connector("pmod", 3, "R16 P16 N16 L16 - - P15 N15 N14 L14 - -"),

        # 0 on top, 1 on bottom, odd/even rows
        Connector("gpio", 0,
                  " -   -  N6  N7  B11 A12 L9  N8  R9  N9 " # ( 1-10)
                  "A6  A7  C6  B8  C10  -  A11 C11 B12 C12" # (11-20)
                  "B13 A14 B14 A15 D14 E15 F16 F14 G15 G14" # (21-30)
                  "J14 J16 G12 F13 M14 M15 T14 R13 P13 R12" # (31-40)
                  ),
        Connector("gpio", 1,
                  " -   -   -   -   -   -  T5   -  T3  T4 " # ( 1-10)
                  " -   -  E9  E8  T15 C13 T13 M11 B10 A13" # (11-20)
                  "H12 G11 H13 J12 K12 K13 L13 K11 R11 T12" # (21-30)
                  "P11 T11 G16 H15 H16 H14 K16 J15 K15 K14" # (31-40)
                  ),
    ]


class TangPrimer20kDockPlatform(TangPrimer20kPlatform):
    resources = TangPrimer20kPlatform.resources + [
        *LEDResources(pins="C13 A13 N16 N14 L14 L16", invert=True,
                      attrs=Attrs(IO_TYPE="LVCMOS33")),

        # WS2812 RGB LED
        Resource("ws2812", 0, Pins("T9", dir="o"),
                 Attrs(IO_TYPE="LVCMOS33")),

        *ButtonResources(pins={0: "T10"}, invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS33")),
        *ButtonResources(pins={1: "T3", 2: "T2", 3: "D7", 4: "C7"}, invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS15")),

        *SwitchResources(pins={0: "B10"},
                         attrs=Attrs(PULL_MODE="DOWN", IO_TYPE="LVCMOS33")),
        *SwitchResources(pins={1: "E9", 2: "E8", 3: "T4", 4: "T5"},
                         attrs=Attrs(PULL_MODE="DOWN", IO_TYPE="LVCMOS15")),

        Resource("eth_clk50", 0, Pins("A9", dir="i"),
                 Clock(50e6), Attrs(IO_TYPE="LVCMOS33")),
        Resource("eth_rmii", 0,
                 Subsignal("rst",     PinsN("F10", dir="o")),
                 Subsignal("mdio",    Pins("F16", dir="io")),
                 Subsignal("mdc",     Pins("F14", dir="o")),
                 Subsignal("tx_en",   Pins("E16", dir="o")),
                 Subsignal("tx_data", Pins("D16 E14", dir="o")),
                 Subsignal("rx_crs",  Pins("M6",  dir="i")),
                 Subsignal("rx_er",   Pins("L8" , dir="i")),
                 Subsignal("rx_data", Pins("F15 C9", dir="i")),
                 Attrs(IO_TYPE="LVCMOS33")),

        ULPIResource(0, data="G11 H12 J12 H13 T14 R13 P13 R12",
                     clk="T15", dir="K12", nxt="K13", stp="K11",
                     rst="F10", rst_invert=True,
                     attrs=Attrs(PULL_MODE="NONE", IO_TYPE="LVCMOS33")),

        Resource("hdmi", 0,
                 Subsignal("clk", DiffPairs(p="G16", n="H15", dir="o")),
                 Subsignal("d",   DiffPairs(p="H14 J15 K14", n="H16 K16 K15", dir="o")),
                 Subsignal("hdp", Pins("J11", dir="i"),
                           Attrs(IO_TYPE="LVCMOS33")),
                 Subsignal("cec", Pins("L12", dir="io"),
                           Attrs(IO_TYPE="LVCMOS33")),
                 Subsignal("sda", Pins("F14", dir="io"),
                           Attrs(IO_TYPE="LVCMOS33")),
                 Subsignal("scl", Pins("F16", dir="io"),
                           Attrs(IO_TYPE="LVCMOS33")),
                 Attrs(PULL_MODE="NONE")),

        # labeled DISPLAY or RGB LCD
        Resource("lcd", 0,
                 Subsignal("bl",  Pins("E10", dir="o")),
                 Subsignal("clk", Pins("R9",  dir="o")),
                 Subsignal("de",  Pins("E15", dir="o")),
                 Subsignal("hs",  PinsN("A15", dir="o")),
                 Subsignal("vs",  PinsN("D14", dir="o")),
                 Subsignal("r",   Pins("L9 N8 N9 N7 N6", dir="o")),
                 Subsignal("g",   Pins("D11 A11 B11 P7 R7 D10", dir="o")),
                 Subsignal("b",   Pins("B12 C12 B13 A14 B14", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33")),

        # labeled CAM or DVP
        Resource("dvp", 0,
                 Subsignal("d",
                           Pins("T12 T11 P11 R11 M15 M14 J16 J14", dir="i")),
                 Subsignal("scl",  Pins("F14", dir="io")),
                 Subsignal("sda",  Pins("F16", dir="io")),
                 Subsignal("pclk", Pins("F13", dir="i")),
                 Subsignal("xclk", Pins("G12", dir="o")),
                 Subsignal("rst",  PinsN("L13", dir="o")),
                 Subsignal("vs",   Pins("G15", dir="i")),
                 Subsignal("pwdn", Pins("C10", dir="o")),
                 Subsignal("hs",   Pins("G14", dir="i")),
                 Attrs(IO_TYPE="LVCMOS33")),

        # labeled TP or CTP
        Resource("lcd_touch", 0,
                 Subsignal("sda", Pins("F14", dir="io")),
                 Subsignal("scl", Pins("F16", dir="io")),
                 Subsignal("int", Pins("C11", dir="i")),
                 Subsignal("rst", PinsN("A12", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33")),

        # labeled GPIO or MIC ARRAY
        Resource("mic_i2s", 0,
                 Subsignal("sd",  Pins("P8 T8 R8 T7", dir="i")),
                 Subsignal("ws",  Pins("P6", dir="i")),
                 Subsignal("clk", Pins("T6", dir="i")),
                 Attrs(IO_TYPE="LVCMOS33")),
        Resource("mic_led", 0,
                 Subsignal("clk", Pins("P9", dir="o")),
                 Subsignal("dat", Pins("T9", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33")),

        # 3.5mm audio via PT8211
        Resource("dac_i2s", 0,
                 Subsignal("sd",    Pins("P15", dir="o")),
                 Subsignal("ws",    Pins("P16", dir="o")),
                 Subsignal("clk",   Pins("N15", dir="o")),
                 Subsignal("pa_en", Pins("R16", dir="o")),
                 Attrs(PULL_MODE="UP", IO_TYPE="LVCMOS33"))
    ]

    connectors = TangPrimer20kPlatform.connectors + [
        # top left to top right
        Connector("pmod", 0, "B11 D11 N7  N8  - - A11 N6  N9  L9  - -"),
        Connector("pmod", 1, "E15 A15 A14 C12 - - D14 B14 B13 B12 - -"),
        Connector("pmod", 2, "P11 R11 M15 J16 - - T11 T12 M14 J14 - -"),
        Connector("pmod", 3, "P6  T7  P8  T9  - - T6  R8  T8  P9  - -"),
    ]


if __name__ == "__main__":
    from .test.blinky import *
    TangPrimer20kDockPlatform().build(Blinky(), do_program=True)
