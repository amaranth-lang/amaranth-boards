import os
import shutil
import subprocess

from amaranth.build import *
from amaranth.vendor import XilinxPlatform
from .resources import *


__all__ = ["AlchitryPtV2Platform", "AlchitryPtV2AlphaPlatform"]


def find_loader():
    alchitry_cmd = os.environ.get("ALCHITRY_CLI", shutil.which("alchitry"))
    if alchitry_cmd is None:
        raise EnvironmentError(
            "Could not find the alchitry command line program, either "
            "place it in the path or specify a location via the "
            "ALCHITRY_CLI environment variable."
        )
    return alchitry_cmd


alpha_top_connectors = [
    Connector(
        "alchitry_a", 0,
        "-    -    AB22 AB18 AB21 AA18 -    -    E3   N2   F3   P2   -    -    M2   L1   M3   M1   -    -    "
        "J6   D2   K6   E2   -    -    M5   L4   M6   L5   -    -    P4   N5   P5   P6   -    -    G4   G3   "
        "H4   H3   -    -    J4   K3   K4   L3   -    -    P1   N3   R1   N4   -    -    B2   A1   C2   B1   "
        "-    -    F1   D1   G1   E1   -    -    H5   G2   J5   H2   -    -    J1   J2   K1   K2   -    -    "
    ),
    Connector(
        "alchitry_b", 0,
        "-    -    AB13 AA11 AA13 AA10 -    -    AB12 Y14  AB11 W14  -    -    AB15 W16  AA15 W15  -    -    "
        "AB17 V19  AB16 V18  -    -    Y19  V20  Y18  U20  -    -    AB10 W10  AA9  V10  -    -    W12  Y12  "
        "W11  Y11  -    -    V14  V15  V13  U15  -    -    AB20 AA16 AA19 Y16  -    -    W17  T15  V17  T14  "
        "-    -    AA14 R16  Y13  P15  -    -    R17  T18  P16  R18  -    -    N14  P17  N13  N17  -    -    "
    ),
    Connector(
        "alchitry_c", 0,
        "-    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    "
        "-    -    -    -    -    -    -    -    U18  Y1   U17  W1   V2   R14  U2   P14  -    -    -    -    "
    ),
]


top_connectors = [
    Connector(
        "alchitry_a", 0,
        "-    -    AB22 AB18 AB21 AA18 -    -    E3   N2   F3   P2   -    -    M2   L1   M3   M1   -    -    "
        "J6   D2   K6   E2   -    -    M5   L4   M6   L5   -    -    P4   N5   P5   P6   -    -    G4   G3   "
        "H4   H3   -    -    J4   K3   K4   L3   -    -    P1   N3   R1   N4   -    -    B2   A1   C2   B1   "
        "-    -    F1   D1   G1   E1   -    -    H5   G2   J5   H2   -    -    J1   J2   K1   K2   -    -    "
    ),
    Connector(
        "alchitry_b", 0,
        "-    -    R14  R16  P14  P15  -    -    R17  P17  P16  N17  -    -    W17  T18  V17  R18  -    -    "
        "AB20 V19  AA19 V18  -    -    Y19  V20  Y18  U20  -    -    AB10 AB15 AA9  AA15 -    -    W12  Y12  "
        "W11  Y11  -    -    V14  V15  V13  U15  -    -    W10  AB17 V10  AB16 -    -    AB12 AA16 AB11 Y16  "
        "-    -    AA11 T15  AA10 T14  -    -    AB13 Y14  AA13 W14  -    -    AA14 W16  Y13  W15  -    -    "
    ),
    Connector(
        "alchitry_c", 0,
        "-    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    "
        "-    -    -    -    -    -    -    -    U18  Y1   U17  W1   V2   N14  U2   N13  -    -    -    -    "
    ),
]


bottom_connectors = [
    Connector(
        "alchitry_a", 1,
        "-    -    AB13 AA11 AA13 AA10 -    -    AB12 Y14  AB11 W14  -    -    AB15 W16  AA15 W15  -    -    "
        "AB17 V19  AB16 V18  -    -    Y19  V20  Y18  U20  -    -    AB10 W10  AA9  V10  -    -    W12  Y12  "
        "W11  Y11  -    -    V14  V15  V13  U15  -    -    AB20 AA16 AA19 Y16  -    -    W17  T15  V17  T14  "
        "-    -    AA14 R16  Y13  P15  -    -    R17  T18  P16  R18  -    -    N14  P17  N13  N17  -    -    "
    ),
    Connector(
        "alchitry_b", 1,
        "-    -    Y2   AB6  W2   AB7  -    -    Y7   AB8  Y8   AA8  -    -    AA6  AB5  Y6   AA5  -    -    "
        "AB2  Y9   AB3  W9   -    -    T6   W7   R6   V7   -    -    V8   V5   V9   U6   -    -    W4   AA4  "
        "V4   Y4   -    -    T4   U5   R4   T5   -    -    E10  E6   F10  F6   -    -    C7   C11  D7   D11  "
        "-    -    A6   A10  B6   B10  -    -    C5   C9   D5   D9   -    -    A4   A8   B4   B8   -    -    "
    ),
    Connector(
        "alchitry_c", 1,
        "-    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    "
        "-    -    -    -    -    -    -    -    U1   W5   T1   W6   R2   V3   R3   U3   -    -    -    -    "
    ),
]


class AlchitryPtV2Platform(XilinxPlatform):
    device = "xc7a100t"
    package = "fgg484"
    speed = "2"
    default_clk = "clk100"
    default_rst = "rst"

    resources = [
        Resource(
            "clk100", 0, Pins("W19", dir="i"),
            Clock(100e6), Attrs(IOSTANDARD="LVCMOS33"),
        ),
        Resource("rst", 0, PinsN("N15", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        # Connected to the onboard FT2232HQ (This and the FIFO are mutually exclusive)
        UARTResource(0, rx="AA20", tx="AA21", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        # Connected to the onboard FT2232HQ (This and the UART are mutually exclusive)
        Resource("ftdi_fifo_async", 0,
            Subsignal("d", Pins("AA20 AA21 W21  W22  Y21  Y22  F15  U7", dir="io")),
            Subsignal("rxf", PinsN("F21", dir="i")),
            Subsignal("txe", PinsN("T3", dir="i")),
            Subsignal("rd", PinsN("T16", dir="o")),
            Subsignal("wr", PinsN("U16", dir="o")),
            Subsignal("siwu", Pins("U16", dir="o")),
            Attrs(IO_STANDARD="LVCMOS33")
        ),

        # Connected to the onboard LED array
        *LEDResources(pins="P19  P20  T21  R19  V22  U21  T20  W20", attrs=Attrs(IOSTANDARD="LVCMOS33")),
        # NOTE: This is also the config flash so don't blow it away
        *SPIFlashResources(0,
            cs_n="T19", clk="L12", copi="P22", cipo="R22", wp_n="P21", hold_n="R21",
            attrs=Attrs(IO_STANDARD="LVCMOS33"),
        ),
        # Connected to the QWIIC connector, not called out in the official pinout
        I2CResource(0, scl="F4", sda="L6", attrs=Attrs(IO_STANDARD="LVCMOS33")),

        # TODO: Currently untested
        DDR3Resource(0,
            rst_n="J19", clk_p="K17", clk_n="J17", clk_en="M22", cs_n="N16", we_n="L19", ras_n="L20", cas_n="N22",
            a="K14  M15  N18  K16  L14  K18  M13  L18  L13  M18  K13  L15  M16  L16",
            ba="K19  N20  M20",
            dqs_p="K21  J14", dqs_n="K22  H14",
            dq="J22  M21  L21  J20  H20  G20  J21  H19  H13  G18  J15  H17  G15  G17  G16  H15",
            dm="H22  G13", odt="M17",
            diff_attrs=Attrs(IOSTANDARD="LVDS"),
            attrs=Attrs(IOSTANDARD="LVCMOS15")
        ),
    ]
    connectors = top_connectors + bottom_connectors

    # Programming with QSPI flash on a part this size is painful
    # without bitstream compression
    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_before_bitstream":
                "set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]\n"
                "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    # TODO: Support vivado and openocd for programming
    def toolchain_program(self, products, name, *, flash=True):
        loader = find_loader()
        with products.extract(f"{name}.bin") as bitstream_filename:
            subprocess.check_call([
                loader, "load", "--board", "PtV2", "--bin",
                bitstream_filename, "--flash" if flash else "--ram"
            ])


class AlchitryPtV2AlphaPlatform(AlchitryPtV2Platform):
    connectors = alpha_top_connectors + bottom_connectors


if __name__ == "__main__":
    from amaranth_boards.test.blinky import Blinky
    AlchitryPtV2Platform().build(Blinky(), do_program=True)
