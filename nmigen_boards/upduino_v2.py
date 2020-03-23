import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *
from .upduino_v1 import UpduinoV1Platform


__all__ = ["UpduinoV2Platform"]


class UpduinoV2Platform(UpduinoV1Platform):
    # Mostly identical to the V1 board, but it has an integrated
    # programmer and a 12MHz oscillator which is NC by default.
    resources = UpduinoV1Platform.resources + [
        # Solder pin 12 to the adjacent 'J8' osc_out pin to enable.
        Resource("clk12", 0, Pins("12", dir="i"),
                 Clock(12e6), Attrs(IO_STANDARD="SB_LVCMOS")),
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([iceprog, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    UpduinoV2Platform().build(Blinky(), do_program=True)
