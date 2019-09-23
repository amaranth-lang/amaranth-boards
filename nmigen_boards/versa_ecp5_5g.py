from .versa_ecp5 import VersaECP5Platform


__all__ = ["VersaECP55GPlatform"]


class VersaECP55GPlatform(VersaECP5Platform):
    device      = "LFE5UM5G-45F"
    # Everything else is identical between 3G and 5G Versa boards.


if __name__ == "__main__":
    from .test.blinky import *
    VersaECP55GPlatform().build(Blinky(), do_program=True)
