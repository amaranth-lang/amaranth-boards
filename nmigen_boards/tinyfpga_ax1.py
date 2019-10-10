from nmigen.build import *
from nmigen.vendor.lattice_machxo2 import *
from .resources import *


__all__ = ["TinyFPGAAX1Platform"]


class TinyFPGAAX1Platform(LatticeMachXO2Platform):
    device      = "LCMXO2-256HC"
    package     = "SG32"
    speed       = "4"
    connectors  = [
        Connector("gpio", 0,
            # Left side of the board
            #  1  2  3  4  5  6  7  8  9 10 11
             "13 14 16 17 20 21 23 25 26 27 28 "
            # Right side of the board
            # 12 13 14 15 16 17 18 19 20 21 22
             "-  -  -  -  4  5  8  9  10 11 12 "
        ),
    ]

    # This board doesn't have an integrated programmer.
