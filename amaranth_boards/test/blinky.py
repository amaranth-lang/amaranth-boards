import itertools

from amaranth import *
from amaranth.build import ResourceError
from amaranth.lib import io


__all__ = ["Blinky"]


class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number, dir="-"))
                except ResourceError:
                    break
            return resources

        rgb_leds = [res for res in get_all_resources("rgb_led")]
        leds     = [io.Buffer("o", res) for res in get_all_resources("led")]
        leds.extend([io.Buffer("o", led.r) for led in rgb_leds])
        leds.extend([io.Buffer("o", led.g) for led in rgb_leds])
        leds.extend([io.Buffer("o", led.b) for led in rgb_leds])
        buttons  = [io.Buffer("i", res) for res in get_all_resources("button")]
        switches = [io.Buffer("i", res) for res in get_all_resources("switch")]

        m.submodules += leds + buttons + switches

        inverts  = [0 for _ in leds]
        for index, button in zip(itertools.cycle(range(len(inverts))), buttons):
            inverts[index] ^= button.i
        for index, switch in zip(itertools.cycle(range(len(inverts))), switches):
            inverts[index] ^= switch.i

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//2)), init=int(clk_freq//2) - 1)
        flops = Signal(len(leds))

        m.d.comb += Cat(led.o for led in leds).eq(flops ^ Cat(inverts))
        with m.If(timer == 0):
            m.d.sync += timer.eq(timer.init)
            m.d.sync += flops.eq(~flops)
        with m.Else():
            m.d.sync += timer.eq(timer - 1)

        return m
