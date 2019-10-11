from nmigen.build import *


__all__ = ["UARTResource", "IrDAResource", "SPIResource"]


def UARTResource(*args, rx, tx, rts=None, cts=None, dtr=None, dsr=None, dcd=None, ri=None,
                 conn=None, attrs=None):
    io = []
    io.append(Subsignal("rx", Pins(rx, dir="i", conn=conn, assert_width=1)))
    io.append(Subsignal("tx", Pins(tx, dir="o", conn=conn, assert_width=1)))
    if rts is not None:
        io.append(Subsignal("rts", Pins(rts, dir="o", conn=conn, assert_width=1)))
    if cts is not None:
        io.append(Subsignal("cts", Pins(cts, dir="i", conn=conn, assert_width=1)))
    if dtr is not None:
        io.append(Subsignal("dtr", Pins(dtr, dir="o", conn=conn, assert_width=1)))
    if dsr is not None:
        io.append(Subsignal("dsr", Pins(dsr, dir="i", conn=conn, assert_width=1)))
    if dcd is not None:
        io.append(Subsignal("dcd", Pins(dcd, dir="i", conn=conn, assert_width=1)))
    if ri is not None:
        io.append(Subsignal("ri", Pins(ri, dir="i", conn=conn, assert_width=1)))
    if attrs is not None:
        io.append(attrs)
    return Resource.family(*args, default_name="uart", ios=io)


def IrDAResource(number, *, rx, tx, en=None, sd=None,
                 conn=None, attrs=None):
    # Exactly one of en (active-high enable) or sd (shutdown, active-low enable) should
    # be specified, and it is mapped to a logic level en subsignal.
    assert (en is not None) ^ (sd is not None)

    io = []
    io.append(Subsignal("rx", Pins(rx, dir="i", conn=conn, assert_width=1)))
    io.append(Subsignal("tx", Pins(tx, dir="o", conn=conn, assert_width=1)))
    if en is not None:
        io.append(Subsignal("en", Pins(en, dir="o", conn=conn, assert_width=1)))
    if sd is not None:
        io.append(Subsignal("en", PinsN(sd, dir="o", conn=conn, assert_width=1)))
    if attrs is not None:
        io.append(attrs)
    return Resource("irda", number, *io)


def SPIResource(*args, cs, clk, mosi, miso, int=None, reset=None,
                conn=None, attrs=None, role="host"):
    assert role in ("host", "device")

    io = []
    if role == "host":
        io.append(Subsignal("cs", PinsN(cs, dir="o", conn=conn)))
        io.append(Subsignal("clk", Pins(clk, dir="o", conn=conn, assert_width=1)))
        io.append(Subsignal("mosi", Pins(mosi, dir="o", conn=conn, assert_width=1)))
        io.append(Subsignal("miso", Pins(miso, dir="i", conn=conn, assert_width=1)))
    else:  # device
        io.append(Subsignal("cs", PinsN(cs, dir="i", conn=conn, assert_width=1)))
        io.append(Subsignal("clk", Pins(clk, dir="i", conn=conn, assert_width=1)))
        io.append(Subsignal("mosi", Pins(mosi, dir="i", conn=conn, assert_width=1)))
        io.append(Subsignal("miso", Pins(miso, dir="oe", conn=conn, assert_width=1)))
    if int is not None:
        if role == "host":
            io.append(Subsignal("int", Pins(int, dir="i", conn=conn)))
        else:
            io.append(Subsignal("int", Pins(int, dir="oe", conn=conn, assert_width=1)))
    if reset is not None:
        if role == "host":
            io.append(Subsignal("reset", Pins(reset, dir="o", conn=conn)))
        else:
            io.append(Subsignal("reset", Pins(reset, dir="i", conn=conn, assert_width=1)))
    if attrs is not None:
        io.append(attrs)
    return Resource.family(*args, default_name="spi", ios=io)
