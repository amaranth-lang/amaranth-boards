from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from nmigen_boards.resources.user import *

__all__ = [ "ZedBoardPlatform" ]

class ZedBoardPlatform(Xilinx7SeriesPlatform):
    """Platform file for the ZedBoard.
    http://zedboard.org/product/zedboard
    """

    device = "xc7z020"
    package = "clg484"
    speed = 1

    def __init__(self, *, VADJ="2V5", **kwargs):
        super().__init__(**kwargs)

        if not VADJ in ("1V8", "2V5", "3V3"):
            raise RuntimeError("VADJ must be \"1V8\", \"2V5\", or \"3V3\"")

        self._VADJ = VADJ

    def bank34_35_iostandard(self):
        if self._VADJ == "1V8":
            return "LVCMOS18"
        elif self._VADJ == "2V5":
            return "LVCMOS25"
        elif self._VADJ == "3V3":
            return "LVCMOS33"

    default_clk = "clk100"

    resources = [
        Resource("clk100", 0, Pins("Y9", dir="i"), Clock(100e6), Attrs(IOSTANDARD="LVCMOS33")),    # GCLK

        *LEDResources(pins="T22 T21 U22 U21 V22 W22 U19 U14", attrs=Attrs(IOSTANDARD="LVCMOS33")), # LD0 - LD7

        Resource("button", 0, Pins("T18", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),       # BTNU
        Resource("button", 1, Pins("N15", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),       # BTNL
        Resource("button", 2, Pins("R16", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),       # BTND
        Resource("button", 3, Pins("R18", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),       # BTNR
        Resource("button", 4, Pins("P16", dir="i"), Attrs(IOSTANDARD=bank34_35_iostandard)),       # BTNC

        *SwitchResources(pins="F22 G22 H22 F21 H19 H18 H17 M15",                                   # SW0 - SW7
            attrs=Attrs(IOSTANDARD=bank34_35_iostandard))
    ]

    connectors = [
        Connector("pmod", 0, "Y11 AA11 Y10 AA9 - - AB11 AB10 AB9 AA8 - -"), # JA
        Connector("pmod", 1, "W12 W11 V10 W8 - - V12 W10 V9 V8 - -"),       # JB
        Connector("pmod", 2, "AB7 AB6 Y4 AA4 - - R6 T6 T4 U4 - -"),         # JC (differential)
        Connector("pmod", 3, "V7 W7 V5 V4 - - W6 W5 U6 U5 - -")             # JD (differential)
        # pmod4 (JE) is connected to the PS
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        # The Zynq driver in the FPGA Manager framework on mainline Linux
        # expects bitstreams that are byte swapped with respect to what the
        # Vivado command `write_bitstream -bin_file` produces. Thus, use the
        # `write_cfgmem` command with appropriate options to generate the
        # bitstream (.bin file).
        overrides = {
            "script_after_bitstream":
                "write_cfgmem -force -format bin -interface smapx32 -disablebitswap "
                "-loadbit \"up 0 {name}.bit\" {name}.bin".format(name=name)
        }

        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)
