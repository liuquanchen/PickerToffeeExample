from Bundle import *
from toffee.agent import *
from toffee import Executor


class FIFOAgent(Agent):

    def __init__(self, fifo_bundle, fifo_internal_bundle):
        super().__init__(fifo_bundle)
        self.write = fifo_bundle.write
        self.read = fifo_bundle.read
        self.status = fifo_bundle.status
        self.internal = fifo_internal_bundle

    @driver_method()
    async def reset(self, ):
        self.status.rst_n.value = 0
        await self.monitor_step()
        self.status.rst_n.value = 1
        await self.monitor_step()

    @driver_method()
    async def enqueue(self, data):
        self.write.we_i.value = 1
        self.write.data_i.value = data
        await self.monitor_step()
        self.write.we_i.value = 0
    
    @driver_method()
    async def dequeue(self):
        self.read.re_i.value = 1
        await self.monitor_step()
        data = self.read.data_o.value
        self.read.re_i.value = 0
        return data

    @driver_method()
    async def en_de_queue(self, data_i):
        async with Executor() as exec:
            exec(self.enqueue(data_i))
            exec(self.dequeue())

# class FIFOAgent(Agent):

#     def __init__(self, fifo_bundle):
#         super().__init__(fifo_bundle)
#         self.write = fifo_bundle.write
#         self.read = fifo_bundle.read
#         self.status = fifo_bundle.status

#     @driver_method()
#     async def reset(self, ):
#         self.status.rst_n.value = 0
#         await self.monitor_step()
#         self.status.rst_n.value = 1
#         await self.monitor_step()

#     @driver_method()
#     async def enqueue(self, data):
#         self.write.we_i.value = 1
#         self.write.data_i.value = data
#         await self.monitor_step()
#         self.write.we_i.value = 0
    
#     @driver_method()
#     async def dequeue(self):
#         self.read.re_i.value = 1
#         await self.monitor_step()
#         data = self.read.data_o.value
#         self.read.re_i.value = 0
#         return data

#     @driver_method()
#     async def en_de_queue(self, data_i):
#         async with Executor() as exec:
#             exec(self.enqueue(data_i))
#             exec(self.dequeue())