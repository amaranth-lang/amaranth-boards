import itertools

from nmigen import *
from nmigen.build import ResourceError


class Blinky(Elaboratable):
    def __init__(self, clk_name):
        self.clk_name = clk_name

    def elaborate(self, platform):
        m = Module()

        clk = platform.request(self.clk_name)
        clk_freq = platform.get_clock_constraint(clk)
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk.i)

        leds = []
        for n in itertools.count():
            try:
                leds.append(platform.request("user_led", n))
            except ResourceError:
                break
        leds = Cat(led.o for led in leds)

        ctr = Signal(max=int(clk_freq//2), reset=int(clk_freq//2) - 1)
        with m.If(ctr == 0):
            m.d.sync += ctr.eq(ctr.reset)
            m.d.sync += leds.eq(~leds)
        with m.Else():
            m.d.sync += ctr.eq(ctr - 1)

        return m


def build_and_program(platform_cls, clk_name, **kwargs):
    platform_cls().build(Blinky(clk_name), do_program=True, **kwargs)
