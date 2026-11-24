from amaranth.build import *
from amaranth.vendor import LatticeECP5Platform

from .resources import *


__all__ = ["ButterStickPlatform"]


class ButterStickPlatform(LatticeECP5Platform):
    """
    This platform does not have VIO voltages enabled by default; you are
    required to provide gateware that implements a sigma-delta DAC in
    order to set the IO voltage and enable the regulators. Example gateware
    that implements what is needed follows below:

    ```python
    import math
    from amaranth import *
    from amaranth.lib import wiring

    class ButterStckVCCIOCtl(wiring.Component):
        def __init__(self, *, vccioa: float, vcciob: float, vccioc: float):
            assert vccioa >= 1.0 and vccioa <= 3.3
            assert vcciob >= 1.0 and vcciob <= 3.3
            assert vccioc >= 1.8 and vccioc <= 3.3 # ULPI Phy specs min 1.8V

            self._vccioa = vccioa
            self._vcciob = vcciob
            self._vccioc = vccioc

            super().__init__({
                "power_good": wiring.Out(1)
            })


        def _control_voltage(self, vcc_out):
            Vfb = 0.6          # Controlloop feedback voltage
            Ri = 68_000        # Current Injection Resistor
            Rf = 53_600        # Feedback Resistor
            Rs = 13_000        # Set Resistor
            I_total = Vfb / Rs # Current through set resistor

            # The bank IO voltage is set by a buck converter with current
            # injected by a sigma-delta DAC driven by the FPGA.
            #
            # The buck holds the output such that the voltage on the feedback
            # node is equal to its internal reference of 0.6V; this gives a fixed
            # current I_total through the set resistor of 13kOhm of:
            # I_total = Vfb / Rs
            #
            # The current from the sigma delta DAC that flows through the set resistor
            # is given by:
            # I_injected = (vctl - Vfb) / Ri
            #
            # The current flowing through the feedback resistor Rf is then given by:
            # I_feedback = I_total - I_injected
            #
            # Which sets the output voltage to be:
            # vcc_out = I_feedback * Rf
            #
            # Rearanging all this and solving for vctl in terms of vcc_out we get:
            vctl = Vfb * (1 + Ri / Rf) + Ri * I_total - (Ri / Rf) * vcc_out
            assert vctl >= 0.0 and vctl <= 3.3

            return vctl


        def elaborate(self, platform):
            m = Module()
            sd_counter = Signal(10)
            m.d.sync += sd_counter.eq(sd_counter + 1)


            clk_freq = platform.default_clk_frequency
            sd_cutoff = 1 / (2 * math.pi * 68_000 * 0.1e-6)

            assert clk_freq / (1 << len(sd_counter)) > 4 * sd_cutoff, "PWM Frequency should be >> Sigma Delta Cutoff Frequency"

            control = platform.request("vccio_ctrl")
            for i, vccio in enumerate([self._vccioa, self._vcciob, self._vccioc]):
                vctl = self._control_voltage(vccio)
                frac = vctl / 3.3
                assert frac > 0 and frac < 1

                timer_val = int(frac * (1 << len(sd_counter)))
                m.d.sync += control.pdm.o[i].eq(sd_counter < timer_val)

            # Datasheet gives a ~1ms start time
            soft_cycles = int(0.001 * clk_freq)
            boot_cycles = int(4 * (1 / sd_cutoff) * clk_freq)
            boot_counter = Signal(range(boot_cycles + soft_cycles + 1))
            m.d.sync += boot_counter.eq(boot_counter + 1)
            with m.If(boot_counter >= boot_cycles - 1):
                m.d.sync += control.en.o.eq(1)
            with m.If(boot_counter >= (boot_cycles + soft_cycles - 1)):
                m.d.sync += self.power_good.eq(1)

            return m
    ```
    """


    device      = "LFE5UM5G-85F"
    package     = "BG381"
    speed       = "8"
    default_clk = "clk30"

    def __init__(self, *, VCCIOA=None, VCCIOB=None, VCCIOC=None, **kwargs):
        super().__init__(**kwargs)
        # labeled VIO0 on silk
        assert VCCIOA in ("3V3", "2V5", "1V8", "1V5", "1V2", None)
        # labeled VIO1 on silk
        assert VCCIOB in ("3V3", "2V5", "1V8", "1V5", "1V2", None)
        # labaled VIO3 on silk
        assert VCCIOC in ("3V3", "2V5", "1V8", None) # ULPI Phy specs min 1.8V

        self._VCCIOA = VCCIOA
        self._VCCIOB = VCCIOB
        self._VCCIOC = VCCIOC

    def _vccio_to_iostandard(self, vccio):
        if vccio == "1V2":
            return "LVCMOS12"
        if vccio == "1V5":
            return "LVCMOS15"
        if vccio == "1V8":
            return "LVCMOS25"
        if vccio == "2V5":
            return "LVCMOS25"
        if vccio == "3V3":
            return "LVCMOS33"
        assert False

    def syzygya_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIOA)

    def syzygyb_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIOB)

    def syzygyc_iostandard(self):
        return self._vccio_to_iostandard(self._VCCIOC)

    resources   = [
        Resource("clk30", 0, Pins("B12", dir="i"),
                 Clock(30e6), Attrs(IO_TYPE="LVCMOS33")),

        # RGB LEDs don't really match the standard expectation
        Resource("rgb_leds_muxed", 0,
            Subsignal("leds", Pins("C13 D12 U2 T3 D13 E13 C16")),
            Subsignal("r", Pins("T1")),
            Subsignal("g", Pins("U1")),
            Subsignal("b", Pins("R1")),
            Attrs(IO_TYPE="LVCMOS33"),
        ),

        *ButtonResources(
            pins={0: "U16", 1: "T17" }, invert=True,
            attrs=Attrs(IO_TYPE="SSTL135_I")),

        *SPIFlashResources(0,
            cs_n="R2", clk="U3", cipo="V2", copi="W2", wp_n="Y2", hold_n="W1",
            attrs=Attrs(IO_TYPE="LVCMOS33"),
        ),

        *SDCardResources(0,
            clk="B13", cmd="A13", dat0="C12", dat1="A12", dat2="D14", dat3="A14", cd="B15",
            attrs=Attrs(IO_TYPE="LVCMOS33"),
        ),

        DDR3Resource(0,
            rst_n = "E17", clk_p="C20 J19", clk_n="D19 K19", clk_en="F18 J18", cs_n="J20 J16", we_n="G19", ras_n="K18", cas_n="J17",
            a="G16 E19 E20 F16 F19 E16 F17 L20 M20 E18 G18 D18 H18 C18 D17 G20",
            ba="H16 F20 H20",
            dqs_p="T19 N16", dqs_n="R18 M17",
            dq="U19 T18 U18 R20 P18 P19 P20 N20 L19 L17 L16 R16 N18 R17 N17 P17",
            dm="U20 L18", odt="K20 H17",
            diff_attrs=Attrs(IO_TYPE="SSTL135D_I", TERMINATION="OFF", DIFFRESISTOR="100"),
            attrs=Attrs(IO_TYPE="SSTL135_I")
        ),

        Resource("eth_rgmii", 0,
            Subsignal("rst",     PinsN("B20", dir="o")),
            Subsignal("mdc",     Pins("A19", dir="o")),
            Subsignal("mdio",    Pins("D16", dir="io")),
            Subsignal("tx_clk",  Pins("E15", dir="o")),
            Subsignal("tx_ctl",  Pins("D15", dir="o")),
            Subsignal("tx_data", Pins("C15 B16 A18 B19", dir="o")),
            Subsignal("rx_clk",  Pins("D11", dir="i")),
            Subsignal("rx_ctl",  Pins("B18", dir="i")),
            Subsignal("rx_data", Pins("A16 C17 B17 A17", dir="i")),
            Attrs(IO_TYPE="LVCMOS33")
        ),

        ULPIResource(0, data="B9 C6 A7 E9 A8 D9 C10 C7",
                     rst="C9", clk="B6", dir="A6", stp="C8", nxt="B8",
                     clk_dir="o", rst_invert=True, attrs=Attrs(IO_TYPE=syzygyc_iostandard)),

        I2CResource(0, scl="E14", sda="C14",
                    attrs=Attrs(IO_TYPE="LVCMOS33")),

        # SYGYZY VIO level control pwm pins (use with care)
        Resource("vccio_ctrl", 0,
                 Subsignal("pdm", Pins("V1 E11 T2", dir="o")),
                 Subsignal("en", Pins("E12", dir="o")),
                 Attrs(IO_TYPE="LVCMOS33")
        ),

        # Used to reload FPGA configuration (drives program_n)
        Resource("program", 0, PinsN("R3", dir="o"), Attrs(IO_TYPE="LVCMOS33")),
    ]

    connectors = [
        Connector("syzygy", 0, {
            # single ended
            "S0":  "G2", "S1":  "J3",
            "S2":  "F1", "S3":  "K3",
            "S4":  "J4", "S5":  "K2",
            "S6":  "J5", "S7":  "J1",
            "S8":  "N2", "S9":  "L3",
            "S10": "M1", "S11": "L2",
            "S12": "N3", "S13": "N4",
            "S14": "M3", "S15": "P5",
            "S16": "H1", "S17": "K5",
            "S18": "K4", "S19": "K1",
            "S20": "L4", "S21": "L1",
            "S22": "L5", "S23": "M4",
            "S24": "N1", "S25": "N5",
            "S26": "P3", "S27": "P4",
            "S28": "H2", "S29": "P1",
            "S30": "G1", "S31": "P2",

            # diff pairs
            "D0P": "G2", "D0N": "D5",
            "D1P": "F1", "D1N": "K3",
            "D2P": "J4", "D2N": "J5",
            "D3P": "K2", "D3N": "J1",
            "D4P": "A2", "D4N": "B1",
            "D5P": "L3", "D5N": "L2",
            "D6P": "N3", "D6N": "M3",
            "D7P": "N4", "D7N": "P5",

            # clock pairs
            "C2PP":"P1", "C2PN":"P2",
            "P2CP":"H2", "P2CN":"G1",
        }),

        Connector("syzygy", 1, {
            # single ended
            "S0":  "E4", "S1":  "A4",
            "S2":  "D5", "S3":  "A5",
            "S4":  "C4", "S5":  "B2",
            "S6":  "B4", "S7":  "C2",
            "S8":  "A2", "S9":  "C1",
            "S10": "B1", "S11": "D1",
            "S12": "F4", "S13": "D2",
            "S14": "E3", "S15": "E1",
            "S16": "B5", "S17": "E5",
            "S18": "F5", "S19": "C5",
            "S20": "B3", "S21": "A3",
            "S22": "D3", "S23": "C3",
            "S24": "H5", "S25": "G5",
            "S26": "H3", "S27": "H4",
            "S28": "F2", "S29": "G3",
            "S30": "E2", "S31": "F3",

            # diff pairs
            "D0P": "E4", "D0N": "D5",
            "D1P": "A4", "D1N": "A5",
            "D2P": "C4", "D2N": "B4",
            "D3P": "B2", "D3N": "C2",
            "D4P": "A2", "D4N": "B1",
            "D5P": "C1", "D5N": "D1",
            "D6P": "F4", "D6N": "E3",
            "D7P": "D2", "D7N": "E1",

            # clock pairs
            "C2PP":"G3", "C2PN":"F3",
            "P2CP":"F2", "P2CN":"E2",
        }),

        # Note: pairs 2 and 3 of both TX and RX are swapped in the schematic
        # with respect to what is in the spec. The spec numbering is what us
        # used here
        Connector("syzygy-txr", 0, {
            # DCU pairs
            "RX0P": "Y5",  "RX0N": "Y6",
            "RX1P": "Y7",  "RX1N": "Y8",
            "RX2P": "Y16", "RX2N": "Y17",
            "RX3P": "Y14", "RX3N": "Y15",
            "TX0P": "W4",  "TX0N": "W5",
            "TX1P": "W8",  "TX1N": "W9",
            "TX2P": "W17", "TX2N": "W18",
            "TX3P": "W13", "TX3N": "W14",
            "REFP": "Y11", "REFN": "Y12",

            # single ended
            "S0":   "C11", "S1":   "B11",
            "S2":   "D6",  "S3":   "D7",
            "S4":   "E6",  "S5":   "E7",
            "S6":   "D8",  "S7":   "E8",
            "S8":   "E10", "S9":   "D10",
            "S10":  "A10", "S11":  "A9",
            "S12":  "A11", "S13":  "B10",

            # clock pairs
            "C2PP":  "A9", "C2PN": "B10",
            "P2CP": "A10", "P2CN": "A11",
        })
    ]
