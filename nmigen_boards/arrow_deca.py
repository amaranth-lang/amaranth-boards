import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *
from .resources import *


__all__ = ["ArrowDECAPlatform"]


class ArrowDECAPlatform(IntelPlatform):
    device      = "10M50DA" # MAX 10
    package     = "F484"
    speed       = "C6"
    suffix      = "GES"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("M8", dir="i"),
            Clock(50e6), Attrs(io_standard="2.5 V")),
        Resource("clk50", 1, Pins("P11", dir="i"),
            Clock(50e6), Attrs(io_standard="3.3 V")),
        Resource("clk50", 2, Pins("N15", dir="i"),
            Clock(50e6), Attrs(io_standard="1.5 V")),
        Resource("clk10", 0, Pins("M9", dir="i"),
            Clock(10e6), Attrs(io_standard="2.5 V")),

        *LEDResources(
            pins="C7 C8 A6 B7 C4 A5 B4 C5",
            invert=True,
            attrs=Attrs(io_standard="1.2 V")),
        *ButtonResources(
            pins="H21 H22",
            invert=True,
            attrs=Attrs(io_standard="1.5 V")),
        *SwitchResources(
            pins="J21 J22",
            attrs=Attrs(io_standard="1.5 V")),
    ]
    connectors  = [
        Connector("gpio", 0,
            "W18  Y18  Y19  AA17 AA20 AA19 AB21 AB20 AB19 Y16  V16  "
            "AB18 V15  W17  AB17 AA16 AB16 W16  AB15 W15  Y14  AA15 "
            "AB14 AA14 AB13 AA13 AB12 AA12 AB11 AA11 AB10 Y13  Y11  "
            "W13  W12  W11  V12  V11  V13  V14  Y17  W14  U15  R13"),
        Connector("gpio", 1,
            "Y5   Y6   W6   W7   W8   V8   AB8   V7  R11  AB7  AB6  "
            "AA7  AA6  Y7   V10  U7   W9   W5   R9   W4    P9  V17  "
            "W3"),
    ]

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename])

    @property
    def file_templates(self):
        # Configure the voltages of the I/O banks by appending the global
        # assignments to the template. However, we create our own copy of the
        # file templates before modifying them to avoid modifying the original.
        return {
            **super().file_templates,
            "{{name}}.qsf": r"""
                set_global_assignment -name IOBANK_VCCIO 2.5V -section_id 1A
                set_global_assignment -name IOBANK_VCCIO 2.5V -section_id 1B
                set_global_assignment -name IOBANK_VCCIO 2.5V -section_id 2
                set_global_assignment -name IOBANK_VCCIO 3.3V -section_id 3
                set_global_assignment -name IOBANK_VCCIO 3.3V -section_id 4
                set_global_assignment -name IOBANK_VCCIO 1.5V -section_id 5
                set_global_assignment -name IOBANK_VCCIO 1.5V -section_id 6
                set_global_assignment -name IOBANK_VCCIO 1.8V -section_id 7
                set_global_assignment -name IOBANK_VCCIO 1.2V -section_id 8

                set_global_assignment -name FORCE_CONFIGURATION_VCCIO ON
                set_global_assignment -name AUTO_RESTART_CONFIGURATION OFF
                set_global_assignment -name ENABLE_CONFIGURATION_PINS OFF
                set_global_assignment -name ENABLE_BOOT_SEL_PIN OFF
            """
        }


if __name__ == "__main__":
    from .test.blinky import Blinky
    ArrowDECAPlatform().build(Blinky(), do_program=True)
