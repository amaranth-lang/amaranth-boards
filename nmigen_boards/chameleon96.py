import os
import subprocess

from nmigen import *
from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["Chameleon96Platform"]


class Chameleon96Platform(IntelPlatform):
    device      = "5CSEBA6" # Cyclone V SE 110K LEs
    package     = "U19"     # UBGA-484
    speed       = "I7"
    default_clk = "cyclonev_oscillator"
    resources   = [
        # WIFI and BT LEDs
        *LEDResources(
            pins="Y19 Y20",
            attrs=Attrs(io_standard="2.5 V")),

        # TDA19988 HDMI transmitter
        Resource("tda19988", 0,
            Subsignal("vpa",       Pins("    W8  W7  V6  V5  U6 ", dir="o")), # bits 3 to 7
            Subsignal("vpb",       Pins("AB5 AA5 AA8 AB8 AB9 Y11", dir="o")), # bits 2 to 7
            Subsignal("vpc",       Pins("    W6  Y5  AB7 AA7 AA6", dir="o")), # bits 3 to 7
            Subsignal("pclk",      Pins("AB10", dir="o")),
            Subsignal("hsync",     Pins("V10 ", dir="o")),
            Subsignal("vsync",     Pins("V7  ", dir="o")),
            Subsignal("de",        Pins("Y8  ", dir="o")),
            Attrs(io_standard="1.8 V")
        ),

        I2CResource("tda19988_i2c", 0,
            scl="U7", sda="U10",
            attrs=Attrs(io_standard="1.8 V"),
        ),

        Resource("tda19988_i2s", 0,
            Subsignal("mclk",  Pins("V11 ", dir="o")), # OSC_IN/AP3
            Subsignal("txd",   Pins("AA11", dir="o")), # AP1
            Subsignal("txc",   Pins("W11 ", dir="o")), # ACLK
            Subsignal("txfs",  Pins("V9  ", dir="o")), # AP0
            Attrs(io_standard="1.8 V")
        ),

        # Wifi and BT module
        *SDCardResources("wifi", 0,
            clk="AB20", cmd="AB18", dat0="Y14", dat1="AB19", dat2="AA18", dat3="AB15",
            attrs=Attrs(io_standard="1.8 V"),
        ),

        Resource("bt", 0,
            Subsignal("host_wake", Pins("AB12", dir="o")),
            Attrs(io_standard="1.8 V"),
        ),

        Resource("bt_i2s", 0,
            Subsignal("txd",   Pins("Y15 ", dir="o")), # BT_PCM_IN
            Subsignal("rxd",   Pins("Y16 ", dir="i")), # BT_PCM_OUT
            Subsignal("txc",   Pins("AA13", dir="i")), # BT_PCM_CLK
            Subsignal("txfs",  Pins("AB13", dir="i")), # BT_PCM_SYNC
            Attrs(io_standard="1.8 V"),
        ),

        UARTResource("bt_uart", 0,
            rx="AB14", cts="AB17", tx="AA15", rts="AA16", role="dte",
            attrs=Attrs(io_standard="1.8 V"),
        ),
    ]

    connectors  = [
        # J3, 2x20 expansion port
        Connector("J", 3,
            "-      -      Y13    -      W14    -      C5     -      C6     -"
            "-      -      -      -      -      E5     -      F5     -      A6"
            "-      A5     -      -      -      -      -      -      -      -"
            "-      -      -      -      -      -      -      -      -      -"
        ),

        # J8, 2x30 high speed expansion port (MIPI CSI)
        Connector("J", 8,
            "-      V16    -      U17    -      -      -      V17    -      W18"
            "-      -      -      U18    W12    V19    -      -      -      -"
            "-      -      -      -      -      -      -      -      -      -"
            "-      -      -      -      -      -      -      -      -      -"
            "-      -      -      -      -      -      -      -      -      -"
            "-      -      -      -      -      -      -      -      -      -"
        ),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            # The @2 selects the second device in the JTAG chain, because this chip
            # puts the ARM cores first.
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename + "@2"])


if __name__ == "__main__":
    from .test.blinky import Blinky
    Chameleon96Platform().build(Blinky(), do_program=True)
