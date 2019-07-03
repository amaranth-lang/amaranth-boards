from nmigen.build import *


__all__ = ["UARTResource", "IrDAResource"]


def UARTResource(number, *, rx, tx, rts=None, cts=None, dtr=None, dsr=None, dcd=None, ri=None,
                 attrs=None):
    io = []
    io.append(Subsignal("rx", Pins(rx, dir="i")))
    io.append(Subsignal("tx", Pins(tx, dir="o")))
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


def IrDAResource(number, *, rx, tx, en=None, sd=None, attrs=None):
    # Exactly one of en (active-high enable) or sd (shutdown, active-low enable) should
    # be specified, and it is mapped to a logic level en subsignal.
    assert (en is not None) ^ (sd is not None)
    io = []
    io.append(Subsignal("rx", Pins(rx, dir="i")))
    io.append(Subsignal("tx", Pins(tx, dir="o")))
    if en is not None:
        io.append(Subsignal("en", Pins(en, dir="o")))
    if sd is not None:
        io.append(Subsignal("en", PinsN(sd, dir="o")))
    if attrs is not None:
        io.append(attrs)
    return Resource("irda", number, *io)
