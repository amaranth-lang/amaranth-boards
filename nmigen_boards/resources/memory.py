from amaranth_boards.resources.memory import *
from amaranth_boards.resources.memory import __all__


import warnings
warnings.warn("instead of nmigen_boards.resources.memory, use amaranth_boards.resources.memory",
              DeprecationWarning, stacklevel=2)
