from nmigen.build import *


__all__ = ["SPIFlashResources"]


def SPIFlashResources(number, *, cs, clk, mosi, miso, wp=None, hold=None, attrs=None):
    resources = []

    io_all = []
    if attrs is not None:
        io_all.append(attrs)
    io_all.append(Subsignal("cs",  PinsN(cs, dir="o")))
    io_all.append(Subsignal("clk", Pins(clk, dir="o")))

    io_1x = list(io_all)
    io_1x.append(Subsignal("mosi", Pins(mosi, dir="o")))
    io_1x.append(Subsignal("miso", Pins(miso, dir="i")))
    if wp is not None and hold is not None:
        io_1x.append(Subsignal("wp",   PinsN(wp,   dir="o")))
        io_1x.append(Subsignal("hold", PinsN(hold, dir="o")))
    resources.append(Resource("spi_flash", number, *io_1x))

    io_2x = list(io_all)
    io_2x.append(Subsignal("dq", Pins(" ".join([mosi, miso]), dir="io")))
    resources.append(Resource("spi_flash_2x", number, *io_2x))

    if wp is not None and hold is not None:
        io_4x = list(io_all)
        io_4x.append(Subsignal("dq", Pins(" ".join([mosi, miso, wp, hold]), dir="io")))
        resources.append(Resource("spi_flash_4x", number, *io_4x))

    return resources
