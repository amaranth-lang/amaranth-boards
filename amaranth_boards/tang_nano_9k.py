import os
import subprocess

from amaranth.build import *
from amaranth.vendor.gowin import *

try:
    from .resources import *
except:
    from resources import *


__all__ = ["TangNano9kPlatform"]


class TangNano9kPlatform(GowinPlatform):
    device      = "GW1N-9C" # tied to chip-db
    series      = "GW1NR"
    size        = "9"
    subseries   = "C"
    voltage     = "LV"
    package     = "QN88P"
    speed       = "C6/I5"
    default_clk = "clk27" # or "sys_clk0" to use on-chip oscillator
    osc_div     = 100     # only for on-chip oscillator, range(2, 128, 2)
    board       = "tangnano9k"
    resources   = [
        Resource("clk27", 0, Pins("52", dir="i"),
                 Clock(27e6), Attrs(IO_TYPE="LVCMOS33")),

        *ButtonResources(pins="3 4",
                         attrs=Attrs(IO_TYPE="LVCMOS33")),

        # Pins 5 to 8 are JTAG (TMS, TCK, TDI, TDO) from BL702

        # Pin 12 is VCC03_1V8
        *LEDResources(pins="10 11 13 14 15 16",
                      attrs=Attrs(IO_TYPE="LVCMOS33")),

        # Connects to BL702 UART1
        UARTResource(0, rx="18", tx="17",
            attrs=Attrs(PULL_MODE="UP", IO_TYPE="LVCMOS33")),

        *SPIFlashResources(0,
            cs_n="60", clk="59", copi="61", cipo="62",
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        *SDCardResources(0,
            clk="36", cmd="37", dat0="39", dat3="38", wp_n="-",
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        Resource("backlight_pwm", 0, Pins("86", dir="o"),
            Attrs(IO_TYPE="LVCMOS33")),

        # Missing 1.14 inch LCD
        # LCD_RESET  RESET PIN47_EN
        # PIN49_RS   RS
        # PIN77_MO   SDA
        # PIN76_MCLK SCL
        # PIN48_CS   CS

        Resource("hdmi", 0,  # FPGA_HDMI
                 Subsignal("clk",
                           DiffPairs(p="69", n="68", dir="o")),
                 Subsignal("d",
                           DiffPairs(p="71 73 75",
                                     n="70 72 74", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33")),

    ]
    connectors  = [
        Connector("gpio", 0,
            # I/O banks: 1: 3.3V, 2: 3.3V, 3: 1.8V

            # Some pins are not available, when certain boot modes are enabled:
            # MSPI: MI, MO, MCS_N, MCLK, FASTRD_N
            # SSPI: SI, SO, SSPI_CS_N
            # See 'overrides' below in toolchain_prepare()

            # When viewed from top (FPGA-side up), from USB to HDMI
            # top row
            #  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17     # gpio Pin
            #                                                    5V  # voltage
            #  1  3  3  3  3  3  3  3  3  1  1  1  1  1  1  1  1     # bank
            " 63 86 85 84 83 82 81 80 79 77 76 75 74 73 72 71 70  -"
            # 19 20 21 22          # gpio Pin
            #             GND 3V3  # voltage
            # 1  1  2  2           # bank
            " 48 49 31 32   -   -"
            # bottom row
            # 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42  # gpio Pin
            #  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  1  1  # bank
            " 38 37 36 39 25 26 27 28 29 30 33 34 40 35 41 42 51 53"
            # 43 44 45 46 47 48   # gpio Pin
            #     x  x  x         # special, don't use
            #  1  1  1  1  1  1   # bank
            " 54 55 56 57 68 69"
        ),
        # TODO: Convert to Resource
        Connector("rgb_lcd", 0,
            # LEDK LEDA GND +3V3 GND GND GND
            "    -    -   -    -   -   -   -"
            # HDMI_D2 ...    GND ... HDMI_CK_N
            # R3 R4 R5 R6 R7     G2 G3 G4
            " 75 74 73 72 71 - - 70 69 68"
            # RGB_G5 ... GND ...     RGB_B7 GND
            # G5 G6 G7       B3 B4 B7 B6 B7
            " 57 56 55 - - - 54 53 51 42 41   -"
            # RGB_CK +3V3 RGB_HS RGB_VS RGB_DE NC GND
            # CLK    DISP  HSYNC  VSYNC    DEN
            " 35        -     40     34     33  -   -"
            # RGB_INIT ...GND GND
            # XR YD XL YU
            " 32 31 63 50   -   -"
        )
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "add_options":
                "set_option -use_mspi_as_gpio 1 -use_sspi_as_gpio 1",
            "gowin_pack_opts":
                "--sspi_as_gpio --mspi_as_gpio"
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        with products.extract("{}.fs".format(name)) as bitstream_filename:
            subprocess.check_call(["openFPGALoader",
                                   "-b", self.board,
                                   bitstream_filename])


if __name__ == "__main__":
    try:
        from .test.blinky import *
    except:
        from test.blinky import *
    TangNano9kPlatform().build(Blinky(), do_program=True)
