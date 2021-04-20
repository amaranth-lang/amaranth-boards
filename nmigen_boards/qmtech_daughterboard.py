from nmigen.build import *
from nmigen_boards.resources import *

__all__ = ["QMTechDaughterboard"]

class QMTechDaughterboard:
    resources = [
        UARTResource(0,
            rx="J_2:13", tx="J_2:14",
            attrs=Attrs(IOSTANDARD="LVCMOS33")
        ),

        *LEDResources(
            pins="J_2:38 J_2:37 J_2:36 J_2:35 J_2:34", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(
            pins="J_3:5 J_2:42 J_2:41 J_2:40 J_2:39", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        Resource("eth_gmii", 0,
            Subsignal("rst",     PinsN("-", dir="o")),
            Subsignal("int",     PinsN("J_3:24", dir="o")),
            Subsignal("mdio",    Pins("J_3:13", dir="io")),
            Subsignal("mdc",     Pins("J_3:14", dir="o")), # Max 8.3MHz
            Subsignal("gtx_clk", Pins("J_3:27", dir="o")),
            Subsignal("tx_clk",  Pins("J_3:20", dir="i")),
            Subsignal("tx_en",   Pins("J_3:26", dir="o")),
            Subsignal("tx_er",   Pins("J_3:15", dir="o")),
            Subsignal("tx_data", Pins("J_3:25 J_3:23 J_3:22 J_3:21 J_3:19 J_3:18 J_3:17 J_3:16", dir="o")),
            Subsignal("rx_clk",  Pins("J_3:35", dir="i")),
            Subsignal("rx_dv",   Pins("J_3:40", dir="i"), Attrs(PULLDOWN="TRUE")),
            Subsignal("rx_er",   Pins("J_3:30", dir="i")),
            Subsignal("rx_data", Pins("J_3:39 J_3:38 J_3:37 J_3:36 J_3:34 J_3:33 J_3:32 J_3:31", dir="i")),
            Subsignal("col",     Pins("J_3:29", dir="i")),
            Subsignal("crs",     Pins("J_3:28", dir="i")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # 3 digit 7 segment display
        Display7SegResource(0,
            a="J_2:29", b="J_2:24", c="J_2:26", d="J_2:30", e="J_2:32", f="J_2:27", g="J_2:23", dp="J_2:28",
            invert=True),
        Resource("display_7seg_ctrl", 0,
            Subsignal("en", Pins("J_2:31 J_2:25 J_2:33", dir="o", invert=False)),
        ),

        Resource("vga", 0,
            Subsignal("r", Pins("J_3:55 J_3:54 J_3:57 J_3:56 J_3:58", dir="o")),
            Subsignal("g", Pins("J_3:49 J_3:48 J_3:51 J_3:50 J_3:52 J_3:53", dir="o")),
            Subsignal("b", Pins("J_3:44 J_3:43 J_3:46 J_3:45 J_3:47", dir="o")),
            Subsignal("hs", Pins("J_3:42", dir="o")),
            Subsignal("vs", Pins("J_3:41", dir="o")),
            Attrs(io_standard="3.3-V LVTTL")
        ),

        *SDCardResources(0, clk="J_3:9", cmd="J_3:10", dat0="J_3:8", dat1="J_3:7",
                            dat2="J_3:12", dat3="J_3:11", cd="J_3:6",
                            attrs=Attrs(IOSTANDARD="LVCMOS33")),
    ]

    connectors = [
        Connector("pmod", 0, "J_2:15 J_2:17 J_2:19 J_2:21 - - J_2:16 J_2:18 J_2:20 J_2:22 - -"), #J10
        Connector("pmod", 1, "J_2:5  J_2:7  J_2:9  J_2:11 - - J_2:6  J_2:8  J_2:10 J_2:12 - -"), #J11
        Connector("J", 1, {
            "3": "J_2:58",
            "4": "J_2:57",
            "5": "J_2:56",
            "6": "J_2:55",
            "7": "J_2:54",
            "8": "J_2:53",
            "9": "J_2:52",
            "10": "J_2:51",
            "11": "J_2:50",
            "12": "J_2:49",
            "13": "J_2:48",
            "14": "J_2:47",
            "15": "J_2:46",
            "16": "J_2:45",
            "17": "J_2:44",
            "18": "J_2:43"
        }), #J1
    ]

if __name__ == "__main__":
    print("The class in this file serves as an extension to other platforms only and cannot be built on its own.")