from nmigen.build import *


__all__ = ["SPIResource"]


def SPIResource(number, *, cs, clk, mosi, miso, int=None, reset=None, attrs=None):
    io = []
    io.append(Subsignal("cs", PinsN(cs, dir="o")))
    io.append(Subsignal("clk", Pins(clk, dir="o")))
    io.append(Subsignal("mosi", Pins(mosi, dir="o")))
    io.append(Subsignal("miso", Pins(miso, dir="i")))
    if int is not None:
        io.append(Subsignal("int", Pins(int, dir="i")))
    if reset is not None:
        io.append(Subsignal("reset", Pins(reset, dir="o")))
    if attrs is not None:
        io.append(attrs)
    return Resource("spi", number, *io)
