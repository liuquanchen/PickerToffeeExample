from agent import FIFOAgent
from Bundle import SyncFIFOBundle, InternalBundle
from SyncFIFO import DUTSyncFIFO
import toffee_test
import toffee 
from toffee import Executor


@toffee_test.testcase
async def test_agent(fifo_agent):
    # reset
    await fifo_agent.reset()

    # enqueue 0x114 and 0x514
    await fifo_agent.enqueue(0x114)
    await fifo_agent.enqueue(0x514)

    # dequeue 0x114 and 0x514
    await fifo_agent.dequeue()
    await fifo_agent.bundle.step()
    assert fifo_agent.read.data_o.value == 0x114, "data_o.value is not 0x114"

    await fifo_agent.dequeue()
    await fifo_agent.bundle.step()
    assert fifo_agent.read.data_o.value == 0x514, "data_o.value is not 0x514"

    
@toffee_test.testcase
async def test_agent_exec(fifo_agent):
    # reset
    await fifo_agent.reset()

    # enqueu 0x114
    await fifo_agent.enqueue(0x114)

    # enqueu 0x514 and dequeue 0x114 at the same time
    await fifo_agent.en_de_queue(0x514)
    
    await fifo_agent.bundle.step()
    assert fifo_agent.read.data_o.value == 0x114, "data_o.value is not 0x114"


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

    return fifo_agent
