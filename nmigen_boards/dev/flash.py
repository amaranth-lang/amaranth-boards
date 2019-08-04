from nmigen.build import *


__all__ = ["SPIFlashResources"]


def SPIFlashResources(*args, cs, clk, mosi, miso, wp=None, hold=None, attrs=None):
    resources = []

    io_all = []
    if attrs is not None:
        io_all.append(attrs)
    io_all.append(Subsignal("cs",  PinsN(cs, dir="o")))
    io_all.append(Subsignal("clk", Pins(clk, dir="o", assert_width=1)))

    io_1x = list(io_all)
    io_1x.append(Subsignal("mosi", Pins(mosi, dir="o", assert_width=1)))
    io_1x.append(Subsignal("miso", Pins(miso, dir="i", assert_width=1)))
    if wp is not None and hold is not None:
        io_1x.append(Subsignal("wp",   PinsN(wp,   dir="o", assert_width=1)))
        io_1x.append(Subsignal("hold", PinsN(hold, dir="o", assert_width=1)))
    resources.append(Resource.family(*args, default_name="spi_flash", ios=io_1x,
                                     name_suffix="1x"))

    io_2x = list(io_all)
    io_2x.append(Subsignal("dq", Pins(" ".join([mosi, miso]), dir="io",
                                      assert_width=2)))
    resources.append(Resource.family(*args, default_name="spi_flash", ios=io_2x,
                                     name_suffix="2x"))

    if wp is not None and hold is not None:
        io_4x = list(io_all)
        io_4x.append(Subsignal("dq", Pins(" ".join([mosi, miso, wp, hold]), dir="io",
                                          assert_width=4)))
        resources.append(Resource.family(*args, default_name="spi_flash", ios=io_4x,
                                         name_suffix="4x"))

    return resources
