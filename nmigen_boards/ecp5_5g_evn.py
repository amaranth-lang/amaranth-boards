import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ecp5 import *
from .resources import *


__all__ = ["ECP55GEVNPlatform"]


class ECP55GEVNPlatform(LatticeECP5Platform):
    device      = "LFE5UM5G-85F"
    package     = "BG381"
    speed       = "8"
    default_clk = "clk12"
    default_rst = "rst"
    resources   = [
        Resource("rst", 0, PinsN("G2", dir="i"), Attrs(IO_TYPE="LVCMOS33")),
        Resource("clk12", 0, Pins("A10", dir="i"),
                 Clock(12e6), Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins="A13 A12 B19 A18 B18 C17 A17 B17",
                      attrs=Attrs(IO_TYPE="LVCMOS33")),
        *SwitchResources(pins="P4", invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS33")),

        # TODO: add other resources
    ]
    connectors  = [
        # TODO: add connectors
    ]

    @property
    def file_templates(self):
        return {
            **super().file_templates,
            "{{name}}-openocd.cfg": r"""
            interface ftdi
            ftdi_device_desc "Lattice ECP5 Evaluation Board"
            ftdi_vid_pid 0x0403 0x6010
            ftdi_channel 0
            ftdi_layout_init 0xfff8 0xfffb
            reset_config none
            adapter_khz 25000

            jtag newtap ecp5 tap -irlen 8 -expected-id 0x81113043
            """
        }

    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}-openocd.cfg".format(name), "{}.svf".format(name)) \
                as (config_filename, vector_filename):
            subprocess.check_call([openocd,
                "-f", config_filename,
                "-c", "transport select jtag; init; svf -quiet {}; exit".format(vector_filename)
            ])


if __name__ == "__main__":
    from .test.blinky import *
    ECP55GEVNPlatform().build(Blinky(), do_program=True)
