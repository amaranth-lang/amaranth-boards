from amaranth.build import *
from amaranth.vendor.lattice_ice40 import *


__all__ = ["DopplerPlatform"]


# Dadamachines Doppler USB stick https://github.com/dadamachines/doppler/
class DopplerPlatform(LatticeICE40Platform):
    device      = "iCE40UP5K"
    package     = "SG48"
    default_clk = "SB_HFOSC"
    hfosc_div   = 0
    resources   = [
        # PCB button1, button2
        Resource("button", 0, Pins("2", dir="i", invert=True),
                 Attrs(IO_STANDARD="SB_LVCMOS33", PULLUP=1)),
        Resource("button", 1, Pins("3", dir="i", invert=True),
                 Attrs(IO_STANDARD="SB_LVCMOS33", PULLUP=1)),

        # LED matrix anodes and cathodes
        Resource("aled", 0, Pins("26 27 28 31", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("kled", 0, Pins("42", dir="oe"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("kled", 1, Pins("43", dir="oe"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("kled", 2, Pins("44", dir="oe"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("kled", 3, Pins("45", dir="oe"), Attrs(IO_STANDARD="SB_LVCMOS")),

        # SAMD51 SERCOM5
        # CS:   SERCOM 1.3/3.3, Arduino pin 11
        # MISO: SERCOM 5.2/3.2, Arduino pin 12
        # MOSI: SERCOM 5.3/3.3, Arduino pin 13
        # CLK:  SERCOM 3.0/5.1, Arduino pin 14
        # Configured for bidirectional IO, use `.oe` subsignal to enable
        # output driver.
        Resource("spi", 0,
            Subsignal("cs", Pins("6", dir="io")),
            Subsignal("miso", Pins("4", dir="io")),
            Subsignal("mosi", Pins("9", dir="io")),
            Subsignal("clk", Pins("10", dir="io")),
            Attrs(IO_STANDARD="SB_LVCMOS"),
        ),

        # Configuration SPI interface
        # SO:  PB02, SERCOM 5.0, Arduino pin 23
        # SCK: PB03, SERCOM 5.1, Arduino pin 21
        # CS:  PB22, SERCOM 1.2/5.2, Arduino pin 24
        # SI: PB23, SERCOM 1.3/5.3, Arduino pin 22
        Resource("cfg", 1,
            Subsignal("so", Pins("14", dir="o")),
            Subsignal("sck", Pins("15", dir="i")),
            Subsignal("cs", Pins("16", dir="i")),
            Subsignal("si", Pins("17", dir="i")),
            Attrs(IO_STANDARD="SB_LVCMOS"),
        ),

        # Pins breakout downside/upside.
        # Configured for bidirectional IO, use `.oe` subsignal to enable output
        # driver.
        Resource("pinbank", 0, Pins("11 12 13 18 19 20 21 23", dir="io"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("pinbank", 1, Pins("41 40 39 38 37 36 35 34", dir="io"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),

    ]
    # Connectors for pinbanks as an alternative way to connect to these pins,
    # use platform.add_resource to connect to them.
    connectors = [
        Connector("pinbank", 0, "11 12 13 18 19 20 21 23"),
        Connector("pinbank", 1, "41 40 39 38 37 36 35 34"),
    ]
