from nmigen.build import *


__all__ = [
    "SPIFlashResources", "SDCardResources",
    "SRAMResource", "SDRAMResource", "NORFlashResources",
]


def SPIFlashResources(*args, cs, clk, copi, cipo, wp=None, hold=None,
                      conn=None, attrs=None):
    resources = []

    io_all = []
    if attrs is not None:
        io_all.append(attrs)
    io_all.append(Subsignal("cs",  PinsN(cs, dir="o", conn=conn)))
    io_all.append(Subsignal("clk", Pins(clk, dir="o", conn=conn, assert_width=1)))

    io_1x = list(io_all)
    io_1x.append(Subsignal("copi", Pins(copi, dir="o", conn=conn, assert_width=1)))
    io_1x.append(Subsignal("cipo", Pins(cipo, dir="i", conn=conn, assert_width=1)))
    if wp is not None and hold is not None:
        io_1x.append(Subsignal("wp",   PinsN(wp,   dir="o", conn=conn, assert_width=1)))
        io_1x.append(Subsignal("hold", PinsN(hold, dir="o", conn=conn, assert_width=1)))
    resources.append(Resource.family(*args, default_name="spi_flash", ios=io_1x,
                                     name_suffix="1x"))

    io_2x = list(io_all)
    io_2x.append(Subsignal("dq", Pins(" ".join([copi, cipo]), dir="io", conn=conn,
                                      assert_width=2)))
    resources.append(Resource.family(*args, default_name="spi_flash", ios=io_2x,
                                     name_suffix="2x"))

    if wp is not None and hold is not None:
        io_4x = list(io_all)
        io_4x.append(Subsignal("dq", Pins(" ".join([copi, cipo, wp, hold]), dir="io", conn=conn,
                                          assert_width=4)))
        resources.append(Resource.family(*args, default_name="spi_flash", ios=io_4x,
                                         name_suffix="4x"))

    return resources


def SDCardResources(*args, clk, cmd, dat0, dat1=None, dat2=None, dat3=None, cd=None, wp=None,
                    conn=None, attrs=None):
    resources = []

    io_common = []
    if attrs is not None:
        io_common.append(attrs)
    if cd is not None:
        io_common.append(Subsignal("cd", Pins(cd, dir="i", conn=conn, assert_width=1)))
    if wp is not None:
        io_common.append(Subsignal("wp", PinsN(wp, dir="i", conn=conn, assert_width=1)))

    io_native = list(io_common)
    io_native.append(Subsignal("clk", Pins(clk, dir="o", conn=conn, assert_width=1)))
    io_native.append(Subsignal("cmd", Pins(cmd, dir="o", conn=conn, assert_width=1)))

    io_1bit = list(io_native)
    io_1bit.append(Subsignal("dat", Pins(dat0, dir="io", conn=conn, assert_width=1)))
    if dat3 is not None:
        # DAT3 has a pullup and works as electronic card detect
        io_1bit.append(Subsignal("ecd", Pins(dat3, dir="i", conn=conn, assert_width=1)))
    resources.append(Resource.family(*args, default_name="sd_card", ios=io_1bit,
                                     name_suffix="1bit"))

    if dat1 is not None and dat2 is not None and dat3 is not None:
        io_4bit = list(io_native)
        io_4bit.append(Subsignal("dat", Pins(" ".join((dat0, dat1, dat2, dat3)), dir="io",
                                             conn=conn, assert_width=4)))
        resources.append(Resource.family(*args, default_name="sd_card", ios=io_4bit,
                                         name_suffix="4bit"))

    if dat3 is not None:
        io_spi = list(io_common)
        # DAT3/CS# has a pullup and doubles as electronic card detect
        io_spi.append(Subsignal("cs", PinsN(dat3, dir="io", conn=conn, assert_width=1)))
        io_spi.append(Subsignal("clk", Pins(clk, dir="o", conn=conn, assert_width=1)))
        io_spi.append(Subsignal("copi", Pins(cmd, dir="o", conn=conn, assert_width=1)))
        io_spi.append(Subsignal("cipo", Pins(dat0, dir="i", conn=conn, assert_width=1)))
        resources.append(Resource.family(*args, default_name="sd_card", ios=io_spi,
                                         name_suffix="spi"))

    return resources


def SRAMResource(*args, cs, oe=None, we, a, d, dm=None,
                 conn=None, attrs=None):
    io = []
    io.append(Subsignal("cs", PinsN(cs, dir="o", conn=conn, assert_width=1)))
    if oe is not None:
        # Asserted WE# deactivates the D output buffers, so WE# can be used to replace OE#.
        io.append(Subsignal("oe", PinsN(oe, dir="o", conn=conn, assert_width=1)))
    io.append(Subsignal("we", PinsN(we, dir="o", conn=conn, assert_width=1)))
    io.append(Subsignal("a", Pins(a, dir="o", conn=conn)))
    io.append(Subsignal("d", Pins(d, dir="io", conn=conn)))
    if dm is not None:
        io.append(Subsignal("dm", PinsN(dm, dir="o", conn=conn))) # dm="LB# UB#"
    if attrs is not None:
        io.append(attrs)
    return Resource.family(*args, default_name="sram", ios=io)


def SDRAMResource(*args, clk, cke=None, cs=None, we, ras, cas, ba, a, dq, dqm=None,
                  conn=None, attrs=None):
    io = []
    io.append(Subsignal("clk", Pins(clk, dir="o", conn=conn, assert_width=1)))
    if cke is not None:
        io.append(Subsignal("clk_en", Pins(cke, dir="o", conn=conn, assert_width=1)))
    if cs is not None:
        io.append(Subsignal("cs",  PinsN(cs,  dir="o", conn=conn, assert_width=1)))
    io.append(Subsignal("we",  PinsN(we,  dir="o", conn=conn, assert_width=1)))
    io.append(Subsignal("ras", PinsN(ras, dir="o", conn=conn, assert_width=1)))
    io.append(Subsignal("cas", PinsN(cas, dir="o", conn=conn, assert_width=1)))
    io.append(Subsignal("ba", Pins(ba, dir="o", conn=conn)))
    io.append(Subsignal("a",  Pins(a,  dir="o", conn=conn)))
    io.append(Subsignal("dq", Pins(dq, dir="io", conn=conn)))
    if dqm is not None:
        io.append(Subsignal("dqm", Pins(dqm, dir="o", conn=conn))) # dqm="LDQM# UDQM#"
    if attrs is not None:
        io.append(attrs)
    return Resource.family(*args, default_name="sdram", ios=io)


def NORFlashResources(*args, rst=None, byte=None, cs, oe, we, wp, by, a, dq,
                      conn=None, attrs=None):
    resources = []

    io_common = []
    if rst is not None:
        io_common.append(Subsignal("rst", Pins(rst, dir="o", conn=conn, assert_width=1)))
    io_common.append(Subsignal("cs", PinsN(cs, dir="o", conn=conn, assert_width=1)))
    io_common.append(Subsignal("oe", PinsN(oe, dir="o", conn=conn, assert_width=1)))
    io_common.append(Subsignal("we", PinsN(we, dir="o", conn=conn, assert_width=1)))
    io_common.append(Subsignal("wp", PinsN(wp, dir="o", conn=conn, assert_width=1)))
    io_common.append(Subsignal("rdy", Pins(by, dir="i", conn=conn, assert_width=1)))

    if byte is None:
        io_8bit = list(io_common)
        io_8bit.append(Subsignal("a", Pins(a, dir="o", conn=conn)))
        io_8bit.append(Subsignal("dq", Pins(dq, dir="io", conn=conn, assert_width=8)))
        resources.append(Resource.family(*args, default_name="nor_flash", ios=io_8bit,
                                         name_suffix="8bit"))
    else:
        *dq_0_14, dq15_am1 = dq.split()

        # If present in a requested resource, this pin needs to be strapped correctly.
        io_common.append(Subsignal("byte", PinsN(byte, dir="o", conn=conn, assert_width=1)))

        io_8bit = list(io_common)
        io_8bit.append(Subsignal("a", Pins(" ".join((dq15_am1, a)), dir="o", conn=conn)))
        io_8bit.append(Subsignal("dq", Pins(" ".join(dq_0_14[:8]), dir="io", conn=conn,
                                            assert_width=8)))
        resources.append(Resource.family(*args, default_name="nor_flash", ios=io_8bit,
                                         name_suffix="8bit"))

        io_16bit = list(io_common)
        io_16bit.append(Subsignal("a", Pins(a, dir="o", conn=conn)))
        io_16bit.append(Subsignal("dq", Pins(dq, dir="io", conn=conn, assert_width=16)))
        resources.append(Resource.family(*args, default_name="nor_flash", ios=io_16bit,
                                         name_suffix="16bit"))

    return resources
