import asyncio
from toffee import DriverPort, MonitorPort
from toffee.model import Model, driver_hook

# 函数调用模板构建 RM
class FIFORefModelFunc(Model):
    def __init__(self):
        super().__init__()
        self.ram = [0] * 16
        self.wptr = 0
        self.rptr = 0
        self.counter = 0
        self.data_o = 0

    @driver_hook(agent_name="fifo_agent", driver_name="reset")
    def handle_reset(self):
        self.ram = [0] * 16
        self.wptr = 0
        self.rptr = 0
        self.counter = 0
        self.data_o = 0
        return None

    @driver_hook(agent_name="fifo_agent", driver_name="enqueue")
    def handle_enqueue(self, data):
        if self.counter == 16:
            return None

        self.ram[self.wptr] = data
        self.wptr = (self.wptr + 1) % 16
        self.counter += 1
        return None

    @driver_hook(agent_name="fifo_agent", driver_name="dequeue")
    def handle_dequeue(self):
        ret = self.data_o
        if self.counter > 0:
            self.data_o = self.ram[self.rptr]
            self.rptr = (self.rptr + 1) % 16
            self.counter -= 1
        return ret


# 独立执行流模式构建 RM
class FIFORefModelCtrl(Model):
    def __init__(self):
        super().__init__()
        self.ram = [0] * 16
        self.wptr = 0
        self.rptr = 0
        self.counter = 0
        self.data_o = 0

        self.reset = DriverPort(agent_name="fifo_agent", driver_name="reset")
        self.enqueue = DriverPort(agent_name="fifo_agent", driver_name="enqueue")
        self.dequeue = DriverPort(agent_name="fifo_agent", driver_name="dequeue")

        self.monitor_dequeue_data = MonitorPort(agent_name="fifo_agent", monitor_name="monitor_dequeue_data",)

    async def _handle_reset(self):
        while True:
            await self.reset()
            self.ram = [0] * 16
            self.wptr = 0
            self.rptr = 0
            self.counter = 0
            self.data_o = 0

    async def _handle_enqueue(self):
        while True:
            data = await self.enqueue()
            if self.counter < 16:
                self.ram[self.wptr] = data
                self.wptr = (self.wptr + 1) % 16
                self.counter += 1
                print(f"RM enqueue data: {data}")

    async def _handle_dequeue(self):
        while True:
            await self.dequeue()

            expected = self.data_o
            if self.counter > 0:
                self.data_o = self.ram[self.rptr]
                self.rptr = (self.rptr + 1) % 16
                self.counter -= 1

            actual = await self.monitor_dequeue_data()
            print(f"DUT dequeue data: {actual}, RM dequeue data: {expected}")
            assert actual == expected, f"dequeue mismatch: expected {expected}, got {actual}"

    async def main(self):
        await asyncio.gather(           # 并发启动三个独立的处理协程
            self._handle_reset(),
            self._handle_enqueue(),
            self._handle_dequeue(),
        )
