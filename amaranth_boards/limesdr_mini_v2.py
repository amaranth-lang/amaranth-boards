import os
import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_ecp5 import *
from .resources import *


__all__ = ["LimeSDRminiv2Platform"]


class LimeSDRminiv2Platform(LatticeECP5Platform):
    device      = "LFE5U-45F"
    package     = "MG285"
    speed       = "6"
    default_clk = "clk40"
    #default_rst = "rst"

    resources   = [
        #Resource("rst", 0, PinsN("G2", dir="i"), Attrs(IO_TYPE="LVCMOS33")),
        Resource("clk40", 0, Pins("A9", dir="i"),
                 Clock(40e6), Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(pins="R16 M18 T17 V17 R18 R17", invert=True, # Shared with GPIO pins GPIO 4-7
                      attrs=Attrs(IO_TYPE="LVCMOS33")),
        
        # In order to use the UART as a UART you need to solder on a header,
        # and potentially reconfigure the onboard FTDI chip, I used Pins GPIO0 and GPIO1 on J3
        # Which translates to Pins FPGA N15 = FPGA_GPIO0 = TX, N18 = FPGA_GPIO1 = RX 
        # Still needs to be done on my board to test, code is just a place holder...

        UARTResource(0,
            rx="N18", tx="N15",
            #attrs=Attrs(IO_TYPE=bank6_iostandard, PULLMODE="UP")
            attrs=Attrs(IO_TYPE="LVCMOS33", PULLMODE="UP")
        ),
        
        # Have a question about RGB LEDS. Apparently the LimeSDR-mini-v2 only has 2 colour LEDS.
        # not 3, so it's Red and Green, but creates yellow with both green and red.
        # The RGB resource would need to be changed to relect that.
        # Commented out for now.

        #RGBLEDResource(0, r="V17", g="R16", b=" ", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        #RGBLEDResource(1, r="R18", g="M18", b=" ", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        #RGBLEDResource(2, r="R17", g="T17", b=" ", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        
        *SPIFlashResources(0,
            cs_n="U17", clk="U16", cipo="U18", copi="T18", attrs=Attrs(IO_TYPE="LVCMOS33")
        ),


        Resource("i2c", 0,
            Subsignal("scl",        Pins("C10", dir="io")),
            Subsignal("sda",        Pins("B9", dir="io")),
            #Subsignal("scl_pullup", Pins("A14", dir="o")),
            #Subsignal("sda_pullup", Pins("A13", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")
        )
    ]

        # TODO: add other resources
    connectors  = [
        # Expansion connectors
        Connector("J", 39, "A10 A8"), #FPGA_EGIO 0 and 1 to keep Amaranth-Boards Happy..
    ]

    @property
    def file_templates(self):
        return {
            **super().file_templates,
            "{{name}}-openocd.cfg": r"""
            adapter driver ftdi
            #ftdi_device_desc "Lattice ECP5 Evaluation Board"
            ftdi_vid_pid 0x0403 0x6010
            ftdi_channel 0
            ftdi_layout_init 0xfff8 0xfffb
            reset_config none
            adapter speed 250000

            jtag newtap ecp5 tap -irlen 8 -expected-id 0x41112043
            """
        }

    def toolchain_program(self, products, name):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract("{}-openocd.cfg".format(name), "{}.svf".format(name)) \
                as (config_filename, vector_filename):
            subprocess.check_call([openocd,
                "-f", config_filename,
                "-c", "transport select jtag; init; svf -quiet {}; exit".format(vector_filename)
            ])


if __name__ == "__main__":
    from .test.blinky import *
#    LimeSDRminiv2Platform().build(Blinky(), do_program=False)
    LimeSDRminiv2Platform().build(Blinky(), do_program=True)
