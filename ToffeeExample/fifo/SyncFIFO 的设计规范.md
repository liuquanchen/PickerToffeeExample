# 同步 FIFO 的设计规范和代码

Created Jul 22, 2025 - Last updated: Jul 22, 2025

## 设计规范

1. 模块名称：SyncFIFO
2. 描述：此模块实现一个 32 位宽、容量为 16 个元素的同步 FIFO（先入先出）缓冲区。FIFO 用于暂存数据，提供写入和读取操作，并支持满/空状态指示。它具有时钟同步行为，适用于数据流处理、接口缓冲等场景。该设计遵循同步操作，使用单一时钟信号进行读写。

## 端口说明
    端口名称	方向	宽度（bit）	描述
    clk	input	1	时钟信号
    rst_n	input	1	低电平时初始化 FIFO
    we_i	input	1	写使能信号，高有效，当为 1 时，允许向 FIFO 写入数据。
    re_i	input	1	读使能信号，高有效，当为 1 时，允许从 FIFO 读取数据。
    data_i	input	32	写入 FIFO 的数据
    data_o	output	32	读取 FIFO 的数据
    full_o	output	1	表明 FIFO 是否为满
    empty_o	output	1	表明 FIFO 是否为空

## 功能描述：
- 写入操作：
    - 当we_i为 1 时，FIFO 可以接收数据并存储到内部缓冲区ram中。
    - 写指针wptr指示下一个写入位置，随着每次写入操作递增。
    - 当 FIFO 已满时，full_o为 1，写入无效。
- 读取操作：
    - 当re_i为 1 时，FIFO 将根据读取指针rptr从ram中输出数据。
    - 读取指针rptr指示下一个读取位置，随着每次读取操作递增。
    - 当 FIFO 为空时，empty_o为 1，读取无效。
- 指针更新：
    - wptr（写指针）和rptr（读指针）在时钟上升沿更新。rptr仅在re_i有效并且 FIFO 非空时更新，wptr仅在we_i有效并且 FIFO 非满时更新。
    - FIFO 操作时，通过比较wptr和rptr的位置，FIFO 会自动调整数据的读写位置。
- 计数器：
    - counter用于跟踪 FIFO 中的数据量（从 0 到 16）。每次写入数据时，counter加 1，每次读取数据时，counter减 1。
    - 当counter值为 0 时，empty_o信号为 1，表示 FIFO 为空；当counter值为 16 时，full_o信号为 1，表示 FIFO 已满。

## 时序与复位
- 同步时序： 所有的操作（写入、读取、指针更新、计数器更新）都在时钟信号的上升沿同步。
- 复位： 在rst_n为低时，FIFO 内部所有指针（wptr、rptr）和数据输出（data_o）都将被清零，并且计数器counter会被复位为 0。

## 功能块说明
1. 指针更新：
    - 负责同步更新写入和读取指针。
    - 在每个时钟周期内，如果we_i为 1 并且 FIFO 不满，则数据会被写入 FIFO，且wptr自增。
    - 如果re_i为 1 并且 FIFO 不空，则会读取数据并将其输出，rptr自增。
2. 计数器更新：
    - 计数器counter用于追踪 FIFO 的当前数据量。
    - 每次写入时，counter自增；每次读取时，counter自减。
    - FIFO 满时，counter达到 16，full_o为 1；FIFO 空时，counter为 0，empty_o为 1。

## 设计约束与假设

- 数据宽度与深度： 本设计采用 32 位宽度，16 深度的 FIFO，适用于较小规模的数据缓存需求。
- 时钟域： FIFO 模块假设在单一时钟域内工作，且时钟信号与复位信号是同步的。
- 数据保持： FIFO 的数据存储在一个 16 个元素的 RAM 数组中，每个元素为 32 位。
- 读写并行：FIFO 未满且不为空时，允许同时进行读、写操作。
- 边界条件:
    - 当 FIFO 已满且we_i信号为高时，写入操作将被阻塞。
    - 当 FIFO 为空且re_i信号为高时，读取操作将被阻塞。
