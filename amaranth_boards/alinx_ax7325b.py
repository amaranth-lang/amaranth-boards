import os
import subprocess

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["AX7325BPlatform"]


class AX7325BPlatform(XilinxPlatform):
    """
    https://www.en.alinx.com/Product/FPGA-Development-Boards/Kintex-7/AX7325B.html

    Power Supply Function

    POWER
    +1.0V FPGA core voltage
    +3.3V FPGA Bank0, Bank14, Bank15, QSIP FLASH, Clock Crystal, SD Card, SFP Optical Module
    +1.8V Gigabit Ethernet, HDMI, USB
    +1.5V DDR3, SODIMM, FPGA Bank33, Bank34, Bank35, VADJ(+2.5V) FPGA Bank12, Bank13, FMC
    VREF, VTT (+0.75V) DDR3, SODIMM
    MGTAVCC(+1.0V) FPGA Bank115, Bank116, Bank117, Bank118
    MGTAVTT(+1.2V) FPGA Bank115, Bank116, Bank117, Bank118
    MGT_1.8V (+1.2V) FPGA GTX auxiliary voltage
    """
    device      = "xc7k325t"
    package     = "ffg900"
    speed       = "2"
    default_clk = "clk"
    resources   = [
        Resource("clk", 0, DiffPairs("AE10", "AF10", dir="i"), Clock(200e6), Attrs(IOSTANDARD="LVDS")),
        Resource("clk0", 0, DiffPairs("F20", "E20", dir="i"), Clock(200e6), Attrs(IOSTANDARD="LVDS")),
        Resource("clk_sfp", 0, DiffPairs("G8", "G7", dir="i"), Clock(156.25e6), Attrs(IOSTANDARD="LVDS")),
        Resource("clk_qsfp", 0, DiffPairs("C8", "C7", dir="i"), Clock(125e6), Attrs(IOSTANDARD="LVDS")),
        *LEDResources(pins="A22 C19 B19 E18", attrs=Attrs(IOSTANDARD="LVCMOS15")),
        DDR3Resource(0,
            rst_n="Y11",
            clk_p="AG10",
            clk_n="AH10",
            clk_en="AD12",
            cs_n="AF11",
            we_n="AD9",
            ras_n="AE9",
            cas_n="AE11",
            a="AA12 AB12 AA8 AB8 AB9 AC9 AB13 Y10 AA11 AA10 AA13 AD8 AB10 AC10 AJ9",
            ba="AE8 AC12 AC11",
            dqs_p="Y19 AJ18 AH16 AC16 AH7 AG4 AG2 AD2",
            dqs_n="Y18 AK18 AJ16 AC15 AJ7 AG3 AH1 AD1",
            dq="""AD18 AB18 AD17 AB19 AD16 AC19 AE18 AB17
                 AG19 AK19 AD19 AJ19 AF18 AH19 AE19 AG18
                 AK15 AJ17 AH15 AF15 AG14 AH17 AG15 AK16
                 AE15 Y16 AC14 AA15 AA17 AD14 AA16 AB15
                 AK6 AJ8 AJ6 AF8 AK4 AK8 AK5 AG7
                 AE4 AF1 AE5 AE1 AF6 AE3 AF5 AF2
                 AH4 AJ2 AH5 AJ4 AH2 AK1 AH6 AJ1
                 AC2 AC5 AD3 AC7 AE6 AD6 AC1 AC4""",
            dm="AA18 AF17 AE16 Y15 AF7 AF3 AJ3 AD4",
            odt="AD11",
            diff_attrs=Attrs(IOSTANDARD="LVDS"),
            attrs=Attrs(IOSTANDARD="LVCMOS15")),
        DDR3Resource(1,
           # "sodimm",
            rst_n="F17",
            #clk_p="D17 E19",
            clk_p="D17",
            #clk_n="D18 D19",
            clk_n="D18",
            #clk_en="L17 G17",
            clk_en="L17",
            #cs_n="F22 C21",
            cs_n="F22",
            we_n="H21",
            ras_n="G20",
            cas_n="K20",
            a="F21 D21 E21 F18 H17 B17 J19 C17 J18 C16 K19 G18 K18 G22 D16 L18",
            ba="H19 H20 J17",
            dqs_p="L12 J16 C12 D14 F25 B28 C29 G27",
            dqs_n="L13 H16 B12 C14 E25 A28 B29 F27",
            dq="""L15 K14 J14 L11 K15 L16 J13 K16
                  J12 J11 H15 G14 H11 H12 G13 G15
                  D12 A11 D13 E13 F11 E11 A12 F12
                  B13 A13 B15 C15 B14 A15 E15 F15
                  A23 D24 E24 E26 E23 B23 D23 G23
                  B24 C24 C26 A27 A25 A26 B27 D26
                  D27 A30 C30 D29 C27 B30 E29 E28
                  F28 F30 H30 G28 H24 G29 H27 H26""",
            dm="K13 H14 D11 E14 F26 C25 D28 G30",
            #odt="D22 H22",
            odt="D22",
            diff_attrs=Attrs(IOSTANDARD="LVDS"),
            attrs=Attrs(IOSTANDARD="LVCMOS15")),
        # QSPI Flash
        *SPIFlashResources(0,
            cs_n="U19", clk="B10", copi="P24", cipo="R25", wp_n="R20", hold_n="R21",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
        UARTResource(0,
            rx="AJ26", tx="AK26",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
        # 4x SFP (BANK117, ref clock 156.25MHz)
        Resource("sfp", 0,
            Subsignal("tx",     DiffPairs(p="K2", n="K1", dir="o")),
            Subsignal("rx",     DiffPairs(p="K6", n="K5", dir="i")),
            Subsignal("tx_dis", Pins("T28", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("loss",   Pins("R28", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        ),
        Resource("sfp", 1,
            Subsignal("tx",     DiffPairs(p="J4", n="J3", dir="o")),
            Subsignal("rx",     DiffPairs(p="H6", n="H5", dir="i")),
            Subsignal("tx_dis", Pins("T28", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("loss",   Pins("T26", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        ),
        Resource("sfp", 2,
            Subsignal("tx",     DiffPairs(p="H2", n="H1", dir="o")),
            Subsignal("rx",     DiffPairs(p="G4", n="G3", dir="i")),
            Subsignal("tx_dis", Pins("U28", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("loss",   Pins("U27", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        ),
        Resource("sfp", 3,
            Subsignal("tx",     DiffPairs(p="F2", n="F1", dir="o")),
            Subsignal("rx",     DiffPairs(p="F6", n="F5", dir="i")),
            Subsignal("tx_dis", Pins("U25", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("loss",   Pins("A18", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        ),
        # QSFP+ (BANK118, ref clock 125MHz)
        Resource("qsfp", 0,
            Subsignal("tx",      DiffPairs(p="D2 B2 C4 A4", n="D1 B1 C3 A3", dir="o")),
            Subsignal("rx",      DiffPairs(p="E4 B6 D6 A8", n="E3 B5 D5 A7", dir="i")),
            Subsignal("modsel",  PinsN("R30", dir="o"),  Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("rst",     PinsN("U30", dir="o"),  Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("modprs",  PinsN("U22", dir="i"),  Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("int",     PinsN("R24", dir="i"),  Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("lpmode",  Pins("V26", dir="o"),   Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("scl",     Pins("A20", dir="io"),  Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("sda",     Pins("A21", dir="io"),  Attrs(IOSTANDARD="LVCMOS33")),
        ),
        # PCIe x8 (BANK115, BANK116)
        Resource("pcie", 0,
            Subsignal("rst",    PinsN("B18", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("rx",     DiffPairs(p="M6 P6 R4 T6 V6 W4 Y6 AA4",
                                          n="M5 P5 R3 T5 V5 W3 Y5 AA3", dir="i")),
            Subsignal("tx",     DiffPairs(p="L4 M2 N4 P2 T2 U4 V2 Y2",
                                          n="L3 M1 N3 P1 T1 U3 V1 Y1", dir="o")),
        ),
        Resource("temperature", 0,
            Subsignal("scl",        Pins("P23", dir="i")),
            Subsignal("sda",        Pins("N25", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),
        *SDCardResources(0, clk="AH21", cmd="AJ21", dat0="AJ22", dat1="AJ23",
                         dat2="AG20", dat3="AH20", cd="AE20",
                         attrs=Attrs(IOSTANDARD="LVCMOS25")),
        *ButtonResources(pins="AG27 AG28", attrs=Attrs(IOSTANDARD="LVCMOS25")),
    ]
    connectors  = [
        # FMC LPC connector (BANK12, BANK13, VADJ=2.5V)
        Connector("fmc", 0,
                  {"clk0_p":     "AD23",
                   "clk0_n":     "AE24",
                   "clk1_p":     "AG29",
                   "clk1_n":     "AH29",
                   "la00_cc_p":  "AF22",
                   "la00_cc_n":  "AG23",
                   "la01_cc_p":  "AG24",
                   "la01_cc_n":  "AH24",
                   "la02_p":     "AK23",
                   "la02_n":     "AK24",
                   "la03_p":     "AJ24",
                   "la03_n":     "AK25",
                   "la04_p":     "AG25",
                   "la04_n":     "AH25",
                   "la05_p":     "AE23",
                   "la05_n":     "AF23",
                   "la06_p":     "AG22",
                   "la06_n":     "AH22",
                   "la07_p":     "AC24",
                   "la07_n":     "AD24",
                   "la08_p":     "AE25",
                   "la08_n":     "AF25",
                   "la09_p":     "AC22",
                   "la09_n":     "AD22",
                   "la10_p":     "AD21",
                   "la10_n":     "AE21",
                   "la11_p":     "AB22",
                   "la11_n":     "AB23",
                   "la12_p":     "AB24",
                   "la12_n":     "AC25",
                   "la13_p":     "AC20",
                   "la13_n":     "AC21",
                   "la14_p":     "Y21",
                   "la14_n":     "AA21",
                   "la15_p":     "Y23",
                   "la15_n":     "Y24",
                   "la16_p":     "AA22",
                   "la16_n":     "AA23",
                   "la17_cc_p":  "AE28",
                   "la17_cc_n":  "AF28",
                   "la18_cc_p":  "AB27",
                   "la18_cc_n":  "AC27",
                   "la19_p":     "AK29",
                   "la19_n":     "AK30",
                   "la20_p":     "AJ27",
                   "la20_n":     "AK28",
                   "la21_p":     "AG30",
                   "la21_n":     "AH30",
                   "la22_p":     "AJ28",
                   "la22_n":     "AJ29",
                   "la23_p":     "AA27",
                   "la23_n":     "AB28",
                   "la24_p":     "AD29",
                   "la24_n":     "AE29",
                   "la25_p":     "AE30",
                   "la25_n":     "AF30",
                   "la26_p":     "Y28",
                   "la26_n":     "AA28",
                   "la27_p":     "Y26",
                   "la27_n":     "AA26",
                   "la28_p":     "AC29",
                   "la28_n":     "AC30",
                   "la29_p":     "AD27",
                   "la29_n":     "AD28",
                   "la30_p":     "Y30",
                   "la30_n":     "AA30",
                   "la31_p":     "AB29",
                   "la31_n":     "AB30",
                   "la32_p":     "W27",
                   "la32_n":     "W28",
                   "la33_p":     "W29",
                   "la33_n":     "Y29",
                   "scl":        "A16",
                   "sda":        "A17"}),
        # J16 Expansion Header (active pins only, numbered by header pin)
        Connector("j16", 0,
                  { "3": "J24",  "4": "J23",
                    "5": "J22",  "6": "J21",
                    "7": "J26",  "8": "K26",
                    "9": "K30", "10": "L30",
                   "11": "L28", "12": "M28",
                   "13": "M27", "14": "N27",
                   "15": "N30", "16": "N29",
                   "17": "L27", "18": "L26",
                   "19": "J28", "20": "J27",
                   "21": "H29", "22": "J29",
                   "23": "K29", "24": "K28",
                   "25": "L20", "26": "M20",
                   "27": "K21", "28": "L21",
                   "29": "L23", "30": "L22",
                   "31": "K24", "32": "K23",
                   "33": "K25", "34": "L25",
                   "35": "M29", "36": "M19"}),
    ]

    def toolchain_program(self, product, name):
        # openfpgaloader
        openfpgaloader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with product.extract("{}.bin".format(name)) as fn:
            # included with board
            subprocess.check_call([openfpgaloader, "-c", "ft232", fn])


if __name__ == "__main__":
    from .test.blinky import *
    AX7325BPlatform().build(Blinky(), do_program=True)
