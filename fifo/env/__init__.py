from toffee.env import *
from .agent import FIFOAgent
from .bundle import SyncFIFOBundle, InternalBundle
from .RM import FIFORefModel

class SyncFIFOEnv(Env):
    """一个包含两个栈接口 Agent 的验证环境示例"""
    def __init__(self, fifo_bundle: SyncFIFOBundle, fifo_internal_bundle: InternalBundle):
        # 调用父类的初始化方法
        super().__init__()

        # 在 Env 内部实例化所需的 Agent，并将 Bundle 传递给它们
        # Agent 实例通常作为 Env 的属性，方便后续访问
        self.fifo_agent = FIFOAgent(fifo_bundle, fifo_internal_bundle)

        self.attach(FIFORefModel())