from SyncFIFO import DUTSyncFIFO
import toffee_test
import toffee
from Bundle import SyncFIFOBundle


@toffee_test.testcase
async def test_bundle(dut: DUTSyncFIFO):

    fifo_bundle = SyncFIFOBundle()
    fifo_bundle.bind(dut)

    # 复位信号
    fifo_bundle.status.rst_n.value = 0
    await dut.AStep(1)
    fifo_bundle.status.rst_n.value = 1
    await dut.AStep(1)

    # 写入数据
    await fifo_bundle.write.enqueue(0x114)
    await fifo_bundle.write.enqueue(0x514)

    assert fifo_bundle.status.empty_o.value == 0, "empty_o.value is not 0"
    assert fifo_bundle.status.full_o.value == 0, "full_o.value is not 0"

    # 读出数据
    await fifo_bundle.read.dequeue()
    await fifo_bundle.read.dequeue()

    assert fifo_bundle.read.data_o.value == 0x114, "data_o.value is not 0x114"

    await dut.AStep(1)
    assert fifo_bundle.read.data_o.value == 0x514, "data_o.value is not 0x514"
    assert fifo_bundle.status.empty_o.value == 1, "empty_o.value is not 1"

    print(f"\n ======================================================")

@toffee_test.testcase
async def test_full_empty(dut:DUTSyncFIFO):
    
    fifo_bundle = SyncFIFOBundle()
    fifo_bundle.bind(dut)

    # 复位信号
    fifo_bundle.status.rst_n.value = 0
    await dut.AStep(1)
    fifo_bundle.status.rst_n.value = 1
    await dut.AStep(1)

    # 准备 16 个测试数据
    write_data = [0x100 + i for i in range(16)]  # 0x100, 0x101, ..., 0x10F
    read_data = []

    # 写入数据(写满)
    for data in write_data:
        await fifo_bundle.write.enqueue(data)

    await dut.AStep(1)
    assert fifo_bundle.status.full_o.value == 1, f"full_o.value is not 1"


    # 读出数据(清空)    
    for i in range(16):
        await fifo_bundle.read.dequeue()
        if i > 0:
            print(f"read_data: {fifo_bundle.read.data_o.value}")
            read_data.append(fifo_bundle.read.data_o.value)

    await dut.AStep(1)
    print(f"read_data: {fifo_bundle.read.data_o.value}")
    read_data.append(fifo_bundle.read.data_o.value)

    assert fifo_bundle.status.empty_o.value == 1, f"empty_o.value is not 1, got {fifo_bundle.status.empty_o.value}"
    for i in range(16):
        assert read_data[i] == write_data[i], f"Data mismatch at index {i}: expected 0x{write_data[i]:X}, got 0x{read_data[i]:X}"

    print(f"\n ======================================================")


@toffee_test.fixture
async def dut(toffee_request: toffee_test.ToffeeRequest):
    # 使用toffee创建DUT并绑定时钟
    dut = toffee_request.create_dut(DUTSyncFIFO, "clk")

    # 让toffee驱动时钟，只能在异步函数中调用
    toffee.start_clock(dut)
    return dut
