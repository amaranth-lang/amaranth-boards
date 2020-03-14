from nmigen.build import *


__all__ = ["Display7SegResource"]


def Display7SegResource(*args, a, b, c, d, e, f, g, dp=None, invert=False,
                        conn=None, attrs=None):
    ios = []
    ios.append(Subsignal("a", Pins(a, dir="o", invert=invert, conn=conn, assert_width=1)))
    ios.append(Subsignal("b", Pins(b, dir="o", invert=invert, conn=conn, assert_width=1)))
    ios.append(Subsignal("c", Pins(c, dir="o", invert=invert, conn=conn, assert_width=1)))
    ios.append(Subsignal("d", Pins(d, dir="o", invert=invert, conn=conn, assert_width=1)))
    ios.append(Subsignal("e", Pins(e, dir="o", invert=invert, conn=conn, assert_width=1)))
    ios.append(Subsignal("f", Pins(f, dir="o", invert=invert, conn=conn, assert_width=1)))
    ios.append(Subsignal("g", Pins(g, dir="o", invert=invert, conn=conn, assert_width=1)))
    if dp is not None:
        ios.append(Subsignal("dp", Pins(dp, dir="o", invert=invert, conn=conn, assert_width=1)))
    if attrs is not None:
        ios.append(attrs)
    return Resource.family(*args, default_name="display_7seg", ios=ios)
