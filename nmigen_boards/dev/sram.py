from nmigen.build import *


__all__ = ["SRAMResource"]


def SRAMResource(*args, cs, oe=None, we, a, d, dm=None, attrs=None):
    io = []
    io.append(Subsignal("cs", PinsN(cs, dir="o", assert_width=1)))
    if oe is not None:
        # Asserted WE# deactivates the D output buffers, so WE# can be used to replace OE#.
        io.append(Subsignal("oe", PinsN(oe, dir="o", assert_width=1)))
    io.append(Subsignal("we", PinsN(we, dir="o", assert_width=1)))
    io.append(Subsignal("a", Pins(a, dir="o")))
    io.append(Subsignal("d", Pins(d, dir="io")))
    if dm is not None:
        io.append(Subsignal("dm", PinsN(dm, dir="o"))) # dm="LB# UB#"
    if attrs is not None:
        io.append(attrs)
    return Resource.family(*args, default_name="sram", ios=io)
