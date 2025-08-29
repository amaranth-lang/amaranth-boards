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
        Resource("clk_sfp", 0, DiffPairs("G8", "G7", dir="i"), Clock(156e6), Attrs(IOSTANDARD="LVDS")),
        Resource("clk_qsfp", 0, DiffPairs("C8", "C7", dir="i"), Clock(125e6), Attrs(IOSTANDARD="LVDS")),
        *LEDResources(pins="A22 C19 B19 E18", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        DDR3Resource(0,
            rst_n="Y11",
            clk_p="AG10",
            clk_n="AH10",
            clk_en="AD12",
            cs_n="AF11",
            we_n="AD9",
            ras_n="AE9",
            cas_n="AE11",
            a="AB12 AA8 AB9 AC9 AB13 Y10 AA11 AA10 AA13 AD8 AB10 AC10 AJ9",
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
        # TODO QSPI Flash
        # CCLK B10
        # CE_B U19
        # D0 P24
        # D1 R25
        # D2 R20
        # D3 R21
        # *SPIFlashResources(0,
        #     cs_n="", clk="", copi="", cipo="", wp_n="", hold_n="",
        #     attrs=Attrs(IOSTANDARD="LVCMOS33")
        # ),
        UARTResource(0,
            rx="AJ26", tx="AK26",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
        # TODO: 4x SFP
        # SFP1_TX_P K2
        # SFP1_TX_N K1
        # SFP1_RX_P K6
        # SFP1_RX_P K5
        # SFP1_TX_DIS T28
        # SFP1_LOSS R28
        # SFP2_TX_P J4
        # SFP2_TX_N J3
        # SFP2_RX_P H6
        # SFP2_RX_P H5
        # SFP2_TX_DIS T28
        # SFP2_LOSS T26
        # SFP3_TX_P H2
        # SFP3_TX_N H1
        # SFP3_RX_P G4
        # SFP3_RX_P G3
        # SFP3_TX_DIS U28
        # SFP3_LOSS U27
        # SFP4_TX_P F2
        # SFP4_TX_N F1
        # SFP4_RX_P F6
        # SFP4_RX_P F5
        # SFP4_TX_DIS U25
        # SFP4_LOSS A18
        # TODO: QSFP
        # QSFP1_TX_P D2
        # QSFP1_TX_N D1
        # QSFP2_TX_P B2
        # QSFP2_TX_N B1
        # QSFP3_TX_P C4
        # QSFP3_TX_N C3
        # QSFP4_TX_P A4
        # QSFP4_TX_N A3
        # QSFP1_RX_P E4
        # QSFP1_RX_N E3
        # QSFP2_RX_P B6
        # QSFP2_RX_N B5
        # QSFP3_RX_P D6
        # QSFP3_RX_N D5
        # QSFP4_RX_P A8
        # QSFP4_RX_N A7
        # QSFP_MODSELL R30
        # QSFP_RESETL U30
        # QSFP_MMODPRSL U22
        # QSFP_INTL R24
        # QSFP_LPMODE V26
        # QSFP_SCL A20
        # QSFP_SDA A21
        # TODO: PCIe x8
        # PCIE_RX0_P M6
        # PCIE_RX0_N M5
        # PCIE_RX1_P P6
        # PCIE_RX1_N P5
        # PCIE_RX2_P R4
        # PCIE_RX2_N R3
        # PCIE_RX3_P T6
        # PCIE_RX3_N T5
        # PCIE_RX4_P V6
        # PCIE_RX4_N V5
        # PCIE_RX5_P W4
        # PCIE_RX5_N W3
        # PCIE_RX6_P Y6
        # PCIE_RX6_N Y5
        # PCIE_RX7_P AA4
        # PCIE_RX7_N AA3
        # PCIE_TX0_P L4
        # PCIE_TX0_N L3
        # PCIE_TX1_P M2
        # PCIE_TX1_N M1
        # PCIE_TX2_P N4
        # PCIE_TX2_N N3
        # PCIE_TX3_P P2
        # PCIE_TX3_N P1
        # PCIE_TX4_P T2
        # PCIE_TX4_N T1
        # PCIE_TX5_P U4
        # PCIE_TX5_N U3
        # PCIE_TX6_P V2
        # PCIE_TX6_N V1
        # PCIE_TX7_P Y2
        # PCIE_TX7_N Y1
        # PCIE_PERST B18
        Resource("temperature", 0,
            Subsignal("scl",        Pins("P23", dir="i")),
            Subsignal("sda",        Pins("N25", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),
        *SDCardResources(0, clk="AH21", cmd="AJ21", dat0="AJ22", dat1="AJ23",
                         dat2="AG20", dat3="AH20", cd="AE20",
                         attrs=Attrs(IOSTANDARD="LVCMOS33")),
        # TODO: FMC
        # TODO: J16 Expansion Header
        *ButtonResources(pins="AG27 AG28", attrs=Attrs(IOSTANDARD="LVCMOS33")),
    ]
    connectors  = []

    def toolchain_program(self, product, name):
        # openfpgaloader
        openfpgaloader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with product.extract("{}.bin".format(name)) as fn:
            # included with board
            subprocess.check_call([openfpgaloader, "-c", "ft232", fn])


if __name__ == "__main__":
    from .test.blinky import *
    AX7325BPlatform().build(Blinky(), do_program=True)
