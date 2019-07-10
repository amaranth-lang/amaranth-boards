from nmigen.build import *


__all__ = ["SPIResource"]


def SPIResource(*args, cs, clk, mosi, miso, int=None, reset=None, attrs=None, role="host"):
    assert role in ("host", "device")

    io = []
    if role == "host":
        io.append(Subsignal("cs", PinsN(cs, dir="o")))
        io.append(Subsignal("clk", Pins(clk, dir="o", assert_width=1)))
        io.append(Subsignal("mosi", Pins(mosi, dir="o", assert_width=1)))
        io.append(Subsignal("miso", Pins(miso, dir="i", assert_width=1)))
    else:  # device
        io.append(Subsignal("cs", PinsN(cs, dir="i", assert_width=1)))
        io.append(Subsignal("clk", Pins(clk, dir="i", assert_width=1)))
        io.append(Subsignal("mosi", Pins(mosi, dir="i", assert_width=1)))
        io.append(Subsignal("miso", Pins(miso, dir="oe", assert_width=1)))
    if int is not None:
        if role == "host":
            io.append(Subsignal("int", Pins(int, dir="i")))
        else:
            io.append(Subsignal("int", Pins(int, dir="oe", assert_width=1)))
    if reset is not None:
        if role == "host":
            io.append(Subsignal("reset", Pins(reset, dir="o")))
        else:
            io.append(Subsignal("reset", Pins(reset, dir="i", assert_width=1)))
    if attrs is not None:
        io.append(attrs)
    return Resource.family(*args, default_name="spi", ios=io)
