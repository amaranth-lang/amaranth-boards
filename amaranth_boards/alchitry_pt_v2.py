import os
import subprocess
import shutil

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["AlchitryPtV2Platform"]


def find_loader():
    loader_prgm = os.environ.get("ALCHITRY_LOADER", shutil.which("loader"))
    if loader_prgm is None:
        raise EnvironmentError(
            "Could not find Alchrity Loader. Place "
            "it directly in PATH or specify path explicitly via the "
            "ALCHITRY_LOADER environment variable"
        )
    bridge_bin = os.environ.get(
        "ALCHITRY_BRIDGE_BIN",
        os.path.join(os.path.dirname(loader_prgm), "pt_v2_loader.bin"),
    )
    return (loader_prgm, bridge_bin)


# Based on pinouts published by Alchitry Labs, latest commit 7a6bd06d133ee2033c34f2e89a751889329da12b
# https://github.com/alchitry/Alchitry-Labs-V2/blob/master/src/main/kotlin/com/alchitry/labs2/hardware/pinout/PtV2TopPin.kt
# https://github.com/alchitry/Alchitry-Labs-V2/blob/master/src/main/kotlin/com/alchitry/labs2/hardware/pinout/PtV2AlphaTopPin.kt
# https://github.com/alchitry/Alchitry-Labs-V2/blob/master/src/main/kotlin/com/alchitry/labs2/hardware/pinout/PtV2BottomPin.kt


class AlchitryPtV2Platform(XilinxPlatform):
    device = "xc7a100t"
    package = "fgg484"
    speed = "2"
    default_clk = "clk100"

    resources = [
        Resource(
            "clk100",
            0,
            Pins("W19", dir="i"),
            Clock(100e6),
            Attrs(IOSTANDARD="LVCMOS33"),
        ),
        Resource("rst_n", 0, Pins("N15", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("led", 0, Pins("P19", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("led", 1, Pins("P20", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("led", 2, Pins("T21", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("led", 3, Pins("R19", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("led", 4, Pins("V22", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("led", 5, Pins("U21", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("led", 6, Pins("T20", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("led", 7, Pins("W20", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        # FTDI USB Interface
        Resource(
            "usb",
            0,
            Subsignal("rx", Pins("AA20", dir="i")),
            Subsignal("tx", Pins("AA21", dir="o")),
            # Note: The following D pins have different banks
            Subsignal("d", Pins("W21 W22 Y21 Y22 F15 U7", dir="io")),  # D2-D7
            Subsignal("rxf_n", Pins("F21", dir="o")),  # RXF#
            Subsignal("txe_n", Pins("T3", dir="o")),  # TXE#
            Subsignal("rd_n", Pins("T16", dir="o")),  # RD#
            Subsignal("wr_n", Pins("U16", dir="o")),  # WR#
            Subsignal("siwua", Pins("Y17", dir="o")),  # SIWUA
            Attrs(IOSTANDARD="LVCMOS33"),
        ),
        # QSPI Flash
        Resource(
            "spi_flash",
            0,
            Subsignal("cs_n", Pins("T19", dir="o")),
            # CLK is on a dedicated clock pin, but used as a standard IO for SPI
            Subsignal("clk", Pins("L12", dir="o")),
            Subsignal("dq", Pins("P22 R22 P21 R21", dir="io")),  # D0, D1, D2, D3
            Attrs(IOSTANDARD="LVCMOS33"),
        ),
        # Analog differential pair (e.g., for XADC)
        Resource("vp_vn", 0, DiffPairs("L10", "M9", dir="i")),
        # DDR3 SDRAM
        Resource(
            "ddr3",
            0,
            Subsignal(
                "a",
                Pins(
                    "K14 M15 N18 K16 L14 K18 M13 L18 L13 M18 K13 L15 M16 L16", dir="o"
                ),
            ),
            Subsignal("ba", Pins("K19 N20 M20", dir="o")),
            Subsignal("cas_n", Pins("N22", dir="o")),
            Subsignal("cke", Pins("M22", dir="o")),
            Subsignal("clk", DiffPairs("K17", "J17", dir="o")),
            Subsignal("cs_n", Pins("N19", dir="o")),
            Subsignal("dm", Pins("H22 G13", dir="o")),
            Subsignal(
                "dq",
                Pins(
                    "J22 M21 L21 J20 H20 G20 J21 H19 H13 G18 J15 H17 G15 G17 G16 H15",
                    dir="io",
                ),
            ),
            Subsignal(
                "dqs",
                Subsignal("p", Pins("K21 J14", dir="io")),
                Subsignal("n", Pins("K22 H14", dir="io")),
            ),
            Subsignal("odt", Pins("M17", dir="o")),
            Subsignal("ras_n", Pins("L20", dir="o")),
            Subsignal("reset_n", Pins("J19", dir="o")),
            Subsignal("we_n", Pins("L19", dir="o")),
            Attrs(IOSTANDARD="SSTL135", SLEW="FAST"),
            Attrs(IOSTANDARD="DIFF_SSTL135", SLEW="FAST", on="clk"),
            Attrs(IOSTANDARD="DIFF_SSTL135", SLEW="FAST", on="dqs"),
        ),
    ]

    connectors = [
        Connector(
            "top_a",
            0,
            {
                "A3": "AB22",
                "A4": "AB18",
                "A5": "AB21",
                "A6": "AA18",
                "A9": "E3",
                "A10": "N2",
                "A11": "F3",
                "A12": "P2",
                "A15": "M2",
                "A16": "L1",
                "A17": "M3",
                "A18": "M1",
                "A21": "J6",
                "A22": "D2",
                "A23": "K6",
                "A24": "E2",
                "A27": "M5",
                "A28": "L4",
                "A29": "M6",
                "A30": "L5",
                "A33": "P4",
                "A34": "N5",
                "A35": "P5",
                "A36": "P6",
                "A39": "G4",
                "A40": "G3",
                "A41": "H4",
                "A42": "H3",
                "A45": "J4",
                "A46": "K3",
                "A47": "K4",
                "A48": "L3",
                "A51": "P1",
                "A52": "N3",
                "A53": "R1",
                "A54": "N4",
                "A57": "B2",
                "A58": "A1",
                "A59": "C2",
                "A60": "B1",
                "A63": "F1",
                "A64": "D1",
                "A65": "G1",
                "A66": "E1",
                "A69": "H5",
                "A70": "G2",
                "A71": "J5",
                "A72": "H2",
                "A75": "J1",
                "A76": "J2",
                "A77": "K1",
                "A78": "K2",
            },
        ),
        Connector(
            "top_c",
            0,
            {
                "C29": "U18",
                "C30": "Y1",
                "C31": "U17",
                "C32": "W1",
                "C33": "V2",
                "C34": "N14",
                "C35": "U2",
                "C36": "N13",
            },
        ),
        Connector(
            "bottom_a",
            0,
            {
                "A3": "AB1",
                "A4": "AA3",
                "A5": "AA1",
                "A6": "Y3",
                "A9": "D16",
                "A10": "A16",
                "A11": "E16",
                "A12": "A15",
                "A15": "A19",
                "A16": "A21",
                "A17": "A18",
                "A18": "B21",
                "A21": "C20",
                "A22": "D21",
                "A23": "D20",
                "A24": "E21",
                "A27": "B22",
                "A28": "D22",
                "A29": "C22",
                "A30": "E22",
                "A33": "B13",
                "A34": "A14",
                "A35": "C13",
                "A36": "A13",
                "A39": "C17",
                "A40": "B18",
                "A41": "D17",
                "A42": "B17",
                "A45": "C19",
                "A46": "D19",
                "A47": "C18",
                "A48": "E19",
                "A51": "F14",
                "A52": "B16",
                "A53": "F13",
                "A54": "B15",
                "A57": "E17",
                "A58": "F20",
                "A59": "F16",
                "A60": "F19",
                "A63": "E18",
                "A64": "A20",
                "A65": "F18",
                "A66": "B20",
                "A69": "G22",
                "A70": "C15",
                "A71": "G21",
                "A72": "C14",
                "A75": "D15",
                "A76": "E14",
                "A77": "D14",
                "A78": "E13",
            },
        ),
        Connector(
            "bottom_b",
            0,
            {
                "B3": "Y2",
                "B4": "AB6",
                "B5": "W2",
                "B6": "AB7",
                "B9": "Y7",
                "B10": "AB8",
                "B11": "Y8",
                "B12": "AA8",
                "B15": "AA6",
                "B16": "AB5",
                "B17": "Y6",
                "B18": "AA5",
                "B21": "AB2",
                "B22": "Y9",
                "B23": "AB3",
                "B24": "W9",
                "B27": "T6",
                "B28": "W7",
                "B29": "R6",
                "B30": "V7",
                "B33": "V8",
                "B34": "V5",
                "B35": "V9",
                "B36": "U6",
                "B39": "W4",
                "B40": "AA4",
                "B41": "V4",
                "B42": "Y4",
                "B45": "T4",
                "B46": "U5",
                "B47": "R4",
                "B48": "T5",
                "B51": "E10",
                "B52": "E6",
                "B53": "F10",
                "B54": "F6",
                "B57": "C7",
                "B58": "C11",
                "B59": "D7",
                "B60": "D11",
                "B63": "A6",
                "B64": "A10",
                "B65": "B6",
                "B66": "B10",
                "B69": "C5",
                "B70": "C9",
                "B71": "D5",
                "B72": "D9",
                "B75": "A4",
                "B76": "A8",
                "B77": "B4",
                "B78": "B8",
            },
        ),
        Connector(
            "bottom_c",
            0,
            {
                "C29": "U1",
                "C30": "W5",
                "C31": "T1",
                "C32": "W6",
                "C33": "R2",
                "C34": "V3",
                "C35": "R3",
                "C36": "U3",
            },
        ),
        Connector(
            "top_b",
            0,
            {
                "B3": "R14",
                "B4": "R16",
                "B5": "P14",
                "B6": "P15",
                "B9": "R17",
                "B10": "P17",
                "B11": "P16",
                "B12": "N17",
                "B15": "W17",
                "B16": "T18",
                "B17": "V17",
                "B18": "R18",
                "B21": "AB20",
                "B22": "V19",
                "B23": "AA19",
                "B24": "V18",
                "B27": "Y19",
                "B28": "V20",
                "B29": "Y18",
                "B30": "U20",
                "B33": "AB10",
                "B34": "AB15",
                "B35": "AA9",
                "B36": "AA15",
                "B39": "W12",
                "B40": "Y12",
                "B41": "W11",
                "B42": "Y11",
                "B45": "V14",
                "B46": "V15",
                "B47": "V13",
                "B48": "U15",
                "B51": "W10",
                "B52": "AB17",
                "B53": "V10",
                "B54": "AB16",
                "B57": "AB12",
                "B58": "AA16",
                "B59": "AB11",
                "B60": "Y16",
                "B63": "AA11",
                "B64": "T15",
                "B65": "AA10",
                "B66": "T14",
                "B69": "AB13",
                "B70": "Y14",
                "B71": "AA13",
                "B72": "W14",
                "B75": "AA14",
                "B76": "W16",
                "B77": "Y13",
                "B78": "W15",
            },
        ),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toolchain_program(self, products, name):
        (loader, bridge_bin) = find_loader()
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call(
                [loader, "-e", "-f", bitstream_filename, "-p", bridge_bin]
            )


if __name__ == "__main__":
    from .test.blinky import Blinky

    AlchitryPtV2Platform().build(Blinky(), do_program=True)
