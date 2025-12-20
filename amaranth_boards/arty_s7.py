import os
import textwrap
import subprocess

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["ArtyS7_25Platform", "ArtyS7_50Platform"]


class _ArtyS7Platform(XilinxPlatform):
    package     = "csga324"
    speed       = "1"
    default_clk = "clk100"
    default_rst = "rst"
    resources   = [
        Resource("clk100", 0, Pins("R2", dir="i"),
                 Clock(100e6), Attrs(IOSTANDARD="SSTL135")),
        Resource("rst", 0, PinsN("C18", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        *LEDResources(pins="E18 F13 E13 H15", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        RGBLEDResource(0, r="J15", g="G17", b="F15", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        RGBLEDResource(1, r="E15", g="F18", b="E14", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(pins="G15 K16 J16 H13", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        *SwitchResources(pins="H14 H18 G18  M5", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        UARTResource(0,
            rx="V12", tx="R12",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        SPIResource(0,
            cs_n="H16", clk="G16", copi="H17", cipo="K14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        I2CResource(0,
            scl="J14", sda="J13",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        *SPIFlashResources(0,
            cs_n="M13", clk="D11", copi="K17", cipo="K18", wp_n="L14", hold_n="M15",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        Resource("ddr3", 0,
            Subsignal("rst",    PinsN("J6", dir="o")),
            Subsignal("clk",    DiffPairs("R5", "T4", dir="o"), Attrs(IOSTANDARD="DIFF_SSTL135")),
            Subsignal("clk_en", Pins("T2", dir="o")),
            Subsignal("cs",     PinsN("R3", dir="o")),
            Subsignal("we",     PinsN("P7", dir="o")),
            Subsignal("ras",    PinsN("U1", dir="o")),
            Subsignal("cas",    PinsN("V3", dir="o")),
            Subsignal("a",      Pins("U2 R4 V2 V4 T3 R7 V6 T6 U7 V7 P6 T5 R6 U6", dir="o")),
            Subsignal("ba",     Pins("V5 T1 U3", dir="o")),
            Subsignal("dqs",    DiffPairs("K1 N3", "L1 N2", dir="io"),
                                Attrs(IOSTANDARD="DIFF_SSTL135")),
            Subsignal("dq",     Pins("K2 K3 L4 M6 K6 M4 L5 L6 N4 R1 N1 N5 M2 P1 M1 P2", dir="io"),
                                Attrs(IN_TERM="UNTUNED_SPLIT_40")),
            Subsignal("dm",     Pins("K4 M3", dir="o")),
            Subsignal("odt",    Pins("P5", dir="o")),
            Attrs(IOSTANDARD="SSTL135", SLEW="FAST"),
        ),
    ]
    connectors  = [
        Connector("pmod", 0, "L17 L18 M14 N14 - - M16 M17 M18 N18 - -"), # JA
        Connector("pmod", 1, "P17 P18 R18 T18 - - P14 P15 N15 P16 - -"), # JB
        Connector("pmod", 2, "U15 V16 U17 U18 - - U16 P13 R13 V14 - -"), # JC
        Connector("pmod", 3, "V15 U12 V13 T12 - - T13 R11 T11 U11 - -"), # JD

        Connector("ck_io", 0, {
            # Outer Digital Header
            "io0":  "L13",
            "io1":  "N13",
            "io2":  "L16",
            "io3":  "R14",
            "io4":  "T14",
            "io5":  "R16",
            "io6":  "R17",
            "io7":  "V17",
            "io8":  "R15",
            "io9":  "T15",
            "io10": "H16",
            "io11": "H17",
            "io12": "K14",
            "io13": "G16",

            # Inner Digital Header
            "io26": "U11",
            "io27": "T11",
            "io28": "R11",
            "io29": "T13",
            "io30": "T12",
            "io31": "V13",
            "io32": "U12",
            "io33": "V15",
            "io34": "V14",
            "io35": "R13",
            "io36": "P13",
            "io37": "U16",
            "io38": "U18",
            "io39": "U17",
            "io40": "V16",
            "io41": "U15",

            # Outer Analog Header as Digital IO
            "a0": "G13",
            "a1": "B16",
            "a2": "A16",
            "a3": "C13",
            "a4": "C14",
            "a5": "D18",

            # Inner Analog Header as Digital IO
            "io20": "B14",
            "io21": "A14",
            "io22": "D16",
            "io23": "D17",
            "io24": "D14",
            "io25": "D15"
        }),
        Connector("xadc", 0, {
            # Outer Analog Header
            "vaux0_p": "B13",
            "vaux0_n": "A13",
            "vaux1_p": "B15",
            "vaux1_n": "A15",
            "vaux9_p": "E12",
            "vaux9_n": "D12",
            "vaux2_p": "B17",
            "vaux2_n": "A17",
            "vaux10_p": "C17",
            "vaux10_n": "B18",
            "vaux11_p": "E16",
            "vaux11_n": "E17",

            # Inner Analog Header
            "vaux8_p": "B14",
            "vaux8_n": "A14",
            "vaux3_p": "D16",
            "vaux3_n": "D17",
        })
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_before_bitstream":
                "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "script_after_bitstream":
                "write_cfgmem -force -format mcs -interface spix4 -size 16 "
                "-loadbit \"up 0x0 {name}.bit\" -file {name}.mcs".format(name=name),
            "add_constraints":
                "set_property INTERNAL_VREF 0.675 [get_iobanks 34]"
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, product, name, *, programmer="vivado", flash=True):
        assert programmer in ("vivado", "openocd")

        if programmer == "vivado":
            if flash:
                # It does not appear possible to reset the FPGA via TCL after
                # flash programming.
                with product.extract("{}.bin".format(name)) as bitstream_filename:
                    cmd = textwrap.dedent("""
                        open_hw_manager
                        connect_hw_server
                        open_hw_target
                        current_hw_device [lindex [get_hw_devices] 0]
                        create_hw_cfgmem -hw_device [current_hw_device] s25fl128sxxxxxx0-spi-x1_x2_x4
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
            openocd = os.environ.get("OPENOCD", "openocd")
            # In order, OpenOCD searches these directories for files:
            # * $HOME/.openocd if $HOME exists (*nix)
            # * Path pointed to by $OPENOCD_SCRIPTS if $OPENOCD_SCRIPTS exists
            # * $APPDATA/OpenOCD on Windows
            # Place the bscan_spi_xc7s50.bit proxy bitstream under a directory
            # named "proxy" in one of the above directories so OpenOCD finds it.
            if flash:
                with product.extract("{}.bin".format(name)) as fn:
                    subprocess.check_call([openocd, "-f", "board/arty_s7.cfg",
                        "-c", """init;
                        jtagspi_init 0 [find proxy/bscan_spi_xc7s50.bit];
                        jtagspi_program {} 0;
                        xc7_program xc7.tap;
                        shutdown""".format(fn)])
            else:
                with product.extract("{}.bit".format(name)) as fn:
                    subprocess.check_call(["openocd", "-f", "board/arty_s7.cfg",
                        "-c", """init;
                        pld load 0 {};
                        shutdown""".format(fn)])


class ArtyS7_50Platform(_ArtyS7Platform):
    device      = "xc7s50"


class ArtyS7_25Platform(_ArtyS7Platform):
    device      = "xc7s25"


if __name__ == "__main__":
    from .test.blinky import *
    ArtyS7_25Platform().build(Blinky(), do_program=True)
