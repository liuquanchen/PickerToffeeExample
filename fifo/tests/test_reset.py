from agent import FIFOAgent
from Bundle import SyncFIFOBundle, InternalBundle
from SyncFIFO import DUTSyncFIFO
from toffee import Executor
from toffee.funcov import CovGroup
import random
import toffee_test
import toffee 
from toffee import create_task, Value

"""
Test cases
"""

@toffee_test.testcase
async def test_reset(fifo_agent):

    # init
    await fifo_agent.reset()

    # RST-01: 随机读写 15 次后，执行复位操作，
    for i in range(15):
        print(f"Cycle{i}:")
        if random.randint(0, 3) == 0:
            await fifo_agent.dequeue()
            print(f"dequeue")
        else:
            await fifo_agent.enqueue(i+10)
            print(f"enqueue {i+10}")

    await fifo_agent.bundle.step()
    assert fifo_agent.internal.counter.value !=0, "counter is 0"

    fifo_agent.status.rst_n.value = 0
    await fifo_agent.bundle.step(2)
    assert fifo_agent.read.data_o.value   == 0, "data_o is not 0"
    assert fifo_agent.internal.wptr.value == 0, "wptr value is not 0"
    assert fifo_agent.internal.rptr.value == 0, "rpte value is not 0"
    assert fifo_agent.internal.counter.value == 0, "counter is not 0"

    # RST-02：保存复位 5 个周期
    fifo_agent.status.rst_n.value = 0
    await fifo_agent.bundle.step(6)
    assert fifo_agent.read.data_o.value   == 0, "data_o is not 0"
    assert fifo_agent.internal.wptr.value == 0, "wptr value is not 0"
    assert fifo_agent.internal.rptr.value == 0, "rpte value is not 0"
    assert fifo_agent.internal.counter.value == 0, "counter is not 0"

    # RST-03：释放复位，检测是否保持状态不变
    fifo_agent.status.rst_n.value = 1
    await fifo_agent.bundle.step(6)
    assert fifo_agent.read.data_o.value   == 0, "data_o is not 0"
    assert fifo_agent.internal.wptr.value == 0, "wptr value is not 0"
    assert fifo_agent.internal.rptr.value == 0, "rpte value is not 0"
    assert fifo_agent.internal.counter.value == 0, "counter is not 0"

"""
Coverage definition
"""
def get_cover_group_fifo_state(agent: FIFOAgent) -> CovGroup:

    def check_reset_operation(bundle: InternalBundle):   # 参数是 InternalBundle
        return (bundle.wptr.value == 0 and
                bundle.rptr.value == 0 and
                bundle.counter.value == 0)

    def check_reset_hold(bundle: InternalBundle):
        return (bundle.wptr.value == 0 and
                bundle.rptr.value == 0 and
                bundle.counter.value == 0)

    def check_reset_release(bundle: InternalBundle):
        return (bundle.wptr.value == 0 and
                bundle.rptr.value == 0 and
                bundle.counter.value == 0)


    # 创建一个名为 "FIFO state" 的覆盖组
    group = CovGroup("FIFO state")

    # ... 在这里添加覆盖点 ...
    group.add_watch_point(agent.internal, {"event": check_reset_operation}, name="RST-01")
    group.add_watch_point(agent.internal, {"event": check_reset_hold}, name="RST-02")
    group.add_watch_point(agent.internal, {"event": check_reset_release}, name="RST-03")
    return group


"""
Initialize before each test
"""

@toffee_test.fixture
async def fifo_agent(toffee_request: toffee_test.ToffeeRequest):
    # Creat DUT
    dut = toffee_request.create_dut(DUTSyncFIFO, "clk")
    
    # Start clock
    toffee.start_clock(dut)

    # Create Bundles
    fifo_bundle = SyncFIFOBundle()
    fifo_internal_bundle = InternalBundle(
        wptr=dut.GetInternalSignal("SyncFIFO.wptr", use_vpi=True),
        rptr=dut.GetInternalSignal("SyncFIFO.rptr", use_vpi=True),
        counter=dut.GetInternalSignal("SyncFIFO.counter", use_vpi=True),
    )

    # Bind FIFO Bundle to DUT
    fifo_bundle.bind(dut)                                                 

    # Create Agent
    fifo_agent = FIFOAgent(fifo_bundle, fifo_internal_bundle)

    # Add Custom Group
    cover_reset = [get_cover_group_fifo_state(fifo_agent)]

    # Async Func
    async def Reset_Sequence():
        await dut.ACondition(
            lambda: fifo_agent.status.rst_n.value == 0 
                    and 0 < fifo_agent.internal.counter.value < 16
        )

        await dut.ACondition(
            lambda: fifo_agent.internal.counter.value == 0
                    and fifo_agent.internal.wptr.value == 0
                    and fifo_agent.internal.rptr.value == 0
        )
        cover_reset[0].sample()

    async def Reset_Hold_Sequence():
        await dut.ACondition(
            lambda: fifo_agent.status.rst_n.value == 0
        )
        await fifo_agent.bundle.step()
        cover_reset[0].sample()

    async def Reset_Release_Sequence():
        await dut.ACondition(
            lambda: fifo_agent.status.rst_n.value == 1
        )
        prev_wptr = fifo_agent.internal.wptr.value
        prev_rptr = fifo_agent.internal.rptr.value
        prev_counter = fifo_agent.internal.counter.value
        await fifo_agent.bundle.step()
        if (fifo_agent.internal.wptr.value == prev_wptr and
            fifo_agent.internal.rptr.value == prev_rptr and
            fifo_agent.internal.counter.value == prev_counter):
            cover_reset[0].sample()
    
    create_task(Reset_Sequence())
    create_task(Reset_Hold_Sequence())
    create_task(Reset_Release_Sequence())

    # Return Agent
    yield fifo_agent

    toffee_request.cov_groups.extend(cover_reset)