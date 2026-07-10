try:
    from UT_SyncFIFO import *
except:
    try:
        from SyncFIFO import *
    except:
        from __init__ import *


if __name__ == "__main__":
    dut = DUTSyncFIFO()
    # dut.InitClock("clk")

    dut.Step(1)

    dut.Finish()
