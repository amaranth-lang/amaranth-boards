import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ecp5 import *
from nmigen_boards.resources import *


__all__ = ['Colorlight5a75b70Platform']


class Colorlight5a75b70Platform(LatticeECP5Platform):
    device = 'LFE5U-25F'
    package = 'BG256'
    default_clk = 'clk25'
    speed = '8'

    resources = [
        Resource('clk25', 0, Pins('P6'), Clock(25e6), Attrs(GLOBAL=True, IO_STANDARD='LVCMOS33')),

        *LEDResources(pins='P11', attrs=Attrs(IO_STANDARD='LVCMOS33')),
        Resource('user_led', 0, PinsN('P11', dir='o'), Attrs(IO_STANDARD='LVCMOS33')),

        *ButtonResources(pins='M13', attrs=Attrs(IO_STANDARD='LVCMOS33')),
        Resource('user_btn', 0, PinsN('M13'), Attrs(IO_STANDARD='LVCMOS33')),

        # available in the J19 connector (rx = btn, tx=led)
        UARTResource(0,
            rx='P11', tx='M13',
            attrs=Attrs(IO_STANDARD='LVCMOS33')
        ),

        # W25Q32JV
        #SPIResource(0,
        #    cs='N8', mosi='T8', miso='T7',  # clk driven through USRMCLK
        #    attrs=Attrs(IO_STANDARD='LVCMOS33')
        #),

        # M12616161A
        Resource('sdram_clock', 0, Pins('C6'), Attrs(IO_STANDARD='LVCMOS33')),
        Resource('sdram', 0,
            Subsignal('a', Pins('A9 E10 B12 D13 C12 D11 D10 E9 D9 B7 C8')),
            Subsignal('dq', Pins(
                'B13 C11 C10 A11 C9 E8  B6  B9  '
                'A6  B5  A5  B4  B3 C3  A2  B2  '
                'E2  D3  A4  E4  D4 C4  E5  D5  '
                'E6  D6  D8  A8  B8 B10 B11 E11  '
            )),
            Subsignal('we_n',  Pins('C7')),
            Subsignal('ras_n', Pins('D7')),
            Subsignal('cas_n', Pins('E7')),
            Subsignal('ba',    Pins('A7')),
            Attrs(IO_STANDARD='LVCMOS33')
        ),

        # B50612D
        Resource('eth_clocks', 0,
            Subsignal('tx', Pins('M2')),
            Subsignal('rx', Pins('M1')),
            Attrs(IO_STANDARD='LVCMOS33')
        ),
        Resource('eth', 0,
            Subsignal('rst_n',   Pins('P5')),
            Subsignal('mdio',    Pins('T2')),
            Subsignal('mdc',     Pins('P3')),
            Subsignal('rx_ctl',  Pins('N6')),
            Subsignal('rx_data', Pins('N1 M5 N5 M6')),
            Subsignal('tx_ctl',  Pins('M3')),
            Subsignal('tx_data', Pins('L1 L3 P2 L4')),
            Attrs(IO_STANDARD='LVCMOS33')
        ),
        Resource('eth_clocks', 1,
            Subsignal('tx', Pins('M12')),
            Subsignal('rx', Pins('M16')),
            Attrs(IO_STANDARD='LVCMOS33')
        ),
        Resource('eth', 1,
            Subsignal('rst_n',   Pins('P5')),
            Subsignal('mdio',    Pins('T2')),
            Subsignal('mdc',     Pins('P3')),
            Subsignal('rx_ctl',  Pins('L15')),
            Subsignal('rx_data', Pins('P13 N13 P14 M15')),
            Subsignal('tx_ctl',  Pins('R15')),
            Subsignal('tx_data', Pins('T14 R12 R13 R14')),
            Attrs(IO_STANDARD='LVCMOS33')
        ),

        Resource('usb', 0,
            Subsignal('d_p',    Pins('M8')),
            Subsignal('d_n',    Pins('R2')),
            Subsignal('pullup', Pins('P4')),
            Attrs(IO_STANDARD='LVCMOS33')
        ),
    ]

    connectors = [
        Connector('j', 1, 'F3  F1  G3  - G2  H3  H5  F15 L2 K1 J5 K2 B16 J14 F12 -'),
        Connector('j', 2, 'J4  K3  G1  - K4  C2  E3  F15 L2 K1 J5 K2 B16 J14 F12 -'),
        Connector('j', 3, 'H4  K5  P1  - R1  L5  F2  F15 L2 K1 J5 K2 B16 J14 F12 -'),
        Connector('j', 4, 'P4  R2  M8  - M9  T6  R6  F15 L2 K1 J5 K2 B16 J14 F12 -'),
        Connector('j', 5, 'M11 N11 P12 - K15 N12 L16 F15 L2 K1 J5 K2 B16 J14 F12 -'),
        Connector('j', 6, 'K16 J15 J16 - J12 H15 G16 F15 L2 K1 J5 K2 B16 J14 F12 -'),
        Connector('j', 7, 'H13 J13 H12 - G14 H14 G15 F15 L2 K1 J5 K2 B16 J14 F12 -'),
        Connector('j', 8, 'A15 F16 A14 - E13 B14 A13 F15 L2 K1 J5 K2 B16 J14 F12 -'),
    ]


if __name__ == '__main__':
    from nmigen_boards.test.blinky import Blinky
    Colorlight5a75b70Platform().build(Blinky())
