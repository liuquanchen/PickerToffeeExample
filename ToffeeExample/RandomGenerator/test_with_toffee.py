import random
import toffee
import toffee_test
import sys
from pathlib import Path

_picker = Path(__file__).resolve().parent / "picker_out_rmg"
if _picker.is_dir() and str(_picker) not in sys.path:
    sys.path.insert(0, str(_picker))


# 定义参考模型
class LFSR_16:
    def __init__(self, seed):
        self.state = seed & ((1 << 16) - 1)

    def Step(self):
        new_bit = (self.state >> 15) ^ ((self.state >> 14) & 1)
        self.state = ((self.state << 1) | new_bit) & ((1 << 16) - 1)
from RandomGenerator import DUTRandomGenerator

@toffee_test.testcase
async def test_with_ref(dut: DUTRandomGenerator):
    seed = random.randint(0, 2**16 - 1)  # 生成随机种子
    dut.seed.value = seed                # 设置 DUT 种子
    ref = LFSR_16(seed)                  # 创建参考模型用于对比

    dut.reset.value = 1                  # reset 信号置1
    await dut.AStep(1)                   # 推进一个时钟周期
    dut.reset.value = 0                  # reset 信号置0
    await dut.AStep(1)                   # 推进一个时钟周期

    

    for i in range(65536):               # 循环65536次
        await dut.AStep(1)               # dut 推进一个时钟周期，生成随机数
        ref.Step()                       # ref 推进一个时钟周期，生成随机数
        
        # 对比DUT和参考模型生成的随机数
        assert dut.random_number.value == ref.state, "Mismatch"


@toffee_test.fixture
async def dut(toffee_request: toffee_test.ToffeeRequest):
    # 使用toffee创建DUT并绑定时钟
    rand_dut = toffee_request.create_dut(DUTRandomGenerator, "clk")
    
    # 让toffee驱动时钟，只能在异步函数中调用
    toffee.start_clock(rand_dut)  
    return rand_dut