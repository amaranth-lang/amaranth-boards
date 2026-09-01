import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["DE2_115Platform"]


class DE2_115Platform(IntelPlatform):

    device = "EP4CE115"
    package = "F29"
    speed = "C7"
    default_clk = "clk50"

    resources = [
        Resource("clk50", 0, Pins("Y2", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("AG14", dir="i"), 
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("AG15", dir="i"), 
            Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        # 
        # SMA Clock In/Out
        #

        Resource("sma_clkin", 0, Pins("AH14", dir="i"),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("sma_clkout", 0, Pins("AE23", dir="o"),
            Attrs(io_standard="3.3-V LVTTL")),

        #
        # LEDs, Buttons, Switches
        #

        # Alias all of the LEDs
        *LEDResources(pins="G19 F19 E19 F21 F18 E18 J19 H19 J17 G17 J15 H16 J16 H17 F15 G15 G16 H15 E21 E22 E25 E24 H21 G20 G22 G21 F17",
            attrs=Attrs(io_standard="2.5 V")),

        Resource("led_r", 0, Pins("G19 F19 E19 F21 F18 E18 J19 H19 J17 G17 J15 H16 J16 H17 F15 G15 G16 H15", dir="o"), Attrs(io_standard="2.5 V")),
        Resource("led_g", 0, Pins("E21 E22 E25 E24 H21 G20 G22 G21 F17", dir="o"), Attrs(io_standard="2.5 V")),

        *ButtonResources(
            pins="M23 M21 N21 R24", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        *SwitchResources(
            pins="AB28 AC28 AC27 AD27 AB27 AC26 AD26 AB26 AC25 AB25 AC24 AB24 AB23 AA24 AA23 AA22 Y24 Y23",
            attrs=Attrs(io_standard="2.5 V")),

        #
        # 7-Seg
        #

        Display7SegResource(0,
            a="G18", b="F22", c="E17", d="L26", e="L25", f="J22", g="H22", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        Display7SegResource(1,
            a="M24", b="Y22", c="W21", d="W22", e="W25", f="U23", g="U24", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        Display7SegResource(2,
            a="AA25", b="AA26", c="Y25", d="W26", e="Y26", f="W27", g="W28", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        Display7SegResource(3,
            a="V21", b="U21", c="AB20", d="AA21", e="AD24", f="AF23", g="Y19", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        Display7SegResource(4,
            a="AB19", b="AA19", c="AG21", d="AH21", e="AE19", f="AF19", g="AE18", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        Display7SegResource(5,
            a="AD18", b="AC18", c="AB18", d="AH19", e="AG19", f="AF18", g="AH18", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        Display7SegResource(6,
            a="AA17", b="AB16", c="AA16", d="AB17", e="AB15", f="AA15", g="AC17", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        Display7SegResource(7,
            a="AD17", b="AE17", c="AG17", d="AH17", e="AF17", f="AG18", g="AA14", invert=True,
            attrs=Attrs(io_standard="2.5 V")),

        #
        # LCD
        #

        Resource("lcd_hd44780", 0,
            Subsignal("data", Pins("L3 L1 L2 K7 K1 K2 M3 M5", dir="io")),
            Subsignal("blon", Pins("L6", dir="o")),
            Subsignal("rw",   Pins("M1", dir="o")),
            Subsignal("en",   Pins("L4", dir="o")),
            Subsignal("rs",   Pins("M2", dir="o")),
            Subsignal("on",   Pins("L5", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        #
        # RS232
        #

        UARTResource(0,
            rx="G12", tx="G9", rts="G14", cts="J13", role="dte",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        #
        # PS/2
        #

        PS2Resource(0, clk="G6", dat="H5",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        PS2Resource(1, clk="G5", dat="F5",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        #
        # SD Card
        #

        *SDCardResources(0,
            clk="AE13", cmd="AD14", dat0="AE14", dat1="AF13", dat2="AB14", dat3="AC14", wp_n="AF14",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        #
        # VGA (Analog Devices ADV7123 DAC)
        #

        Resource("vga", 0,
            Subsignal("r", Pins("E12 E11 D10 F12 G10 J12 H8 H10", dir="o")),    # Goes to DAC chip
            Subsignal("g", Pins("G8 G11 F8 H12 C8 B8 F10 C9", dir="o")),        # Goes to DAC chip
            Subsignal("b", Pins("B10 A10 C11 B11 A11 C12 D11 D12", dir="o")),   # Goes to DAC chip
            Subsignal("blank", PinsN("F11", dir="o")),                          # Goes to DAC chip
            Subsignal("clk", Pins("A12", dir="o")),                             # Goes to DAC chip
            Subsignal("sync", PinsN("C10", dir="o")),                          # Goes to DAC chip
            Subsignal("hs", Pins("G13", dir="o")),                              # Direct D-Sub connection
            Subsignal("vs", Pins("C13", dir="o")),                              # Direct D-Sub connection
            Attrs(io_standard="3.3-V LVTTL")),

        #
        # Audio (Wolfson WM8731)
        #

        Resource("audio", 0,
            Subsignal("adc_dat",   Pins("D2", dir="i")),
            Subsignal("adc_lrclk", Pins("C2", dir="io")),
            Subsignal("dac_dat",   Pins("D1", dir="o")),
            Subsignal("dac_lrclk", Pins("E3", dir="io")),
            Subsignal("bclk",      Pins("F2", dir="io")), # Bitstream clock
            Subsignal("xck",       Pins("E1", dir="o")),  # Chip clock
            Attrs(io_standard="3.3-V LVTTL")),

        #
        # I2C
        #

        # EEPROM
        I2CResource(0, scl="D14", sda="E14",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        # Audio CODEC, TV Decoder, HSMC Connector
        I2CResource(1, scl="B7", sda="A8",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        #
        # Ethernet 0/1 (2x Marvell 88E1111)
        #
        # JP1 1-2 = ENET0 RGMII (default)
        # JP1 2-3 = ENET0 MII
        #
        # JP2 1-2 = ENET1 RGMII (default)
        # JP2 2-3 = ENET1 MII
        #

        Resource("enet_clk25", 0, Pins("A14", dir="i"), Clock(25e6),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("enet_link100_leds", 0, Pins("C14 D13"),
            Attrs(io_standard="3.3-V LVTTL")),

        Resource("enet", 0,
            Subsignal("tx_data", Pins("C18 D19 A19 B19", dir="o")),
            Subsignal("rx_data", Pins("C16 D16 D17 C15", dir="i")),
            Subsignal("gtx_clk", Pins("A17", dir="o")),
            Subsignal("tx_en",   Pins("A18", dir="o")),
            Subsignal("tx_er",   Pins("B18", dir="o")),
            Subsignal("int",     PinsN("A21", dir="i")),
            Subsignal("rst",     PinsN("C19", dir="o")),
            Subsignal("rx_dv",   Pins("C17", dir="i")),
            Subsignal("rx_er",   Pins("D18", dir="i")),
            Subsignal("rx_crs",  Pins("D15", dir="i")),
            Subsignal("rx_col",  Pins("E15", dir="i")),
            Subsignal("rx_clk",  Pins("A15", dir="i")),
            Subsignal("tx_clk",  Pins("B17", dir="i")),
            Subsignal("mdc",     Pins("C20", dir="o")),
            Subsignal("mdio",    Pins("B21", dir="io")),
            Attrs(io_standard="2.5 V")),

        Resource("enet", 1,
            Subsignal("tx_data", Pins("C25 A26 B26 C26", dir="o")),
            Subsignal("rx_data", Pins("B23 C21 A23 D21", dir="i")),
            Subsignal("gtx_clk", Pins("C23", dir="o")),
            Subsignal("tx_en",   Pins("B25", dir="o")),
            Subsignal("tx_er",   Pins("A25", dir="o")),
            Subsignal("int",     PinsN("D24", dir="i")),
            Subsignal("rst",     PinsN("D22", dir="o")),
            Subsignal("rx_dv",   Pins("A22", dir="i")),
            Subsignal("rx_er",   Pins("C24", dir="i")),
            Subsignal("rx_crs",  Pins("D20", dir="i")),
            Subsignal("rx_col",  Pins("B22", dir="i")),
            Subsignal("rx_clk",  Pins("B15", dir="i")),
            Subsignal("tx_clk",  Pins("C22", dir="i")),
            Subsignal("mdc",     Pins("D23", dir="o")),
            Subsignal("mdio",    Pins("D25", dir="io")),
            Attrs(io_standard="2.5 V")),

        #
        # TV Decoder (Analog Devices ADV7180)
        #

        Resource("tv", 0,
            Subsignal("hs",    Pins("E5", dir="i")),
            Subsignal("vs",    Pins("E4", dir="i")),
            Subsignal("rst",   PinsN("G7", dir="o")),
            Subsignal("clk27", Pins("B14", dir="i")),
            Subsignal("data",  Pins("E8 A7 D8 C7 D7 D6 E7 F7", dir="i")),
            Attrs(io_standard="3.3-V LVTTL")),

        #
        # USB
        #

        # NOTE!
        # There are two revs of this board:
        #  - NXP SI1362
        #  - Cypress CY7C67200

        # Only available on older revs
        Resource("usb_si1362", 0,
            Subsignal("addr",   Pins("H7 C3", dir="o")),
            Subsignal("cs",     PinsN("A3", dir="o")),
            Subsignal("dack",   PinsN("C4 D4", dir="o")),
            Subsignal("data",   Pins("J6 K4 J5 K3 J4 J3 J7 H6 H3 H4 G1 G2 G3 F1 F3 G4", dir="io")),
            Subsignal("dreq",   Pins("J1 B4", dir="i")),
            Subsignal("fspeed", Pins("C6", dir="io")),
            Subsignal("int",    Pins("A6 D5", dir="i")),
            Subsignal("lspeed", Pins("B6", dir="io")),
            Subsignal("rd",     PinsN("B3", dir="o")),
            Subsignal("rst",    PinsN("C5", dir="o")),
            Subsignal("we",     PinsN("A4", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        # Only available on newer revs
        Resource("usb_cy7c67200", 0,
            Subsignal("addr",   Pins("H7 C3", dir="o")),
            Subsignal("cs",     PinsN("A3", dir="o")),
            Subsignal("data",   Pins("J6 K4 J5 K3 J4 J3 J7 H6 H3 H4 G1 G2 G3 F1 F3 G4", dir="io")),
            Subsignal("int",    Pins("D5", dir="i")),
            Subsignal("rd",     PinsN("B3", dir="o")),
            Subsignal("rst",    PinsN("C5", dir="o")),
            Subsignal("we",     PinsN("A4", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

        #
        # IrDA
        #

        Resource("irda_rx", 0, Pins("Y15", dir="i"),
            Attrs(io_standard="3.3-V LVTTL")),

        #
        # SDRAM
        #

        SDRAMResource(0,
            clk="AE5", cke="AA6", cs_n="T4", we_n="V6", ras_n="U6", cas_n="V7",
            ba="U7 R4", a="R6 V8 U8 P1 V5 W8 W7 AA7 Y5 Y6 R5 AA5 Y7",
            dq="W3 W2 V4 W1 V3 V2 V1 U3 Y3 Y4 AB1 AA3 AB2 AC1 AB3 AC2 M8 L8 P2 N3 N4 M4 M7 L7 U5 R7 R1 R2 R3 T3 U4 U1",
            dqm="U2 W4 K8 N8", attrs=Attrs(io_standard="3.3-V LVTTL")),

        #
        # SRAM 
        #

        SRAMResource(0,
            cs_n="AF8", oe_n="AD5", we_n="AE8", dm_n="AD4 AC4",
            a="AB7 AD7 AE7 AC7 AB6 AE6 AB5 AC5 AF5 T7 AF2 AD3 AB4 AC3 AA4 AB11 AC11 AB9 AB8 T8",
            d="AH3 AF4 AG4 AH4 AF6 AG6 AH6 AF7 AD1 AD2 AE2 AE1 AE3 AE4 AF3 AG3",
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        #
        # Flash
        #

        # Not using NORFlashResource due to different signal wires (rst not inverted, etc)
        Resource("flash", 0,
            Subsignal("addr", Pins("AG12 AH7 Y13 Y14 Y12 AA13 AA12 AB13 AB12 AB10 AE9 AF9 AA10 AD8 AC8 Y10 AA8 AH12 AC12 AD12 AE10 AD10 AD11", dir="o")),
            Subsignal("dq",   Pins("AH8 AF10 AG10 AH10 AF11 AG11 AH11 AF12", dir="io")),
            Subsignal("ce",   PinsN("AG7", dir="o")),
            Subsignal("oe",   PinsN("AG8", dir="o")),
            Subsignal("rst",  PinsN("AE11", dir="o")),
            Subsignal("ry",   Pins("Y1", dir="i")),
            Subsignal("we",   PinsN("AC10", dir="o")),
            Subsignal("wp",   PinsN("AE12", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")),

    ]

    connectors = [

        #
        # EX_IO
        #

        # Comments indicate Terasic's original connector pin assignments
        # Pin 1 (D9/EX_IO[6]) is pulled to ground
        # Pins 3/5/7/9/13 are pulled to 3v3
        Connector("ex_io", 0,
            "D9  - " # EX_IO[6] GND
            "E10 - " # EX_IO[5] GND
            "F14 - " # EX_IO[4] GND
            "H14 - " # EX_IO[3] GND
            "H13 - " # EX_IO[2] GND
            "J14 - " # EX_IO[1] GND
            "J10 - " # EX_IO[0] 3v3
        ),

        #
        # GPIO
        #

        Connector("gpio", 0,
            "AB22 AC15 "
            "AB21 Y17  "
            "AC21 Y16  "
            "AD21 AE16 "
            "AD15 AE15 "
            "-    -    " # 5v0 GND
            "AC19 AF16 "
            "AD19 AF15 "
            "AF24 AE21 "
            "AF25 AC22 "
            "AE22 AF21 "
            "AF22 AD22 "
            "AG25 AD25 "
            "AH25 AE25 "
            "-    -    " # 3v3 GND
            "AG22 AE24 "
            "AH22 AF26 "
            "AE20 AG23 "
            "AF20 AH26 "
            "AH23 AG26 "
        ),

        #
        # HSMC
        #

        # Definitions as plain FPGA pins
        Connector("hsmc", 0,
            "-     -    "
            "-     -    "

            "-     -    "
            "-     -    "

            "-     -    "
            "-     -    "

            "-     -    "
            "-     -    "

            "-     -    "
            "-     -    "

            "-     -    "
            "-     -    "

            "-     -    "
            "-     -    "

            "-     -    "
            "-     -    "

            "-     -    " # HSMC_SDA       HSMC_SCL      (request I2C 1 if you need these pins)
            "-     -    " # HSMC_TCK       HSMC_TMS

            "-     -    " # HSMC_TDO       HSMC_TDI
            "AD28  AH15 " # HSMC_CLKOUT0   HSMC_CLKIN0

            # Gap

            "AE26  AE28 " # HSMC_D0        HSMC_D1
            "AE27  AF27 " # HSMC_D2        HSMC_D3
            "-     -    " # 3v3            12v
            "D27   F24  " # HSMC_TX_D_P0   HSMC_RX_D_P0
            "D28   F25  " # HSMC_TX_D_N0   HSMC_RX_D_N0
            "-     -    " # 3v3            12v
            "E27   D26  " # HSMC_TX_D_P1   HSMC_RX_D_P1
            "E28   C27  " # HSMC_TX_D_N1   HSMC_RX_D_N1
            "-     -    " # 3v3            12v
            "F27   F26  " # HSMC_TX_D_P2   HSMC_RX_D_P2
            "F28   E26  " # HSMC_TX_D_N2   HSMC_RX_D_N2
            "-     -    " # 3v3            12v
            "G27   G25  " # HSMC_TX_D_P3   HSMC_RX_D_P3
            "G28   G26  " # HSMC_TX_D_N3   HSMC_RX_D_N3
            "-     -    " # 3v3            12v
            "K27   H25  " # HSMC_TX_D_P4   HSMC_RX_D_P4
            "K28   H26  " # HSMC_TX_D_N4   HSMC_RX_D_N4
            "-     -    " # 3v3            12v
            "M27   K25  " # HSMC_TX_D_P5   HSMC_RX_D_P5
            "M28   K26  " # HSMC_TX_D_N5   HSMC_RX_D_N5
            "-     -    " # 3v3            12v
            "K21   L23  " # HSMC_TX_D_P6   HSMC_RX_D_P6
            "K22   L24  " # HSMC_TX_D_N6   HSMC_RX_D_N6
            "-     -    " # 3v3            12v
            "H23   M25  " # HSMC_TX_D_P7   HSMC_RX_D_P7
            "H24   M26  " # HSMC_TX_D_N7   HSMC_RX_D_N7
            "-     -    " # 3v3            12v
            "G23   J27  " # HSMC_CLKOUT_P1 HSMC_CLKIN_P1
            "G24   J28  " # HSMC_CLKOUT_N1 HSMC_CLKIN_N1
            "-     -    " # 3v3            12v

            # Gap

            "J23   R25  " # HSMC_TX_D_P8   HSMC_RX_D_P8
            "J24   R26  " # HSMC_TX_D_N8   HSMC_RX_D_N8
            "-     -    " # 3v3            12v
            "P27   T25  " # HSMC_TX_D_P9   HSMC_RX_D_P9
            "P28   T26  " # HSMC_TX_D_N9   HSMC_RX_D_N9
            "-     -    " # 3v3            12v
            "J25   U25  " # HSMC_TX_D_P10  HSMC_RX_D_P10
            "J26   U26  " # HSMC_TX_D_N10  HSMC_RX_D_N10
            "-     -    " # 3v3            12v
            "L27   L21  " # HSMC_TX_D_P11  HSMC_RX_D_P11
            "L28   L22  " # HSMC_TX_D_N11  HSMC_RX_D_N11
            "-     -    " # 3v3            12v
            "V25   N25  " # HSMC_TX_D_P12  HSMC_RX_D_P12
            "V26   N26  " # HSMC_TX_D_N12  HSMC_RX_D_N12
            "-     -    " # 3v3            12v
            "R27   P25  " # HSMC_TX_D_P13  HSMC_RX_D_P13
            "R28   P26  " # HSMC_TX_D_N13  HSMC_RX_D_N13
            "-     -    " # 3v3            12v
            "U27   P21  " # HSMC_TX_D_P14  HSMC_RX_D_P14
            "U28   R21  " # HSMC_TX_D_N14  HSMC_RX_D_N14
            "-     -    " # 3v3            12v
            "V27   R22  " # HSMC_TX_D_P15  HSMC_RX_D_P15
            "V28   R23  " # HSMC_TX_D_N15  HSMC_RX_D_N15
            "-     -    " # 3v3            12v
            "U22   T21  " # HSMC_TX_D_P16  HSMC_RX_D_P16
            "V22   T22  " # HSMC_TX_D_N16  HSMC_RX_D_N16
            "-     -    " # 3v3            12v
            "V23   Y27  " # HSMC_CLKOUT_P2 HSMC_CLKIN_P2
            "V24   Y28  " # HSMC_CLKOUT_N2 HSMC_CLKIN_N2
            "-     -    " # 3v3            HSMC_PSNT_n
        ),

        # Definitions as HSMC LVDS pins
        Connector("hsmc_lvds", 0, {

            # TX differential pairs
            "HSMC_TX_D_P0":     "D27",
            "HSMC_TX_D_N0":     "D28",
            "HSMC_TX_D_P1":     "E27",
            "HSMC_TX_D_N1":     "E28",
            "HSMC_TX_D_P2":     "F27",
            "HSMC_TX_D_N2":     "F28",
            "HSMC_TX_D_P3":     "G27",
            "HSMC_TX_D_N3":     "G28",
            "HSMC_TX_D_P4":     "K27",
            "HSMC_TX_D_N4":     "K28",
            "HSMC_TX_D_P5":     "M27",
            "HSMC_TX_D_N5":     "M28",
            "HSMC_TX_D_P6":     "K21",
            "HSMC_TX_D_N6":     "K22",
            "HSMC_TX_D_P7":     "H23",
            "HSMC_TX_D_N7":     "H24",
            "HSMC_TX_D_P8":     "J23",
            "HSMC_TX_D_N8":     "J24",
            "HSMC_TX_D_P9":     "P27",
            "HSMC_TX_D_N9":     "P28",
            "HSMC_TX_D_P10":    "J25",
            "HSMC_TX_D_N10":    "J26",
            "HSMC_TX_D_P11":    "L27",
            "HSMC_TX_D_N11":    "L28",
            "HSMC_TX_D_P12":    "V25",
            "HSMC_TX_D_N12":    "V26",
            "HSMC_TX_D_P13":    "R27",
            "HSMC_TX_D_N13":    "R28",
            "HSMC_TX_D_P14":    "U27",
            "HSMC_TX_D_N14":    "U28",
            "HSMC_TX_D_P15":    "V27",
            "HSMC_TX_D_N15":    "V28",
            "HSMC_TX_D_P16":    "U22",
            "HSMC_TX_D_N16":    "V22",

            # RX differential pairs
            "HSMC_RX_D_P0":     "F24",
            "HSMC_RX_D_N0":     "F25",
            "HSMC_RX_D_P1":     "D26",
            "HSMC_RX_D_N1":     "C27",
            "HSMC_RX_D_P2":     "F26",
            "HSMC_RX_D_N2":     "E26",
            "HSMC_RX_D_P3":     "G25",
            "HSMC_RX_D_N3":     "G26",
            "HSMC_RX_D_P4":     "H25",
            "HSMC_RX_D_N4":     "H26",
            "HSMC_RX_D_P5":     "K25",
            "HSMC_RX_D_N5":     "K26",
            "HSMC_RX_D_P6":     "L23",
            "HSMC_RX_D_N6":     "L24",
            "HSMC_RX_D_P7":     "M25",
            "HSMC_RX_D_N7":     "M26",
            "HSMC_RX_D_P8":     "R25",
            "HSMC_RX_D_N8":     "R26",
            "HSMC_RX_D_P9":     "T25",
            "HSMC_RX_D_N9":     "T26",
            "HSMC_RX_D_P10":    "U25",
            "HSMC_RX_D_N10":    "U26",
            "HSMC_RX_D_P11":    "L21",
            "HSMC_RX_D_N11":    "L22",
            "HSMC_RX_D_P12":    "N25",
            "HSMC_RX_D_N12":    "N26",
            "HSMC_RX_D_P13":    "P25",
            "HSMC_RX_D_N13":    "P26",
            "HSMC_RX_D_P14":    "P21",
            "HSMC_RX_D_N14":    "R21",
            "HSMC_RX_D_P15":    "R22",
            "HSMC_RX_D_N15":    "R23",
            "HSMC_RX_D_P16":    "T21",
            "HSMC_RX_D_N16":    "T22",

            # Clock signals
            "HSMC_CLKOUT0":     "AD28",
            "HSMC_CLKIN0":      "AH15",
            "HSMC_CLKOUT_P1":   "G23",
            "HSMC_CLKOUT_N1":   "G24",
            "HSMC_CLKIN_P1":    "J27",
            "HSMC_CLKIN_N1":    "J28",
            "HSMC_CLKOUT_P2":   "V23",
            "HSMC_CLKOUT_N2":   "V24",
            "HSMC_CLKIN_P2":    "Y27",
            "HSMC_CLKIN_N2":    "Y28",

            # Single-ended data
            "HSMC_D0":          "AE26",
            "HSMC_D1":          "AE28",
            "HSMC_D2":          "AE27",
            "HSMC_D3":          "AF27",
        }),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import Blinky
    plat = DE2_115Platform()
    plat.build(Blinky(), do_program=True)
