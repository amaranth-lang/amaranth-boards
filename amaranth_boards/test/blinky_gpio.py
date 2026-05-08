### main deps
from amaranth import *
from amaranth.build import Platform, Resource, Pins
#from amaranth_boards.resources import Pins
from typing import List, Dict, Tuple, Optional

__all__ = ["BlinkyGpio"]

class BlinkyGpio(Elaboratable):
    """A one second cycle, 50% duty to drive a led on a target gpio of a connector.
    
    Striped down version of the amaranth-board 'blinky'."""

    def __init__(self, connectorName:str, connectorIndex:int, pinIndex:int, attrs = None):
        """Store the parameters for the elaboration

        Args:
            connectorName (str): The connector name
            connectorIndex (int): The connector name
            pinIndex (int): The index of the pin to use
            attrs (Attrs, optional): The attributes to setup the pin, platform dependant. Defaults to None.
        """
        self.connectorName = connectorName
        self.connectorIndex = connectorIndex
        self.targetPinIndex = pinIndex
        self.attrs = attrs

    def setup(self, platform):
        """Demonstrate how to setup a pin of the platform

        Args:
            platform (Platform): the platform to update.
        """
        # retrieve the targeted pin
        pin_name = platform.connectors[self.connectorName, self.connectorIndex].mapping[str(self.targetPinIndex)]
        print(f"pin name = {pin_name}")

        # setup pin as resource
        res = Resource("my_gpio",0,Pins(pin_name, dir="o"))
        if self.attrs is not None:
            res.attrs.update(self.attrs)
        
        # append resource into platform
        platform.add_resources([res])

    def elaborate(self, platform):
        m = Module()

        # -- -- configure the targeted pin as "my_gpio" index 0
        self.setup(platform)

        # -- -- make my_gpio[0] blink
        target = platform.request("my_gpio",0)

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//2)), reset=int(clk_freq//2) - 1)
        blink = Signal(reset=1)

        m.d.comb += target.eq(blink)
        with m.If(timer == 0):
            m.d.sync += timer.eq(timer.reset)
            m.d.sync += blink.eq(~blink)
        with m.Else():
            m.d.sync += timer.eq(timer - 1)

        return m 