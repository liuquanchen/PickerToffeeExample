# Reset Agent 代码覆盖率统计设计

## 背景

当前 [fifo/tests/test_reset.py](fifo/tests/test_reset.py) 已经具备 reset 场景的功能覆盖定义，但目标是进一步让 `reset_agent` 这组测试在 `toffee_test` 报告里同时产出：

- Line Coverage
- Function Coverage
- Branch Coverage

参考 `adder` 示例后确认：

1. **代码覆盖率报告** 由 `toffee_test` 的 report 流程统一汇总。
2. **DUT 级代码覆盖率数据** 由 `toffee_request.create_dut(...)` 创建 DUT 后，通过 `SetCoverage()` 导出 `.dat` 文件，再由 `genhtml --branch-coverage` 转成 HTML 报告。
3. **功能覆盖信息** 由 `CovGroup` 采样并挂到 `toffee_request` 上，再在报告阶段一起汇总。
4. 最终报告页面中会展示 Line / Functions / Branches 三类代码覆盖率指标，但它们的前提是当前 `DUTSyncFIFO` 构建产物本身已经包含相应 coverage 数据。

因此，本次工作不重写 reset 测试逻辑，而是在现有结构上补齐 code coverage 接线。

## 目标

在不改变现有 reset 用例语义的前提下，实现以下结果：

1. 运行 `test_reset` 时，可由 `toffee_test --toffee-report` 汇总生成 line / function / branch 覆盖率。
2. 保留现有 reset 功能覆盖点 `RST-01` / `RST-02` / `RST-03`。
3. 改动尽量局限在 [fifo/tests/test_reset.py](fifo/tests/test_reset.py)；仅在必要时补充最小运行配置。

## 方案选择

### 方案 A（采用）
在 [fifo/tests/test_reset.py](fifo/tests/test_reset.py) 的 fixture 中同时接入：

- `toffee_request.create_dut(...)` 的 code coverage 导出能力
- `toffee_request.add_cov_groups(...)` 的功能覆盖登记能力

这样 `toffee_test` 结束测试时会自动：

- 收集 DUT 生成的 `.dat`
- 合并代码覆盖率报告
- 合并 `CovGroup` 的功能覆盖结果

### 未采用方案

- **抽独立 coverage helper**：可复用，但本次目标只针对 `reset_agent`，会增加不必要改动面。
- **先功能覆盖后代码覆盖分两步做**：更适合排障，不适合当前一次性补齐目标。

## 设计

### 1. DUT 创建与代码覆盖接线

保留现有 `fifo_agent` fixture 的主体结构，继续通过 `toffee_request.create_dut(DUTSyncFIFO, "clk")` 创建 DUT。

这里的关键不是新增自定义 coverage 逻辑，而是确保 `test_reset` 这条路径正确使用 `toffee_request.create_dut(...)` 创建 DUT。`toffee_test` 会在 `--toffee-report` 模式下自动为支持 coverage 的 DUT 生成默认 `.dat` 输出路径，并在 teardown 时登记到报告系统。

设计上不手工拼接 line/function/branch 统计脚本，也不直接调用 `genhtml`。这些动作交给 `toffee_test` 自身完成，避免和现有框架重复。

### 2. 功能覆盖登记方式

当前文件中已经存在 `get_cover_group_fifo_state(...)` 与异步采样任务。这里保留该结构，但统一改用：

- `toffee_request.add_cov_groups(...)` 进行功能覆盖登记

而不是直接操作 `toffee_request.cov_groups.extend(...)`。

原因：

1. `add_cov_groups(...)` 是 `toffee_test` 提供的正式入口。
2. 它能在 DUT 已创建时自动挂接周期采样逻辑。
3. 语义更清晰，后续若再加 coverage group 不需要直接操作内部列表。

对于 reset 这类依赖事件时序的覆盖点，仍然保留显式 `sample()` 触发，不依赖周期采样命中业务语义。

### 3. reset 覆盖点与采样边界

保留三个覆盖点：

- `RST-01`：随机读写后触发 reset，并观测内部状态归零
- `RST-02`：保持 reset 若干周期，状态持续为零
- `RST-03`：释放 reset 后，状态保持稳定

采样逻辑继续放在 fixture 内创建的异步任务中，因为这些点本质上依赖：

- `rst_n` 的时序变化
- `counter / wptr / rptr` 的瞬时组合关系

这类条件更适合保留当前“等待条件满足后 sample”的模式，而不是改造成单纯的静态 cover point。

### 4. 对当前代码结构的最小调整

预计只做以下结构性调整：

1. 清理 `test_reset.py` 中未使用的 import，避免无关噪音影响测试可读性。
2. 将功能覆盖组注册改为 `toffee_request.add_cov_groups(...)`。
3. 保持现有 fixture、测试用例和异步覆盖采样任务的职责边界不变。

不改动 [fifo/agent/__init__.py](fifo/agent/__init__.py) 中 `FIFOAgent.reset()` 的行为，也不改写 reset 场景本身的断言顺序。

## 数据流

1. `pytest` 启动 `test_reset`
2. `fifo_agent` fixture 调用 `toffee_request.create_dut(...)`
3. DUT 若支持 code coverage，则在 report 模式下自动配置 `.dat` 输出
4. fixture 注册 `CovGroup`
5. `test_reset` 驱动 reset 行为
6. 异步任务在命中 RST-01/02/03 时调用 `sample()`
7. fixture teardown 时 `toffee_test` 同时回收：
   - 功能覆盖结果
   - 代码覆盖数据
8. `toffee_test` 统一生成报告

## 错误处理

本次不引入额外 defensive 逻辑，只关注两个边界：

1. **DUT 不支持 code coverage**：此时 `toffee_test` 不会产出 `.dat`，报告中不会出现完整的 Line / Functions / Branches 统计。实现阶段需要通过实际运行确认当前 `DUTSyncFIFO` 已开启 coverage metric。
2. **功能覆盖未命中**：不影响测试是否通过，但会在报告里体现为功能覆盖缺口；这属于测试质量信号，不作为额外异常处理。

## 测试与验证

实现阶段按 TDD 执行，但验证重点是报告行为：

1. 先运行 `test_reset`，确认当前行为基线。
2. 修改后以 `--toffee-report` 运行 `fifo/tests/test_reset.py`。
3. 确认报告目录中存在 line coverage 数据页面，且页面包含：
   - Line Coverage
   - Functions
   - Branches
4. 确认功能覆盖组仍显示 `RST-01` / `RST-02` / `RST-03`。

## 预期改动文件

- [fifo/tests/test_reset.py](fifo/tests/test_reset.py)

若验证时发现当前项目缺少启用 code coverage 的运行参数或 DUT 构建设置，再单独补最小必要改动，但不预设扩大范围。
