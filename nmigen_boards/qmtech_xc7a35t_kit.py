from nmigen.build import *
from nmigen.vendor.xilinx_7series import *
from nmigen_boards.resources import *
from nmigen_boards.qmtech_xc7a35t_core import QMTechXC7A35TCorePlatform
from nmigen_boards.qmtech_daughterboard import QMTechDaughterboard


__all__ = ["QMTechXC7A35TKitPlatform"]

class QMTechXC7A35TKitPlatform(QMTechXC7A35TCorePlatform):
    def __init__(self, toolchain="Vivado"):
        self.connectors += QMTechDaughterboard.connectors
        self.resources  += QMTechDaughterboard.resources
        super().__init__(standalone=False, toolchain=toolchain)

if __name__ == "__main__":
    from nmigen_boards.test.blinky import *
    QMTechXC7A35TKitPlatform().build(Blinky(), do_program=True)
