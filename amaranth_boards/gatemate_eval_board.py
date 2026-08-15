import os
import argparse
import subprocess
import shutil
import unittest

from amaranth.build import *
from amaranth.vendor import GateMatePlatform
from .resources import *


__all__ = [
    "GateMate_Eval_Board"
]

class GateMate_Eval_Board(GateMatePlatform):
    device                 = "GateMate_Eval_Board"
    package                = "CCGM1A1"
    default_clk            = "clk0"

    resources = [
        Resource("clk0", 0, Pins("IO_SB_A8", dir = "i"), Clock(10e6), Attrs(SCHMITT_TRIGGER="true")),

        *LEDResources(pins = "IO_EB_B1", attrs=Attrs()),
        *ButtonResources("but", pins="IO_EB_B0", attrs=Attrs()),

    ]

    connectors = []


    def toolchain_program(self, products, name):
        tool = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}_00.cfg.bit".format(name)) as bitstream_filename:
            subprocess.check_call([tool, "-b", "gatemate_evb_jtag", "--cable", "dirtyJtag", bitstream_filename])


class TestCase(unittest.TestCase):
    def test_smoke(self):
        from .test.blinky import Blinky
        GateMate_Eval_Board().build(Blinky(), do_build= False)



if __name__ == "__main__":
    from .test.blinky import *

    platform = GateMate_Eval_Board()
    platform.build(Blinky(), do_program=True)



