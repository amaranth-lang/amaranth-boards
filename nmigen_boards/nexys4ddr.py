import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from .resources import *


__all__ = ["Nexys4DDRPlatform"]


class Nexys4DDRPlatform(Xilinx7SeriesPlatform):
    device      = "xc7a100t"
    package     = "csg324"
    speed       = "1"
    default_clk = "clk100"
    default_rst = "rst"
    resources   = [
        Resource("clk100", 0,
            Pins("E3", dir="i"), Clock(100e6), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("rst", 0,
            PinsN("C12", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        *SwitchResources(
            pins="J15 L16 M13 R15 R17 T18 U18 R13 T8  U8  R16 T13 H6  U12 U11 V10",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(
            pins="H17 K15 J13 N14 R18 V17 U17 U16 V16 T15 U14 T16 V15 V14 V12 V11",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        RGBLEDResource(0,
            r="N15", g="M16", b="R12",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),
        RGBLEDResource(1,
            r="N16", g="R11", b="G14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Display7SegResource(0,
            a="T10", b="R10", c="K16", d="K13", e="P15",
            f="T11", g="L18", dp="H15", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),
        Resource("display_7seg_an", 0,
            PinsN("J17 J18 T9 J14 P14 T14 K2 U13", dir="o"),
            Attrs(IOSTANDARD="LVCMOS33")),

        Resource("button_reset", 0,
            PinsN("C12", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("button_center", 0,
            Pins("N17",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("button_up", 0,
            Pins("M18",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("button_left", 0,
            Pins("P17",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("button_right", 0,
            Pins("M17",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("button_down", 0,
            Pins("P18",  dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        Resource("vga", 0,
            Subsignal("r",  Pins("A3 B4 C5 A4", dir="o")),
            Subsignal("g",  Pins("C6 A5 B6 A6", dir="o")),
            Subsignal("b",  Pins("B7 C7 D7 D8", dir="o")),
            Subsignal("hs", Pins("B11"        , dir="o")),
            Subsignal("vs", Pins("B12"        , dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")),

        *SDCardResources(0,
            clk="B1",  cmd="C1",  cd="A1",
            dat0="C2", dat1="E1", dat2="F1", dat3="D2",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),
        Resource("sd_card_reset", 0,
            Pins("E2", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),

        Resource("accelerometer", 0,                        # ADXL362
            Subsignal("cs",   PinsN("D15",    dir="o")),
            Subsignal("clk",  Pins("F15",     dir="o")),
            Subsignal("mosi", Pins("F14",     dir="o")),
            Subsignal("miso", Pins("E15",     dir="i")),
            Subsignal("int",  Pins("B13 C16", dir="i"),
                Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE")),
            Attrs(IOSTANDARD="LVCMOS33")),

        Resource("temp_sensor", 0,                          # ADT7420
            Subsignal("scl", Pins("C14", dir="o")),
            Subsignal("sda", Pins("C15", dir="io")),
            Subsignal("int", Pins("D13", dir="i"), Attrs(PULLUP="TRUE")),
            Subsignal("ct",  Pins("B14", dir="i"), Attrs(PULLUP="TRUE")),
            Attrs(IOSTANDARD="LVCMOS33")),

        Resource("microphone", 0,                           # ADMP421
            Subsignal("clk",    Pins("J5", dir="o")),
            Subsignal("data",   Pins("H5", dir="i")),
            Subsignal("lr_sel", Pins("F5", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")),

        Resource("audio", 0,
            Subsignal("pwm", Pins("A11",  dir="o")),
            Subsignal("sd",  PinsN("D12", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")),

        UARTResource(0,
            rx="C4", tx="D4", rts="D3", cts="E5",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("ps2_host", 0,
            Subsignal("clk", Pins("F4", dir="i")),
            Subsignal("dat", Pins("B2", dir="io")),
            Attrs(IOSTANDARD="LVCMOS33", PULLUP="TRUE")),

        Resource("eth", 0,                                  # LAN8720A
            Subsignal("mdio",   Pins("A9",      dir="io")),
            Subsignal("mdc",    Pins("C9",      dir="o")),
            Subsignal("reset",  Pins("B3",      dir="o")),
            Subsignal("rxd",    Pins("C11 D10", dir="io")),
            Subsignal("rxerr",  Pins("C10",     dir="io")),
            Subsignal("txd",    Pins("A10 A8",  dir="o")),
            Subsignal("txen",   Pins("B9",      dir="o")),
            Subsignal("crs_dv", Pins("D9",      dir="io")),
            Subsignal("int",    PinsN("B8",     dir="io")),
            Subsignal("clk",    Pins("D5",      dir="o"), Clock(50e6)),
            Attrs(IOSTANDARD="LVCMOS33")),

        *SPIFlashResources(0,
            cs="L13", clk="E9", mosi="K17", miso="K18", wp="L14", hold="M14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("ddr2", 0,                                 # MT47H64M16HR-25:H
            Subsignal("a",
                Pins("M4 P4 M6 T1 L3 P5 M2 N1 L4 N5 R2 K5 N6 K3", dir="o")),
            Subsignal("dq",
                Pins("R7 V6 R8 U7 V7 R6 U6 R5 T5 U3 V5 U4 V4 T4 V1 T3", dir="io"),
                    Attrs(IN_TERM="UNTUNED_SPLIT_50")),
            Subsignal("ba",  Pins("P2 P3 R1", dir="o")),
            Subsignal("clk", DiffPairs("L6", "L5", dir="o"),
                Attrs(IOSTANDARD="DIFF_SSTL18_I")),
            Subsignal("clk_en", Pins("M1", dir="o")),
            Subsignal("cs",  PinsN("K6", dir="o")),
            Subsignal("we",  PinsN("N2", dir="o")),
            Subsignal("ras", PinsN("N4", dir="o")),
            Subsignal("cas", PinsN("L1", dir="o")),
            Subsignal("dqs", DiffPairs("U9 U2", "V9 V2", dir="o"),
                Attrs(IOSTANDARD="DIFF_SSTL18_I")),
            Subsignal("dm",  Pins("T6 U1", dir="o")),
            Subsignal("odt", Pins("R5",    dir="o")),
            Attrs(IOSTANDARD="SSTL18_I", SLEW="FAST"))
    ]
    connectors = [
        Connector("pmod", 0, "C17 D18 E18 G17 - - D17 E17 F18 G18 - -"),  # JA
        Connector("pmod", 1, "D14 F16 G16 H14 - - E16 F13 G13 H16 - -"),  # JB
        Connector("pmod", 2, "K1  F6  J2  G6  - - E7  J3  J4  E6  - -"),  # JC
        Connector("pmod", 3, "H4  H1  G1  G3  - - H2  G4  G2  F3  - -")   # JD
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_before_bitstream":
                "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "script_after_bitstream":
                "write_cfgmem -force -format bin -interface spix4 -size 16 "
                "-loadbit \"up 0x0 {name}.bit\" -file {name}.bin".format(name=name),
            "add_constraints":
                """
                set_property INTERNAL_VREF 0.9 [get_iobanks 34]
                set_property CFGBVS VCCO [current_design]
                set_property CONFIG_VOLTAGE 3.3 [current_design]
                """
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        xc3sprog = os.environ.get("XC3SPROG", "xc3sprog")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([xc3sprog, "-c", "nexys4", bitstream_filename], check=True)


if __name__ == "__main__":
    from .test.blinky import *
    Nexys4DDRPlatform().build(Blinky(), do_program=True)
