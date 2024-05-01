from amaranth import *
from amaranth.build import *
from amaranth.vendor import IntelPlatform
from .resources import *

__all__ = ["MiSTPlatform"]


class MiSTPlatform(IntelPlatform):
    """MiST is the original Amiga/Atari ST retro FPGA board. It has been
    the inspiration for the MiSTer board.

    More information can be found on the wiki page:
    https://github.com/mist-devel/mist-board/wiki
    """
    device = "EP3C25" # Cyclone III 25K LEs
    package = "E144"
    speed = "C8"
    default_clk = "clk27"
    resources = [
        Resource(
            "clk27", 0, Pins("54", dir="i"),
            Clock(27e6), Attrs(io_standard="3.3-V LVTTL"),
        ),
        Resource(
            "clk27", 1, Pins("55", dir="i"),
            Clock(27e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(
            pins="7",
            attrs=Attrs(io_standard="3.3-V LVTTL"),
        ),

        VGAResource(0,
            r="135 137 141 142 143 144",
            g="106 110 111 112 113 114",
            b="115 120 121 125 132 133",
            hs="119", vs="136",
            attrs=Attrs(io_standard="3.3-V LVTTL"),
        ),

        UARTResource(0,
            rx="31", tx="46",
            attrs=Attrs(io_standard="3.3-V LVTTL"),
        ),

        SPIResource(0,
            cs_n="127 91 90", # SS2/FPGA, SS3/OSD, SS4/SD_DIRECT
            clk="126", copi="88", cipo="105",
            attrs=Attrs(io_standard="3.3-V LVTTL"),
        ),

        SDRAMResource(0,
            clk="43", cs_n="59", we_n="66", ras_n="60", cas_n="64",
            ba="58 51", a="49 44 42 39 4 6 8 10 11 28 50 30 32",
            dq="83 79 77 76 72 71 69 68 86 87 98 99 100 101 103 104",
            dqm="67 85",
            attrs=Attrs(io_standard="3.3-V LVCMOS"),
        ),

        Resource("audio", 0,
            Subsignal("l", Pins("65", dir="o")),
            Subsignal("r", Pins("80", dir="o")),
            Attrs(io_standard="3.3-V LVTTL"),
        ),

        Resource("conf_data0", 0,
            Pins("13", dir="i"),
            Attrs(io_standard="3.3-V LVTTL"),
        ),
    ]
    connectors = []


if __name__ == "__main__":
    from .test.blinky import Blinky
    MiSTPlatform().build(Blinky(), do_program=False)
    print((
        "To use test bitstream on MiST; copy 'build/top.rbf' to file\n"
        "named 'core.rbf' on SD card so it will be loaded by MiST firmware"
    ))
