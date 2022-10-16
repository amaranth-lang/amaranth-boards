import os
import subprocess
import textwrap

from amaranth.build import *
from amaranth.vendor.xilinx import XilinxPlatform
from .resources import *

__all__ = ["DigilentSpartan3ePlatform"]

class DigilentSpartan3ePlatform(XilinxPlatform):
    """Platform file for Digilent Spartan 3E board.
    Product URL: https://digilent.com/reference/programmable-logic/spartan-3e/start
    User Guide:  https://digilent.com/reference/_media/reference/programmable-logic/spartan-3e/s3estarter_ug.pdf"""

    device =  "xc3s500e"
    package = "fg320"
    speed = "4"

    default_clk = "clk50"

    resources = [

        # ==== Clock inputs (CLK) ==== (Pg. 21 in User Guide)
        Resource("clk50",   0, Pins("C9" , dir="i"), Attrs(IOSTANDARD="LVCMOS33"), Clock(50e6)),
        Resource("clk_aux", 0, Pins("B8" , dir="i"), Attrs(IOSTANDARD="LVCMOS33")), 
        Resource("clk_sma", 0, Pins("A10", dir="i"), Attrs(IOSTANDARD="LVCMOS33")), 

        # ==== Pushbuttons (BTN) ==== (Pg. 16,17 in User Guide)
        *ButtonResources(pins="H13 V4 K17 D18 V16",
            attrs=Attrs(IOSTANDARD="LVTTL", PULLDOWN=True)),
        
        # ==== Discrete LEDs (LED) ==== (Pg. 19 in User Guide)
        *LEDResources(pins="F12 E12 E11 F11 C11 D11 E9 F9",
            attrs=Attrs(IOSTANDARD="LVTTL", SLEW="SLOW", DRIVE="8")),
        
        # ==== Slide Switches (SW) ==== (Pg. 15 in User Guide)
        *SwitchResources(pins="L13 L14 H18 N17",
            attrs=Attrs(IOSTANDARD="LVTTL", PULLUP=True)),
        
        # ==== PS/2 Mouse/Keyboard Port (PS2) ==== (Pg. 62 in User Guide)
        PS2Resource(0,
            clk="G14",
            dat="G13",
            attrs=Attrs(IOSTANDARD="LVCMOS33", DRIVE="8", SLEW="SLOW")),

        # ==== RS-232 Serial Ports (RS232) ==== (Pg. 59 in User Guide)
        UARTResource(0,
            rx="R7",
            tx="M14",
            attrs=Attrs(IOSTANDARD="LVTTL")),

        UARTResource(1,
            rx="U8",
            tx="M13",
            attrs=Attrs(IOSTANDARD="LVTTL")),
        
        # ==== Analog-to-Digital Converter (ADC) ==== (Pg. 74 in User Guide)
        SPIResource("adc", 0,
            role="peripheral",
            cs_n="P11", #AD_CONV
            clk="U16",  #SPI_SCK
            copi=None,
            cipo="N10", #SPI_MISO
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # ==== Programmable Gain Amplifier (AMP) ==== (Pg. 74 in User Guide)
        SPIResource("amp", 0,
            role="peripheral",
            cs_n="N7",  #AMP_CS
            clk="U16",  #SPI_SCK
            copi="T4",  #SPI_MOSI
            cipo="E18", #AMP_DOUT
            reset="P7", #AMP_SHDN
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # ==== Digital-to-Analog Converter (DAC) ==== (Pg. 67 in User Guide)
        SPIResource("dac", 0,
            role="peripheral",
            cs_n="N8",  #DAC_CS
            clk="U16",  #SPI_SCK
            copi="T4",  #SPI_MOSI
            cipo="N10", #SPI_MISO
            reset="P8", #DAC_CLR
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # ==== STMicro SPI serial Flash (SPI) ==== (Pg. 89 in User Guide)
        SPIResource("spi_flash", 0,
            role="peripheral",
            cs_n="U3",  #SPI_SS_B
            clk="U16",  #SPI_SCK
            copi="T4",  #SPI_MOSI
            cipo="N10", #SPI_MISO
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # ==== VGA Port (VGA) ==== (Pg. 54 in User Guide)
        VGAResource(0,
            r="H14",
            g="H15",
            b="G15",
            vs="F14",
            hs="F15",
            attrs=Attrs(IOSTANDARD="LVTTL", DRIVE="8", SLEW="FAST")),

        # ==== 1-Wire Secure EEPROM (DS) ==== (Pg. 127 in User Guide)
        Resource("ds_wire", 0, Pins("U4"), Attrs(IOSTANDARD="LVTTL", SLEW="SLOW", DRIVE="8")), 

        # ==== Ethernet PHY (E) ==== (Pg. 110 in User Guide)
        Resource("ethernet", 0,
            Subsignal("col",    Pins("U6")), 
            Subsignal("crs",    Pins("U13")), 
            Subsignal("mdc",    Pins("P9"), Attrs(SLEW="SLOW", DRIVE="8")),
            Subsignal("mdio",   Pins("U5"), Attrs(SLEW="SLOW", DRIVE="8")), 
            Subsignal("rx_clk", Pins("V3")), 
            Subsignal("rx_dv",  Pins("V2")), 
            Subsignal("rxd",    Pins("V8 T11 U11 V14 U14")),
            Subsignal("tx_clk", Pins("T7")), 
            Subsignal("tx_en",  Pins("P15"), Attrs(SLEW="SLOW", DRIVE="8")), 
            Subsignal("txd",    Pins("R11 T15 R5 T5 R6"), Attrs(SLEW="SLOW", DRIVE="8")),
            Attrs(IOSTANDARD="LVCMOS33")),
            
        # ==== FPGA Configuration Mode, INIT_B Pins (FPGA) ==== (Pg. 26 in User Guide)
        Resource("fpga", 0,
            Subsignal("m0",     Pins("M10"), Attrs(SLEW="SLOW", DRIVE="8")),
            Subsignal("m1",     Pins("V11"), Attrs(SLEW="SLOW", DRIVE="8")),
            Subsignal("m2",     Pins("T10"), Attrs(SLEW="SLOW", DRIVE="8")),
            Subsignal("init_b", Pins("T3"),  Attrs(SLEW="SLOW", DRIVE="4")),
            Subsignal("rdwr_b", Pins("U10"), Attrs(SLEW="SLOW", DRIVE="4")),
            Subsignal("hswap",  Pins("B3")),
            Attrs(IOSTANDARD="LVCMOS33")), 

        # ==== Character LCD (LCD) ==== (Pg. 41 in User Guide)
        Resource("lcd", 0,
            Subsignal("e",  Pins("M18")), 
            Subsignal("rs", Pins("L18")), 
            Subsignal("rw", Pins("L17")), 
            Subsignal("d",  Pins("R15 R16 P17 M15")),
            Attrs(IOSTANDARD="LVCMOS33", DRIVE="4", SLEW="SLOW")),

        # ==== Rotary Pushbutton Switch (ROT) ==== (Pg. 17 in User Guide)
        Resource("rotary_encoder", 0,
            Subsignal("a", Pins("K18", dir="i")), 
            Subsignal("b", Pins("G18", dir="i")),
            Attrs(IOSTANDARD="LVTTL", PULLUP=True)),

        # ==== DDR SDRAM (SD) ==== (I/O Bank 3, VCCO=2.5V) (Pg. 104 in User Guide)
        Resource("ddr", 0,
            Subsignal("a",      Pins("T1 R3 R2 P1 F4 H4 H3 H1 H2 N4 T2 N5 P2")), 
            Subsignal("ba",     Pins("K5 K6")),
            Subsignal("cas",    Pins("C2")), 
            Subsignal("clk",    DiffPairs("J4", "J5")),
            Subsignal("clk_en", Pins("K3")), 
            Subsignal("cs",     Pins("K4")), 
            Subsignal("dq",     Pins("L2 L1 L3 L4 M3 M4 M5 M6 E2 E1 F1 F2 G6 G5 H6 H5")),
            Subsignal("ldm",    Pins("J2")), 
            Subsignal("ldqs",   Pins("L6")), 
            Subsignal("ras",    Pins("C1")), 
            Subsignal("udm",    Pins("J1")), 
            Subsignal("udqs",   Pins("G3")), 
            Subsignal("we",     Pins("D1")), 
            Subsignal("ck_fb",  Pins("B9"), Attrs(IOSTANDARD="LVCMOS33")),
            Attrs(IOSTANDARD="SSTL2_I")),

        # ==== Intel StrataFlash Parallel NOR Flash (SF) ==== (Pg. 82 in User Guide)
        Resource("strataflash", 0,
            Subsignal("a",     Pins("H17 J13 J12 J14 J15 J16 J17 K14 K15 K12 K13 L15 L16 T18 R18 T17 U18 T16 U15 V15 T12 V13 V12 N11 A11"),
                               Attrs(DRIVE="4", SLEW="SLOW")), 
            Subsignal("byte",  Pins("C17"), Attrs(DRIVE="4", SLEW="SLOW")), 
            Subsignal("ce0",   Pins("D16"), Attrs(DRIVE="4", SLEW="SLOW")), 
            Subsignal("d",     Pins("P10 R10 V9 U9 R9 M9 N9 R15 R16 P17 M15 M16 P6 R8 T8"),
                               Attrs(DRIVE="4", SLEW="SLOW")), 
            Subsignal("oe",    Pins("C18"), Attrs(DRIVE="4", SLEW="SLOW")), 
            Subsignal("sts",   Pins("B18")), 
            Subsignal("we",    Pins("D17"), Attrs(DRIVE="4", SLEW="SLOW")), 
            Attrs(IOSTANDARD="LVCMOS33")),

        # ==== Xilinx CPLD (XC) ==== (Pg. 127 in User Guide)
        Resource("cpld", 0,
            Subsignal("cmd",     Pins("P18 N18"), Attrs(IOSTANDARD="LVTTL", DRIVE="4", SLEW="SLOW")),
            Subsignal("cpld_en", Pins("B10"), Attrs(IOSTANDARD="LVTTL")), 
            Subsignal("d",       Pins("G16 F18 F17"), Attrs(IOSTANDARD="LVTTL", DRIVE="4", SLEW="SLOW")),
            Subsignal("trig",    Pins("R17"), Attrs(IOSTANDARD="LVCMOS33")), 
            Subsignal("gck0",    Pins("H16"), Attrs(IOSTANDARD="LVCMOS33", DRIVE="4", SLEW="SLOW")),
            Subsignal("gclk10",  Pins("C9"), Attrs(IOSTANDARD="LVCMOS33", DRIVE="4", SLEW="SLOW"))),
    ]

    connectors = [
        # ==== 6-pin header J1 ==== (Pg. 121 in User Guide)
        Connector("j", 1,
            "B4 A4 D5 C5 - -"),

        # ==== 6-pin header J2 ==== (Pg. 121 in User Guide)
        Connector("j", 2,
            "A6 B6 E7 F7 - -"),

        # ==== FX2 Connector (FX2) ==== (Pg. 113 in User Guide)
        Connector("j", 3,
            "-   -   -   -   -   B4  A4  D5  C5  A6 B6  E7  F7 D7 C7  F8  E8  F9  E9 D11 C11 F11 E11 E12 F12"
            "A13 B13 A14 B14 C14 D14 A16 B16 E13 C4 B11 A11 A8 G9 D12 C12 A15 B15 C3 C15 -   D10 -   -   -  "
            "-   -   -   -   -   -   -   -   -   -  -   -   -  -  -   -   -   -   -  -   -   -   -   -   -  "
            "-   -   -   -   -   -   -   -   -   -  -   -   -  -  -   -   -   -   -  -   E10 -   D9  -   -  "),

        # ==== 6-pin header J4 ==== (Pg. 121 in User Guide)
        Connector("j", 4,
            "D7 C7 F8 E8 - -"),
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.bit".format(name)) as bitfile:
            cmd = textwrap.dedent("""
                setMode -bs
                setCable -port auto
                Identify -inferir
                IdentifyMPM
                assignFile -p 1 -file "{}"
                Program -p 1
                quit
            """).format(bitfile).encode('utf-8')
            subprocess.run(["impact", "-batch"], input=cmd, check=True)

if __name__ == "__main__":
    from .test.blinky import *
    DigilentSpartan3ePlatform().build(Blinky(), do_program=True)