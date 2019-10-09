import itertools

from nmigen import *
from nmigen.build import ResourceError


__all__ = ["Blinky"]


class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number))
                except ResourceError:
                    break
            return resources

        leds     = [res.o for res in get_all_resources("led")]
        buttons  = [res.i for res in get_all_resources("button")]
        switches = [res.i for res in get_all_resources("switch")]

        inverts  = [0 for _ in leds]
        for index, button in zip(itertools.cycle(range(len(inverts))), buttons):
            inverts[index] ^= button
        for index, switch in zip(itertools.cycle(range(len(inverts))), switches):
            inverts[index] ^= switch

        clk_freq = platform.default_clk_frequency
        timer = Signal(max=int(clk_freq//2), reset=int(clk_freq//2) - 1)
        flops = Signal(len(leds))

        m.d.comb += Cat(leds).eq(flops ^ Cat(inverts))
        with m.If(timer == 0):
            m.d.sync += timer.eq(timer.reset)
            m.d.sync += flops.eq(~flops)
        with m.Else():
            m.d.sync += timer.eq(timer - 1)

        return m
