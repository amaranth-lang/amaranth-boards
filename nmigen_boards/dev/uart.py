from nmigen.build import *


__all__ = ["UARTResource"]


def UARTResource(number, *, rx, tx, rts=None, cts=None, dtr=None, dsr=None, dcd=None, ri=None,
                 attrs=None):
    io = []
    io.append(Subsignal("rx", Pins(rx, dir="i")))
    io.append(Subsignal("tx", Pins(rx, dir="o")))
    if rts is not None:
        io.append(Subsignal("rts", Pins(rts, dir="o")))
    if cts is not None:
        io.append(Subsignal("cts", Pins(cts, dir="i")))
    if dtr is not None:
        io.append(Subsignal("dtr", Pins(dtr, dir="o")))
    if dsr is not None:
        io.append(Subsignal("dsr", Pins(dsr, dir="i")))
    if dcd is not None:
        io.append(Subsignal("dcd", Pins(dcd, dir="i")))
    if ri is not None:
        io.append(Subsignal("ri", Pins(ri, dir="i")))
    if attrs is not None:
        io.append(attrs)
    return Resource("uart", number, *io)
