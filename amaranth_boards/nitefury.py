import os
import subprocess
import textwrap
import unittest

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["NitefuryIIPlatform", "LitefuryPlatform"]


class _BasePlatform(XilinxPlatform):
    speed       = "2"
    default_clk = "clk200"

    resources   = [
        Resource("clk200", 0, DiffPairs(p="J19", n="H19", dir="i"),
                 Clock(200e6), Attrs(IOSTANDARD="DIFF_SSTL15")),
        # 4 Programmable LEDs
        *LEDResources(pins="G3 H3 G4 H4", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        # SPIFlash
        *SPIFlashResources(0,
            cs_n="T19", clk="L16", copi="P22", cipo="R22", wp_n="P21", hold_n="R21",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
        # 1 M.2 indicator LED
        Resource("m2led", 0, Pins("M1"), Attrs(IOSTANDARD="LVCMOS33")),
        # PCIE
        Resource("pcie", 0,
            Subsignal("clkreq", PinsN("G1", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
            Subsignal("rst",    PinsN("J1", dir="o"), Attrs(IOSTANDARD="LVCMOS33", PULLUP=1)),
            Subsignal("clk",    DiffPairs(p="F6", n="E6", dir="i"), Attrs(IOSTANDARD="DIFF_SSTL15")),
            Subsignal("rx",     DiffPairs(p="B10 B8 D11 D9", n="A10 A8 C11 C9", dir="i")),
            Subsignal("tx",     DiffPairs(p="B6 B4 D5 D7", n="A6 A4 C5 C7", dir="o")),
        ),
        # DDR
        Resource("ddr3", 0,
            Subsignal("rst",    PinsN("K16", dir="o"), Attrs(IOStandard="LVCMOS15")),
            Subsignal("clk",    DiffPairs(p="K17", n="J17", dir="o")),
            Subsignal("clk_en", Pins("H22", dir="o")),
            # Subsignal("cs",     PinsN("U8", dir="o")),
            Subsignal("we",     PinsN("L16", dir="o")),
            Subsignal("ras",    PinsN("H20", dir="o")),
            Subsignal("cas",    PinsN("K18", dir="o")),
            Subsignal("a",      Pins("M15 L21 M16 L18 K21 M18 M21 N20 M20 N19 J21 M22 K22 N18 N22 J22", dir="o")),
            Subsignal("ba",     Pins("L19 J20 L20", dir="o")),
            Subsignal("dqs",    DiffPairs(p="F18 B21", n="E18 A21", dir="io"),
                                Attrs(IOSTANDARD="DIFF_SSTL135")),
            Subsignal("dq",     Pins("D19 B20 E19 A20 F19 C19 F20 C18 E22 G21 D20 E21 C22 D21 B22 D22", dir="io"),
                                Attrs(IN_TERM="UNTUNED_SPLIT_50")),
            Subsignal("dm",     Pins("A19 G22", dir="o")),
            Subsignal("odt",    Pins("K19", dir="o")),
            Attrs(IOSTANDARD="SSTL15", SLEW="FAST"),
        ),
    ]
    connectors  = []

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_before_bitstream":
                """
                set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
                set_property BITSTREAM.CONFIG.CONFIGRATE 16 [current_design]
                set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
                """,
            "script_after_bitstream":
                "write_cfgmem -force -format bin -interface spix4 -size 16 "
                "-loadbit \"up 0x0 {name}.bit\" -file {name}.bin".format(name=name),
            "add_constraints":
                """
                set_property INTERNAL_VREF 0.675 [get_iobanks 34]
                set_property CFGBVS VCCO [current_design]
                set_property CONFIG_VOLTAGE 3.3 [current_design]
                """
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, product, name, *, programmer="openfpgaloader", flash=True):
        assert programmer in ("vivado", "openfpgaloader")

        if programmer == "vivado":
            if flash:
                # It does not appear possible to reset the FPGA via TCL after
                # flash programming.
                with product.extract("{}.bin".format(name)) as bitstream_filename:
                    cmd = textwrap.dedent("""
                        open_hw_manager
                        connect_hw_server
                        open_hw_target
                        current_hw_device [lindex [get_hw_devices xc7a*] 0]]
                        create_hw_cfgmem -hw_device [current_hw_device] s25fl256sxxxxxx0-spi-x1_x2_x4
                        set_property PROGRAM.FILES {{{}}} [current_hw_cfgmem]
                        set_property PROGRAM.ADDRESS_RANGE  {{use_file}} [current_hw_cfgmem]
                        set_property PROGRAM.BLANK_CHECK  1 [current_hw_cfgmem]
                        set_property PROGRAM.ERASE  1 [current_hw_cfgmem]
                        set_property PROGRAM.CFG_PROGRAM  1 [current_hw_cfgmem]
                        set_property PROGRAM.VERIFY  1 [current_hw_cfgmem]
                        create_hw_bitstream -hw_device [current_hw_device] [get_property PROGRAM.HW_CFGMEM_BITFILE [current_hw_device]]
                        program_hw_devices
                        program_hw_cfgmem
                        close_hw_manager
                        puts "Vivado TCL cannot reset boards. Reset or power-cycle your board now."
                    """).format(bitstream_filename).encode("utf-8")
                    subprocess.run(["vivado", "-nolog", "-nojournal", "-mode", "tcl"], input=cmd, check=True)
            else:
                with product.extract("{}.bit".format(name)) as bitstream_filename:
                    cmd = textwrap.dedent("""
                        open_hw_manager
                        connect_hw_server
                        open_hw_target
                        current_hw_device [lindex [get_hw_devices] 0]
                        set_property PROGRAM.FILE {{{}}} [current_hw_device]
                        program_hw_devices
                        close_hw_manager
                    """).format(bitstream_filename).encode("utf-8")
                    subprocess.run(["vivado", "-nolog", "-nojournal", "-mode", "tcl"], input=cmd, check=True)
        else:
            # openfpgaloader
            openfpgaloader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
            with product.extract("{}.bin".format(name)) as fn:
                # TODO: @timkpaine has digilent_hs3 cable
                subprocess.check_call([openfpgaloader, "-c", "digilent_hs3", fn])


class LitefuryPlatform(_BasePlatform):
    device      = "xc7a100t"
    package     = "fgg484"


class NitefuryIIPlatform(_BasePlatform):
    device      = "xc7a200t"
    package     = "fbg484"


class TestCase(unittest.TestCase):
    def test_smoke(self):
        from .test.blinky import Blinky
        NitefuryIIPlatform().build(Blinky(), do_build=False)


if __name__ == "__main__":
    from .test.blinky import *
    NitefuryIIPlatform().build(Blinky(), do_program=True)
