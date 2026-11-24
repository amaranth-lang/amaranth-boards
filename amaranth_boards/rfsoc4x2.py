import os
import subprocess

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["RFSoC4x2Platform"]


class RFSoC4x2Platform(XilinxPlatform):
    device = "xczu48dr"
    package = "ffvg1517"
    speed = "2-e"

    default_rst = "rst"
    default_clk = "clk"
    resources = [
        Resource("rst", 0, PinsN("AN12", dir='i'), Attrs(IOSTANDARD="LVCMOS18")),

        # Driven by Si5395, not runtime configurable
        Resource("clk", 0, DiffPairs("G13", "G12", dir="i"), Clock(100e6), Attrs(IOSTANDARD="LVDS")),
        Resource("clk_qsfp", 0, DiffPairs("AL17", "AM17", dir="i"), Clock(156.25e6), Attrs(IOSTANDARD="LVDS")),
        Resource("clk_ddr4", 0, DiffPairs("G13", "G12", dir="i"), Clock(200e6), Attrs(IOSTANDARD="DIFF_SSTL12")),

        # Driven by LM04828, runtime configured by PS
        Resource("clk_lmk", 8, DiffPairs("AN11", "AP11", dir="i"), Attrs(IOSTANDARD="LVDS")),
        Resource("clk_lmk", 9, DiffPairs("AP18", "AR18", dir="i"), Attrs(IOSTANDARD="LVDS")),

        *ButtonResources(pins="AV12 AV10 AW9  AT12", attrs=Attrs(IOSTANDARD="LVCMOS18")),
        *SwitchResources(pins="AN13 AU12 AW11 AV11", attrs=Attrs(IOSTANDARD="LVCMOS18")),

        *LEDResources(pins="AR11 AW10 AT11 AU10", attrs=Attrs(IOSTANDARD="LVCMOS18")),
        RGBLEDResource(0, r="AM8",  g="AM7", b="AN8",  attrs=Attrs(IOSTANDARD="LVCMOS18")),
        RGBLEDResource(1, r="AR12", g="AP8", b="AT10", attrs=Attrs(IOSTANDARD="LVCMOS18")),

        # I2C is routed to PS and is not directly accessible to PL
        Resource("qsfp", 0,
            Subsignal("tx",      DiffPairs(p="Y35  T35  V35  R33", n="Y36  T36  V36  R34", dir="o")),
            Subsignal("rx",      DiffPairs(p="R38  W38  U38 AA38", n="R39  W39  U39 AA39", dir="i")),
            Subsignal("modsel",  PinsN("AK22", dir="o"),  Attrs(IOSTANDARD="LVCMOS18")),
            Subsignal("rst",     PinsN("AL21", dir="o"),  Attrs(IOSTANDARD="LVCMOS18")),
            Subsignal("modprs",  PinsN("AL22", dir="i"),  Attrs(IOSTANDARD="LVCMOS18")),
            Subsignal("int",     PinsN("AM22", dir="i"),  Attrs(IOSTANDARD="LVCMOS18")),
            Subsignal("lpmode",  Pins("AN22", dir="o"),   Attrs(IOSTANDARD="LVCMOS18")),
        ),

        # PPS input
        Resource("pps", 0,
            Subsignal("comparator", Pins("AJ13", dir="i"), Attrs(IOSTANDARD="LVCMOS18")),
            Subsignal("schmidt",    Pins("AH13", dir="i"), Attrs(IOSTANDARD="LVCMOS18")),
        ),
        SPIResource(0, # ADS7885 ADC connected to 1PPS input
                    cs_n="AG14", clk="AH12",
                    copi=None,   cipo="AK13",
                    attrs=Attrs(IOSTANDARD="LVCMOS18")),
        DDR4Resource(0,
                     rst_n="E14", clk_p="J11", clk_n="J10", clk_en="F12",
                     cs_n="E11", we_n="K13", ras_n="E13", cas_n="F14", act_n="B14",
                     a="B13 G6  A14 F10 D14 F11 J7  H13 A11 H6  C15 G7  D13 H11",
                     ba="A12 H10", bg="H12",
                     dqs_p="K19 L15 B18 G19 D23 J20 B22 K21",
                     dqs_n="K18 L14 B17 F19 D24 H20 A22 K22",
                     dq=   "K17 J16 H17 H16 J18 K16 J19 L17"
                           "N17 N13 N15 L12 M17 M13 M15 M12"
                           "D16 A17 C17 A19 D15 C16 B19 A16"
                           "G18 E16 F16 G15 H18 E17 E18 F15"
                           "E24 D21 E22 E21 E23 F20 F24 G20"
                           "J21 G22 K24 G23 L24 H22 H23 H21"
                           "C21 A24 B24 A20 C22 A21 C20 B20"
                           "M20 L20 L22 L21 N19 M19 L23 L19",
                     dm_n= "J15 N14 D18 G17 F21 J23 C23 N20", odt="A15",
                     diff_pod_attrs=Attrs(IOSTANDARD="DIFF_POD12_DCI"),
                     pod_attrs=Attrs(IOSTANDARD="POD12_DCI"),
                     diff_attrs=Attrs(IOSTANDARD="DIFF_SSTL12_DCI"),
                     attrs=Attrs(IOSTANDARD="SSTL12_DCI")),
    ]
    connectors = [
        # Dual PMOD Port with some extra pins in the middle
        Connector("pmod", 0,
                  "AF16 AG17 AJ16 AK17 - - "
                  "AF15 AF17 AH17 AK16 - - "),
        Connector("pmod", 1,
                  "AW13 AR13 AU13 AV13 - - "
                  "AU15 AP14 AT15 AU14 - - "),
        Connector("pmod_extra", 0,
                  "AW16 AW15 AW14"
                  "AR16 AV16 AT16"),

        # VIO Driven by DAC controlled by PS
        Connector("syzygy", 0, {
            # single ended
            "S0":  "AU2", "S1":   "A7",
            "S2":  "AU1", "S3":   "A6",
            "S4":  "AV3", "S5":   "C8",
            "S6":  "AV2", "S7":   "C7",
            "S8":  "AW4", "S9":   "E9",
            "S10": "AW3", "S11":  "E8",
            "S12": "AT7", "S13":  "F6",
            "S14": "AT6", "S15":  "E6",
            "S16":  "B8", "S17": "AR6",
            "S18":  "D6", "S19": "AR7",
            "S20":  "C6", "S21": "AU7",
            "S22":  "B5", "S23": "AV7",
            "S24":  "A5", "S25": "AU8",
            "S26":  "C5", "S27": "AV8",
            "S28": "AV6", "S29": "B10",
            "S30": "AV5", "S31":  "B9",

            # diff pairs
            "D0P": "AU2", "D0N": "AU1",
            "D1P":  "A7", "D1N":  "A6",
            "D2P": "AV3", "D2N": "AV2",
            "D3P":  "C8", "D3N":  "C7",
            "D4P": "AW4", "D4N": "AW3",
            "D5P":  "E9", "D5N":  "E8",
            "D6P": "AT7", "D6N": "AT6",
            "D7P":  "F6", "D7N":  "E6",

            # clock pairs
            "C2PP":"B10", "C2PN": "B9",
            "P2CP":"AV6", "P2CN":"AV5",
        }),
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_before_bitstream":
            "set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]",
        }
        return super().toolchain_prepare(
            fragment, name, **overrides, **kwargs)

    # OpenOCD doesn't have the ZU48dr in its idcode database for
    # zynqmp yet and gets confused, and we are dependent on vivado
    # for the immediate future anyways
    def toolchain_program(self, products, name):
        xsdb = os.environ.get("XSDB", "xsdb")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([
                xsdb,
                "-eval", "connect; fpga -file {}".format(bitstream_filename)])


if __name__ == "__main__":
    from .test.blinky import *
    RFSoC4x2Platform().build(Blinky(), do_program=True)
