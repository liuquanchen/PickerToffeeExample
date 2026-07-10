from SyncFIFO import DUTSyncFIFO
import toffee_test
import toffee

@toffee_test.testcase
async def test_smoke_dut(dut: DUTSyncFIFO):
    # 复位信号
    dut.rst_n.value = 0
    await dut.AStep(1)
    dut.rst_n.value = 1
    await dut.AStep(1)

    # 写入数据
    dut.we_i.value = 1
    dut.data_i.value = 0x114
    await dut.AStep(1)

    dut.we_i.value = 1
    dut.data_i.value = 0x514
    await dut.AStep(1)

    assert dut.empty_o.value == 0, "empty_o.value is not 0"
    assert dut.full_o.value == 0, "full_o.value is not 0"

    dut.we_i.value = 0

    # 读出数据
    dut.re_i.value = 1
    await dut.AStep(2)

    assert dut.data_o.value == 0x114, "data_o.value is not 0x114"

    await dut.AStep(1)
    assert dut.data_o.value == 0x514, "data_o.value is not 0x514"
    assert dut.empty_o.value == 1, "empty_o.value is not 1"

    print("======================================================")

@toffee_test.fixture
async def dut(toffee_request: toffee_test.ToffeeRequest):
    # 使用toffee创建DUT并绑定时钟
    dut = toffee_request.create_dut(DUTSyncFIFO, "clk")

    # 让toffee驱动时钟，只能在异步函数中调用
    toffee.start_clock(dut)
    return dut