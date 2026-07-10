from SyncFIFO import DUTSyncFIFO


def test_reset_dut():
    # 实例化 DUT 并初始化时钟
    dut = DUTSyncFIFO()
    dut.InitClock("clk")
    dut.rst_n.AsImmWrite()
    
    # 复位信号
    dut.rst_n.value = 1
    dut.Step(1)
    dut.rst_n.value = 0
    dut.Step(1)

    # 写入数据
    dut.rst_n.value = 0
    dut.Step(5)
    dut.rst_n.value = 1
    dut.Step(2)
    dut.Step()

    assert dut.data_o.value == 0, "data_o.value is not 0"
    assert dut.full_o.value == 0, "full_o.value is not 0"
    assert dut.empty_o.value == 1, "empty_o.value is not 1"

    assert dut.GetInternalSignal("SyncFIFO.wptr", use_vpi=True).value == 0, "wptr.value is not 0"
    assert dut.GetInternalSignal("SyncFIFO.rptr", use_vpi=True).value == 0, "rptr.value is not 0"
    assert dut.GetInternalSignal("SyncFIFO.counter", use_vpi=True).value == 0, "counter.value is not 0"
    print(f"\n ======================================================")
    dut.Finish()

def test_smoke_dut():
    # 实例化 DUT 并初始化时钟
    dut = DUTSyncFIFO()
    dut.InitClock("clk")
    
    # 复位信号
    dut.rst_n.value = 0
    dut.Step(1)
    dut.rst_n.value = 1
    dut.Step(2)

    # 写入数据
    dut.we_i.value = 1
    dut.data_i.value = 0x114
    dut.Step(1)

    dut.we_i.value = 1
    dut.data_i.value = 0x514
    dut.Step(1)

    print(f"\nempty_o.value: {dut.empty_o.value}, expected: 0")
    print(f"full_o.value: {dut.full_o.value}, expected: 0")
    assert dut.empty_o.value == 0, "empty_o.value is not 0"
    assert dut.full_o.value == 0, "full_o.value is not 0"

    dut.we_i.value = 0
    dut.Step(1)

    # 读出数据
    dut.re_i.value = 1
    dut.Step(2)

    print(f"data_o.value: {dut.data_o.value}, expected: 0x114")
    assert dut.data_o.value == 0x114, "data_o.value is not 0x114"

    dut.Step(1)
    print(f"data_o.value: {dut.data_o.value}, expected: 0x514")
    assert dut.data_o.value == 0x514, "data_o.value is not 0x514"
    assert dut.empty_o.value == 1, "empty_o.value is not 1"

    print("======================================================")
    dut.Finish()

if __name__ == "__main__":
    # test_reset_dut()

    test_smoke_dut()