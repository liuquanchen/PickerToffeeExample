try:
    from UT_Adder import *
except:
    try:
        from Adder import *
    except:
        from __init__ import *


if __name__ == "__main__":
    dut = DUTAdder()
    # dut.InitClock("clk")

    dut.Step(1)

    dut.Finish()
