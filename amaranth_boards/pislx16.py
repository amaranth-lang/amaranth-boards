#!/usr/bin/env python3

import os
import subprocess

from amaranth.build import *
from amaranth.vendor.xilinx_spartan_3_6 import *
from amaranth_boards.resources import *

__all__ = ["PiSLX16Platform"]

"""
http://piswords.com/xc6slx16.html 

Xilinx spartan6 XC6SLX16 Core Board Xilinx spartan 6 FPGA development board with 256mbit SDRAM

Useful notes on getting the openocd interface working : 

https://tomverbeure.github.io/2019/09/15/Loading-a-Spartan-6-bitstream-with-openocd.html
"""

class PiSLX16Platform(XilinxSpartan6Platform):
    device      = "xc6slx16"
    package     = "ftg256"
    speed       = "3"
    default_clk = "clk50"
    resources   = [
        Resource("clk50", 0, Pins("T8", dir="i"),
                 Clock(50e6), Attrs(IOSTANDARD="LVCMOS33")),

        # 4 Blue LEDs, LED0 .. LED3
        *LEDResources(pins="P4 N5 P5 M6", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # RESET key is L3 (all keys have pull-ups onboard)
        *ButtonResources(pins="C3 D3 E4 E3 L3", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # SPI Flash M25P16
        *SPIFlashResources(0,
            cs_n="T3", clk="R11", copi="T10", cipo="P10", attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),
 
        # UART CH340C
        UARTResource(0, rx="C11", tx="D12", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # DRAM H57V2562GTR SDRAMResource TODO
        # I2C AT24C02 EEPROM I2CResource TODO
        # SDCardResources TODO
    ]
    connectors  = [
        Connector("p", 1,
            "-    -    K16  J16  L16  K15  M15  M16  P16  N16  "
            "R16  P15  T15  R15  T14  R14  R12  T13  R9   T12  "
            "L8   T9   R7   T7   T5   T6   T4   R5   R1   R2   "
            "P2   M4   P6   N6   M5   N4   -    -    -    -    "
        ),
        Connector("p", 2,
            "-    -    A4   B5   A5   B6   A6   A7   B8   A8   "
            "C8   A9   A10  B10  A11  A12  B12  A13  A14  B14  "
            "B15  B16  C15  C16  D16  E15  C9   E11  C10  D11  "
            "E16  F15  F16  G16  H15  H16  -    -    -    -    "
        ),
    ]

    # Programming using openocd (programs FPGA's volatile config)

    @property
    def file_templates(self):
        return {
            **super().file_templates,
            "{{name}}-openocd.cfg": "adapter_khz 8000",
        }

    def toolchain_program_open_ocd(self, products, name, config=None, **kwargs):
        openocd = os.environ.get("OPENOCD", "openocd")
        with products.extract(f"{name}-openocd.cfg", f"{name}.bit") \
                as (config_filename, vector_filename):
            cmd = ";".join([ 
                "transport select jtag",
                "init",
                "xc6s_program xc6s.tap",
                f"pld load 0 {vector_filename}",
                "exit",
            ])
            subprocess.check_call([openocd,
                "-f", config,
                "-f", "cpld/xilinx-xc6s.cfg",
                "-f", config_filename,
                "-c", cmd,
            ])

    # Programming using openFPGALoader (SPI flash)

    def toolchain_program_open_fpga_loader(self, products, name, config=None, addr=None, dev=None, **kwargs):
        with products.extract(f"{name}.bit") as filename:
            conf = config or "digilent_hs3"
            cmd = [
                "openFPGALoader",
                "--fpga-part", self.device + self.package, # "xc6slx16ftg256", 
                "-c", conf,
                filename,
            ]
            if addr is not None:
                cmd += [ "-f", "-o", str(addr) ]
            if dev is not None:
                cmd += [ "-d", dev ]

            subprocess.check_call(cmd)

    # Programming (default to using Digilent JTAG-HS3)
    def toolchain_program(self, products, name, **kwargs):
        if kwargs.get("openocd"):
            config = kwargs.get("config", "interface/ftdi/digilent_jtag_hs3.cfg")
            self.toolchain_program_open_ocd(products, name, config=config)
        else:
            self.toolchain_program_open_fpga_loader(products, name, **kwargs)


if __name__ == "__main__":
    from amaranth_boards.test.blinky import Blinky
    dut = Blinky()
    opts = {
        #"openocd" : True,
        "config" : "digilent_hs3", # default
        "addr" : 0, # write to flash at this offset
    }
    PiSLX16Platform().build(dut, do_program=True, program_opts=opts, verbose=True)

