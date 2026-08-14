from .arty_s7 import ArtyS7_50Platform


if __name__ == "__main__":
    from .test.blinky import *
    ArtyS7_50Platform().build(Blinky(), do_program=True)
