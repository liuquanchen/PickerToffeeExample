#!/usr/bin/env
try:
    from UT_RandomGenerator import *
except:
    try:
        from RandomGenerator import *
    except:
        from __init__ import *

import random

def lfsr_next(val):
    """Reference model: 16-bit LFSR with feedback = bit15 XOR bit14"""
    feedback = ((val >> 15) ^ (val >> 14)) & 1
    return ((val << 1) | feedback) & 0xFFFF

def main():
    dut = DUTRandomGenerator()
    dut.InitClock("clk")
    seed = random.randint(0, 0xFFFF)
    dut.seed.value = seed
    ref_val = seed
    dut.RefreshComb()

    # ==================== Reset Phase ====================
    dut.reset.value = 1
    dut.Step(1)                    # hold reset for several cycles
    dut.reset.value = 0
    dut.Step(1)                    # wait for reset to fully propagate

    # ==================== Test Phase ====================
    for i in range(65536):
        dut.Step(1)
        ref_val = lfsr_next(ref_val)
        dut_val = dut.random_number.value
        assert dut_val == ref_val, \
            f"Cycle {cycle+1}: DUT=0x{dut_val:04x}, REF=0x{ref_val:04x} mismatch"
        print(f"Cycle {i}, DUT: {dut_val:x}, REF: {ref_val:x}")

    print("===============================================")
    print(f"TEST PASS! seed=0x{seed:04x}")
    dut.Finish()

if __name__ == "__main__":
    main()
