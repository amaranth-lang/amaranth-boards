import os
import subprocess

from nmigen.build import *
from nmigen.vendor.xilinx_spartan_3_6 import *
from .dev import *
from .dev.user import Display7SegResource


__all__ = ["MercuryPlatform"]


class MercuryPlatform(XilinxSpartan3APlatform):
    """
    Original Mercury Board from Micro-Nova: https://www.micro-nova.com

    Mercury Manual: https://www.micro-nova.com/s/mercury_rm.pdf
    Mercury Schematic: https://www.micro-nova.com/s/mercury_schematic.pdf

    The Mercury board is often paired with an extension board called the
    Baseboard, which provides an ample set of I/O for FPGA beginners.

    Baseboard Manual: https://www.micro-nova.com/s/baseboard_rm.pdf
    Baseboard Schematics: https://www.micro-nova.com/s/baseboard_schematic.pdf

    Mercury and Baseboard Resources: https://www.micro-nova.com/resources-mercury
    """

    device  = "xc3s200a"
    package = "vq100"
    speed   = "4"

    default_clk = "clk50"
    resources = [
        Resource("clk50", 0, Pins("P43", dir="i"),
                 Attrs(IOSTANDARD="LVCMOS33"), Clock(50e6)),

        Resource("user_btn", 0, Pins("P41", dir="i"),
                 Attrs(IOSTANDARD="LVTTL")),

        # The serial interface and flash memory have a shared SPI bus.
        # FPGA is secondary.
        SPIResource("spi_serial", 0, role="device",
            cs="P39", clk="P53", mosi="P46", miso="P51",
            attrs=Attrs(IOSTANDARD="LVTTL"),
        ),

        # FPGA is primary.
        *SPIFlashResources(0,
            cs="P27", clk="P53", mosi="P46", miso="P51",
            attrs=Attrs(IOSTANDARD="LVTTL")
        ),

        # ADC over SPI- FPGA is primary.
        SPIResource("spi_adc", 0, role="host",
            cs="P12", clk="P9", mosi="P10", miso="P21",
            attrs=Attrs(IOSTANDARD="LVTTL"),
        ),

        # GPIO/SRAM Control
        # 5V tolerant GPIO is shared w/ the SRAM (on 200k gate devices) using
        # this pin. All GPIO except gpio:30 (and gpio:20, though see comment
        # under SRAMResource) interface to the SRAM. On assertion, this signal
        # will tristate the level-shifters, preventing any output on the 5V
        # GPIO pins (including gpio:30 and gpio:20).
        Resource("bussw_oe", 0, PinsN("P30N", dir="o"),
            Attrs(IOSTANDARD="LVTTL"))
    ]

    # Perhaps define some connectors as having a specific purpose- i.e. a 5V GPIO
    # bus with data, peripheral-select, and control signals?
    connectors = [
        Connector("gpio", 0, """P59 P60 P61 P62 P64 P57
                                P56 P52 P50 P49 P85 P84
                                P83 P78 P77 P65 P70 P71
                                P72 P73 P5  P4  P6  P98
                                P94 P93 P90 P89 P88 P86"""),  # 5V I/O- LVTTL.
        Connector("dio", 0, "P20 P32 P33 P34 P35 P36 P37"),  # Fast 3.3V IO
        # (Directly attached to FPGA)- LVCMOS33.
        Connector("clkio", 0, "P40 P44"),  # Clock IO (Can be used as GPIO)-
        # LVCMOS33.
        Connector("input", 0, "P68 P97 P7 P82"),  # Input-only pins- LVCMOS33.
        Connector("led", 0, "P13 P15 P16 P19"),  # LEDs can be used as pins
        # as well- LVTTL.
        Connector("pmod", 0, "P5 P4 P6 P98 P94 P93 P90 P89")  # Baseboard PMOD.
        # Overlaps w/ GPIO bus.
    ]

    # Some default useful extensions. Attach to platform using:
    # p.add_resources(p.leds)
    # pmod_btn = plat.request("led")
    leds = [
        Resource("led", 0, Pins("1", dir="o", conn=("led", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("led", 1, Pins("2", dir="o", conn=("led", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("led", 2, Pins("3", dir="o", conn=("led", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("led", 3, Pins("4", dir="o", conn=("led", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
    ]

    sram = [
        SRAMResource(0,
            cs="P3", we="gpio_0:29",
            # According to the schematic, A19/Pin 25 on the SRAM is wired to
            # gpio-0:20. However, according to the SRAM's datasheet, pin 25 is
            # a NC. Do not expose for now.
            a=""" gpio_0:1  gpio_0:2  gpio_0:3  gpio_0:4  gpio_0:5  gpio_0:6
                  gpio_0:7  gpio_0:8  gpio_0:9 gpio_0:10 gpio_0:11 gpio_0:12
                 gpio_0:13 gpio_0:14 gpio_0:15 gpio_0:16 gpio_0:17 gpio_0:18
                 gpio_0:19""",
            d="""gpio_0:21 gpio_0:22 gpio_0:23 gpio_0:24 gpio_0:25 gpio_0:26
                 gpio_0:27 gpio_0:28""",
            attrs=Attrs(IOSTANDARD="LVTTL", SLEW="FAST")
        )
    ]

    # The "serial port" is in fact over SPI. The creators of the board provide
    # a VHDL file for talking over this interface. In light of space
    # constraints and the fact that both the FT245RL and FPGA can BOTH be
    # SPI primaries, however, it may be necessary to sacrifice two "high-speed"
    # (DIO, INPUT) pins instead.
    serial = [
        # RX: FTDI D0, TX: FTDI D1
        UARTResource(0, rx="input_0:1", tx="dio_0:1",
            attrs=Attrs(IOSTANDARD="LVCMOS33"))
    ]

    # The remaining peripherals only make sense w/ the Baseboard installed.
    # See: http://www.micro-nova.com/mercury-baseboard/
    _switches = [
        Resource("switch", 0, Pins("1", dir="i", conn=("gpio", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("switch", 1, Pins("2", dir="i", conn=("gpio", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("switch", 2, Pins("3", dir="i", conn=("gpio", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("switch", 3, Pins("4", dir="i", conn=("gpio", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("switch", 4, Pins("5", dir="i", conn=("gpio", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("switch", 5, Pins("6", dir="i", conn=("gpio", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("switch", 6, Pins("7", dir="i", conn=("gpio", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("switch", 7, Pins("8", dir="i", conn=("gpio", 0)),
                 Attrs(IOSTANDARD="LVTTL"))
    ]

    _buttons = [
        Resource("button", 1, Pins("1", dir="i", conn=("input", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("button", 2, Pins("2", dir="i", conn=("input", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("button", 3, Pins("3", dir="i", conn=("input", 0)),
                 Attrs(IOSTANDARD="LVTTL")),
        Resource("button", 4, Pins("4", dir="i", conn=("input", 0)),
                 Attrs(IOSTANDARD="LVTTL"))
    ]

    _vga = [
        Resource("vga_out", 0,
            Subsignal("hsync", PinsN("led_0:3", dir="o")),
            Subsignal("vsync", PinsN("led_0:4", dir="o")),

            Subsignal("r", Pins("dio_0:1 dio_0:2 dio_0:3", dir="o")),
            Subsignal("g", Pins("dio_0:4 dio_0:5 dio_0:6", dir="o")),
            Subsignal("b", Pins("dio_0:7 clkio_0:1", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33", SLEW="FAST")
        )
    ]

    _extclk = [
        Resource("extclk", 0, Pins("1", dir="i", conn=("clkio", 1)),
                 Attrs(IOSTANDARD="LVCMOS33"))
    ]

    _sevenseg = [
        Display7SegResource(0,
            a="gpio_0:13", b="gpio_0:14", c="gpio_0:15", d="gpio_0:16",
            e="gpio_0:17", f="gpio_0:18", g="gpio_0:19", dp="gpio_0:20",
            invert=True, attrs=Attrs(IOSTANDARD="LVTTL")
        ),
        Resource("display_7seg_ctrl", 0,
            Subsignal("en", Pins("9 10 11 12", dir="o", conn=("gpio", 0))),
            Attrs(IOSTANDARD="LVTTL")
        )
    ]

    _ps2 = [
        Resource("ps2", 0,
             Subsignal("clk", Pins("2", dir="io", conn=("led", 0))),
             Subsignal("data", Pins("1", dir="io", conn=("led", 0))),
             Attrs(IOSTANDARD="LVTTL")
        )
    ]

    _audio = [
        Resource("audio", 0,
             Subsignal("l", Pins("30", dir="o", conn=("gpio", 0))),
             Subsignal("r", Pins("29", dir="o", conn=("gpio", 0))),
             Attrs(IOSTANDARD="LVTTL")
        )
    ]

    baseboard_sram    = _buttons + _vga + _extclk + _ps2
    baseboard_no_sram = baseboard_sram + _switches + _sevenseg + _audio

    def toolchain_program(self, products, name):
        # https://github.com/cr1901/mercpcl
        mercpcl = os.environ.get("MERCPCL", "mercpcl")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([mercpcl, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    plat = MercuryPlatform()
    plat.add_resources(plat.leds)
    plat.build(Blinky(), do_program=True)
