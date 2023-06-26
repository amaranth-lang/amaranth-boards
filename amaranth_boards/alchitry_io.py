import os
import shutil
import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_ice40 import *
from amaranth_boards.alchitry_au import *
from amaranth_boards.alchitry_cu import *
from .resources import *

__all__ = ["AlchitryCuIOPlatform"]

class AlchitryCuIOPlatform(AlchitryCuPlatform):
    resources = [
        *Display7SegResource(0, 
            a="3", b="4", c="18", d="19",
            e="20", d="2", g="1", dp="17", 
            conn=("bank",0), invert=True, attrs="SB_LVCMOS"
            ),

        # Not sure how to handle multiplex display..
        # Control line for anode are 21 22 5 6 [display 0-3]
        Resource("anodes",0,
            Subsignal("7seg_0", Pins("21", dir="o")),
            Subsignal("7seg_1", Pins("22", dir="o")),
            Subsignal("7seg_2", Pins("5",  dir="o")),
            Subsignal("7seg_3", Pins("6",  dir="o")),
            conn=("bank",0), invert=True, Attrs(IO_STANDARD="SB_LVCMOS")
            ),

        # Kind of a weird hack because I want to use generic connector
        # numbering but S5 is on a different connector than S1-4.
        # I guess rely on user to pick these up and use the pinouts correctly
        # in their application? Maybe they can just use something similar to
        # get_all_resources from .test/blinky to get all the things.
        *ButtonResources(0, 
            pins="31 32 15 16", conn=("bank",1), 
            invert=True, attrs="SB_LVCMOS"
            ),

        *ButtonResources(1,
            pins="18", conn=("bank",2),
            invert=True, attrs="SB_LVCMOS"
            ),

        #Same with the switches and LEDs.
        *SwitchResources(0, 
            pins="23 24 25 26 27 28", conn=("bank",1),
            invert=True, attrs="SB_LVCMOS"
            ),

        *SwitchResources(1,
            pins="31 32", conn=("bank",0),
            invert=True, attrs="SB_LVCMOS"
            ),

        *SwitchResources(2,
            pins="17 18 19 20 21 22", conn=("bank",1),
            invert=True, attrs="SB_LVCMOS"
            ),

        *SwitchResources(3,
            pins="23 24 25 26 27 28 29 30", conn=("bank",0),
            invert=True, attrs="SB_LVCMOS"
            ),
            
        # Total of 24 LED (3 banks of 8). Banks are split between connectors
        # So no easy way to resolve.
        *LEDResources(0, 
            pins="14 13 12 11 10 9 8 7 6 5 4 3 2 1", conn=("bank",1),
            invert=True, attrs="SB_LVCMOS"
            ),
        
        *LEDResources(1,
            pins="16 15 14 13 12 11 10 9 8 7", conn=("bank",0),
            invert=True, attrs="SB_LVCMOS"
            )
    ]
