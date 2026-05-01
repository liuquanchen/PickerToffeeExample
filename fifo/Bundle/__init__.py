from toffee import Bundle, Signals, Signal

class WriteBundle(Bundle):
    we_i, data_i = Signals(2)
    
    """执行一次FIFO写入操作"""
    # async def enqueue(self, data):
        
    #     self.we_i.value = 1
    #     self.data_i.value = data
    #     await self.step()
    #     self.we_i.value = 0

class ReadBundle(Bundle):
    re_i, data_o = Signals(2)
    
    """执行一次FIFO读取操作, 返回读取的数据"""
    # async def dequeue(self):
    #     self.re_i.value = 1
    #     await self.step(1)
    #     data = self.data_o.value
    #     self.re_i.value = 0
    #     return data

# class InternalBundle(Bundle):
#     wptr, rptr, counter, ram = Signals(4)

class InternalBundle:
    def __init__(self, wptr, rptr, counter, ram=None):
        self.wptr = wptr
        self.rptr = rptr
        self.counter = counter
        self.ram = ram


class StatusBundle(Bundle):
    rst_n, full_o, empty_o = Signals(3)

class SyncFIFOBundle(Bundle):
    # select = Signal()

    write = WriteBundle()
    read = ReadBundle()
    status = StatusBundle()