import os
import subprocess
import shutil

from amaranth.build import *
from amaranth.vendor.lattice_ecp5 import *
from .resources import *


__all__ = ["ButterStickPlatform"]


class ButterStickPlatform(LatticeECP5Platform):
    device      = "LFE5UM5G-85F"
    package     = "BG381"
    speed       = "8"
    default_clk = "clk30"

    def ulpi_io_type(self):
        return _vccio_iotype(2)

    resources   = [
        Resource("clk30", 0, Pins("B12", dir="i"),
                 Clock(30e6), Attrs(IO_TYPE="LVCMOS33")),

        # LED Anodes
        *LEDResources(pins="C13 D12 U2 T3 D13 E13 C16", attrs=Attrs(IO_TYPE="LVCMOS33")),

        # LED Cathodes. Use invert to default as on to allow LEDs to be used in white with single bit IO
        # note that G and B are swapped to match the LEDs and not the schematic labels
        RGBLEDResource(0, r="T1", g="U1", b="R1", invert=True, attrs=Attrs(IO_TYPE="LVCMOS33")),

        *ButtonResources(
            pins={0: "U16", 1: "T17" }, invert=True,
            attrs=Attrs(IO_TYPE="SSTL135_I")),

        *SPIFlashResources(0,
            cs_n="R2", clk="U3", cipo="V2", copi="W2", wp_n="Y2", hold_n="W1",
            attrs=Attrs(IO_TYPE="LVCMOS33", SLEWRATE="FAST"),
        ),

        *SDCardResources("sdcard", 0,
            clk="B13", cmd="A13", dat0="C12", dat1="A12", dat2="D14", dat3="A14",
            attrs=Attrs(IO_TYPE="LVCMOS33", SLEWRATE="FAST"),
        ),

        Resource("ddr3", 0,
            Subsignal("rst",     PinsN("E17", dir="o")),
            Subsignal("clk",     DiffPairs("C20", "J19", dir="o"), Attrs(IO_TYPE="SSTL135D_I")),
            Subsignal("clk_en",  Pins("F18 J18", dir="o")),
            Subsignal("cs",      PinsN("J20 J16", dir="o")),
            Subsignal("we",      PinsN("G19", dir="o")),
            Subsignal("ras",     PinsN("K18", dir="o")),
            Subsignal("cas",     PinsN("J17", dir="o")),
            Subsignal("a",       Pins("G16 E19 E20 F16 F19 E16 F17 L20 M20 E18 G18 D18 H18 C18 D17 G20", dir="o")),
            Subsignal("ba",      Pins("H16 F20 H20", dir="o")),
            Subsignal("dqs",     DiffPairs("T19 N16", "R18 M17", dir="io"),
                      Attrs(IO_TYPE="SSTL135D_I", TERMINATION="OFF",
                      DIFFRESISTOR="100")),
            Subsignal("dq",      Pins("U19 T18 U18 R20 P18 P19 P20 N20 L19 L17 L16 R16 N18 R17 N17 P17",
                                      dir="io"), Attrs(TERMINATION="75")),
            Subsignal("dm",      Pins("U20 L18", dir="o")),
            Subsignal("odt",     Pins("K20 H17", dir="o")),
            Attrs(IO_TYPE="SSTL135_I", SLEWRATE="FAST")
        ),

        Resource("eth_rgmii", 0,
            Subsignal("rst",     PinsN("B20", dir="o")),
            Subsignal("mdc",     Pins("A19", dir="o")),
            Subsignal("mdio",    Pins("D16", dir="io")),
            Subsignal("tx_clk",  Pins("E15", dir="o")),
            Subsignal("tx_ctl",  Pins("D15", dir="o")),
            Subsignal("tx_data", Pins("C15 B16 A18 B19", dir="o")),
            Subsignal("rx_clk",  Pins("D11", dir="i")),
            Subsignal("rx_ctl",  Pins("B18", dir="i")),
            Subsignal("rx_data", Pins("A16 C17 B17 A17", dir="i")),
            Attrs(IO_TYPE="LVCMOS33", SLEWRATE="FAST")
        ),

        ULPIResource(0, data="B9 C6 A7 E9 A8 D9 C10 C7",
                     rst="C9", clk="B6", dir="A6", stp="C8", nxt="B8",
                     clk_dir="o", rst_invert=True, attrs=Attrs(IO_TYPE="LVCMOS18")),

        I2CResource(0, scl="E14", sda="C14",
                    attrs=Attrs(IO_TYPE="LVCMOS33")),

        # SYGYZY VIO level control pwm pins (use with care)
        Resource("vccio_ctrl", 0,
                 Subsignal("pdm", Pins("V1 E11 T2", dir="o")),
                 Subsignal("en", Pins("E12", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33")
        ),
        # Used to reload FPGA configuration (drives program_n)
        Resource("program", 0, PinsN("R3", dir="o"), Attrs(IO_TYPE="LVCMOS33")),
    ]
    connectors = [
        Connector("syzygy", 0, {
            # single ended
            "S0":"G2",  "S1":"J3",
            "S2":"F1",  "S3":"K3",
            "S4":"J4",  "S5":"K2",
            "S6":"J5",  "S7":"J1",
            "S8":"N2",  "S9":"L3",
            "S10":"M1", "S11":"L2",
            "S12":"N3", "S13":"N4",
            "S14":"M3", "S15":"P5",
            "S16":"H1", "S17":"K5",
            "S18":"K4", "S19":"K1",
            "S20":"L4", "S21":"L1",
            "S22":"L5", "S23":"M4",
            "S24":"N1", "S25":"N5",
            "S26":"P3", "S27":"P4",
            "S28":"H2", "S29":"P1",
            "S30":"G1", "S31":"P2",
            # diff pairs

        }),
        Connector("syzygy", 1, {
            # single ended
            "S0": "E4", "S1": "A4",
            "S2": "D5", "S3": "A5",
            "S4": "C4", "S5": "B2",
            "S6": "B4", "S7": "C2",
            "S8": "A2", "S9": "C1",
            "S10":"B1", "S11":"D1",
            "S12":"F4", "S13":"D2",
            "S14":"E3", "S15":"E1",

            "S16":"B5", "S17":"E5",
            "S18":"F5", "S19":"C5",
            "S20":"B3", "S21":"A3",
            "S22":"D3", "S23":"C3",
            "S24":"H5", "S25":"G5",
            "S26":"H3", "S27":"H4",
            "S28":"F2", "S29":"G3",
            "S30":"E2", "S31":"F3",
            
            # diff pairs
            "D0P":"E4", "D0N":"D5",
            "D1P":"A4", "D1N":"A5",
            "D2P":"C4", "D2N":"B4",
            "D3P":"B2", "D3N":"C2",
            "D4P":"A2", "D4N":"B1",
            "D5P":"C1", "D5N":"D1",
            "D6P":"F4", "D6N":"E3",
            "D7P":"D2", "D7N":"E1",
        }),
    ]

    def __init__(self, *, vccio_enable=True, vccio_voltages = [ 3.3, 3.3, 1.8 ], **kwargs):
        super().__init__(**kwargs)
        self._vccio_enable   = vccio_enable
        self._vccio_voltages = vccio_voltages

    def vccio_voltage(self, vccio_index):
        if not self._vccio_enable:
            return None
        else:
            return self._vccio_voltages[vccio_index]

    def _vccio_iotype(self, vccio_index):
        if not self._vccio_enable or self._vccio_voltages[vccio_index] == 3.3:
            return "LVCMOS33"
        if self._vccio_voltages[vccio_index] == 2.5:
            return "LVCMOS25"
        if self._vccio_voltages[vccio_index] == 1.8:
            return "LVCMOS18"
        assert False

    @property
    def required_tools(self):
        return super().required_tools + [
            "dfu-suffix"
        ]

    @property
    def command_templates(self):
        return super().command_templates + [
            r"""
            {{invoke_tool("dfu-suffix")}}
                -v 1209 -p 5af1 -a {{name}}.bit
            """
        ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = dict(ecppack_opts="--compress --freq 38.8")
        overrides.update(kwargs)
        return super().toolchain_prepare(fragment, name, **overrides)

    def toolchain_program(self, products, name):
        dfu_util = os.environ.get("DFU_UTIL", "dfu-util")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([dfu_util, "-a", "0", "-D", bitstream_filename, "-R"])


if __name__ == "__main__":
    from .test.blinky import *
    ButterStickPlatform().build(Blinky(), do_program=True)
