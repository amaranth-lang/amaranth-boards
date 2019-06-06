from nmigen.build import *


__all__ = ["SPIFlashResources"]


def SPIFlashResources(number, *, cs_n, clk, mosi, miso, wp_n=None, hold_n=None, attrs=None):
    resources = []

    io_all = []
    if attrs is not None:
        io_all.append(attrs)
    io_all.append(Subsignal("cs_n", Pins(cs_n, dir="o")))
    io_all.append(Subsignal("clk",  Pins(clk,  dir="o")))

    io_1x = list(io_all)
    io_1x.append(Subsignal("mosi", Pins(mosi, dir="o")))
    io_1x.append(Subsignal("miso", Pins(miso, dir="i")))
    if wp_n is not None and hold_n is not None:
        # Tristate these pins by default, and rely on a pullup on the board or within the flash.
        # An alternative would be to define them as outputs with reset value of 1, but that's
        # not currently possible in nMigen.
        io_1x.append(Subsignal("wp_n",   Pins(wp_n, dir="oe")))
        io_1x.append(Subsignal("hold_n", Pins(hold_n, dir="oe")))
    resources.append(Resource("spiflash", number, *io_1x))

    io_2x = list(io_all)
    io_2x.append(Subsignal("dq", Pins(" ".join([mosi, miso]), dir="io")))
    resources.append(Resource("spiflash2x", number, *io_2x))

    if wp_n is not None and hold_n is not None:
        io_4x = list(io_all)
        io_4x.append(Subsignal("dq", Pins(" ".join([mosi, miso, wp_n, hold_n]), dir="io")))
        resources.append(Resource("spiflash4x", number, *io_4x))

    return resources
