import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *

__all__ = ["RZEasyFPGAA2_2Platform"]

class RZEasyFPGAA2_2Platform(IntelPlatform):
    device      = "EP4CE6" # Cyclone IV 6K LEs
    package     = "E22"    # EQFP 144 pins
    speed       = "C8"
    default_clk = "clk50" # 50MHz builtin clock
    resources   = [
        # Clock
        Resource("clk50", 0, Pins("23", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        # LEDs, located on the bottom of the board.
        *LEDResources(
            pins="87 86 85 84", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),
        
        # Buttons, located on the bottom of the board, right of the LEDs.
        *ButtonResources(
            pins="88 89 90 91", invert=True,
            attrs=Attrs(io_standard="3.3-V LVTTL")),

        # Connections to the SKHynix RAM chip on board.
        SDRAMResource(0,
            clk="43", cs="72", we="69", ras="71", cas="70",
            ba="73 74", a="76 77 80 83 68 67 66 65 64 60 75 59",
            dq="28 30 31 32 33 34 38 39 54 53 52 51 50 49 46 44",
            dqm="42 55", attrs=Attrs(io_standard="3.3-V LVCMOS")),

        # Reset switch, located on the lower left of the board.
        Resource("reset_switch", 0, PinsN("25", dir="i"), Attrs(io_standard="3.3-V LVTTL")),

        # VGA connector, located on the right of the board.
        Resource("vga", 0,
            Subsignal("r", Pins("106", dir="o")),
            Subsignal("g", Pins("105", dir="o")),
            Subsignal("b", Pins("104", dir="o")),

            # Note: This pin is also the same pin that nCEO reserves.
            # To avoid an when using VGA, add the following to the
            # arguments of your call to RZEasyFPGA2_2Platform.build(): 
            # add_settings='''set_global_assignment -name CYCLONEII_RESERVE_NCEO_AFTER_CONFIGURATION "USE AS REGULAR IO"'''
            Subsignal("hs", Pins("101", dir="o")),

            Subsignal("vs", Pins("103", dir="o")),
        ),

        # 4 digit 7 segment display, located on top of the board.
        Resource("display_7seg", 0,
            # MSB is the very left digit, LSB is the very right digit.
            Subsignal("dig", Pins("133 135 136 137", dir="o", invert=True)),
            Subsignal("seg",  Pins("128 121 125 129 132 126 124 127", dir="o", invert=True)),
        ),

        # PS2 port, located on upper right of the board.
        Resource("ps2_host", 0, 
            Subsignal("clk", Pins("119", dir="i")),
            Subsignal("dat", Pins("120", dir="io")),
        ),

        I2CResource(0, scl="112", sda="113"),
        I2CResource(1, scl="99" , sda="98" ),

        # Serial port, located above the VGA port.
        UARTResource(0, tx="114", rx="115"),

        # LCD connector, located above the 7 segment display.
        Resource("lcd", 0,
            Subsignal("rs", Pins("141", dir="o")),
            Subsignal("rw", Pins("138", dir="o")),
            Subsignal("e" , Pins("143", dir="o")),
            Subsignal("d0", Pins("142", dir="o")),
            Subsignal("d1", Pins("1"  , dir="o")),
            Subsignal("d2", Pins("144", dir="o")),
            Subsignal("d3", Pins("3"  , dir="o")),
            Subsignal("d4", Pins("2"  , dir="o")),
            Subsignal("d5", Pins("10" , dir="o")),
            Subsignal("d6", Pins("7"  , dir="o")),
            Subsignal("d7", Pins("11" , dir="o")),
        ),

        # IR receiver, located right of the buttons.
        Resource("ir", 0,
            Subsignal("ir", Pins("100", dir="i"))
        ),
    ]

    connectors  = [
        # Located above the chip.
        Connector("gpio", 0,
            "-   -   11  7   2   144 142 138 136 133 129 127 125 121 119 114 112 110 -  "
            "-   -   24  10  3   1   143 141 137 135 132 128 126 124 120 115 113 111 -  "),
        
        # Located right of the chip.
        Connector("gpio", 1,
            "-   -  "
            "106 105"
            "104 103"
            "101 100"
            "99  98 "
            "91  90 "
            "89  88 "
            "87  86 "
            "85  84 "
            "-   -  "),
        
        # Located below the chip.
        Connector("gpio", 2,
            "30 32 34 39 43 46 50 52 54 58 60 65 67 71 73 75 77 83 -  -  - "
            "28 31 33 38 42 44 51 53 55 59 64 66 68 70 72 74 76 80 -  -  - "),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import Blinky
    RZEasyFPGAA2_2Platform().build(Blinky(), do_program=True)
