import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from .resources import *


__all__ = ["Genesys2Platform"]


class Genesys2Platform(Xilinx7SeriesPlatform):
    """Platform file for Diglient Genesys2 Kitex-7 board.
    https://reference.digilentinc.com/reference/programmable-logic/genesys-2/start"""

    device = "xc7k325t"
    package = "ffg900"
    speed = "2"

    def __init__(self, JP6="2V5"):
        super().__init__()

        assert JP6 in ["1V2", "1V8", "2V5", "3V3"]
        self._JP6 = JP6

    def bank15_16_17_iostandard(self):
        return "LVCMOS" + self._JP6

    default_rst = "rst"
    default_clk = "clk"
    resources = [
        Resource("rst", 0, PinsN("R19", dir="i"),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("clk", 0, DiffPairs(p="AD12 ", n="AD11", dir="i"),
                 Clock(200e6), Attrs(IOSTANDARD="LVDS")),
        *ButtonResources(pins={
                "w": "M20",
                "e": "C19",
                "n": "B19",
                "s": "M19",
                "c": "E18"}, attrs=Attrs(IOSTANDARD=bank15_16_17_iostandard)),
        *SwitchResources(pins="G19 G25 H24 K19 N19 P19",
                         attrs=Attrs(IOSTANDARD=bank15_16_17_iostandard)),
        *SwitchResources(pins={
                6: "P26",
                7: "P27"}, attrs=Attrs(IOSTANDARD="LVCMOS33")),
        *LEDResources(pins="T28 V19 U30 U29 V20 V26 W24 W23",
                      attrs=Attrs(IOSTANDARD="LVCMOS33")),
        Resource("fan", 0,
                 Subsignal("pwm", Pins("W19", dir="o")),
                 Subsignal("tach", Pins("V21", dir="i")),
                 Attrs(IOSTANDARD="LVCMOS33")),
        UARTResource(0, rx="Y20", tx="Y23",
                     attrs=Attrs(IOSTANDARD="LVCMOS33")),
        Resource("i2c", 0,
                 Subsignal("scl", Pins("AE30", dir="io")),
                 Subsignal("sda", Pins("AF30", dir="io")),
                 Attrs(IOSTANDARD="LVCMOS33")),
        Resource("ddr3", 0,
                 Subsignal("rst", PinsN("AG5", dir="o"),
                           Attrs(IOSTANDARD="SSTL15")),
                 Subsignal("clk",
                           DiffPairs(p="AB9", n="AC9", dir="o"),
                           Attrs(IOSTANDARD="DIFF_SSTL15_DCI")),
                 Subsignal("clk_en", Pins("AJ9", dir="o")),
                 Subsignal("cs", PinsN("AH12", dir="o")),
                 Subsignal("we", PinsN("AG13", dir="o")),
                 Subsignal("ras", PinsN("AE11", dir="o")),
                 Subsignal("cas", PinsN("AF11", dir="o")),
                 Subsignal("a", Pins(
                     "AC12 AE8 AD8 AC10 AD9 AA13 AA10 AA11 "
                     "Y10 Y11 AB8 AA8 AB12 AA12 AH9 AG9", dir="o")),
                 Subsignal("ba", Pins("AE9 AB10 AC11", dir="o")),
                 Subsignal("dqs",
                           DiffPairs(p="AD2 AG4 AG2 AH7",
                                     n="AD1 AG3 AH1 AJ7", dir="io"),
                           Attrs(IOSTANDARD="DIFF_SSTL15_DCI", ODT="RTT_40")),
                 Subsignal("dq", Pins(
                     "AD3 AC2 AC1 AC5 AC4 AD6 AE6 AC7 "
                     "AF2 AE1 AF1 AE4 AE3 AE5 AF5 AF6 "
                     "AJ4 AH6 AH5 AH2 AJ2 AJ1 AK1 AJ3 "
                     "AF7 AG7 AJ6 AK6 AJ8 AK8 AK5 AK4", dir="io"),
                     Attrs(ODT="RTT_40")),
                 Subsignal("dm", Pins("AD4 AF3 AH4 AF8", dir="o")),
                 Subsignal("odt", Pins("AK9", dir="o")),
                 Attrs(IOSTANDARD="SSTL15_DCI", SLEW="FAST",
                       OUTPUT_IMPEDANCE="RDRV_40_40")),
        Resource("audio_i2c", 0,  # ADAU1761 I2C
                 Subsignal("scl", Pins("AE19", dir="io")),
                 Subsignal("sda", Pins("AF18", dir="io")),
                 Subsignal("adr", Pins("AD19 AG19", dir="o")),
                 Attrs(IOSTANDARD="LVCMOS18")),
        Resource("audio_i2s", 0,  # ADAU1761 ADC, I2S
                 Subsignal("clk", Pins("AG18", dir="o")), # BCLK
                 Subsignal("sd_adc", Pins("AH19", dir="o")), # ADC_SDATA
                 Subsignal("sd_dac", Pins("AJ19", dir="i")),  # DAC_SDATA
                 Subsignal("ws", Pins("AJ18", dir="o")), # LRCLK
                 Attrs(IOSTANDARD="LVCMOS18")),
        Resource("audio_clk", 0,  # ADAU1761 MCLK
                 Pins("AK19", dir="o"), Attrs(IOSTANDARD="LVCMOS18")),
        SPIResource(0,  # OLED, SSD1306, 128 x 32
                    cs="dummy-cs0", clk="AF17", mosi="Y15",
                    miso="dummy-miso0", reset="AB17",
                    attrs=Attrs(IOSTANDARD="LVCMOS18")),
        Resource("oled", 0,  # OLED, UG-2832HSWEG04
                 Subsignal("dc", Pins("AC17", dir="o")),
                 Subsignal("vdd_en", PinsN("AG17", dir="o")),
                 Subsignal("vbat_en", PinsN("AB22", dir="o"),
                           Attrs(IOSTANDARD="LVCMOS33")),
                 Attrs(IOSTANDARD="LVCMOS18")),
        Resource("hdmi", 0,  # HDMI TX, connector J4
                 Subsignal("scl", Pins("AF27", dir="io"),
                           Attrs(IOSTANDARD="LVCMOS33")),
                 Subsignal("sda", Pins("AF26", dir="io"),
                           Attrs(IOSTANDARD="LVCMOS33")),
                 Subsignal("clk",
                           DiffPairs(p="AA20", n="AB20", dir="o")),
                 Subsignal("d",
                           DiffPairs(p="AC20 AA22 AB24",
                                     n="AC21 AA23 AC25", dir="o")),
                 Attrs(IOSTANDARD="TMDS_33")),
        Resource("hdmi", 1,  # HDMI RX, connector J5
                 Subsignal("scl", Pins("AJ28", dir="io"),
                           Attrs(IOSTANDARD="LVCMOS33")),
                 Subsignal("sda", Pins("AJ29", dir="io"),
                           Attrs(IOSTANDARD="LVCMOS33")),
                 Subsignal("clk", DiffPairs(p="AE28", n="AF28", dir="i")),
                 Subsignal("rx",
                           DiffPairs(p="AJ26 AG27 AH26",
                                     n="AK26 AG28 AH27", dir="i")),
                 Attrs(IOSTANDARD="TMDS_33")),
        Resource("vga", 0,
                 Subsignal("r", Pins("AK25 AG25 AH25 AK24 AJ24", dir="o")),
                 Subsignal("g", Pins("AJ23 AJ22 AH22 AK21 AJ21 AK23",
                                     dir="o")),
                 Subsignal("b", Pins("AH20 AG20 AF21 AK20 AG22", dir="o")),
                 Subsignal("hsync", PinsN("AF20", dir="o")),
                 Subsignal("vsync", PinsN("AG23", dir="o")),
                 Attrs(IOSTANDARD="LVCMOS33")),
        *SDCardResources(0, clk="R28", cmd="R29", dat0="R26", dat1="R30",
                         dat2="P29", dat3="T30", cd="P28",
                         attrs=Attrs(IOSTANDARD="LVCMOS33")),
        Resource("sd_card_rst", 0,
                 Pins("AE24", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("ulpi", 0,
                 Subsignal("rst", PinsN("AB14", dir="o")),
                 Subsignal("clk", Pins("AD18", dir="i")),
                 Subsignal("d", Pins("AE14 AE15 AC15 AC16 "
                                     "AB15 AA15 AD14 AC14", dir="io")),
                 Subsignal("dir", Pins("Y16", dir="i")),
                 Subsignal("stp", Pins("AA17", dir="o")),
                 Subsignal("nxt", Pins("AA16", dir="i")),
                 Attrs(IOSTANDARD="LVCMOS18")),
        Resource("vusb_oc", 0,
                 PinsN("AF16", dir="i"), Attrs(IOSTANDARD="LVCMOS18")),
        Resource("eth_rgmii", 0,
                 Subsignal("rst", PinsN("AH24", dir="o"),
                           Attrs(IOSTANDARD="LVCMOS33")),
                 Subsignal("mdc", Pins("AF12", dir="o")),
                 Subsignal("mdio", Pins("AG12", dir="io")),
                 Subsignal("tx_clk", Pins("AE10", dir="o")),
                 Subsignal("tx_ctl", Pins("AK14", dir="o")),
                 Subsignal("tx_data", Pins("AJ12 AK11 AJ11 AK10", dir="o")),
                 Subsignal("rx_clk", Pins("AG10", dir="i")),
                 Subsignal("rx_ctl", Pins("AH11", dir="i")),
                 Subsignal("rx_data", Pins("AJ14 AH14 AK13 AJ13", dir="i")),
                 Attrs(IOSTANDARD="LVCMOS15"))]

    connectors = [
        Connector("pmod", 0,  # JA
                  "U27 U28 T26 T27 - - "
                  "T22 T23 T20 T21 - -"),
        Connector("pmod", 1,  # JB
                  "V29 V30 V25 W26 - - "
                  "T25 U25 U22 U23 - -"),
        Connector("pmod", 2,  # JC
                  "AC26 AJ27 AH30 AK29 - - "
                  "AD26 AG30 AK30 AK28 - -"),
        Connector("pmod", 3,  # JD
                  "V27 Y30 V24 W22 - - "
                  "U24 Y26 V22 W21 - -"),
        Connector("pmod", 4,  # JXADC
                  "J23 K23 L22 L21 - - "
                  "J24 K24 L23 K21 - -"),
        Connector("hpc", 0,
                  {"dp1_m2c_p": "Y6",
                   "dp1_m2c_n": "Y5",
                   "dp2_m2c_p": "W4",
                   "dp2_m2c_n": "W3",
                   "dp3_m2c_p": "V6",
                   "dp3_m2c_n": "V5",
                   "dp1_c2m_p": "V2",
                   "dp1_c2m_n": "V1",
                   "dp2_c2m_p": "U4",
                   "dp2_c2m_n": "U3",
                   "dp3_c2m_p": "T2",
                   "dp3_c2m_n": "T1",
                   "dp0_c2m_p": "Y2",
                   "dp0_c2m_n": "Y1",
                   "dp0_m2c_p": "AA4",
                   "dp0_m2c_n": "AA3",
                   "la06_p": "D29",
                   "la06_n": "C30",
                   "la10_p": "B27",
                   "la10_n": "A27",
                   "la14_p": "C24",
                   "la14_n": "B24",
                   "la18_cc_p": "D17",
                   "la18_cc_n": "D18",
                   "la27_p": "A20",
                   "la27_n": "A21",
                   "ha01_cc_p": "M28",
                   "ha01_cc_n": "L28",
                   "ha05_p": "J29",
                   "ha05_n": "H29",
                   "ha09_p": "L30",
                   "ha09_n": "K30",
                   "ha13_p": "K26",
                   "ha13_n": "J26",
                   "ha16_p": "M22",
                   "ha16_n": "M23",
                   "ha20_p": "G27",
                   "ha20_n": "F27",
                   "clk1_m2c_p": "E28",
                   "clk1_m2c_n": "D28",
                   "la00_cc_p": "D27",
                   "la00_cc_n": "C27",
                   "la03_p": "E29",
                   "la03_n": "E30",
                   "la08_p": "C29",
                   "la08_n": "B29",
                   "la12_p": "F26",
                   "la12_n": "E26",
                   "la16_p": "E23",
                   "la16_n": "D23",
                   "la20_p": "G22",
                   "la20_n": "F22",
                   "la22_p": "J17",
                   "la22_n": "H17",
                   "la25_p": "D22",
                   "la25_n": "C22",
                   "la29_p": "B18",
                   "la29_n": "A18",
                   "la31_p": "C17",
                   "la31_n": "B17",
                   "la33_p": "D16",
                   "la33_n": "C16",
                   "ha03_p": "N25",
                   "ha03_n": "N26",
                   "ha07_p": "M29",
                   "ha07_n": "M30",
                   "ha11_p": "P23",
                   "ha11_n": "N24",
                   "ha14_p": "N27",
                   "ha14_n": "M27",
                   "ha18_p": "E19",
                   "ha18_n": "D19",
                   "ha22_p": "D21",
                   "ha22_n": "C21",
                   "gbtclk1_m2c_p": "N8",
                   "gbtclk1_m2c_n": "N7",
                   "gbtclk0_m2c_p": "L8",
                   "gbtclk0_m2c_n": "L7",
                   "la01_cc_p": "D26",
                   "la01_cc_n": "C26",
                   "la05_p": "B30",
                   "la05_n": "A30",
                   "la09_p": "B28",
                   "la09_n": "A28",
                   "la13_p": "E24",
                   "la13_n": "D24",
                   "la17_cc_p": "F21",
                   "la17_cc_n": "E21",
                   "la23_p": "G17",
                   "la23_n": "F17",
                   "la26_p": "B22",
                   "la26_n": "A22",
                   "pg_m2c": "AH21",
                   "ha00_cc_p": "K28",
                   "ha00_cc_n": "K29",
                   "ha04_p": "M24",
                   "ha04_n": "M25",
                   "ha08_p": "J27",
                   "ha08_n": "J28",
                   "ha12_p": "L26",
                   "ha12_n": "L27",
                   "ha15_p": "J21",
                   "ha15_n": "J22",
                   "ha19_p": "G29",
                   "ha19_n": "F30",
                   "prsnt_m2c_b": "AA21",
                   "clk0_m2c_p": "F20",
                   "clk0_m2c_n": "E20",
                   "la02_p": "H30",
                   "la02_n": "G30",
                   "la04_p": "H26",
                   "la04_n": "H27",
                   "la07_p": "F25",
                   "la07_n": "E25",
                   "la11_p": "A25",
                   "la11_n": "A26",
                   "la15_p": "B23",
                   "la15_n": "A23",
                   "la19_p": "H21",
                   "la19_n": "H22",
                   "la21_p": "L17",
                   "la21_n": "L18",
                   "la24_p": "H20",
                   "la24_n": "G20",
                   "la28_p": "J19",
                   "la28_n": "H19",
                   "la30_p": "A16",
                   "la30_n": "A17",
                   "la32_p": "K18",
                   "la32_n": "J18",
                   "ha02_p": "P21",
                   "ha02_n": "P22",
                   "ha06_p": "N29",
                   "ha06_n": "N30",
                   "ha10_p": "N21",
                   "ha10_n": "N22",
                   "ha17_cc_p": "C25",
                   "ha17_cc_n": "B25",
                   "ha21_p": "G28",
                   "ha21_n": "F28",
                   "ha23_p": "G18",
                   "ha23_n": "F18"})]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_after_read": "auto_detect_xpm",
            "script_before_bitstream":
            "set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]",
            "add_constraints": """
            set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]
            set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
            set_property BITSTREAM.CONFIG.SPI_32BIT_ADDR YES [current_design]
            set_property BITSTREAM.CONFIG.SPI_FALL_EDGE YES [current_design]
            set_property CFGBVS VCCO [current_design]
            set_property CONFIG_VOLTAGE 3.3 [current_design]
            """}
        return super().toolchain_prepare(
            fragment, name, **overrides, **kwargs)

    @property
    def file_templates(self):
        return {
            **super().file_templates,
            "{{name}}-openocd.cfg": r"""
            source [find interface/ftdi/digilent-hs1.cfg]
            # fix channel
            ftdi_channel 1
            adapter_khz 25000
            transport select jtag
            source [find cpld/xilinx-xc7.cfg]
            source [find cpld/jtagspi.cfg]
            """
        }

    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}-openocd.cfg".format(name),
                              "{}.bit".format(name)) as (
                                  config_filename, bitstream_filename):
            subprocess.check_call([
                openocd,
                "-f", config_filename,
                "-c", "init; pld load 0 {}; exit".format(bitstream_filename)])


if __name__ == "__main__":
    from .test.blinky import Blinky
    Genesys2Platform().build(Blinky(), do_program=True)
