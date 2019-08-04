from nmigen.build import *


__all__ = ["SRAMResource"]


def SRAMResource(*args, cs, oe, we, a, d, dm=None, attrs=None):
    io = []
    io.append(Subsignal("cs", PinsN(cs, dir="o")))
    io.append(Subsignal("oe", PinsN(oe, dir="o")))
    io.append(Subsignal("we", PinsN(we, dir="o")))
    io.append(Subsignal("a", Pins(a, dir="o")))
    io.append(Subsignal("d", Pins(d, dir="io")))
    if dm is not None:
        io.append(Subsignal("dm", PinsN(dm, dir="o"))) # dm="LB# UB#"
    if attrs is not None:
        io.append(attrs)
    return Resource.family(*args, default_name="sram", ios=io)
