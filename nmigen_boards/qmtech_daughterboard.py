from nmigen.build import *
from nmigen_boards.resources import *

__all__ = ["QMTechDaughterboard"]

class QMTechDaughterboard:
    resources = [
        UARTResource(0,
            rx="J_2:15", tx="J_2:16",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        *LEDResources(
            pins="J_2:40 J_2:39 J_2:38 J_2:37 J_2:36", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(
            pins="J_3:7 J_2:44 J_2:43 J_2:42 J_2:41", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("eth_gmii", 0,
            Subsignal("rst",     PinsN("-", dir="o")),
            Subsignal("int",     PinsN("J_3:26", dir="o")),
            Subsignal("mdio",    Pins("J_3:15", dir="io")),
            Subsignal("mdc",     Pins("J_3:16", dir="o")), # Max 8.3MHz
            Subsignal("gtx_clk", Pins("J_3:29", dir="o")),
            Subsignal("tx_clk",  Pins("J_3:22", dir="i")),
            Subsignal("tx_en",   Pins("J_3:28", dir="o")),
            Subsignal("tx_er",   Pins("J_3:17", dir="o")),
            Subsignal("tx_data", Pins("J_3:27 J_3:25 J_3:24 J_3:23 J_3:21 J_3:20 J_3:19 J_3:18", dir="o")),
            Subsignal("rx_clk",  Pins("J_3:37", dir="i")),
            Subsignal("rx_dv",   Pins("J_3:42", dir="i"), Attrs(PULLDOWN="TRUE")),
            Subsignal("rx_er",   Pins("J_3:32", dir="i")),
            Subsignal("rx_data", Pins("J_3:41 J_3:40 J_3:39 J_3:38 J_3:36 J_3:35 J_3:34 J_3:33", dir="i")),
            Subsignal("col",     Pins("J_3:31", dir="i")),
            Subsignal("crs",     Pins("J_3:30", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # 3 digit 7 segment display
        Display7SegResource(0,
            a="J_2:31", b="J_2:26", c="J_2:28", d="J_2:32", e="J_2:34", f="J_2:29", g="J_2:25", dp="J_2:30",
            invert=True, attrs=Attrs(IOSTANDARD="LVCMOS33")),
        Resource("display_7seg_ctrl", 0,
            Subsignal("en", Pins("J_2:33 J_2:27 J_2:35", dir="o", invert=False)),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        Resource("vga", 0,
            Subsignal("r", Pins("J_3:57 J_3:56 J_3:59 J_3:58 J_3:60", dir="o")),
            Subsignal("g", Pins("J_3:51 J_3:50 J_3:53 J_3:52 J_3:54 J_3:55", dir="o")),
            Subsignal("b", Pins("J_3:46 J_3:45 J_3:48 J_3:47 J_3:49", dir="o")),
            Subsignal("hs", Pins("J_3:44", dir="o")),
            Subsignal("vs", Pins("J_3:43", dir="o")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        *SDCardResources(0, clk="J_3:11", cmd="J_3:12", dat0="J_3:10", dat1="J_3:9",
                            dat2="J_3:14", dat3="J_3:13", cd="J_3:8",
                            attrs=Attrs(IOSTANDARD="LVCMOS33")),
    ]

    connectors = [
        Connector("pmod", 0, "J_2:17 J_2:19 J_2:21 J_2:23 - - J_2:18 J_2:20 J_2:22 J_2:24 - -"), #J10
        Connector("pmod", 1, "J_2:7  J_2:9  J_2:11 J_2:13 - - J_2:8  J_2:10 J_2:12 J_2:14 - -"), #J11
        Connector("J", 1, {
            "3": "J_2:60",
            "4": "J_2:59",
            "5": "J_2:58",
            "6": "J_2:57",
            "7": "J_2:56",
            "8": "J_2:55",
            "9": "J_2:54",
            "10": "J_2:53",
            "11": "J_2:52",
            "12": "J_2:51",
            "13": "J_2:50",
            "14": "J_2:49",
            "15": "J_2:48",
            "16": "J_2:47",
            "17": "J_2:46",
            "18": "J_2:45"
        }), #J1
    ]

if __name__ == "__main__":
    print("The class in this file serves as an extension to other platforms only and cannot be built on its own.")