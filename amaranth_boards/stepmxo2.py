import os
import argparse
import subprocess


from amaranth.build import *
from amaranth.vendor import LatticeMachXO2Platform
from .resources import *


__all__ = ["StepMXO2Platform"]


class StepMXO2Platform(LatticeMachXO2Platform):
    package     = "MG132"
    speed       = "4"
    default_clk = "clk12"
    device      = "LCMXO2-4000HC"
    resources   = [
        Resource("clk12", 0, Pins("C1", dir="i"), Attrs(IO_TYPE="LVCMOS33"),
                 Clock(12e6)),

        UARTResource(0, rx="A3", tx="A2", attrs=Attrs(IO_TYPE="LVCMOS33"),
                     role="dce"),

        *LEDResources(pins="N13 M12 P12 M11 P11 N10 N9 P9",
                      invert=True, attrs=Attrs(IO_TYPE="LVCMOS33")),

        RGBLEDResource(0, r="M2", g="N2", b="P2",
                       invert=True, attrs=Attrs(IO_TYPE="LVCMOS33")),
        RGBLEDResource(1, r="M3", g="N3", b="P4",
                       invert=True, attrs=Attrs(IO_TYPE="LVCMOS33")),

        *ButtonResources(pins="L14 M13 M14 N14", invert=True,
                         attrs=Attrs(IO_TYPE="LVCMOS33")),

        *SwitchResources(pins="M7 M8 M9 M10",
                         attrs=Attrs(IO_TYPE="LVCMOS33")),

        Display7SegResource(0,
            a="A10", b="C11", c="F2", d="E1", e="E2", f="A9", g="B9", dp="F1",
            attrs=Attrs(IO_TYPE="LVCMOS33")
        ),
        Display7SegResource(1,
            a="C12", b="B14", c="J1", d="H1", e="H2", f="B12", g="A11",
            dp="K1", attrs=Attrs(IO_TYPE="LVCMOS33")
        ),
        Resource("display_7seg_ctrl", 0,
            Subsignal("en", Pins("C9 A12", invert=True, dir="o")),
            Attrs(IO_TYPE="LVCMOS33")
        )
    ]
    connectors  = [
        # Special pins for MachXO2 hard IP.
        # I2C: 2- SCL, 3- SDA
        # SPI: 25- CS_N, 24- CLK, 22- COPI, 23- CIPO
        Connector("gpio", 0,
                  # Left side of the board
                  # 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
                  " - C8 B8 E3 F3 G3 H3 I2 I3 K2 K3 L3 N5 P6 N6 P7 N7 P8 N8  -"
                  # Right side of the board
                  # 21  22 23 24 25  26  27  28  29  30  31  32  33  34  35  36  37  38  39 40
                  "  - P13 N4 M4 P3 J12 K13 K14 K12 J14 J13 H12 G14 G13 F14 F13 G12 F12 E12  -"
        ),
    ]

    # This board doesn't have an integrated programmer; the board's MCU
    # implements a mass-storage device. You copy the JED file to it.

    # Workaround a STEP-MXO2-LPC parsing bug in the bootloader, as it doesn't
    # like JED files processed by ddtcmd. Copy the original JED file unchanged
    # to {{name}}-lpc.jed. Prefer this file.
    @property
    def command_templates(self):
        templates = super().command_templates
        cp_template = r"""{%- if syntax == "sh" -%}
                                cp {{name}}_impl/{{name}}_impl.jed {{name}}-lpc.jed
                          {%- else -%}
                                copy {{name}}_impl\{{name}}_impl.jed {{name}}-lpc.jed
                          {%- endif -%}
                       """

        if self.family == "machxo2":
            if self.toolchain == "Diamond":
                return templates + [cp_template]
            if self.toolchain == "Trellis":
                return self.templates
            assert False
        assert False


if __name__ == "__main__":
    from .test.blinky import *

    parser = argparse.ArgumentParser()
    parser.add_argument('toolchain', nargs="?", choices=["Trellis", "Diamond"], default="Diamond")
    args = parser.parse_args()

    StepMXO2Platform(toolchain=args.toolchain).build(Blinky(), do_program=False)
