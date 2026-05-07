from toffee.model import *


class FIFORefModel(Model):
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
        return self.data_o
