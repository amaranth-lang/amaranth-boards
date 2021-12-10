from amaranth_boards.test.blinky import *
from amaranth_boards.test.blinky import __all__


import warnings
warnings.warn("instead of nmigen_boards.test.blinky, use amaranth_boards.test.blinky",
              DeprecationWarning, stacklevel=2)
